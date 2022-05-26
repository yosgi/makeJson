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

nmonth=int(time.strftime("%m"))
nyear=int(time.strftime("%Y"))
etime = "%s-%02d-01 00:00:00" % (nyear,nmonth)

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

def getdata():
    host = "rm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com"
    user = "pi_sns_eefocus"
    passwd = "nWxa97#!xW-1"
    port = 3306
    dbname = 'pi_st_eefocus'
    db = MySQLdb.connect(host=host,user=user,passwd=passwd,db=dbname,port=port,charset='utf8')
    cursor = db.cursor()
    cursor.execute('select id,title,count_click,from_unixtime(time_upload) FROM `eef_video_video` WHERE category >= 158 AND category <= 180;')
    resft = cursor.fetchall()
    db.close()
    return resft

def writexlsx(data):
    workbook = xlsxwriter.Workbook(os.path.join(filespath,'%s_stvideo.xlsx' % etime))
    worksheet = workbook.add_worksheet()
    formatdate = workbook.add_format({'num_format':'yyyy-mm-dd hh:mm:ss'})
    mergeformat = workbook.add_format({'align':'center','valign':'vcenter'})
    #worksheet.merge_range('A1:I1', 'eef_forum_post', mergeformat)
    #worksheet.write('G2','POST')
    #worksheet.write('H2','THREAD')
    #worksheet.set_column(0,0,20)
    worksheet.set_column(1,1,55)
    worksheet.set_column(3,3,25)
    worksheet.set_column(4,4,50)
    #worksheet.set_column(8,8,45)
    row = 0
    for item in data:
        for sub,dt in enumerate(item):
            if sub == 3:
                print dt
                worksheet.write(row,sub,dt,formatdate)
            else:
                worksheet.write(row,sub,dt)
    #worksheet.write(row,num,'="http://www.nxpic.org/module/forum/thread-\"&D%s&\"-1-1.html"' % row)
        worksheet.write(row,4,'="http://www.stmcu.org.cn/video/index/detail/id-\"&A%s&\""' % (row+1))
        row += 1
    workbook.close()
    #sendmail(['yuanshuai@eefocus.com','jiajia.gong@supplyframe.cn'],"自动发送","编辑"," NXP社区发帖和回帖查询","eef_forum_post.xlsx","/pub/scripts/sendmail/files/eef_forum_post.xlsx")
    sendmail(['yuanshuai@eefocus.com','hao.zhao@cn.supplyframe.com'],"自动发送","编辑","ST英文视频 视频播放量统计","%s_stvideo.xlsx" % etime,"%s/stvideo.xlsx" % filespath)
    #sendmail(['yuanshuai@eefocus.com','dan.miao@supplyframe.cn'],"自动发送","编辑","ST英文视频 视频播放量统计","%s_stvideo.xlsx" % etime,"%s/stvideo.xlsx" % filespath)
    #sendmail(['yuanshuai@eefocus.com'],"自动发送","编辑","ST英文视频 视频播放量统计","stvideo.xlsx","%s/stvideo.xlsx" % filespath)
    #sendmail(['yuanshuai@eefocus.com'],"自动发送","编辑","ST 视频播放量统计","stvideo.xlsx","/pub/scripts/sendmail/files/stvideo.xlsx")


if __name__ == "__main__":
    print writexlsx(getdata())
