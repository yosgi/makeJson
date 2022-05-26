#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import sys
import time
import pymysql
import requests
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail

filepath = os.path.realpath(__file__)
curdir = os.path.dirname(filepath)
filespath = os.path.join(curdir,"files")


conn = pymysql.connect(
    host="rm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com",
    user="pi_sns_eefocus",
    password="nWxa97#!xW-1",
    database="pi_rohm_eefocus",
    port=3306,
    charset="utf8")


cursor = conn.cursor()
sql = "select max(id) from eef_member_member;"
cursor.execute(sql)
maxid = cursor.fetchall()[0][0]

# 获取现在 年 月
month = time.strftime('%m')
year = time.strftime('%Y')

# 获取当月 1 号时间戳
day = "%s%s01" % (year, month)
endtime = "%s%s01 00:00:00" % (year, month)
etimeArray = time.strptime(endtime, "%Y%m%d %H:%M:%S")
etimeStamp = int(time.mktime(etimeArray))

# 获取前一天时间戳
tendtime = etimeStamp - 86400

# 获取前一天 年 月 日
tendtimeArray = time.localtime(tendtime)
tendyear = time.strftime("%Y", tendtimeArray)
tendmonth = time.strftime("%m", tendtimeArray)
tendday = time.strftime("%d", tendtimeArray)

# 获取上月 起始日期 结束日期
tstart = "%s%s01" % (tendyear, tendmonth)
tend = "%s%s%s" % (tendyear, tendmonth, tendday)

print tstart
print tend

baseurl = "http://rohm.eefocus.com/member/visitor/export?token=fb350c3c0444380bf2c7b145c5505716&start=%s&end=%s" % (tstart, tend)

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36'}

dfile = requests.get(url=baseurl, headers=headers)
with open('%s/%s.csv' % (filespath,day),"wb") as code:
    code.write(dfile.content)

wobj = open('%s/%s_res.csv' % (filespath,day),'wb')

fobj = open('%s/%s.csv' % (filespath,day))
data = fobj.readlines()
for sub,item in enumerate(data):
    if sub == 0:
        continue
    tmpdata = item.split(',')
    uid = tmpdata[0]
    try:
        timestamp = int(time.mktime(time.strptime(tmpdata[1].strip('"').strip("'"),"%Y-%m-%d %H:%M:%S")))
        maxid += 1
        sql = "insert into eef_member_member value (%s,%s,%s);\n" % (maxid,uid,timestamp)
        print sql
    except Exception as e:
        print e
        continue
    try:
        cursor.execute(sql)
        wobj.write("%s,%s,successfully,%s\n" % (uid,tmpdata[1],maxid))
    except Exception as e:
        print e
        wobj.write("%s,%s,already exists,%s\n" % (uid,tmpdata[1],maxid))

conn.commit()
fobj.close()
wobj.close()
cursor.close()
conn.close()


sendmail(['honghua.wang@cn.supplyframe.com'],"自动发送","编辑","rohm论坛会员导入","rohm_%s.csv" % day,"%s/%s_res.csv" % (filespath,day))
#sendmail(['shuai.yuan@supplyframe.cn'],"自动发送","编辑","rohm论坛会员导入","rohm_%s.csv" % day,"%s/%s_res.csv" % (filespath,day))
