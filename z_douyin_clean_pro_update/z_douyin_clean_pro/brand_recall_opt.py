#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import re
import numpy

"""
1）增加了全部品牌对二手商品类目的映射
2）强制增加了对个别品牌与某一些类目对应的关系
3）强制生成品牌类目对应规则
"""

class BrandRecallOpt(object):
    """
    todo: 米家需要程序单独处理
    """
    def __init__(self, standard_brand_file, special_brand_file):
        if not os.path.exists(standard_brand_file):
            raise Exception("%s does not exists!" % standard_brand_file)
        if not os.path.exists(special_brand_file):
            raise Exception("%s does not exists!" % special_brand_file)
        self.standard_brand_file = standard_brand_file
        self.special_brand_file = special_brand_file
        self.special_brand_dict, self.special_brand_list = self.special_brand_loading()

    def brand_cat1_relation_del(self, bid, cid):
        del_dict = {('10873234', '100033'): ('pp/盼盼', '家具'),
                    ('10873234', '100034'): ('pp/盼盼', '家装建材'),
                    ('10414486', '100010'): ('Hodo/红豆', '食品饮料'),
                    ('10578925', '100009'): ('Amoi/夏新', '母婴童装'),
                    ('10578925', '100006'): ('Amoi/夏新', '服饰内衣'),
                    ('10869390', '100016'):('tonlion/唐狮', '个人护理'),
                    ('10869390', '100034'): ('tonlion/唐狮', '家装建材'),
                    ('10869390', '100014'):('tonlion/唐狮', '家居日用'),
                    ('10869390', '100025'): ('tonlion/唐狮', '厨具'),
                    ('10434992', '100026'): ('初心', '玩具乐器'),
                    ('10434992', '100034'): ('初心', '家装建材'),
                    ('10434992', '100035'): ('初心', '手机及配件'),
                    ('10434992', '100031'): ('初心', '家用电器'),
                    ('10434992', '100028'): ('初心', '电脑、办公'),
                    ('10434992', '100040'): ('初心', '二手商品'),
                    ('10434992', '100033'): ('初心', '家具'),
                    ('10434992', '100015'): ('初心', '礼品'),
                    ('10434992', '100007'): ('初心', '美妆护肤'),
                    ('10434992', '-99'): ('初心', '其他'),
                    ('10047221', '100016'): ('Dove/德芙', '个人护理'),
                    ('10047221', '100002'): ('Dove/德芙','生鲜'),
                    ('10290919', '100026'): ('Sony/索尼', '玩具乐器'),
                    ('10253457', '100006'): ('HYUNDAI/现代', '服饰内衣'),
                    ('10253457', '100029'): ('HYUNDAI/现代', '汽车用品'),
                    ('10200203', '100016'): ('Soyspring/冰泉', '个人护理'),
                    ('10914702', '100010'): ('冰泉', '食品饮料'),
                    ('11027445',  '100007'): ('花月情（HYQING）', '美妆护肤'),
                    ('10640934', '100006'): ('雅鹿', '服饰内衣'),
                    ('10640934', '100011'): ('雅鹿', '家纺'),
                    ('10640934', '100009'): ('雅鹿', '母婴童装'),
                    ('10640934', '100008'): ('雅鹿', '运动户外')}

        if (bid, cid) in del_dict:
            return True
        else:
            return False

    def brand_miss_cat1(self):
        miss_lst = [
              ('10766953',   'Bosideng/波司登',   '100008', '运动户外'), \
              ('10253230',   'MARSSENGER/火星人', '100014', '家居日用'), \
              ('10790422',   '左点',              '100008', '运动户外'), \
              ('10790422',   '左点',              '100034', '家装建材'), \
              ('10157092',   'Three Squirrels/三只松鼠', '100012', '家庭清洁/纸品'), \
              ('10424614',   '良品铺子',           '100042', '生活服务'), \
              ('10292037',   '金龙鱼',             '100012', '家庭清洁/纸品'),
              ('7830374551', '奢姿（SHEZI）',      '100007', '美妆护肤'),
              ('7830374550', 'blispring/冰泉',     '100016', '个人护理'),
              ('7830374550', 'blispring/冰泉',     '100007', '美妆护肤')]

        r_lst = []
        for k in miss_lst:
            bid, bname, cid, cname = k
            ext_bname = self.english_brand_extension(bname)
            r_lst.append("\t".join([bid.strip(), bname.strip(), ext_bname.strip(), cid.strip(), cname.strip(), "0.0"]))
            print("\t".join([bid.strip(), bname.strip(), ext_bname.strip(), cid.strip(), cname.strip(), "0.0"]))
        return r_lst

    def mijia_special_brand_recall(self, b_id, cat1_id, cat1_name):
        """
        标准品牌中将【米家】合并到了小米
        :return:
        """
        # 10698337        Xiaomi/小米     100031  家用电器        1143728907.83730000
        xiaomi_brand_id = "10698337"
        skip_cat1_id = "100035" # 手机及配件
        mijia_brand_id = "10698337"
        mijia_brand_name = "MJ/米家"

        r_lst = []
        # b_id, ori_b_name, cat1_id, cat1, gmv = lst1
        if b_id == xiaomi_brand_id and cat1_id != skip_cat1_id:
            ext_band_name = self.english_brand_extension("MJ/米家/小米米家")
            return "\t".join([mijia_brand_id, mijia_brand_name, ext_band_name, cat1_id, cat1_name, "0.0"])
        else:
            return ""

        """
        10698337	Xiaomi/小米	Xiaomi/小米Xiaomi/小米/Xiaomi小米	100028	电脑、办公	502831022.86170000
        """

    def redmi_special_brand_recall(self, b_id, cat1_id, cat1_name):
        xiaomi_brand_id = "10698337"
        hongmi_brand_id = "10698337"
        hongmi_brand_name = "Redmi/红米"

        r_lst = []
        # b_id, ori_b_name, cat1_id, cat1, gmv = lst1
        if b_id == xiaomi_brand_id:
            ext_band_name = self.english_brand_extension(hongmi_brand_name)
            return "\t".join([hongmi_brand_id, hongmi_brand_name, ext_band_name, cat1_id, cat1_name, "0.0"])
        else:
            return ""

        pass
    def english_brand_extension(self, brand_name):
        """
        target: 将扩展的品牌直接保存值召回品牌中
        1）指定品牌
        2）标准品牌

        第一种情况：去特殊字符
        A.H.C/爱和纯  ->  AHC爱和纯  -> A.H.C/爱和纯/AHC爱和纯
        A.O.史密斯    ->  AO史密斯   -> A.O.史密斯/AO史密斯

        第二种情况：去英文的空格
        MAKE UP FOR EVER  -> MAKEUPFOREVER
        COLOR KEY -> COLORKEY
        a b c/某某某  -> abc/a b c/某某某/abc某某某
        :return:
        """
        def _single_brand_ext(tmp_b_name):
            # 去除空格
            b1 = re.sub(r"[\s]+", "", tmp_b_name)
            # 去除.
            b2 = tmp_b_name.replace(".", "").replace("．", "")
            r_lst = list(set([tmp_b_name, b1, b2]))
            return r_lst

        # 10943455        Hisense/海信（黑电）
        ok_brand_name = ""
        tmp = brand_name.strip().replace("（", "(").replace("）", "").replace(")", "")
        lst2 = tmp.split("(")
        if len(lst2) == 2:
            b1 = lst2[0]
            if tool.is_all_eng(lst2[1]):
                b2 = lst2[1]
                ok_brand_name = b2 + "/" + b1
            else:
                ok_brand_name = b1
        else:
            ok_brand_name = brand_name

        brand_lst = ok_brand_name.strip().split("/")
        re_brand_lst = []
        if len(brand_lst) == 1:
            re_brand_lst += _single_brand_ext(brand_lst[0])
        else:
            en_brand_lst = []
            ch_brand_lst = []
            other_brand_lst = []
            for b in brand_lst:
                if tool.is_all_eng(b):
                    en_brand_lst.append(b)
                elif tool.is_all_chinese(b):
                    ch_brand_lst.append(b)
                else:
                    other_brand_lst.append(b)
            en_brand_ext_lst = []
            for z in en_brand_lst:
                en_brand_ext_lst += _single_brand_ext(z)
            mix_brand_lst = []
            for y in en_brand_ext_lst:
                for x in ch_brand_lst:
                    mix_brand_lst.append(y+x)
                    mix_brand_lst.append(x+y)

            if len(en_brand_lst) > 1:
                for i in range(len(en_brand_ext_lst)):
                    for j in range(i + 1, len(en_brand_lst)):
                        mix_brand_lst.append(en_brand_lst[i] + en_brand_lst[j])
                        mix_brand_lst.append(en_brand_lst[j] + en_brand_lst[i])

            re_brand_lst = mix_brand_lst + en_brand_ext_lst + ch_brand_lst + other_brand_lst

        re_brand_lst = list(set(re_brand_lst))
        #print(re_brand_lst)

        return "/".join(re_brand_lst)

    def special_brand_loading(self):
        ex_brand_dict = tool.get_exchange_brand_pair()

        special_brand_list = []
        special_brand_dict = {}
        b_id_dict = {}
        with open(self.special_brand_file, "r", encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                # brand_id, brand_name, cat1_id, cat1, gmv
                lst1 = line.split("\t")
                if len(lst1) != 2:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name = lst1
                if b_id in b_id_dict:
                    continue
                b_id_dict[b_id] = ''
                if b_name in ex_brand_dict:
                    b_name = ex_brand_dict[b_name]
                b_name = tool.brand_clean(b_name.lower())
                ext_band_name = self.english_brand_extension(b_name)
                special_brand_list.append(ext_band_name)
                special_brand_dict[b_id] = b_name

        return special_brand_dict, special_brand_list


    def special_brand_dealing(self,lst1, ex_brand_dict):
        b_id, b_name = lst1
        if b_name in ex_brand_dict:
            b_name = ex_brand_dict[b_name]
        b_name = tool.brand_clean(b_name.lower())
        ext_band_name = self.english_brand_extension(b_name)

        return ext_band_name

    def del_brand_func(self, b_id):
        del_brand_dict = {'10808927': '茉贝丽思', '11028554':'呼吸37度', \
                          '10540337': 'L’Oreal professionnel/巴黎欧莱雅沙龙专属', \
                          '10943797': '华为智选', '10631209':'GLAD/佳能', \
                          '10697475': 'COSME', '11028527':'爱敬（AGE）', \
                          '12660941': '苹果（Apple）', '10166483': 'ThinkPad'}
        if b_id in del_brand_dict: return True
        else: return False

    def brand_recall(self, output_file="brand_recall_info_tmp_.txt"):
        try:
            ex_brand_dict = tool.get_exchange_brand_pair()
            special_brand_list = self.special_brand_list
            recall_brand_dict = {}
            mijia_lst = []
            pr_list = []
            luolamima_list = []
            boshikou_list = []
            idx = 0
            with open(self.standard_brand_file, "r", encoding="utf-8") as f1:
                for line in f1:
                    line = line.strip()
                    if line == "": continue
                    lst1 = line.split("\t")
                    if len(lst1) != 5:
                        continue
                    lst1 = [tmp.strip() for tmp in lst1]
                    b_id, ori_b_name, cat1_id, cat1, gmv = lst1
                    if self.del_brand_func(b_id): continue
                    # 米家扩展
                    mijia_str = self.mijia_special_brand_recall(b_id, cat1_id, cat1)
                    if mijia_str != "": mijia_lst.append(mijia_str)
                    # 红米扩展
                    redmi_str = self.redmi_special_brand_recall(b_id, cat1_id, cat1)
                    if redmi_str != "": mijia_lst.append(redmi_str)

                    if ori_b_name in ex_brand_dict:
                        b_name = ex_brand_dict[ori_b_name]
                    else:
                        b_name = ori_b_name
                    b_name = tool.brand_clean(b_name)
                    ext_band_name = self.english_brand_extension(b_name)
                    for s_name in special_brand_list:
                        s_name_list = s_name.strip().split("/")
                        for s_name_item in s_name_list:
                            s_name_item = s_name_item.strip()
                            if s_name_item == "": continue
                            idx += 1
                            if idx % 1000000 == 0: print("idx: %s" % idx)
                            ext_band_name = ext_band_name.lower()
                            if len(ext_band_name.split(s_name_item)) > 1:
                                # 单个“后”字召回的品牌错误率很高
                                if s_name_item == "后":
                                    continue
                                if b_id == '10414486' and cat1_id == '100010':
                                    ok = 1
                                '''
                                99714433 蓝月亮（纸品）  100012 家庭清洁 / 纸品 1685455.83320000
                                '''
                                if b_id == '99714433': continue
                                if not self.brand_cat1_relation_del(b_id, cat1_id):
                                    k = "\t".join([b_id, ori_b_name, ext_band_name, cat1_id, cat1, gmv])
                                    recall_brand_dict[k] = ''
                                # 强制添加二手商品的一级类目
                                if not self.brand_cat1_relation_del(b_id, "100040"):
                                    k_tmp = "\t".join([b_id, ori_b_name, ext_band_name, "100040", "二手商品", '0.0'])
                                    recall_brand_dict[k_tmp] = ''

            # 硬添加【米家】添加一级类目【家用电器】
            mijia_lst += ["\t".join(["10698337","MJ/米家", self.english_brand_extension("MJ/米家/小米米家"), "100031", "家用电器", "0.0"])]
            mijia_lst += ["\t".join(["10698337", "MJ/米家", self.english_brand_extension("MJ/米家/小米米家"), "100034", "家装建材", "0.0"])]
            # 硬添加【PLUS RAPIDE】添加一级类目【服饰内衣,运动户外,鞋靴】
            pr_list += [
                "\t".join(["7830374549", "PLUS RAPIDE", self.english_brand_extension("PLUS RAPIDE/GXG旗下品牌PR/GXG旗下PR/GXG旗下男装PR"), "100006", "服饰内衣", "0.0"])]
            pr_list += [
                "\t".join(["7830374549", "PLUS RAPIDE", self.english_brand_extension("PLUS RAPIDE/GXG旗下品牌PR/GXG旗下PR/GXG旗下男装PR"), "100008", "运动户外", "0.0"])]
            pr_list += [
                "\t".join(["7830374549", "PLUS RAPIDE", self.english_brand_extension("PLUS RAPIDE/GXG旗下品牌PR/GXG旗下PR/GXG旗下男装PR"), "100001", "鞋靴", "0.0"])]
            # 硬添加【罗拉密码】添加一级类目【服饰内衣、鞋靴】
            luolamima_list += [
                "\t".join(["99714457", "LOORA PWD/罗拉密码",
                           self.english_brand_extension("LOORA PWD/罗拉密码"), "100006", "服饰内衣",
                           "0.0"])]
            luolamima_list += [
                "\t".join(["99714457", "LOORA PWD/罗拉密码",
                           self.english_brand_extension("LOORA PWD/罗拉密码"), "100001", "鞋靴",
                           "0.0"])]

            # 硬添加【ROYALAPOTHIC/泊诗蔻】添加一级类目【美妆护肤】
            boshikou_list += [
                "\t".join(["11015914", "ROYALAPOTHIC/泊诗蔻",
                           self.english_brand_extension("ROYALAPOTHIC/泊诗蔻"), "100007", "美妆护肤",
                           "0.0"])]

            # 品牌丢失一级类目的情况
            miss_lst = self.brand_miss_cat1()
            r_lst = list(recall_brand_dict.keys()) + mijia_lst + miss_lst + pr_list + luolamima_list + boshikou_list
            with open(output_file, "w", encoding="utf-8") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e

    def gen_brand_cat1_rule(self):
        """
        来自: z_three_en_word_dealing.py
        :return:
        """
        d1 = {}
        with open("brand_recall_info.txt") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                # brand_id, brand_name, cat1_id, cat1, gmv
                lst1 = line.split("\t")
                if '10253230' in line: print(lst1)
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name_ori, b_name, cat1_id, cat1, gmv = lst1
                r_brand_set = tool.brand_dealing(b_name_ori)

                # 二手商品的处理
                # 100040  二手商品
                if cat1_id == '100040': continue
                for tmp in r_brand_set:
                    # print(lst1)
                    k = (b_id, b_name)
                    v = (cat1_id, cat1)
                    if k in d1:
                        z = d1[k]
                        zz = z + [v]
                        zz = list(set(zz))
                        d1[k] = zz
                    else:
                        d1[k] = [v]

        second_hands_set = set()
        rule_set = set()
        for k1, v1 in d1.items():
            bid, bname = k1
            second_hands_set.add("%s|%s" % (bid, '100040'))
            for tmp in v1:
                cid, cname = tmp
                if bid == '10253230': print((bid, cid))
                rule_set.add("%s|%s" % (bid, cid))

        import numpy
        arr0 = numpy.array(list(rule_set))
        arr1 = numpy.array_split(arr0, 10)
        print(arr1[0].tolist())

        i = 1
        n_lst = []
        for tmp in arr1:
            n_lst.append('brand_cat1_fixed_pair_%s' % i)
            print('[brand_cat1_fixed_pair_%s]' % i)
            print("rule=%s" % ",".join(tmp))
            print()
            i += 1

        print("[brand_cat1_fixed_pair_second_hand]")
        print("rule=%s" % ",".join(list(second_hands_set)))

        print()
        print(",".join(n_lst))

    '''
    # 并行化实现
    def loading_data_split(self):
        a_lst = []
        with open(self.standard_brand_file, "r", encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                lst1 = line.split("\t")
                if len(lst1) != 5:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                a_lst.append(lst1)

        arr1 = numpy.array_split(a_lst, 5)
        r_lst = [tmp.tolist() for tmp in arr1]
        return r_lst

    def paralle_main(self, d_lst, special_brand_list, ex_brand_dict):
        try:
            recall_brand_dict = {}
            mijia_lst = []
            idx = 0
            for tmp_line in d_lst:
                b_id, ori_b_name, cat1_id, cat1, gmv = tmp_line
                if self.del_brand_func(b_id): continue
                # 米家扩展
                mijia_str = self.mijia_special_brand_recall(b_id, cat1_id, cat1)
                if mijia_str != "": mijia_lst.append(mijia_str)
                # 红米扩展
                redmi_str = self.redmi_special_brand_recall(b_id, cat1_id, cat1)
                if redmi_str != "": mijia_lst.append(redmi_str)

                if ori_b_name in ex_brand_dict:
                    b_name = ex_brand_dict[ori_b_name]
                else:
                    b_name = ori_b_name
                b_name = tool.brand_clean(b_name)
                ext_band_name = self.english_brand_extension(b_name)
                for s_name in special_brand_list:
                    s_name_list = s_name.strip().split("/")
                    for s_name_item in s_name_list:
                        s_name_item = s_name_item.strip()
                        if s_name_item == "": continue
                        idx += 1
                        if idx % 1000000 == 0: print("idx: %s" % idx)
                        ext_band_name = ext_band_name.lower()
                        if len(ext_band_name.split(s_name_item)) > 1:
                            # 单个“后”字召回的品牌错误率很高
                            if s_name_item == "后":
                                continue
                            k = "\t".join([b_id, ori_b_name, ext_band_name, cat1_id, cat1, gmv])
                            recall_brand_dict[k] = ''
                            # 强制添加二手商品的一级类目
                            k_tmp = "\t".join([b_id, ori_b_name, ext_band_name, "100040", "二手商品", '0.0'])
                            recall_brand_dict[k_tmp] = ''
        except:
            pass
    '''

if __name__ == "__main__":
    obj = BrandRecallOpt("C:/Users/Cwgong/PycharmProjects/z_douyin_clean_pro_update/standard_brand_info.txt", \
                         "../../kuaishou_brand_clean/kuaishou_pro_v1/xiaowu_standard_brand_tmp.txt")

    obj.brand_miss_cat1()