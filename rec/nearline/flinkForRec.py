from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.table.expressions import lit, col
from pyflink.table.window import Slide

from rec.nearline.user_action_udf import topN

kafka_source_ddl = """
CREATE TABLE rec (
 uid BIGINT,
 mid BIGINT,
 times TIMESTAMP(3),
 WATERMARK FOR times AS times - INTERVAL '5' SECOND
) WITH (
 'connector' = 'kafka',
 'topic' = 'rec3',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.zookeeper.connect' = 'localhost:2181',
 'scan.startup.mode' = 'earliest-offset',
 'format' = 'csv'
)
"""

my_sink_ddl = """
    create table mySink (
        mid VARCHAR 
    ) with (
        'connector' = 'filesystem',
        'format' = 'csv',
        'path' = './tmp/output',
        'partition.time-extractor.timestamp-pattern'='$dt $hour:00:00'
    )
"""

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
t_env = StreamTableEnvironment.create(env)
t_env.get_config().set_local_timezone('UTC')

t_env.sql_update(kafka_source_ddl)
t_env.sql_update(my_sink_ddl)

t_env.register_function("topN", topN)
# t_env.create_temporary_function("conca", concat)

result = t_env.from_path("rec").select("uid, mid, times")\
   .window(Slide.over(lit(10).minutes).every(lit(1).minutes).on(col('times')).alias("w"))\
   .group_by("uid, mid, w").select("mid, count(uid) as c, w.start as s")\
   .select("topN(mid, c, s)").insert_into("mySink")

# result = t_env.from_path("rec")\
#    .select("uid, mid, times").window(Slide.over(lit(10).minutes).every(lit(5).minutes).on(col('times')).alias("w"))\
#    .group_by("uid, mid, w").select("conca(mid), uid").insert_into("mySink")

t_env.execute("hotop")
