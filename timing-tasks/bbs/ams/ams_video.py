#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys
import time
import subprocess
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail_nofile

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

# 获取前一天 年 月
tendtimeArray = time.localtime(tendtime)
tendyear = time.strftime("%Y", tendtimeArray)
tendmonth = time.strftime("%m", tendtimeArray)

# 本地 104 ams 日志数据
tdir="/var/log/nginx/ams.eefocus.com/"
video='zgrep "GET /video/index/detail/" %saccess.log-%s%s* | grep -v -i "spider\|Bot" |wc -l' % (tdir,tendyear,tendmonth)
#video="su -l copylog -c 'ssh copylog@172.16.88.59 -o ConnectTimeout=120 \"zgrep \\\"GET /video/index/detail/\\\" %saccess.log-%s%s* | grep -v -i \\\"spider\|Bot\\\" |wc -l\"'" % (tdir,tendyear,tendmonth)

# 远端 103 ams 日志数据
t103="su -l copylog -c 'ssh copylog@172.16.88.59 -o ConnectTimeout=120 \"zgrep \\\"GET /video/index/detail/\\\" %saccess.log-%s%s* | grep -v -i \\\"spider\|Bot\\\" |wc -l\"'" % (tdir,tendyear,tendmonth)

message = ''

try:
    result1 = subprocess.Popen(video,shell=True,stdout=subprocess.PIPE).stdout.read()
except Exception as e:
    message += "数据1出现错误"
try:
    result2 = subprocess.Popen(t103,shell=True,stdout=subprocess.PIPE).stdout.read()
except Exception as e:
    message += "数据2出现错误"

try:
    int(result1)
    int(result2)
except Exception as e:
    message += "数据出错, 及时联系运维"

if not message:
    result = int(result1) + int(result2)
else:
    result = message
#print result

sendmail_nofile(['shuai.yuan@cn.supplyframe.com','fengyu.tian@cn.supplyframe.com'],"自动发送","编辑","ams社区 %s %s 月报数据" % (tendyear,tendmonth),"%s 月 视频播放量:   %s" % (tendmonth, result))
#sendmail_nofile(['shuai.yuan@supplyframe.cn','dan.miao@supplyframe.cn'],"自动发送","编辑","ams社区 %s %s 月报数据" % (tendyear,tendmonth),"%s 月 视频播放量:   %s" % (tendmonth, result))
