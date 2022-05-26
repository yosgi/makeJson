#!/usr/bin/python
# -*- coding=utf8 -*-

import os
import sys
import time
import subprocess
import pymysql
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail_nofile


conn = pymysql.connect(
    host="rm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com",
    user="pi_sns_eefocus",
    password="nWxa97#!xW-1",
    database="pi_ams_eefocus",
    port=3306,
    charset="utf8")

cursor = conn.cursor()

basedir = os.path.dirname(os.path.realpath(__file__))
tardir = os.path.join(basedir, "files")

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

# 获取上月 起始日期
tstart = "%s%s01 00:00:00" % (tendyear, tendmonth)

# 获取上月 1 号时间戳
stimeArray = time.strptime(tstart, "%Y%m%d %H:%M:%S")
stimeStamp = int(time.mktime(stimeArray))

#print stimeStamp
#print etimeStamp

# 数据库查询上月新增帖子id
sql = "select tid from eef_forum_thread where dateline >= %s and dateline < %s;" % (stimeStamp, etimeStamp)
cursor.execute(sql)
allid = cursor.fetchall()

# 日志路径
tdir = "/var/log/nginx/ams.eefocus.com/"

# 存储所需日志路径
wobj = open("%s/%s%s" % (tardir, tendyear, tendmonth), "w")

# 本地执行脚本
tz = 'zgrep "GET /module/forum/forum.php?mod=viewthread&tid=" %saccess.log-%s%s* | grep -v -i "spider\|Bot"' % (tdir, tendyear, tendmonth)

# 远端执行脚本
tz103="su -l copylog -c 'ssh copylog@172.16.88.59 -o ConnectTimeout=120 \"zgrep \\\"GET /module/forum/forum.php?mod=viewthread&tid=\\\" %saccess.log-%s%s* | grep -v -i \\\"spider\|Bot\\\"\"'" % (tdir,tendyear,tendmonth)

message = ''

result1 = subprocess.Popen(tz,shell=True,stdout=subprocess.PIPE).stdout.read()
try:
    result2 = subprocess.Popen(tz103,shell=True,stdout=subprocess.PIPE).stdout.read()
except Exception as e:
    message += "数据2出现错误"

# 写入
wobj.write(result1)
# 104 和 103 分隔符
fg = "---- *  " * 10 + '104--103\n'
wobj.write(fg)
try:
    wobj.write(result2)
except Exception as e:
    message += "数据2出现错误"
wobj.close()

ret = []

# 循环获取
for item in allid:
    data = subprocess.Popen('egrep "GET /module/forum/forum.php\?mod=viewthread&tid=%s\D?" %s/%s%s|wc -l' % (item[0],tardir,tendyear,tendmonth),shell=True,stdout=subprocess.PIPE).stdout.read()
    ret.append((item[0],data))

# 计算总数
total = 0
for item in ret:
    total += int(item[1])
    message += "%s %s\n" % (item[0], item[1])


#sendmail_nofile(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","ams社区 %s %s 新帖访问数据" % (tendyear,tendmonth),"%s 月 新帖总访问量:   %s\n\n单帖访问量:\n%s" % (tendmonth, total, message))
sendmail_nofile(['shuai.yuan@cn.supplyframe.com','fengyu.tian@cn.supplyframe.com'],"自动发送","编辑","ams社区 %s %s 新帖访问数据" % (tendyear,tendmonth),"%s 月 新帖总访问量:   %s\n\n单帖访问量:\n%s" % (tendmonth, total, message))

#echo -e "$month月 新帖总访问量: $total\n\n单帖访问量:\n$tmp"|mail -s "ams社区 $year $month 新帖访问数据" shuai.yuan@supplyframe.cn
#echo -e "$month月 新帖总访问量: $total\n\n单帖访问量:\n$tmp"|mail -s "ams社区 $year $month 新帖访问数据" dan.miao@supplyframe.cn
#
