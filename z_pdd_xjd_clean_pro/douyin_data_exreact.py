#!/usr/bin/env python3
#coding=utf-8

import sys
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession, HiveContext, Row
from pyspark.sql import functions as F
from pyspark.sql.window import Window, WindowSpec
from pyspark.sql.functions import desc

# out_p = sys.argv[1]

cat1_str = '''
100032,
100035,
100022,
100001,
100029,
100025,
100030,
100027,
100028,
100010,
100040,
100003,
100023,
100007,
100011,
100005,
100012,
100018,
100031,
100042,
100015,
100041,
100006,
100021,
100034,
100033,
100039,
100024,
100014,
100026,
100002,
100016,
100009,
100008
'''

# sc = SparkContext(appName="douyin_data")
conf = (SparkConf().setMaster("yarn").setAppName("douyin_data").set("spark.executor.memory", "1g"))
sc = SparkContext(conf = conf)
hiveContext = HiveContext(sc)

# sql="select sku_id, comment_count from (select sku_id, comment_count, crawler_tm, row_number() over(partition by sku_id order by crawler_tm desc) rn from dwd.dwd_jd_spu_comment_day m where dt >= '2020-03-16' and dt < '2020-03-23' and comment_count>0) w where w.rn = 1"
#
# sql = "select sku_id, comment_count from (select sku_id, comment_count, crawler_tm, row_number() over(partition by sku_id order by crawler_tm desc) rn from dwd.dwd_jd_sku_comment_day m where dt >= '2020-03-16' and dt < '2020-03-23' and comment_count>0) w where w.rn = 1 union all select sku_id, comment_count from (select sku_id, comment_count, crawler_tm, row_number() over(partition by sku_id order by crawler_tm desc) rn from dwd.dwd_jd_spu_comment_day m where dt >= '2020-03-16' and dt < '2020-03-23' and comment_count>0) w where w.rn = 1"
#
# sql = "select product_id,product_name,brand_dy,category1_id_std,category1_std from dim.dim_douyin_brand_std_wy "

cat1_list = [tmp.strip() for tmp in cat1_str.split(",")]
data_result_list = []

for cat1_name in cat1_list:
    sql = "select product_id,product_name,brand_dy,category1_id_std,category1_std from dim.dim_douyin_brand_std_wy where cat1_list = '%s' order by rand() limit 1000" %(cat1_name)
    df1 = hiveContext.sql(sql)
    data_result_list.append(df1)
    # df2 = df1.withColumn("idx", F.abs(df1.comment_count) * 0)
    # df3 = df2.select("sku_id", "comment_count", F.row_number().over(Window.partitionBy("idx").orderBy(desc("comment_count"))).alias("idx"))
    # df4 = df3.where(df3.idx <= 500000) \
    #     .select(df3.sku_id, df3.comment_count, df3.idx).rdd \
    #     .map(lambda x: "%s\t%s\t%s" % (x[0], x[1], x[2])) \
    #     .repartition(1).saveAsTextFile(out_p)
print(data_result_list)
sc.stop()