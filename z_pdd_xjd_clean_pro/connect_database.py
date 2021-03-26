import traceback
import os
import json
from pyhive import hive
import random

class HiveOpt(object):

    def __init__(self):
        self.conn = None
        self.cursor = None

        try:
            self.conn = hive.connect(host='172.20.207.6', port=10000, username='supdev')
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise e

    def get_data_from_hive(self):
        try:
            fetch_sql = "SELECT std_brand_name,count(1) AS num FROM dwd.dwd_pdd_xjd_brand_reg_online where dt='2020-10-15' GROUP BY std_brand_name ORDER BY num DESC"
            fetch_sql_dy = "SELECT brand_name_std ,count(1) AS num FROM dim.dim_douyin_brand_std_wy where dt='2020-10-16' GROUP BY brand_name_std  ORDER BY num DESC"
            self.cursor.execute(fetch_sql_dy)
            results = self.cursor.fetchall()
            return results

            # with open("./cursor_brand_data.txt", "a", encoding='utf-8') as f:
            #     # f.write(insert_lst)
            #     json.dump(insert_lst, f, ensure_ascii=False)

        except Exception as e:
            raise e

    def get_data_sample_brand(self,brand_list,output_file):
        try:
            with open(output_file,"w",encoding="utf-8") as f1:
                for brand_item in brand_list:
                    fetch_sql = "SELECT std_brand_name,goods_name,goods_id,cat2_name,b_cat2_name,match_type from dwd.dwd_pdd_xjd_brand_reg_online where dt='2020-10-15' and std_brand_name = '%s'" % (str(brand_item[0]))
                    self.cursor.execute(fetch_sql)
                    results = self.cursor.fetchall()
                    fetch_num = 50
                    if len(results) < 50:
                        fetch_num = len(results)
                    sample_list = random.sample(results,fetch_num)
                    for sample_item in sample_list:
                        f1.write("\t".join([sample_item[0],sample_item[1],sample_item[2],sample_item[3],sample_item[4],sample_item[5]]))
                        f1.write("\n")

        except Exception as e:
            raise e

    def get_data_sample_brand_dy(self,brand_list,output_file):
        try:
            with open(output_file,"w",encoding="utf-8") as f1:
                for brand_item in brand_list:
                    fetch_sql_dy = "SELECT brand_name_std , product_name , brand_dy ,product_id , category1 , category1_id , category1_std , category1_id_std ,match_type from dim.dim_douyin_brand_std_wy where dt='2020-10-16' and brand_name_std = '%s'" % (str(brand_item[0]))
                    self.cursor.execute(fetch_sql_dy)
                    results = self.cursor.fetchall()
                    fetch_num = 50
                    if len(results) < 50:
                        fetch_num = len(results)
                    sample_list = random.sample(results,fetch_num)
                    for sample_item in sample_list:
                        f1.write("\t".join([sample_item[0],sample_item[1],sample_item[2],sample_item[3],sample_item[4],sample_item[5],sample_item[6],sample_item[7],sample_item[8]]))
                        f1.write("\n")

        except Exception as e:
            raise e

    def get_data_mid_sample(self,results,output_file):
        try:
            stat_dict = {}
            for item in results:
                if item[1] not in stat_dict:
                    stat_dict[item[1]] = [item[0]]
                else:
                    stat_dict[item[1]].append(item[0])
            stat_list = [(k,v) for k,v in stat_dict.items()]
            stat_list_ = sorted(stat_list,key=lambda x:str(x[0]),reverse=False)
            brand_list_all = stat_list_[int(len(stat_list_) / 2) - 3:int(len(stat_list_) / 2) + 3]
            brand_list = []
            for brand_list_item in brand_list_all:
                brand_list = brand_list_item[1] + brand_list
            print(brand_list)

            with open(output_file,"w",encoding="utf-8") as f1:
                for brand_item in brand_list:
                    fetch_sql = "SELECT std_brand_name,goods_name,goods_id,cat2_name,b_cat2_name,match_type from dwd.dwd_pdd_xjd_brand_reg_online where dt='2020-10-15' and std_brand_name = '%s'" % (str(brand_item))
                    self.cursor.execute(fetch_sql)
                    results = self.cursor.fetchall()
                    fetch_num = 50
                    if len(results) < 50:
                        fetch_num = len(results)
                    sample_list = random.sample(results,fetch_num)
                    for sample_item in sample_list:
                        f1.write("\t".join([sample_item[0],sample_item[1],sample_item[2],sample_item[3],sample_item[4],sample_item[5]]))
                        f1.write("\n")
        except Exception as e:
            raise e

    def get_data_mid_sample_dy(self,results,output_file):
        try:
            stat_dict = {}
            for item in results:
                if item[1] not in stat_dict:
                    stat_dict[item[1]] = [item[0]]
                else:
                    stat_dict[item[1]].append(item[0])
            stat_list = [(k,v) for k,v in stat_dict.items()]
            stat_list_ = sorted(stat_list,key=lambda x:str(x[0]),reverse=False)
            brand_list_all = stat_list_[int(len(stat_list_) / 2) - 3:int(len(stat_list_) / 2) + 3]
            brand_list = []
            for brand_list_item in brand_list_all:
                brand_list = brand_list_item[1] + brand_list
            print(brand_list)

            with open(output_file,"w",encoding="utf-8") as f1:
                for brand_item in brand_list:
                    fetch_sql_dy = "SELECT brand_name_std , product_name , brand_dy ,product_id , category1 , category1_id , category1_std , category1_id_std ,match_type from dim.dim_douyin_brand_std_wy where dt='2020-10-16' and brand_name_std = '%s'" % (str(brand_item))
                    self.cursor.execute(fetch_sql_dy)
                    results = self.cursor.fetchall()
                    fetch_num = 50
                    if len(results) < 50:
                        fetch_num = len(results)
                    sample_list = random.sample(results,fetch_num)
                    for sample_item in sample_list:
                        f1.write("\t".join([sample_item[0],sample_item[1],sample_item[2],sample_item[3],sample_item[4],sample_item[5],sample_item[6],sample_item[7],sample_item[8]]))
                        f1.write("\n")
        except Exception as e:
            raise e

if __name__ == "__main__":
    behind_output_file = "check_data/behind_data_dy.txt"
    mid_output_file = "check_data/mid_data_dy.txt"
    hiveopt = HiveOpt()
    results = hiveopt.get_data_from_hive()
    hiveopt.get_data_sample_brand_dy(results[len(results) - 100:],behind_output_file)
    # hiveopt.get_data_sample_brand(results[int(len(results)/2) - 5:int(len(results)/2) + 5], mid_output_file)
    hiveopt.get_data_mid_sample_dy(results,mid_output_file)