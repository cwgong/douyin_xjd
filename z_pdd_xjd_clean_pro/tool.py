#!/usr/bin/env python
#coding=utf-8

import sys
import os
import re
import unicodedata

def s_name_dealing(ori_name):
    s_name = re.sub(r"[\s]+", " ", ori_name)
    # 品牌为:半球
    s_name = s_name.lower().replace("半球型", "")\
        .replace("小米有品", "")\
        .replace("眼保仪","")
    stat_dict = {'中国': '', '韩国': '', '泰国': '', '孟加拉国': '', '德国': '', '英国': '', '法国': '', '刚果共和国': '', '刚果民主共和国': '', '美国': '',
     '多米尼加共和国': ''}
    for k, v in stat_dict.items():
        s_name =  s_name.replace(k, "")

    return s_name

def line_deal(line, bug_s, right_brand):
    line = line.strip()
    lst1 = line.split('\x01')
    if len(lst1) != 3:
        return None

    sid, ori_name, sbrand = lst1
    s_name = s_name_dealing(ori_name)
    sbrand = sbrand.strip()

    if sbrand == bug_s:
        return s_name + "|" + right_brand
    else:
        return None

def brand_stat_simple(input_p, output_p):
    if not os.path.exists(input_p):
        sys.exit(-1)
    b_dict = {}
    with open(input_p) as f2:
        for line in f2:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\x01")
            if len(lst1) != 3:
                continue
            s_id, ori_name, s_brand = lst1
            s_brand = s_brand.strip()
            if s_brand in b_dict:
                b_dict[s_brand] = b_dict[s_brand] + 1
            else:
                b_dict[s_brand] = 1
    lst2 = [(k, v) for k, v in b_dict.items()]
    lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)

    lst2 = ["%s\t%s" % tmp for tmp in lst2]
    with open(output_p, 'w') as f3:
        f3.write("\n".join(lst2))
        f3.flush()

def brand_clean(b_str):
    '''
    s1 = b_str.replace("【", ' ').replace("】", ' ') \
        .replace("（"," ").replace("）", " ") \
        .replace("(", " ").replace(")", " ")
    '''
    s1 = b_str.replace("【", ' ').replace("】", ' ')

    s1 = re.sub(r"[\s]+", " ", s1)
    # 繁体转简体
    #s1 = Converter('zh-hans').convert(s1)
    return s1

def brand_dealing(b_name):
    b_name = b_name.replace("|", " ")
    brand = re.sub(r"[\s]+", " ", b_name.lower())
    lst1 = brand.split('/')
    lst1 = [tmp.strip() for tmp in lst1]
    r_set = set()

    for tmp in lst1:
        tmp = tmp.replace("（",")").replace("（", ")")
        lst2 = tmp.split("(")
        if len(lst2) > 1:
            r_set.add(lst2[0])
        else:
            r_set.add(tmp)
    return r_set


def getting_special_brand_dict(brand_file):
    special_brand_dict = {}
    with open(brand_file) as f1:
        for line in f1:
            line = line.strip()
            if line == "": continue
            # brand_id, brand_name, cat1_id, cat1, gmv
            lst1 = line.split("\t")
            if len(lst1) != 2:
                continue
            lst1 = [tmp.strip() for tmp in lst1]
            b_id, b_name = lst1
            special_brand_dict[b_id] = b_name
    return special_brand_dict

def getting_recall_brand_dict(brand_file):
    """
    该文件建立扩展品牌的字典
    :param brand_file:
    :return:
    """
    recall_brand_dict = {}
    with open(brand_file,"r",encoding="utf-8") as f1:
        for line in f1:
            line = line.strip()
            if line == "": continue
            # brand_id, brand_name, cat1_id, cat1, gmv
            lst1 = line.split("\t")
            if len(lst1) != 2:
                continue
            lst1 = [tmp.strip() for tmp in lst1]
            b_id, b_name = lst1
            recall_brand_dict[b_id] = b_name
    return recall_brand_dict

def is_own_eng(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_all_eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_exchange_brand_pair():
    def _brand_pair_checking(exchange_dict):
        s1 = set(list(exchange_dict.keys()))
        s2 = set(list(exchange_dict.values()))
        s3 = s1 & s2
        if len(s3) > 0:
            return False, s3
        else:
            return True, None
    if os.path.exists("pdd_xjd_exchange_brand_info.txt"):
        ex_file = "pdd_xjd_exchange_brand_info.txt"
    elif os.path.exists("../pdd_xjd_exchange_brand_info.txt"):
        ex_file = "../pdd_xjd_exchange_brand_info.txt"
    else:
        raise Exception("pdd_xjd_exchange_brand_info.txt does not exist!")

    exchange_dict = {}
    if not os.path.exists(ex_file):
        raise Exception("%s does not exists!" % ex_file)
    with open(ex_file,"r",encoding="utf-8") as f2:
        for line in f2:
            line = line.strip()
            if line == "": continue
            if line.startswith("#"): continue
            lst1 = line.split("|")
            if len(lst1) != 2:
                continue
            lst1 = [z.strip() for z in lst1]
            k,v = lst1
            if k not in exchange_dict and k != v:
                exchange_dict[k] = v

    # 品牌对检测
    chk_flag, conflict_brand_set = _brand_pair_checking(exchange_dict)
    if not chk_flag:
        err_s = "exchang-brand-pair error: %s" % "\t".join(list(conflict_brand_set))
        raise Exception(err_s)

    return exchange_dict

def multi_blank_clean(s1):
    return re.sub(r"[\s]+", "", s1)
