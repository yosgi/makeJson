#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import sys
import time
import xlsxwriter
import pymysql as MySQLdb
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail

filepath = os.path.realpath(__file__)
curdir = os.path.dirname(filepath)
filespath = os.path.join(curdir,"files")

def gettime():
    nmonth=int(time.strftime("%m"))
    nyear=int(time.strftime("%Y"))
    lmonth=nmonth-1
    if lmonth == 0:
        lmonth = 12
    stime = "%s-%02d-01 00:00:00" % (nyear,lmonth)
    etime = "%s-%02d-01 00:00:00" % (nyear,nmonth)
    #stime = "2019-01-01 00:00:00"
    #etime = "2019-02-01 00:00:00"
    stimeArray = time.strptime(stime,"%Y-%m-%d %H:%M:%S")
    stimeStamp = int(time.mktime(stimeArray))
    etimeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    etimeStamp = int(time.mktime(etimeArray))
    return(stimeStamp,etimeStamp)

def getdata(times):
    host = "rm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com"
    user = "pi_sns_eefocus"
    passwd = "nWxa97#!xW-1"
    port = 3306
    dbname = 'pi_freescale_eefocus'
    db = MySQLdb.connect(host=host,user=user,passwd=passwd,db=dbname,port=port,charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT from_unixtime(t.`dateline`),t.`author`,t.`subject`,t.`tid`,f.`name` FROM `eef_forum_thread` as t,`eef_forum_forum` as f WHERE t.`fid`=f.`fid` and t.`displayorder` >=0 and t.`dateline` > %d and t.`dateline` < %d  order by t.`authorid`' % (times[0],times[1]))
    resft = cursor.fetchall()
    cursor.execute('SELECT from_unixtime(p.`dateline`),p.`author`,t.`subject`,p.`tid`,f.`name`,p.`pid` FROM `eef_forum_post` as p, `eef_forum_thread` as t, `eef_forum_forum` as f WHERE t.tid = p.tid and t.fid = f.fid and p.`invisible` >=0 and p.`dateline` > %d and p.`dateline` < %d order by p.`authorid`'% (times[0],times[1]))
    resht = cursor.fetchall()
    db.close()
    return (resft,resht)

def writexlsx(data):
    ft = data[0]
    ht = data[1]
    workbook = xlsxwriter.Workbook(os.path.join(filespath,'eef_forum_post.xlsx'))
    worksheet = workbook.add_worksheet()
    formatdate = workbook.add_format({'num_format':'yyyy-mm-dd hh:mm:ss'})
    mergeformat = workbook.add_format({'align':'center','valign':'vcenter'})
    worksheet.merge_range('A1:I1', 'eef_forum_post', mergeformat)
    worksheet.write('G2','POST')
    worksheet.write('H2','THREAD')
    worksheet.set_column(0,0,20)
    worksheet.set_column(2,2,25)
    worksheet.set_column(8,8,45)
    row = 2
    for item in ht:
        newdata = list(item)
        newdata.extend(["Y",""])
        num = len(newdata)
        for sub,dt in enumerate(newdata):
            if not sub:
                worksheet.write(row,sub,dt,formatdate)
            else:
                worksheet.write(row,sub,dt)
        worksheet.write(row,num,'="http://www.nxpic.org/module/forum/thread-\"&D%s&\"-1-1.html"' % (row+1))
        row += 1
    for item in ft:
        newdata = list(item)
        newdata.extend(["","","Y"])
        num = len(newdata)
        for sub,dt in enumerate(newdata):
            if not sub:
                worksheet.write(row,sub,dt,formatdate)
            else:
                worksheet.write(row,sub,dt)
        worksheet.write(row,num,'="http://www.nxpic.org/module/forum/thread-"&D%s&"-1-1.html"' % (row+1))
        row += 1
    workbook.close()
    sendmail(['yuanshuai@eefocus.com','hao.zhao@cn.supplyframe.com'],"自动发送","编辑"," NXP社区发帖和回帖查询","eef_forum_post.xlsx",os.path.join(filespath,"eef_forum_post.xlsx"))
    #sendmail(['yuanshuai@eefocus.com'],"自动发送","编辑"," NXP社区发帖和回帖查询","eef_forum_post.xlsx",os.path.join(filespath,"eef_forum_post.xlsx"))


if __name__ == "__main__":
    times = gettime()
    print writexlsx(getdata(times))
