import io
import re
import json
import traceback
import pymysql
import pymongo


def shuffle_data_id(input_file):
    line_list = []
    with io.open(input_file,'r',encoding="utf-8") as f1:
        for line in f1:
            if len(line.strip()) == 0:continue
            line_list.append(line.strip())
    print(','.join(line_list))

def duplicate_data_id(input_file):
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line.strip()) == 0:continue
            line_lst = line.strip().split(",")
            print(len(line_lst))
            line_list_ = set(line_lst)
            print(','.join(line_list_))
            print(len(line_list_))

#全角转成半角
def full2half(s):
    n = ''
    for char in s:
        num = ord(char)
        if num == 0x3000:        #将全角空格转成半角空格
            num = 32
        elif 0xFF01 <=num <= 0xFF5E:       #将其余全角字符转成半角字符
            num -= 0xFEE0
        num = chr(num)
        n += num
    return n

def get_brackets(data):
    brackets_rgx = re.compile(r"(\()(.+)(\))")
    # brackets_rgx = re.compile(r"(\()([^\)]+)(\))")
    brackets_result = brackets_rgx.search(data)
    if brackets_result == None:
        return ''
    else:
        brand_result = brackets_result.group(2)
        return brand_result

def strip_brackets(data):
    brackets_result = re.sub(r"\([^\)]+\)","",data)
    return brackets_result

def simliarity_reg(brand_1,brand_2):
    brand_1_ = brand_1.split("|")[0]
    brand_2_ = brand_2.split("|")[0]
    brand_1_ = full2half(brand_1_)
    brand_2_ = full2half(brand_2_)
    brand_1_list = brand_1_.split("/")
    brand_2_list = brand_2_.split("/")
    brand_1_list_new = []
    brand_2_list_new = []
    flag = False

    for brand_item in brand_1_list:
        brand_1_brackets = get_brackets(brand_item)
        if brand_1_brackets != '':
            brand_1_list_new.append(brand_1_brackets)
        brand_item = strip_brackets(brand_item)
        brand_1_list_new.append(brand_item)

    for brand_item in brand_2_list:
        brand_2_brackets = get_brackets(brand_item)
        if brand_2_brackets != '':
            brand_2_list_new.append(brand_2_brackets)
        brand_item = strip_brackets(brand_item)
        brand_2_list_new.append(brand_item)

    for brand_item in brand_1_list_new:
        if brand_item in brand_2_list_new:
            flag = True
    return flag


def get_duplcate_id(data_list,data_dict):
    brand_all_list = []
    while True:
        brand = data_list[0]
        tmp_dict = {}
        tmp_dict[brand] = data_dict[brand]
        for data_item in data_list:
            if simliarity_reg(data_item,brand):
                tmp_dict[data_item] = data_dict[data_item]
                data_list.remove(data_item)
        brand_all_list.append(tmp_dict)
        # data_list.remove(brand)
        print(len(data_list))
        if len(data_list) < 1:
            break
    return brand_all_list

def stat_duplicate_id(input_file):
    data_dict = {}
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 6:continue
            brand_id,brand_name,brand_name_r,cat_id,cat_name,gmv = line_list
            if (brand_name + "|" + brand_id) in data_dict:
                data_dict[brand_name + "|" + brand_id].append(cat_name)
            else:
                data_dict[brand_name + "|" + brand_id] = [cat_name]

    brand_list = list(data_dict.keys())
    # print(brand_list)
    brand_all_list = get_duplcate_id(brand_list,data_dict)
    with io.open("./stat_duplicate.txt","w",encoding="utf-8") as f2:
        for item in brand_all_list:
            f2.write(str(item) + "\n")
        f2.flush()
    with io.open("./stat_duplicate.json", "w", encoding="utf-8") as f3:
        json.dump(brand_all_list,f3)

def is_all_eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_own_eng(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def stat_simple_eng_brand():
    short_eng_brand = []
    with open("./pdd_xjd_brand_recall_info.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line.strip()) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 6:continue
            brand_id,brand_name,brand_recall_name,cat2_id,cat2_name,gmv = line_list
            recall_name_list = brand_recall_name.split("/")
            for recall_name in recall_name_list:
                if is_all_eng(recall_name) and len(recall_name) <= 3 and check_contain_chinese(brand_name):
                    short_eng_brand.append(line)
    for item in short_eng_brand:
        print(item.strip())

def temp_dict_gen():
    idx = 0
    data_dict = {}
    with io.open("./tmp_file.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            idx += 1
            brand_id,brand_name = line_list
            tmp_list = [brand_name,'长度小于三的英文非重点品牌易出错']
            data_dict[brand_id] = tmp_list
    print(data_dict)
    print(idx)


def get_online_brand():
    data_list1 = {}
    data_list = {}
    data_list_ = []
    data_list = []
    # with io.open("./temp_1.txt","r",encoding="utf-8") as f1:
    #     for line in f1:
    #         if len(line) == 0: continue
    #         line = line.replace(" ","\t")
    #         line_list = line.strip().split("\t")
    #         if len(line_list) != 5:continue
    #         brand_id,_,brand_name,_,gmv = line_list
    #         data_list1[brand_id] = brand_name
    # print(len(data_list1))
    with io.open("./tmp_file.txt","r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            brand_id,brand_name = line_list
            data_list_.append(brand_name)
    # print(len(data_list_))

    try:
        db = pymysql.connect(host='rm-8vb1dlcr1x89lo03z.mysql.zhangbei.rds.aliyuncs.com', \
                             port=3306, user='edw', \
                             passwd='0Zwafqams%GDL3BU', db='mysql', \
                             charset='utf8')

        cursor = db.cursor()
        # industry_name_list = ['家用电器','数码','生鲜']
        for brand in data_list_:
            # sql_str = 'select destinct product_id,product_name,brand_name, first_type_name, brand_match_result from research_online.live_product_maintain_for_brand where brand_match_result = 0'
            # sql_str = 'select product_id,product_name,brand_name, first_type_name ,brand_match_result from research_online.live_product_maintain_for_brand where product_source = "抖音-自营" and brand_match_result = 0 and brand_name = "%s"' % (brand)
            # sql_str = 'select brand_id, brand_name, sum(gmv) as gmv from research_online.live_product_maintain_for_brand where product_source = "拼多多" GROUP BY brand_name order by gmv' % (brand)
            # sql_str = 'select brand_name, count(1) as num from research_online.live_product_maintain_for_brand where brand_match_result = 0 and product_source = "拼多多" GROUP BY brand_name ORDER BY num desc'
            sql_str = 'select product_id,product_name,brand_name from research_online.live_product_maintain_for_brand where brand_match_result = 1 and product_source = "拼多多" and brand_name = "%s" order by gmv limit 50' %(brand)
            # print(sql_str)
            cursor.execute(sql_str)

            # cursor.execute("select product_id, brand_id, brand_name from research_online.live_product_maintain_for_brand q where brand_match_result > 0")
            data = cursor.fetchall()
            data_list.append(data)
        cursor.close()
        db.close()
        return data_list
    except:
        print(traceback.format_exc())

def get_online_brand_hive():
    data_list = []
    data_list_ = []
    with io.open("./mysql_dayv.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            brand_id,brand_name = line_list
            data_list.append(brand_id)

    with io.open("./temp2.txt","r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.split("\t")
            if len(line_list) != 3:continue
            brand_id,brand_name,gmv = line_list
            if brand_id in data_list:
                data_list_.append(line)
                # data_list_.append(brand_id)
    # for data_item in data_list:
    #     if data_item not in data_list_:
    #         print(data_item)
    for data_item in data_list_:
        print(data_item.strip())

def get_increase():
    data_list = []
    with io.open("temp_1.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 3:continue
            data_list.append(line)
    with io.open("all_brand_except_hot.txt","r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 3:continue
            if line not in data_list:
                data_list.append(line)
    for item in data_list:
        print(item.strip())

def get_compare_dayu():
    data_list1 = []
    data_list2 = []
    with io.open("./mysql_dayv.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 5:continue
            brand_id, brand_name, product_id, product_name, gmv = line_list
            data_list1.append(line)
    with io.open("aeasy.txt","r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 5:continue
            product_id, product_name,  gmv, brand_name, brand_id = line_list

def shift_split():
    with io.open("./拼多多商品数据.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line = line.replace("\t","|")
            print(line.strip())

'''
{'keyword': 'KEHEAL科西电风扇家用台式静音摇头扇直流变频遥控立式空气循环扇', 'good_id': '120711879955', 'jd_title': '科西(Keheal)空气循环扇家用 办公室台式立式两用 负离子直流变频遥控  桌面电风扇落地静音F3 F3升级款', 'brand_id': '420669', 'brand_name': 'KEHEAL', 'jd_rootCategoryId': '737', 'jd_categoryId': '738', 'jd_subCategoryId': '751', 'jd_allCategoryId': '737;738;751', 'jd_rootCategoryName': '家用电器', 'jd_categoryName': '生活电器', 'jd_subCategoryName': '电风扇', 'jd_url': 'https://item.jd.com/66376865295.html'}

'''
def get_top_product():
    r_lst = []
    MyMongodb = pymongo.MongoClient(
        'mongodb://spider:spidermining@172.20.207.10:27051,172.20.207.12:27051,172.20.207.13:27051/admin')
    db = MyMongodb.get_database('pdd_map_jd_cate')
    collect = db.get_collection('map_pdd_top_gmv')
    for i in collect.find({}, {'_id': 0}, no_cursor_timeout=True):
        try:
            # if idx >= 5: break
            brand_name = i['brand_name']
            product_id = i['good_id']
            product_name = i['keyword']
            # kw = i['keyword']
            # jd_title = i['jd_title']
            # kw = kw.strip()
            # jd_title = jd_title.strip()
            # if kw == "" or jd_title == "": r_lst.append(kw)
            print(product_id + "\t" + product_name + "\t" + brand_name)
        except Exception as e:
            print(e)

def get_hiatus_product():
    research_dict = {}
    ori_product_dict = {}
    difference_set_list = []
    with io.open("./research_brand_result.txt","r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 3:continue
            product_id, product_name, brand_name = line_list
            research_dict[product_id] = [brand_name,product_name]
    with io.open("./tmp_output.txt","r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 3:continue
            product_id, product_name, brand_name = line_list
            # ori_product_dict[product_id] = [brand_name,product_name]
            brand_name_list = [tmp.lower() for tmp in brand_name.strip().split("/")]
            if product_id not in research_dict:
                difference_set_list.append(str(product_id) + "\t" + str(product_name) + "\t" + str(brand_name) + "\t" + "0" + "\n")
                continue
            if research_dict[product_id][0].lower() not in brand_name_list:
                difference_set_list.append(str(product_id) + "\t" + str(product_name) + "\t" + str(brand_name) + "\t" + research_dict[product_id][0] + "\n")
            else:
                continue
        return difference_set_list


if __name__ == "__main__":
    input_file = 'tmp_file.txt'
    # duplicate_data_id(input_file)
    # result = get_brackets('格力(11)1')
    # print(result)
    # input_file = "./pdd_xjd_brand_recall_info.txt"
    # stat_duplicate_id(input_file)

    #从找回品牌库中找到短的英文品牌，这些品牌易出错做重点关注。
    # stat_simple_eng_brand()

    #批量生成短英文品牌字典
    # temp_dict_gen()

    #去重品牌
    # get_online_brand_hive()
    # data_list_ = get_online_brand()
    # # print(data_list_)
    # with io.open("./tmp_output.txt","w",encoding="utf-8") as f1:
    #     for xx in data_list_:
    #         for item in xx:
    #             f1.write(str(item[0])+'\t'+str(item[1])+'\t'+str(item[2]) + "\n")
    #
    # with io.open("./tmp_output_v0.txt","w",encoding="utf-8") as f2:
    #     for xx in data_list_:
    #         for item in xx:
    #             f2.write(str(item[0])+'|'+str(item[1]) + "\n")

    #去除爆款后新增品牌
    # get_increase()

    #从mongo中取到韩汛检索数据
    # get_top_product()

    #比较韩汛检索和品牌清洗结果的差异不同
    # difference_list = get_hiatus_product()
    # with io.open("./no_same_file.txt","w",encoding="utf-8") as f1:
    #     f1.write("".join(difference_list))
    #     f1.flush()

