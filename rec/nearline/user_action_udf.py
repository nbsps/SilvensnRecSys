from pyflink.table import DataTypes
from pyflink.table.udf import udf

from rec.utils.redisManager import RedisManager

r = RedisManager()


@udf(input_types=[DataTypes.STRING()], result_type=DataTypes.STRING())
def topN(top, score, s):
    r.set('hot' + str(top), score, ex=60)
    print({top: score})
    return "ok"

# @udaf(result_type=DataTypes.STRING(), func_type="pandas")
# def concat(s):
#    print(s)
#    # s = "-".join(str(mid))
#    # print(s)
#    return "---"
