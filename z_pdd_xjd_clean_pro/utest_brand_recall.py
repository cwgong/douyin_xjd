#!/usr/bin/env python3
#coding=utf8

from brand_recall_opt import BrandRecallOpt
obj = BrandRecallOpt("pdd_xjd_standard_brand.txt")
obj.brand_recall()


d1 = {}
with open("pdd_xjd_brand_recall_info.txt") as f1:
    for line in f1:
        line = line.strip()
        if line == "": continue
        if line.startswith("#"): continue
        # brand_id, brand_name, cat1_id, cat1, gmv

        lst1 = line.split("\t")
        if len(lst1) != 6:
            continue
        lst1 = [tmp.strip() for tmp in lst1]
        b_id, b_name_ori, b_name, cat1_id, cat1, gmv = lst1
        d1[b_id] = ''

print(len(d1))
print(','.join(list(d1.keys())))