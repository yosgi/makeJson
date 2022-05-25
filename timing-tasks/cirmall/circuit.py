#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys
import unicodecsv
import time
import subprocess
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail


import sys
reload(sys)
sys.setdefaultencoding('utf8') 

day=time.strftime("%Y-%m-%d")
weekday=int(time.strftime("%w"))
if not weekday:
    weekday = 7
timeArray=time.strptime(day,"%Y-%m-%d")
endtime=int(time.mktime(timeArray)) - (weekday-1)*86400
starttime=endtime - 7*86400

startdate = time.strftime("%m%d %H:%M",time.localtime(starttime))
enddate = time.strftime("%m%d %H:%M",time.localtime(endtime))


#print starttime,endtime
#print startdate,enddate
#sys.exit()

mysql="/bin/mysql -h rm-uf62o8x44q3oizi54.mysql.rds.aliyuncs.com -ucirmall -p'sad2$*x!DF0' -N cndzz -e"

status = {'0':u'拒绝','1':u'通过','3':u'等待审核'}

data = []
def getmes(cid,ttime):
    result = subprocess.Popen('%s "select id,owner_id,created,name,original_price,price,purchases_count,manufacturer_id from circuits where id=%s;"' % (mysql, cid), shell=True,stdout=subprocess.PIPE).stdout.readlines()
#    print result
    tmp = result[0].split("\t")
    id,owner_id,created,name,original_price,price,purchases_count,manufacturer_id = tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7]
    manufacturer = subprocess.Popen('%s "select name from manufacturers where id=%s;"' % (mysql, manufacturer_id), shell=True,stdout=subprocess.PIPE).stdout.read()
    user_name = subprocess.Popen('%s "select user_name from users where id=%s;"' % (mysql, owner_id), shell=True,stdout=subprocess.PIPE).stdout.read()
    screen_name = subprocess.Popen('%s "select screen_name from user_profile where user_id=%s;"' % (mysql, owner_id), shell=True,stdout=subprocess.PIPE).stdout.read()
    if screen_name.strip('\n') in ['','NULL']:
        screen_name = subprocess.Popen('%s "select screen_name from users where id=%s;"' % (mysql, owner_id), shell=True,stdout=subprocess.PIPE).stdout.read()
    tmes = ''
    for item in ttime:
        created = int(item[0])
        uptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(created)))
        mes = status[item[1]]
        tmes += "%s:%s    " % (uptime,mes)
#    print tmes
    
    data.append([u"%s" % id,u"%s" % owner_id,u"%s" % user_name.strip("\n"),u"%s" % screen_name.strip("\n"),u"%s" % name,u"%s" % manufacturer.strip("\n"),u"%s" % original_price,u"%s" % price,u"%s" % purchases_count.strip("\n"),u"%s" %tmes])



# 正在审核队列
wapprove = subprocess.Popen('%s "select * from circuits_in_review where %s < created and created < %s;"' % (mysql,starttime, endtime), shell=True,stdout=subprocess.PIPE).stdout.readlines()

#print wapprove


# 已审核队列
approve =  subprocess.Popen('%s "select circuit_id,submited,approved from circuits_reviewed where %s < submited and submited < %s;"' % (mysql,starttime, endtime) , shell=True,stdout=subprocess.PIPE).stdout.readlines()

#print approve

swapprove = []
# 审核队列是否初次审核
for item in wapprove:
    circuit_id = item.split()[0]
    wpd = subprocess.Popen('%s "select count(*) from circuits_reviewed where circuit_id = %s;"' % (mysql,circuit_id) , shell=True,stdout=subprocess.PIPE).stdout.read().strip("\n")
    if int(wpd) == 0:
        swapprove.append(item)

sapprove = []
# 已审核队列是否初次审核
for item in approve:
    circuit_id = item.split()[0]
    wpd = subprocess.Popen('%s "select count(*) from circuits_reviewed where circuit_id = %s;"' % (mysql,circuit_id) , shell=True,stdout=subprocess.PIPE).stdout.read().strip("\n")
    if int(wpd) == 1:
        sapprove.append(item)

#print sapprove

stotal = []
#sys.exit()
for item in sapprove:
    #print item
    circuit_id = item.split()[0]
    #print subprocess.Popen('%s "select circuit_id,submited,approved from circuits_reviewed where circuit_id = %s;"' % (mysql, item), shell=True,stdout=subprocess.PIPE).stdout.readlines()
    stotal += subprocess.Popen('%s "select circuit_id,submited,approved from circuits_reviewed where circuit_id = %s;"' % (mysql, circuit_id), shell=True,stdout=subprocess.PIPE).stdout.readlines()

#print stotal

stotal += swapprove
#sys.exit()
allid = {}
for item in stotal:
    tmpdata = item.strip("\n").split("\t")
    if len(tmpdata) == 2:
        tmpdata.append('3')
    if allid.get(tmpdata[0]):
#        allid[tmpdata[0]].append((tmpdata[1],tmpdata[2]))
        del allid[tmpdata[0]]
    else:
        allid[tmpdata[0]] = [(tmpdata[1],tmpdata[2])]

#print allid
#sys.exit()

for key,value in allid.iteritems():
#    print key, value
    getmes(key,value)


#print data

fobj=open("%s.csv" % day,"w")
header=[u"id",u"用戶id",u"用户名",u"昵称",u"电路名",u"厂商",u"original_price",u"price",u"数量",u"审核状态"]
csvf=unicodecsv.writer(fobj,encoding='gbk')
csvf.writerow(header)
for line in data:
    #print line
    if u'\ue536' in line[3] or u'\u2665' in line[3] or u'\u20ac' in line[3] or u'\ue310' in line[3] or u'\u0e08' in line[3] or u'\u0e38' in line[3] or  u'\u0e4a' in line[3] or u'\u0e1a' in line[3] or u'\xab' in line[3] or u'\u0669' in line[3] or u'\u488b' in line[3] or u'\xe4' in line[3]or u'\u21b9' in line[3]:
        line[3] = line[3].replace(u'\ue536','').replace(u'\u2665','').replace(u'\u20ac','').replace(u'\ue310','').replace(u'\u0e08','').replace(u'\u0e38','').replace( u'\u0e4a','').replace(u'\u0e1a','').replace(u'\xab','').replace(u'\u0669','').replace(u'\u488b','').replace(u'\xe4','').replace(u'\u21b9','')
    if u'\u200b' in line[4] or u'\u206f' in line[4] or u'\xa0' in line[4]:
        line[4] = line[4].replace(u'\u200b','').replace(u'\u206f','').replace(u'\xa0','')
    if u'\u200b' in line[6] or u'\xa0' in line[6] or u'\u2122' in line[6] or u'\xae' in line[6] or u'\u2665' in line[6]:
        print 11111111
        line[6] = line[6].replace(u'\u200b','').replace(u'\xa0','').replace(u'\u2122','').replace(u'\xae','').replace(u'\u2665','')
        print line
    #print line
    csvf.writerow(line)
fobj.close()

#sendmail(['shuai.yuan@cn.supplyframe.com','lu.bai@cn.supplyframe.com'],"自动发送","编辑","电路城一周(%s -- %s)提交审核电路" % (startdate, enddate),"cirmall_%s.csv" % day,"/pub/scripts/cirmall/%s.csv" % day)
sendmail(['shuai.yuan@cn.supplyframe.com','yuanyuan.he@cn.supplyframe.com','lu.bai@cn.supplyframe.com'],"自动发送","编辑","电路城一周(%s -- %s)提交审核电路" % (startdate, enddate),"cirmall_%s.csv" % day,"/pub/scripts/cirmall/%s.csv" % day)
#sendmail(['shuai.yuan@cn.supplyframe.com','yuanyuan.he@cn.supplyframe.com','weiting.feng@cn.supplyframe.com'],"自动发送","编辑","电路城一周(%s -- %s)提交审核电路" % (startdate, enddate),"cirmall_%s.csv" % day,"/pub/scripts/cirmall/%s.csv" % day)
#sendmail(['shuai.yuan@supplyframe.cn','yuanyuan.he@supplyframe.cn'],"自动发送","编辑","电路城一周(%s -- %s)提交审核电路" % (startdate, enddate),"cirmall_%s.csv" % day,"/pub/scripts/cirmall/%s.csv" % day)
#sendmail(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","测试电路城一周(%s -- %s)上传电路" % (startdate, enddate),"cirmall_%s.csv" % day,"/pub/scripts/cirmall/%s.csv" % day)
