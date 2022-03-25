from typing import Dict, List, Set
import pandas as pd
from rec.online.datastructer.Movie import Movie
from rec.online.datastructer.User import User
from rec.online.datastructer.Rating import Rating
from rec.online.datastructer.Embedding import Embedding


class DataManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.movieMap: Dict[int, Movie] = {}
        self.userMap: Dict[int, User] = {}
        self.genreMoviesMap: Dict[str, List[Movie]] = {}

    def loadData(self, movieDataPath, linkPath, ratingDataPath, movieEmbPath, userEmbPath, movieRedisKey, userRedisKey):
        self.loadMovieData(movieDataPath)
        self.loadLinkData(linkPath)
        self.loadRatingData(ratingDataPath)
        self.loadMovieEmb(movieEmbPath, movieRedisKey)
        self.loadUserEmb(userEmbPath, userRedisKey)

    def loadMovieData(self, movieDataPath):
        print("Loading movie data from " + movieDataPath + "...")
        df = pd.read_csv(movieDataPath)
        for i in range(df.shape[0]):
            line = df.iloc[i]
            title = line["title"].strip()[:-7]
            release_year = line["title"].strip()[-5:-1]
            movie = Movie(int(line["movieId"]), title, int(release_year), line["genres"].split("|"))
            self.movieMap[int(line["movieId"])] = movie
            for genre in line["genres"].split("|"):
                if self.genreMoviesMap.get(genre) is None:
                    self.genreMoviesMap[genre] = []
                self.genreMoviesMap[genre].append(movie)
        print("Loading movie data completed. " + str(len(self.movieMap)) + " movies in total.")

    def loadLinkData(self, linkDataPath):
        print("Loading link data from " + linkDataPath + " ...")
        df = pd.read_csv(linkDataPath)
        for i in range(df.shape[0]):
            line = df.iloc[i]
            movie = self.movieMap[int(line["movieId"])]
            movie.setImdbId(str(line["imdbId"]))
            movie.setTmdbId(str(line["tmdbId"]))
        print("Loading link data completed. " + str(df.shape[0]) + " links in total.")

    def loadRatingData(self, ratingDataPath):
        print("Loading rating data from " + ratingDataPath + " ...")
        df = pd.read_csv(ratingDataPath)
        for i in range(df.shape[0]):
            line = df.iloc[i]
            rating = Rating(int(line["movieId"]), int(line["userId"]), int(line["rating"]), int(line["timestamp"]))
            movie = self.movieMap.get(int(line["movieId"]))
            if movie is not None:
                movie.addRating(rating)
            if self.userMap.get(int(line["userId"])) is None:
                user = User(int(line["userId"]))
                self.userMap[int(line["userId"])] = user
            self.userMap.get(rating.userId).addRating(rating)
        print("Loading rating data completed. " + str(df.shape[0]) + " ratings in total.")

    def loadMovieEmb(self, movieEmbPath, movieRedisKey):
        print("Loading movieEmb data from " + movieEmbPath + " ...")
        df = pd.read_csv(movieEmbPath, sep=":")
        for i in range(df.shape[0]):
            line = df.iloc[i]
            emb = Embedding([float(e) for e in line[1].strip().split(" ")])
            movie = self.movieMap.get(int(line[0]))
            if movie is not None:
                movie.setEmb(emb)
        print("Loading movieEmb data completed. " + str(df.shape[0]) + " movieEmbs in total.")

    def loadUserEmb(self, userEmbPath, userRedisKey):
        """
        userEmb count is large large large!!!
        more likely to load from redis(every user search)
        :param userEmbPath:
        :param userRedisKey:
        :return:
        """
        print("Loading userEmb data from " + userEmbPath + " ...")
        df = pd.read_csv(userEmbPath, sep=":")
        for i in range(df.shape[0]):
            line = df.iloc[i]
            emb = Embedding([float(e) for e in line[1].strip().split(" ")])
            user = self.userMap.get(int(line[0]))
            if user is not None:
                user.setEmb(emb)
        print("Loading userEmb data completed. " + str(df.shape[0]) + " userEmbs in total.")

    def getMoviesByGenre(self, genre, size, sortBy):
        if genre == "":
            return None
        movies: List[Movie] = self.genreMoviesMap[genre]
        if sortBy == "rating":
            movies.sort(key=lambda m: m.averageRating, reverse=True)
        elif sortBy == "releaseYear":
            movies.sort(key=lambda m: m.releaseYear, reverse=True)
        if len(movies) > size:
            movies = movies[:size]
        return movies

    def getMovies(self, size, sortBy):
        movies: List[Movie] = list(self.movieMap.values())
        if sortBy == "rating":
            movies.sort(key=lambda m: m.averageRating, reverse=True)
        elif sortBy == "releaseYear":
            movies.sort(key=lambda m: m.releaseYear, reverse=True)
        if len(movies) > size:
            movies = movies[:size]
        return movies

    def getMoviesById(self, movieId):
        return self.movieMap.get(movieId)

    def getUserById(self, userId):
        return self.userMap.get(userId)




# d = DataManager()
# d.loadData('../../../static/sampledata/movies.csv', '../../../static/sampledata/links.csv',
#            '../../../static/sampledata/ratings.csv', '../../../static/modeldata/item2vecEmb.csv',
#            '../../../static/modeldata/userEmb.csv', '', '')
