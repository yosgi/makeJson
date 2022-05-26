#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import csv
import sys
import time
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail

year = time.strftime("%Y")
month = time.strftime("%m")
datadir = "/data/vhosts/sns.eefocus.com/upload/st/document/tmp"
realpath = os.path.realpath(__file__)
dirpath = os.path.dirname(realpath)
phpfile = "StItemDownloadCount.php"
day = time.strftime("%F")
phpath = "/bin/php56"
filespath = os.path.join(dirpath,"st")

def gettime():
    fday = time.strptime("%s%s" % (year,month) + "01 00:00:00", "%Y%m%d 00:00:00")
    fdaystamp = int(time.mktime(fday))
    ldaystamp = fdaystamp - 86400
    endday = time.strftime("%Y-%m-%d",time.localtime(fdaystamp))
    if int(month) - 1 <= 0:
        lmonth = int(month) + 11
        startday = "%s-%s-01" % (int(year)-1,lmonth)
    else:
        startday = "%s-%02d-01" % (year,int(month)-1)
    #print "%s %s %s %s" % (phpath,os.path.join(dirpath,phpfile),startday,endday)
    os.system("%s %s %s %s" % (phpath,os.path.join(dirpath,phpfile),startday,endday))
    print startday
    print endday
    os.chdir(datadir)
    now = time.time()
#    sys.exit()
    allfile = os.listdir(".")
    tfile = ""
    for item in allfile:
        if item.endswith(".csv") and now - os.path.getmtime(item) < 5:
            tfile = item
            break
    print "xxxfile", tfile
    tcsv = os.path.join(filespath,"%s.csv" % day)
    if os.path.exists(tcsv):
        print "del csv file"
        os.remove(tcsv)
    tmplist = ["01(5).csv","01(6).csv","01(7).csv","01(8).csv","01(9).csv"]
    for tmp in tmplist:
        tmpfile = os.path.join(filespath,tmp)
        if os.path.exists(tmpfile):
            print "del %s" % tmpfile
            os.remove(tmpfile)
    print "write csv file"
    rfobj = open(tfile,"rb")
    reader = csv.reader(rfobj)
    wfobj = open(tcsv,"wb")
    writer = csv.writer(wfobj)
    for sub,row in enumerate(reader):
        if not sub:
            print sub,"drop"
        else:
            writer.writerow(row)
    rfobj.close()
    wfobj.close()

def step1():
    os.chdir(filespath)
    print "exec step1"
    os.system("%s 2015stexportscript_step1.php %s.csv" % (phpath,day))
    os.system("%s 2015stexportscript_step2.php" % phpath)
    os.system("%s 2015stexportscript_step3.php" % phpath)

def step2():
    os.chdir(filespath)
    data = ""
    print "exec step2"
    for i in range(2,5):
        tmonth = (int(month)-i)
        if tmonth <= 0:
            tmonth += 12
            tyear = int(year) - 1
            data += "%s%02dstfinally.csv " % (tyear,tmonth)
        else:
            data += "%s%02dstfinally.csv " % (year,tmonth)
    print(data)
    os.system("%s 2015stexportscript_step4.php %s" % (phpath,data))
    os.system("%s 2015stexportscript_step5.php" % phpath)
    if int(month) == 1:
        filename = "%s%sstfinally.csv" % (int(year)-1,12)
    else:
        filename = "%s%02dstfinally.csv" % (year,int(month)-1)
    print filename
    os.rename("01(9).csv",filename)
    sendmail(['shuai.yuan@cn.supplyframe.com','hao.zhao@cn.supplyframe.com'],"自动发送","编辑","ST社区文档下载量",filename,filename)
    #sendmail(['shuai.yuan@supplyframe.cn','dan.miao@supplyframe.cn'],"自动发送","编辑","ST社区文档下载量",filename,filename)
    #sendmail(['shuai.yuan@supplyframe.cn'],"自动发送","编辑","ST社区文档下载量",filename,filename)

if __name__ == "__main__":
    gettime()
    step1()
    step2()
