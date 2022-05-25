#!/usr/bin/env python
# -*- coding=utf8 -*-

"""
获取所有厂商名称
SELECT meta_value,post_id FROM eef_postmeta  WHERE meta_key = 'eef_company_name_ch'

根据post_id去eef_posts表中id查询post_status状态判断厂商是否在用
SELECT post_status FROM `eef_posts` WHERE `ID` = '1410'
publish 在用
trash 垃圾箱 

股票代码
SELECT meta_value FROM `eef_postmeta` WHERE `meta_key` = 'eef_stock_code' and post_id=1398


SELECT a.meta_value,a.post_id FROM eef_postmeta as a,eef_posts as b WHERE a.meta_key = 'eef_company_name_ch' and a.post_id = b.id and b.post_status='publish'
"""

import re
import pymysql

dbhost = "192.168.2.82"
dbuser = "root"
dbpasswd = "root"
dbname = "eefocus_cms"
dbport = 6033

db = pymysql.connect(host=dbhost,user=dbuser,password=dbpasswd,database=dbname,port=dbport,charset='utf8')

cursor = db.cursor()

def getcode():
    cursor.execute("SELECT a.meta_value,a.post_id FROM eef_postmeta as a,eef_posts as b WHERE a.meta_key ='eef_company_name_ch' and a.post_id=b.id and b.post_status='publish'")
    data = cursor.fetchall()
    print("获取厂商数据")
    for item in data:
        #print(item)
        cursor.execute("SELECT meta_value FROM eef_postmeta WHERE meta_key = 'eef_stock_code' and post_id=%s" % item[1])
        tcode = cursor.fetchall()[0][0]
        codes = re.findall("\d{5,6}",tcode)
        for code in codes:
            #print(code)
            if len(code) == 5:
                print(item[0],"港股")
                import hs
                hs.getpdf(code)
            if len(code) == 6 and code.startswith('3'):
                print(item[0],"创业板")
                import sz
                sz.getpdf(code)
            if len(code) == 6  and code.startswith('0'):
                print(item[0],"深证")
                import sz
                sz.getpdf(code)
            if len(code) == 6  and code.startswith('6'):
                print(item[0],"上证")
                import sh
                sh.getpdf(code)


getcode()

db.close()


