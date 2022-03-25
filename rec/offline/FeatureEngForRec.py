from pyspark import SparkConf
from pyspark.sql import Window
from pyspark.sql.functions import udf, format_number
from pyspark.sql.types import DecimalType, FloatType, IntegerType, LongType
from pyspark.sql import dataframe
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
# from pyspark.sql./ savemode
import redis

# import scala.collection.immutable.ListMap
# import scala.collection.{JavaConversions, mutable}
from rec.utils import redisManager

NUMBER_PRECISION = 2
#   val redisEndpoint = "localhost"
#   val redisPort = 6379
#


def addSampleLabel(ratingSamples: dataframe):
    ratingSamples.show(10)
    ratingSamples.printSchema()
    sampleCount = ratingSamples.count()
    ratingSamples.groupBy(F.col("rating")).count().orderBy(F.col("rating")).withColumn("percentage", F.col("count")/sampleCount).show(100)
    ratingSamples.withColumn("label", F.when(F.col("rating") >= 3.5, 1).otherwise(0))


def addMovieFeatures(movieSamples: dataframe, ratingSamples: dataframe):
    # add movie basic features
    samplesWithMovies1 = ratingSamples.join(movieSamples, F.sequence("movieId"), "left")
    # add release year

    @udf
    def extractReleaseYearUdf(title):
        if title is None or len(title.strip()) < 6:
            return 1990
        else:
            yearString = title.strip()[len(title) - 5: len(title)]
            return int(yearString)

    # add title
    extractTitleUdf = udf(lambda title: title.strip()[:len(title.strip()) - 6].strip())

    samplesWithMovies2 = samplesWithMovies1.withColumn("releaseYear", extractReleaseYearUdf(F.col("title")))\
        .withColumn("title", extractTitleUdf(F.col("title"))).drop("title")  # title is useless currently

    # split genres
    samplesWithMovies3 = samplesWithMovies2.withColumn("movieGenre1", F.split(F.col("genres"), "\\|").getItem(0))\
        .withColumn("movieGenre2", F.split(F.col("genres"), "\\|").getItem(1))\
        .withColumn("movieGenre3", F.split(F.col("genres"), "\\|").getItem(2))

    # add rating features
    movieRatingFeatures = samplesWithMovies3.groupBy(F.col("movieId"))\
        .agg(F.count(F.lit(1)).alias("movieRatingCount"), format_number(F.avg(F.col("rating")), NUMBER_PRECISION).alias("movieAvgRating"),\
        F.stddev(F.col("rating")).alias("movieRatingStddev"))\
        .na.fill(0).withColumn("movieRatingStddev",format_number(F.col("movieRatingStddev"), NUMBER_PRECISION))


    # join movie rating features
    samplesWithMovies4 = samplesWithMovies3.join(movieRatingFeatures, F.Seq("movieId"), "left")
    samplesWithMovies4.printSchema()
    samplesWithMovies4.show(10)

    return samplesWithMovies4


@udf
def extractGenres(genreArray):
    genreMap = {}
    for i in genreArray:
        genres = i.split("|")
        for g in genres:
            genreMap[g] = genreMap.get(g) + 1 if genreMap.get(g) else 0
    sortedgenres = sorted(genreMap.items(), key=lambda i: i[1], reverse=True)
    return [i[1] for i in sortedgenres]


def addUserFeatures(ratingSamples: dataframe):
    samplesWithUserFeatures = ratingSamples.withColumn("userPositiveHistory", F.collect_list(F.when(F.col("label") == 1,
      F.col("movieId")).otherwise(F.lit(None)))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)))\
      .withColumn("userPositiveHistory", F.reverse(F.col("userPositiveHistory")))\
      .withColumn("userRatedMovie1",F.col("userPositiveHistory").getItem(0))\
      .withColumn("userRatedMovie2",F.col("userPositiveHistory").getItem(1))\
      .withColumn("userRatedMovie3",F.col("userPositiveHistory").getItem(2))\
      .withColumn("userRatedMovie4",F.col("userPositiveHistory").getItem(3))\
      .withColumn("userRatedMovie5",F.col("userPositiveHistory").getItem(4))\
      .withColumn("userRatingCount", F.count(F.lit(1))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)))\
      .withColumn("userAvgReleaseYear", F.avg(F.col("releaseYear"))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)).cast(IntegerType))\
      .withColumn("userReleaseYearStddev", F.stddev(F.col("releaseYear"))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)))\
      .withColumn("userAvgRating", format_number(F.avg(F.col("rating"))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)), NUMBER_PRECISION))\
      .withColumn("userRatingStddev", F.stddev(F.col("rating"))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)))\
      .withColumn("userGenres", extractGenres(F.collect_list(F.when(F.col("label") == 1, F.col("genres")).otherwise(F.lit(None)))\
      .over(Window.partitionBy("userId")\
      .orderBy(F.col("timestamp")).rowsBetween(-100, -1)))).na.fill(0)\
      .withColumn("userRatingStddev", format_number(F.col("userRatingStddev"), NUMBER_PRECISION))\
      .withColumn("userReleaseYearStddev", format_number(F.col("userReleaseYearStddev"), NUMBER_PRECISION))\
      .withColumn("userGenre1", F.col("userGenres").getItem(0))\
      .withColumn("userGenre2", F.col("userGenres").getItem(1))\
      .withColumn("userGenre3", F.col("userGenres").getItem(2))\
      .withColumn("userGenre4", F.col("userGenres").getItem(3))\
      .withColumn("userGenre5", F.col("userGenres").getItem(4))\
      .drop("genres", "userGenres", "userPositiveHistory")\
      .filter(F.col("userRatingCount") > 1)

    samplesWithUserFeatures.printSchema()
    samplesWithUserFeatures.show(100)

    return samplesWithUserFeatures


def extractAndSaveMovieFeaturesToRedis(samples: dataframe):
    movieLatestSamples = samples.withColumn("movieRowNum", F.row_number().over(Window.partitionBy("movieId")\
      .orderBy(F.col("timestamp").desc))).filter(F.col("movieRowNum") == 1)\
      .select("movieId","releaseYear", "movieGenre1","movieGenre2","movieGenre3","movieRatingCount",
      "movieAvgRating", "movieRatingStddev").na.fill("")

    movieLatestSamples.printSchema()
    movieLatestSamples.show(100)

    movieFeaturePrefix = "mf:"

  #   redisClient = redisManager()
  #   params = SetParams.setParams()
  #   # set ttl to 24hs * 30
  #   params.ex(60 * 60 * 24 * 30)
  #   val sampleArray = movieLatestSamples.collect()
  #   println("total movie size:" + sampleArray.length)
  #   var insertedMovieNumber = 0
  #   val movieCount = sampleArray.length
  #   for (sample <- sampleArray){
  #     val movieKey = movieFeaturePrefix + sample.getAs[String]("movieId")
  #     val valueMap = mutable.Map[String, String]()
  #     valueMap("movieGenre1") = sample.getAs[String]("movieGenre1")
  #     valueMap("movieGenre2") = sample.getAs[String]("movieGenre2")
  #     valueMap("movieGenre3") = sample.getAs[String]("movieGenre3")
  #     valueMap("movieRatingCount") = sample.getAs[Long]("movieRatingCount").toString
  #     valueMap("releaseYear") = sample.getAs[Int]("releaseYear").toString
  #     valueMap("movieAvgRating") = sample.getAs[String]("movieAvgRating")
  #     valueMap("movieRatingStddev") = sample.getAs[String]("movieRatingStddev")
  #
  #     redisClient.hset(movieKey, JavaConversions.mapAsJavaMap(valueMap))
  #     insertedMovieNumber += 1
  #     if (insertedMovieNumber % 100 ==0){
  #       println(insertedMovieNumber + "/" + movieCount + "...")
  #     }
  #   }
  #
  #   redisClient.close()
  #   movieLatestSamples
  # }
#
#   def splitAndSaveTrainingTestSamples(samples:DataFrame, savePath:String)={
#     //generate a smaller sample set for demo
#     val smallSamples = samples.sample(0.1)
#
#     //split training and test set by 8:2
#     val Array(training, test) = smallSamples.randomSplit(Array(0.8, 0.2))
#
#     val sampleResourcesPath = this.getClass.getResource(savePath)
#     training.repartition(1).write.option("header", "true").mode(SaveMode.Overwrite)
#       .csv(sampleResourcesPath+"/trainingSamples")
#     test.repartition(1).write.option("header", "true").mode(SaveMode.Overwrite)
#       .csv(sampleResourcesPath+"/testSamples")
#   }
#
#   def splitAndSaveTrainingTestSamplesByTimeStamp(samples:DataFrame, savePath:String)={
#     //generate a smaller sample set for demo
#     val smallSamples = samples.sample(0.1).withColumn("timestampLong", col("timestamp").cast(LongType))
#
#     val quantile = smallSamples.stat.approxQuantile("timestampLong", Array(0.8), 0.05)
#     val splitTimestamp = quantile.apply(0)
#
#     val training = smallSamples.where(col("timestampLong") <= splitTimestamp).drop("timestampLong")
#     val test = smallSamples.where(col("timestampLong") > splitTimestamp).drop("timestampLong")
#
#     val sampleResourcesPath = this.getClass.getResource(savePath)
#     training.repartition(1).write.option("header", "true").mode(SaveMode.Overwrite)
#       .csv(sampleResourcesPath+"/trainingSamples")
#     test.repartition(1).write.option("header", "true").mode(SaveMode.Overwrite)
#       .csv(sampleResourcesPath+"/testSamples")
#   }
#
#   def extractAndSaveUserFeaturesToRedis(samples:DataFrame): DataFrame = {
#     val userLatestSamples = samples.withColumn("userRowNum", row_number()
#       .over(Window.partitionBy("userId")
#         .orderBy(col("timestamp").desc)))
#       .filter(col("userRowNum") === 1)
#       .select("userId","userRatedMovie1", "userRatedMovie2","userRatedMovie3","userRatedMovie4","userRatedMovie5",
#         "userRatingCount", "userAvgReleaseYear", "userReleaseYearStddev", "userAvgRating", "userRatingStddev",
#         "userGenre1", "userGenre2","userGenre3","userGenre4","userGenre5")
#       .na.fill("")
#
#     userLatestSamples.printSchema()
#     userLatestSamples.show(100, truncate = false)
#
#     val userFeaturePrefix = "uf:"
#
#     val redisClient = new Jedis(redisEndpoint, redisPort)
#     val params = SetParams.setParams()
#     //set ttl to 24hs * 30
#     params.ex(60 * 60 * 24 * 30)
#     val sampleArray = userLatestSamples.collect()
#     println("total user size:" + sampleArray.length)
#     var insertedUserNumber = 0
#     val userCount = sampleArray.length
#     for (sample <- sampleArray){
#       val userKey = userFeaturePrefix + sample.getAs[String]("userId")
#       val valueMap = mutable.Map[String, String]()
#       valueMap("userRatedMovie1") = sample.getAs[String]("userRatedMovie1")
#       valueMap("userRatedMovie2") = sample.getAs[String]("userRatedMovie2")
#       valueMap("userRatedMovie3") = sample.getAs[String]("userRatedMovie3")
#       valueMap("userRatedMovie4") = sample.getAs[String]("userRatedMovie4")
#       valueMap("userRatedMovie5") = sample.getAs[String]("userRatedMovie5")
#       valueMap("userGenre1") = sample.getAs[String]("userGenre1")
#       valueMap("userGenre2") = sample.getAs[String]("userGenre2")
#       valueMap("userGenre3") = sample.getAs[String]("userGenre3")
#       valueMap("userGenre4") = sample.getAs[String]("userGenre4")
#       valueMap("userGenre5") = sample.getAs[String]("userGenre5")
#       valueMap("userRatingCount") = sample.getAs[Long]("userRatingCount").toString
#       valueMap("userAvgReleaseYear") = sample.getAs[Int]("userAvgReleaseYear").toString
#       valueMap("userReleaseYearStddev") = sample.getAs[String]("userReleaseYearStddev")
#       valueMap("userAvgRating") = sample.getAs[String]("userAvgRating")
#       valueMap("userRatingStddev") = sample.getAs[String]("userRatingStddev")
#
#       redisClient.hset(userKey, JavaConversions.mapAsJavaMap(valueMap))
#       insertedUserNumber += 1
#       if (insertedUserNumber % 100 ==0){
#         println(insertedUserNumber + "/" + userCount + "...")
#       }
#     }
#
#     redisClient.close()
#     userLatestSamples
#   }
#
#   def main(args: Array[String]): Unit = {
#     Logger.getLogger("org").setLevel(Level.ERROR)
#
#     val conf = new SparkConf()
#       .setMaster("local")
#       .setAppName("featureEngineering")
#       .set("spark.submit.deployMode", "client")
#
#     val spark = SparkSession.builder.config(conf).getOrCreate()
#     val movieResourcesPath = this.getClass.getResource("/webroot/sampledata/movies.csv")
#     val movieSamples = spark.read.format("csv").option("header", "true").load(movieResourcesPath.getPath)
#
#     val ratingsResourcesPath = this.getClass.getResource("/webroot/sampledata/ratings.csv")
#     val ratingSamples = spark.read.format("csv").option("header", "true").load(ratingsResourcesPath.getPath)
#
#     val ratingSamplesWithLabel = addSampleLabel(ratingSamples)
#     ratingSamplesWithLabel.show(10, truncate = false)
#
#     val samplesWithMovieFeatures = addMovieFeatures(movieSamples, ratingSamplesWithLabel)
#     val samplesWithUserFeatures = addUserFeatures(samplesWithMovieFeatures)
#
#
#     //save samples as csv format
#     splitAndSaveTrainingTestSamples(samplesWithUserFeatures, "/webroot/sampledata")
#
#     //save user features and item features to redis for online inference
#     //extractAndSaveUserFeaturesToRedis(samplesWithUserFeatures)
#     //extractAndSaveMovieFeaturesToRedis(samplesWithUserFeatures)
#     spark.close()
#   }
#
# }
