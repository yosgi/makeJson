#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import sys
import subprocess
import time

sys.path.append("/pub/scripts/bbs/api")

from sendmail import sendmail_nofile

year = time.strftime("%Y")
month = time.strftime("%m")
datafile = "/data/vhosts/sns.eefocus.com/var/freescale/log/document-download-new2.csv"
realpath = os.path.realpath(__file__)
dirpath = os.path.dirname(realpath)
day = time.strftime("%F")
filespath = os.path.join(dirpath,"nxp")

def gettime():
    fday = time.strptime("%s%s" % (year,month) + "01 00:00:00", "%Y%m%d 00:00:00")
    fdaystamp = int(time.mktime(fday))
    ldaystamp = fdaystamp - 86400
#    endday = time.strftime("%Y-%m-%d",time.localtime(ldaystamp))
    if int(month) - 1 <= 0:
        lmonth = int(month) + 11
        startm = "%s-%s" % (int(year)-1,lmonth)
    else:
        startm = "%s-%02d" % (year,int(month)-1)
    print startm
#    print endday
    data = subprocess.Popen("grep '%s' %s|awk -F ',' '$2 != \"0\" {print $0}'|wc -l" % (startm,datafile),shell=True,stdout=subprocess.PIPE).stdout.read()
    
    sendmail(['shuai.yuan@cn.supplyframe.com','hao.zhao@cn.supplyframe.com'],"自动发送","编辑","NXP社区文档下载量","%s 总下载量: %s" % (startm,data))
    #sendmail(['shuai.yuan@supplyframe.cn','hao.zhao@supplyframe.cn'],"自动发送","编辑","NXP社区文档下载量","%s 总下载量: %s" % (startm,data))
    #sendmail_nofile(['shuai.yuan@supplyframe.cn'],"自动发送","编辑","NXP社区文档下载量","%s 总下载量: %s" % (startm,data))


if __name__ == "__main__":
    gettime()
