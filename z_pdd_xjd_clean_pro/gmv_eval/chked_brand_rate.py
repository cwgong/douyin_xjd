#!/usr/bin/env python3
#coding=utf-8

import sys
import pymysql
import traceback

s1 = """
10551418	Midea/美的
10119229	Chigo/志高
10191422	SUPOR/苏泊尔
10335357	Galanz/格兰仕
10219513	Haier/海尔
10263531	Joyoung/九阳
10490317	SIXTH ELEMENT/第六元素
10410197	ECOVACS/科沃斯
10695945	Royalstar/荣事达
10651059	南极人
10119220	Changhong/长虹
10137056	CLORIS/凯伦诗
10623605	MeiLing/美菱
10291494	扬子
10197261	dyson/戴森
10407445	Gree/格力
10264363	山本
10652455	Konka/康佳
10937418	Camel/骆驼（家用电器）
10767563	Ronshen/容声
10263813	ASHTON/阿诗顿
10930309	Panasonic/松下
10767664	Airmate/艾美特
10129699	Peskoe/半球
12660183	MK-SHIYI/湿毅
10238455	汉朗
10438483	璐瑶
10628264	金正
10119227	FRESTECH/新飞
10698337	Xiaomi/小米
10913449	JARE/佳仁
10153298	SAST/先科
10878098	LIVEN/利仁
10253457	HYUNDAI/现代
10578925	Amoi/夏新
10876053	三的
10182834	DO MASTER/大师傅
10017823	AquaBlue/蓝宝
10786927	康忆安
10222236	康夫
10939478	快霸/Kuarbaa
10077073	Malata/万利达
10917285	红心
10840237	上菱
10265023	IRIS/爱丽思
10943632	小浣熊
10180702	墨氏
10776535	XM/芯美
10180960	HAP/韩派
3330104	钻石牌
10631002	俊媳妇
10854761	罗脉
10376178	Bevan/毕梵（个人护理）
10417842	HanJiaOurs/汉佳欧斯
12653873	湿佳
10469251	Povos/奔腾
10551501	沁园
10936905	焱魔方
10857799	长帝
10660691	航科
10268165	Le Er Kang/乐尔康
10616433	KLINSMANN/克林斯曼
10636190	东智
10263846	Angel/安吉尔
10197883	SINGFUN/先锋
10526215	韩夫人
10511819	西物
10336921	大红鹰
10111462	SY/思育
10839815	Wahson/华生
12659002	金宏运
10363182	GESS
10275858	宝家丽
10641893	Buydeem/北鼎
12656423	金稻（美发工具）
10967795	菊花
10563854	水田
10407545	家实
10700949	bobot
10286257	Seko/新功
10499262	美辰
10263415	Aucma/澳柯玛
10411013	LiBos/锂博士
10047670	Tonze/天际
11027326	松多
10487408	玻妞
10943129	凤瑞
10479544	noirot
10086874	家卫士
10917457	亿力
10608668	小南瓜
10268880	Westinghouse/西屋
10341746	寸草情
10407559	海牌
10772167	GIEC/杰科
10348510	火焰皇
10845147	福菱
10724866	Wfirst/标王
10237560	申花
10186206	Ulike
10164826	AIRPLUS
10931406	家宝风
12657589	DDLSS/德立斯
10667431	USATA/御尚堂
10212278	华心
10937507	BANGCHEN/邦臣
11027106	KEHEAL
10163497	DEDAKJ
10476495	CHINOE/中诺
10957688	玄馨
10428562	艾斯凯
10991315	旭帝
10190432	格立高
10650943	泰昌
10993917	恒宜康
10439486	OLEGA/欧乐家
11001533	惠浦生活
10420632	Whirlpool/惠而浦
10135811	督洋
10657342	本博
10939623	永日
10547289	LOVE IS PERFECT/爱之美
10418510	杰诺
10247286	CRYSTAL PALACE/水晶宫
12655853	荣芝（RONGZHI）
12653875	韩秀
10197997	宝尔玛
10848060	POREE/博锐
10562022	OLAYKS
10721343	OralB/欧乐B
10148974	蒙得
10626826	ARPARC/阿帕其
10809098	Hurom/惠人
10914703	BRITA/碧然德
10918915	科帅
10078735	金凯瑞
10973705	印嘉
10549939	摩飞电器
10263712	Donlim/东菱
10700991	凯琴
12660724	鸣盏
10623189	Laica/莱卡
10286270	GEVILAN
12657550	HULLSI/浩诗
10577241	Philips/飞利浦
10685413	AUX/奥克斯
10840020	Bear/小熊
10272634	DAEWOO/大宇
10700343	Deerma/德尔玛
10943322	TINECO/添可
"""
hot_product_flag = True

topn_brand_dict = {}
for tmp in s1.strip().split('\n'):
    tmp = tmp.strip()
    if tmp == '': continue
    lst1 = tmp.split('\t')
    if len(lst1) != 2: continue
    lst1 = [tmp.strip() for tmp in lst1]
    a, b = lst1
    topn_brand_dict[a] = b

all_brand_gmv = {}
p_gmv_dict = {}
reg_brand_gmv = {}
reg_brand_cnt = {}
with open("all_brand_detail.txt","r",encoding="utf-8") as f0:
    for line in f0:
        line = line.strip()
        if line == "": continue
        lst1 = line.split('\t')
        lst1 = [tmp.strip() for tmp in lst1]
        b_id, b_name, pid, gmv = lst1
        try:
            gmv = float(gmv)
        except:
            continue
        # 99999999999
        if hot_product_flag and gmv >= 99999909999: continue

        if b_id in all_brand_gmv:
            aa = all_brand_gmv[(b_id, b_name)]
            all_brand_gmv[(b_id, b_name)] = aa + gmv
        else:
            all_brand_gmv[(b_id, b_name)] = gmv

        if b_id not in topn_brand_dict: continue

        p_gmv_dict[pid] = gmv
        if b_id in reg_brand_gmv:
            x = reg_brand_gmv[b_id]
            reg_brand_gmv[b_id] = x + gmv
        else:
            reg_brand_gmv[b_id] = gmv

        if b_id in reg_brand_cnt:
            m = reg_brand_cnt[b_id]
            reg_brand_cnt[b_id] = m + 1
        else:
            reg_brand_cnt[b_id] = 1

lst9 = []
for k2, v2 in all_brand_gmv.items():
    lst9.append((k2[0], k2[1], v2))

lst9 = sorted(lst9, key=lambda x: x[2], reverse=True)
lst10 = ["%s\t%s\t%s" % tmp for tmp in lst9[:100]]
if hot_product_flag:
    fname = "output/topn_brand_no_hot.txt"
else:
    fname = 'output/topn_brand.txt'

with open(fname, "w") as f3:
    f3.write("\n".join(lst10))
    f3.flush()

if hot_product_flag:
    fname = "output/topn_brand_diff_no_hot.txt"
else:
    fname = 'output/topn_brand_diff.txt'
lst11 = []
for tmp in lst9[:100]:
    a, b, c = tmp
    if a not in topn_brand_dict:
        lst11.append("%s\t%s\t%s" % tmp)

with open(fname, "w") as f3:
    f3.write("\n".join(lst10))
    f3.flush()

def mysql_opt():
    try:
        db = pymysql.connect(host='rm-8vb1dlcr1x89lo03z.mysql.zhangbei.rds.aliyuncs.com', \
                             port=3306, user='edw', \
                             passwd='0Zwafqams%GDL3BU', db='mysql', \
                             charset='utf8')

        cursor = db.cursor()
        sql_str = """
        SELECT brand_id, 
        brand_name, 
        product_id
        from research_online.live_product_maintain_for_brand
        where platform_name='拼多多' 
        and brand_match_result>0
        """
        cursor.execute(sql_str)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data
    except:
        print(traceback.format_exc())




chked_brand_gmv = {}
chked_brand_cnt = {}
for tmp in mysql_opt():
    bid, bname, pid = tmp
    bid = str(bid)
    pid = str(pid)

    if bid not in topn_brand_dict: continue
    if pid not in p_gmv_dict: continue

    if bid in chked_brand_gmv:
        z = chked_brand_gmv[bid]
        chked_brand_gmv[bid] = z + p_gmv_dict[pid]
    else:
        chked_brand_gmv[bid] = p_gmv_dict[pid]

    if bid in chked_brand_cnt:
        y = chked_brand_cnt[bid]
        chked_brand_cnt[bid] = y + 1
    else:
        chked_brand_cnt[bid] = 1



'''
r_lst = []
with open('../top_brand.txt') as f3:
    for line in f3:
        line = line.strip()
        if line == "": continue
        # brand_id, brand_name, cat1_id, cat1, gmv
        lst1 = line.split("\t")
        if len(lst1) != 5:
            continue
        lst1 = [tmp.strip() for tmp in lst1]
        id, name, cat2_id, cat2_name, _ = lst1
        k1 = (id, name)
        if k1 not in chked_brand_dict or k1 not in reg_brand_dict: continue
        reg_gmv = reg_brand_dict[k1]
        chked_gmv = chked_brand_dict[k1]
        r = 0.0
        if reg_gmv != 0.0:
            r = round(chked_gmv/reg_gmv, 4)
        else:
            r = 0.0
        r_lst.append((id, name, reg_gmv, chked_gmv, r))
'''

r_lst = []
for a, b in topn_brand_dict.items():
    if a not in chked_brand_gmv or a not in reg_brand_gmv: continue
    reg_gmv = reg_brand_gmv[a]
    reg_cnt = reg_brand_cnt[a]
    chked_gmv = chked_brand_gmv[a]
    chked_cnt = chked_brand_cnt[a]
    r = 0.0
    if reg_gmv != 0.0:
        r = round(chked_gmv / reg_gmv, 4)
    else:
        r = 0.0

    r1 = 0
    if reg_cnt != 0:
        r1 = round(1.0*chked_cnt / reg_cnt, 4)
    else:
        r1 = 0

    r_lst.append((a, b, reg_gmv, chked_gmv, r, reg_cnt, chked_cnt, r1))


r_lst = sorted(r_lst, key=lambda x: x[4], reverse=True)
r_lst = ["%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % tmp for tmp in r_lst]
title_lst = ["品牌编\t品牌名\t品牌总的gmv\t品牌已审核gmv\t品牌已审核gmv占比\t品牌商品数\t品牌已审核商品数\t品牌已审核商品数占比"]
r_lst = title_lst + r_lst
if hot_product_flag:
    fname = "output/brand_chked_rate_no_hot.txt"
else:
    fname = 'output/brand_chked_rate.txt'
with open(fname, "w",encoding="utf-8") as f4:
    f4.write("\n".join(r_lst))
    f4.flush()






