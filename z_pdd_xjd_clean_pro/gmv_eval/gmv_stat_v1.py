#!/usr/bin/env python3
#coding=utf-8

'''
分析：
    1:品牌gmv

cat2
    topN-brand
        topN-product
'''

class PddXjdGmvStat(object):
    def __init__(self, gmv_file):
        self.gmv_file = gmv_file

        self.brand_gmv_dict, self.all_brand_product_dict, self.all_product_gmv_dict, \
        self.all_product_gmv_dict_ext, self.all_gmv = self.loading_all_product_info()

    def loading_all_product_info(self):
        t = 0
        all_gmv = 0.0
        brand_gmv_dict = {}
        all_brand_product_dict = {}  # {'b_id|b_name': [p_id, p_id]}
        all_product_gmv_dict = {}
        all_product_gmv_dict_ext = {}
        with open(self.gmv_file) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                lst1 = line.split('\t')
                if len(lst1) != 8: continue
                lst1 = [tmp.strip() for tmp in lst1]
                t += 1
                # if t % 5000 == 0: print("t:", t)
                # 70966	俊媳妇家用压面机多功能不锈钢手动面条机小型擀面皮饺子馄饨皮机	0.0	0.0	俊媳妇	10631002	家用电器
                '''
                a.goods_id
                ,replace(a.goods_name,'\t','') as goods_name
                ,bb.std_brand_name as brand_name
                ,t1.category2_std
                ,a.vol
                ,a.vol*a.price as gmv
                ,bb.std_brand_id as brand_id
                ,t1.category1_std
                '''
                p_id, p_name, b_name, cat2, cnt, gmv, b_id, cat1 = lst1
                if p_id == "": continue
                k1 = "%s|%s" % (b_id, b_name)
                try:
                    gmv = float(gmv) / 10000
                except:
                    continue
                all_gmv += gmv
                if k1 in all_brand_product_dict:
                    z = all_brand_product_dict[k1]
                    z = list(set(z + [p_id]))
                    all_brand_product_dict[k1] = z
                else:
                    all_brand_product_dict[k1] = [p_id]

                if k1 in brand_gmv_dict:
                    x = brand_gmv_dict[k1]
                    brand_gmv_dict[k1] = x + gmv
                else:
                    brand_gmv_dict[k1] = gmv

                all_product_gmv_dict[p_id] = gmv
                all_product_gmv_dict_ext[p_id] = [p_name, gmv]

        return brand_gmv_dict, all_brand_product_dict, all_product_gmv_dict, all_product_gmv_dict_ext, all_gmv

    def brand_gmv_stat(self):
        lst1 = [(k, v) for k, v in self.brand_gmv_dict.items()]
        lst1 = sorted(lst1, key=lambda x: x[1], reverse=True)
        tmp_gmv = 0.0

        for tmp in lst1[:100]:
            x1, b_gmv = tmp
            b_id, b_name = x1.strip().split('|')
            print("%s\t%s\t%s" % (b_name, b_gmv, round(b_gmv/self.all_gmv, 5)))
            tmp_gmv += b_gmv
        print("全部gmv为:\t%s" % self.all_gmv)
        print("top100品牌gmv为:\t%s\t占比:\t%s" % (tmp_gmv,round(tmp_gmv/self.all_gmv, 5)))

    def brand_product_gmv_stat(self):
        lst1 = [(k, v) for k, v in self.brand_gmv_dict.items()]
        lst1 = sorted(lst1, key=lambda x: x[1], reverse=True)

        for tmp in lst1[:100]:
            k1, b_gmv = tmp
            if k1 not in self.all_brand_product_dict: continue
            if k1 not in self.brand_gmv_dict: continue
            b_id, b_name = k1.strip().split('|')
            lst2 = self.all_brand_product_dict[k1]
            tmp_gmv = 0.0
            t = 0
            for x in lst2:
                if x not in self.all_product_gmv_dict: continue
                tmp_gmv += self.all_product_gmv_dict[x]
                t += 1
                if tmp_gmv / b_gmv >= 0.8: break

            print("%s\t%s\t%s" % (b_name, t, len(lst2)))

    def brand_product_name_stat(self):
        lst1 = [(k, v) for k, v in self.brand_gmv_dict.items()]
        lst1 = sorted(lst1, key=lambda x: x[1], reverse=True)

        for tmp in lst1[:100]:
            k1, b_gmv = tmp
            if k1 not in self.all_brand_product_dict: continue
            if k1 not in self.brand_gmv_dict: continue
            b_id, b_name = k1.strip().split('|')
            lst2 = self.all_brand_product_dict[k1]
            tmp_gmv = 0.0
            t = 0
            for x in lst2:
                if x not in self.all_product_gmv_dict: continue
                tmp_gmv += self.all_product_gmv_dict[x]
                t += 1
                if tmp_gmv / b_gmv >= 0.8: break

            print("%s\t%s\t%s" % (b_name, t, len(lst2)))

if __name__ == "__main__":
    obj = PddXjdGmvStat('pdd_xjd_m08_gmv.txt')
    #obj.brand_gmv_stat()
    #obj.brand_product_gmv_stat()