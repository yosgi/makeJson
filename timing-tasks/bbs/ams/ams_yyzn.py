#!/usr/bin/python
# -*- coding=utf8 -*-

import os
import sh
import sys
import time
import subprocess
import xlsxwriter
import pymysql
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail

reload(sys)
sys.setdefaultencoding('utf8')

conn = pymysql.connect(
    host="rm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com",
    user="pi_sns_eefocus",
    password="nWxa97#!xW-1",
    database="pi_ams_eefocus",
    port=3306,
    charset="utf8")

cursor = conn.cursor()

conn_account = pymysql.connect(
    host="rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com",
    user="pi_account",
    password="utC$x!w-f-8c",
    database="pi_account_eefocus",
    port=3306,
    charset="utf8")

cursor_account = conn_account.cursor()

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

print tendyear, tendmonth

# 获取上月 起始日期
tstart = "%s%s01 00:00:00" % (tendyear, tendmonth)

# 获取上月 1 号时间戳
stimeArray = time.strptime(tstart, "%Y%m%d %H:%M:%S")
stimeStamp = int(time.mktime(stimeArray))

# 应用指南地址 https://ams.eefocus.com/document/list/index/category-151
# 数据库查询应用指南文档id
sql = "SELECT id,title FROM `eef_document_detail` WHERE `active` = 1 AND `category` IN (151);"
cursor.execute(sql)
allid = cursor.fetchall()

tid = []
did = {}
for item in allid:
    tid.append(item[0])
    did[item[0]] = item[1]


#tfile = "/data/vhosts/sns.eefocus.com/var/ams/log/document-*.csv"
tfile1 = "/data/vhosts/sns.eefocus.com/var/ams/log/document-download.csv"
tfile2 = "/data/vhosts/sns.eefocus.com/var/ams/log/document-download-new2.csv"
data1=sh.egrep("%s-%s" % (tendyear, tendmonth),tfile1)
data2=sh.egrep("%s-%s" % (tendyear, tendmonth),tfile2)


target = []
tmptarget = []
tmptarget1 = []
data = (str(data1) + str(data2)).split("\n")
for item in data:
    if item:
        user = item.split(',')
        if int(user[-3]) in tid and int(user[1]):
            cursor_account.execute("select company, industry, position, sector from eef_user_custom_work where uid=%s" % user[1])
            tmp = cursor_account.fetchall()[0]
            company, industry, position, sector  = u"%s" % tmp[0],u"%s" % tmp[1],u"%s" % tmp[2],u"%s" % tmp[3]
            cursor_account.execute("select fullname, telephone, country, province, city, contact_email from eef_user_profile where uid=%s" % user[1])
            tmp = cursor_account.fetchall()[0]
            fullname, telephone, country, province, city ,email = u"%s" % tmp[0],u"%s" % tmp[1],u"%s" % tmp[2],u"%s" % tmp[3],u"%s" % tmp[4],u"%s" % tmp[5]
            #cursor_account.execute("select email from eef_core_user_account where id=%s" % user[1])
            #email = cursor_account.fetchall()[0][0]
            time = user[0].replace('-','/').replace('T',' ').replace('+08:00','')
            dname = did[int(user[-3])]
       
            tmptarget.append(u'%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s--;ys;replace;--%s'.replace(',','--;ys;replace;--') % (time,fullname,email,telephone, country, province, city,company, industry, position, sector,dname))

for item in tmptarget:
    tmpdata = item.split('--;ys;replace;--')
    if tmpdata[1:] not in tmptarget1:
        tmptarget1.append(tmpdata[1:])
        target.append(item)

target.sort()

title = ["姓名", "邮箱", "手机", "国家", "省份", "市区", "公司", "行业领域", "职位", "行业类别", "下载时间", "文档名称"]
workbook = xlsxwriter.Workbook('%s/ams应用指南_%s%s.xlsx' % (tardir, tendyear, tendmonth))
worksheet = workbook.add_worksheet()
formatdate = workbook.add_format({'num_format':'yyyy-mm-dd hh:mm:ss'})
mergeformat = workbook.add_format({'align':'center','valign':'vcenter','bold':True,'font_size':16})
titleformat = workbook.add_format({'align':'center','valign':'vcenter','bold':True,'font_size':11,'border':1})
commonformat = workbook.add_format({'align':'center','valign':'vcenter','font_size':11,'border':1,'text_wrap':1})
worksheet.set_column(1,2,19)
worksheet.set_column(2,3,13)
worksheet.set_column(3,6,6)
worksheet.set_column(6,7,24)
worksheet.set_column(7,8,9)
worksheet.set_column(8,10,13)
worksheet.set_column(10,11,20)
worksheet.set_column(11,12,37)

worksheet.set_row(0,42)
worksheet.merge_range('A1:L1', 'ams应用指南文档下载人员信息统计', mergeformat)
for sub,item in enumerate(title):
    worksheet.set_row(1,28)
    worksheet.write(1, sub, item, titleformat)
print len(target)
for sub,item in enumerate(target):
    worksheet.set_row(2+sub,28)
    tmpdata = item.split('--;ys;replace;--')
    data = tmpdata[1:-1]
    data.append(tmpdata[0])
    data.append(tmpdata[-1])
    for sub1,item1 in enumerate(data):
        worksheet.write(2+sub, sub1, item1, commonformat)
workbook.close()



sendmail(['shuai.yuan@cn.supplyframe.com','fengyu.tian@cn.supplyframe.com'],"自动发送","编辑","ams社区 应用指南文档下载人员信息统计(%s %s)" % (tendyear, tendmonth),"ams_yyzn%s%s.xlsx" % (tendyear, tendmonth), '%s/ams应用指南_%s%s.xlsx' % (tardir, tendyear, tendmonth))
#sendmail(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","ams社区 应用指南文档下载人员信息统计(%s %s)" % (tendyear, tendmonth),"ams_yyzn%s%s.xlsx" % (tendyear, tendmonth), '%s/ams应用指南_%s%s.xlsx' % (tardir, tendyear, tendmonth))

cursor.close()
cursor_account.close()
