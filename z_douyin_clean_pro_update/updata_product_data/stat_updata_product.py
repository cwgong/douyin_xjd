import pymysql
import traceback


def get_brand_online(input_file):
    data_list = []
    with open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line.strip()) == 0:continue
            data_list.append(line.strip())
    return data_list

def stat_brand_num(input_file):
    brand_list = []
    try:
        db = pymysql.connect(host='rm-8vb1dlcr1x89lo03z.mysql.zhangbei.rds.aliyuncs.com', \
                             port=3306, user='edw', \
                             passwd='0Zwafqams%GDL3BU', db='mysql', \
                             charset='utf8')

        cursor = db.cursor()
        # industry_name_list = ['家用电器','数码','生鲜']
        # sql_str = 'select destinct product_id,product_name,brand_name, first_type_name, brand_match_result from research_online.live_product_maintain_for_brand where brand_match_result = 0'
        sql_str = 'SELECT brand_name,count(1) AS num from research_online.live_product_maintain_for_brand where brand_match_result = 0 and product_source = "抖音-自营" GROUP BY brand_name ORDER BY num DESC'
        # sql_str = 'select brand_name,brand_id, count(1) as num from research_online.live_product_maintain_for_brand where brand_match_result != 0 and product_source = "拼多多" GROUP BY brand_name ORDER BY num desc'
        # print(sql_str)
        cursor.execute(sql_str)

        # cursor.execute("select product_id, brand_id, brand_name from research_online.live_product_maintain_for_brand q where brand_match_result > 0")
        data = cursor.fetchall()
        cursor.close()
        db.close()

        brand_list_online = get_brand_online(input_file)
        for brand_item in data:
            if brand_item[0] in brand_list_online:
                brand_list.append(str(brand_item[0]) + "\t" + str(brand_item[1]))
            else:
                continue
    except:
        print(traceback.format_exc())
    return brand_list


if __name__ == "__main__":
    # 从hive表里取到每一个品牌的数目信息，然后再通过上线品牌过滤
    idx = 0
    input_file = "./check_utest_brand.txt"
    online_brand_list = stat_brand_num(input_file)
    with open("updata_online_brand_stat.txt","w",encoding="utf-8") as f1:
        f1.write("\n".join(online_brand_list))
        f1.flush()