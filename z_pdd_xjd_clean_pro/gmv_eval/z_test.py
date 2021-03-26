#!/usr/bin/env python3
#coding=utf-8

'''
select
a.brand_id, a.brand_name, a.gmv
from
(select brand_id, brand_name, sum(gmv)/1000000 as gmv
from dwi.dwi_product_maintain_for_brand
where brand_id!='' and brand_id is not null
group by brand_id, brand_name) a
order by a.gmv desc
'''
xb_dict = {'10549939': 'morphy richards/摩飞电器/摩飞',
      '10263712': 'donlim/东菱',
      '12657550': 'hullsi/浩诗',
      '10700991': '凯琴',
      '10623189': 'laica/莱卡',
      '12660724': '鸣盏',
      '10286270': 'gevilan/歌岚'
      }
jp_dict = {'10840020': 'bear/小熊',
      '10272634': 'daewoo/大宇',
      '10685413': 'aux/奥克斯',
      '10577241': 'philips/飞利浦',
      '10700343': 'deerma/德尔玛',
      '10943322': 'tineco/添可'
      }



def stat(f_path):
    xb_lst1 = []
    jp_lst2 = []
    top100_brand_dict = {}
    t_gmv = 0.0
    top100_gmv = 0.0

    idx = 0

    with open(f_path) as f1:
        for line in f1:
            line = line.strip()
            if line == '': continue
            lst1 = line.split(',')
            if len(lst1) != 3: continue
            lst1 = [tmp.strip() for tmp in lst1]
            bid, bname, b_gmv = lst1

            try:
                b_gmv = float(b_gmv)
            except:
                continue

            if bid in xb_dict:
                xb_lst1.append((bid, bname, b_gmv))
            if bid in jp_dict:
                jp_lst2.append((bid, bname, b_gmv))

            t_gmv += b_gmv
            if idx <= 100:
                top100_gmv += b_gmv
                top100_brand_dict[bid] = bname

            idx += 1

    for k1, v1 in xb_dict.items():
        print('%s,%s' % (k1, v1))

    for k2, v2 in jp_dict.items():
        print('%s,%s' % (k2, v2))

    for k3, v3 in top100_brand_dict.items():
        if k3 in xb_dict or k3 in jp_dict: continue
        print('%s,%s' % (k3, v3))


    print()
    print()
    print(top100_gmv/t_gmv)
    print()
    print()
    xb_lst1 = sorted(xb_lst1, key=lambda x: x[2], reverse=True)
    for tmp in xb_lst1:
        print("%s\t%s\t%s" % tmp)

    print()
    print()
    jp_lst2 = sorted(jp_lst2, key=lambda x: x[2], reverse=True)
    for tmp in jp_lst2:
        print("%s\t%s\t%s" % tmp)


#stat("brand_gmv.csv")
stat("brand_gmv_hot.csv")