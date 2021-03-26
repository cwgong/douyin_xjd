#!/usr/bin/env python3
#coding=utf-8

import sys
from brand_reg_tool import BrandRegTool
import tool
import pymysql
import traceback
traceback.format_exc()

def get_error_brand_info_from_mysql(sql_str):
    r_lst = []
    try:
        db = pymysql.connect(host='rm-8vb1dlcr1x89lo03z.mysql.zhangbei.rds.aliyuncs.com', \
                             port=3306, user='edw', \
                             passwd='0Zwafqams%GDL3BU', db='mysql', \
                             charset='utf8')

        cursor = db.cursor()
        cursor.execute(sql_str)

        for d in cursor.fetchall():
            r_lst.append('%s' % d)
    except:
        print(traceback.format_exc())

    return r_lst

def fix_brand_id(b_id):
    sql_str = """
        select distinct product_id 
        from research_online.live_product_maintain_for_brand
        where platform_name='拼多多' 
        and brand_match_result=0 
        and brand_id=%s
        """ % b_id
    return get_error_brand_info_from_mysql(sql_str)

def fix_brand_name(b_name):
    sql_str = """
        select distinct product_id 
        from research_online.live_product_maintain_for_brand
        where platform_name='拼多多' 
        and brand_match_result=0 
        and brand_name='%s'
        """ % b_name
    return get_error_brand_info_from_mysql(sql_str)


def all_error_data():
    sql_str = """
            select distinct product_id 
            from research_online.live_product_maintain_for_brand
            where platform_name='拼多多' 
            and brand_match_result=0
            """
    return get_error_brand_info_from_mysql(sql_str)
try:
    """ 第一批
    10913403  鸳鸯
    10278513  honguo/红果
    10237560  申花
    10003007  sakura/樱花
    10639608  保仪
    10483260  美橙
    10553676  多星
    10624031  delonghi/德龙
    10336562  华尔
    10695079  zlime/致美
    10768362  mini
    """

    """
    茶花
    高科
    奕佳（yijia）
    迪斯
    水香
    多乐/tolo
    早中晚
    alexander/亚历山大
    贝立
    soler/舒乐
    picooc/有品
    evertop/宝丽
    hyundai/现代
    povos/奔腾
    mini
    red double happiness/红双喜
    sast/先科
    xiaomi/小米
    tonze/天际
    tcl
    比亚
    柳叶
    baseus/倍思
    小金
    catmi/猫咪
    修正
    全能
    hello kitty
    格子
    磁悬
    熊猫
    至尊
    山水
    sharp/夏普
    洁霸
    速电
    钻石
    roborock/石头
    兴安邦乐
    """
    utest_lst = fix_brand_id('10253457')
    #utest_lst = fix_brand_name('alexander/亚历山大')
    if len(utest_lst) == 0:
        sys.exit(1)
    #utest_lst = all_error_data()
except:
    print(traceback.format_exc())
    sys.exit(1)

bReg = BrandRegTool("pdd_xjd_brand_recall_info.txt", "pdd_xjd_del_brand_info.txt", \
                    "pdd_xjd_exchange_brand_info.txt", "pdd_xjd_rule_brand.cfg")

idx = 0
err_lst = []
with open("pdd_xjd.txt","r",encoding="utf-8") as f1:
    for line in f1:
        try:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\001")
            if len(lst1) != 4:
                print(lst1)
                continue

            idx += 1

            lst1 = [tmp.strip() for tmp in lst1]
            product_id, product_name, cat1, cat2 = lst1

            if product_id not in utest_lst: continue

            pre_brand_id, pre_brand, match_type, \
            b_cat1_id, b_cat1_name, cat1_id, \
            cat1_name = bReg.brand_recognition(line)
            if pre_brand != None and match_type != None:
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (pre_brand_id, pre_brand, product_id, product_name, cat1, cat2, \
                                                          b_cat1_name, match_type))
            else:
                #err_lst.append(product_id)
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ('', product_id, product_name, cat1, cat2, \
                                                          '', '', '没有识别到任何品牌'))

        except Exception as e:
            print(traceback.format_exc())
    print(err_lst)


#a = bReg.english_brand_recognition("vero moda".lower(), "Vero Moda2020春季新款棉收腰宽摆风衣外套女 320121527 VERO MODA".lower())
#print(a)
