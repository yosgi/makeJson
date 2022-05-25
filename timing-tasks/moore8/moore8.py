#!/usr/bin/env python
# -*- coding=utf8 -*-

import unicodecsv
import time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf8') 
sys.path.append("/pub/scripts/bbs/api")
from sendmail import sendmail



day=time.strftime("%Y-%m-%d")
dayOfWeek=time.strftime("%u")
timeArray=time.strptime(day,"%Y-%m-%d")
endtime=int(time.mktime(timeArray)) - (int(dayOfWeek) - 1) * 86400
starttime=endtime - 7*86400

print "time: ",day,dayOfWeek,starttime,endtime

mysql="/bin/mysql -umoore8 -p8us#@sa1IuX2 -N -hrm-uf62o8x44q3oizi54.mysql.rds.aliyuncs.com moore8 -e "

def chtime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def oplog(arg):
    if not arg:
        return 0
    list1 = arg.split('\n')
    count = 0
    newargs = []
    alluser = []
    usertime = {}
    for item in list1:
        newargs.append(item.split())
    for item in newargs:
        if item[1] not in alluser:
            alluser.append(item[1])
            usertime[item[1]] = []
            usertime[item[1]].append(item[0])
        else:
            usertime[item[1]].append(item[0])
    for key,value in usertime.iteritems():
        num = len(value) - 1
        for item  in xrange(num):
            if int(value[item+1]) - int(value[item]) > 13:
                count += 1
    return count


#total = subprocess.Popen('/bin/mysql -uroot -proot -N -S /tmp/mysql-3315.sock moore8 -e "SELECT COUNT(*) AS numrows FROM (course) WHERE is_deleted =  0 AND verify_status =  2"',shell=True,stdout=subprocess.PIPE).stdout.read().strip("\n")
total = subprocess.Popen('%s "SELECT COUNT(*) AS numrows FROM (course) WHERE is_deleted =  0 AND verify_status =  2"' % mysql.strip('"'),shell=True,stdout=subprocess.PIPE).stdout.read().strip("\n")

print total

print int(total)//20
print int(total)%20

if int(total)%20:
    num = int(total)//20 + 1
else:
    num = int(total)//20
print num

data = []
for i in range(num):
    print  "20 offset %s" % (i*20)

    result = subprocess.Popen('%s"SELECT course.id, version_id, draft_version_id, title, created_at, published_time, num_subscribers, room_id, verify_status, nick_name as owner FROM (course) LEFT JOIN member ON member.user_id = course.owner_id WHERE is_deleted =  0 AND verify_status =  2 ORDER BY published_time desc LIMIT 20 offset %s"' % (mysql.strip('"'), i*20),shell=True,stdout=subprocess.PIPE).stdout.readlines()

    if not result:
        sys.exit(1)

    for item in result:
        item = item.split('\t')
        #print item
        id = item[0]
        title = item[3]
        owner = item[-1]
        create = item[4]
        publish = item[5]
        member = item[6]
        room = item[7]
        version_id = item[1]
        print version_id
        ca_id = subprocess.Popen('%s"SELECT category_id FROM course_category WHERE version_id=%s"' % (mysql.strip('"'),version_id) ,shell=True,stdout=subprocess.PIPE).stdout.read()
        print "-------------"
        print "ca_id", ca_id.replace('\n',',')
        cl = subprocess.Popen('%s"SELECT name FROM (category) WHERE id in (%s)"' % (mysql.strip('"'),ca_id.replace('\n',',').strip(",")) ,shell=True,stdout=subprocess.PIPE).stdout.read().replace('\n',',').strip(",")
        print "++++++++"
        rmember = subprocess.Popen('%s"SELECT COUNT(*) AS numrows FROM (student) WHERE course_id =  %s"' % (mysql.strip('"'), id), shell=True,stdout=subprocess.PIPE).stdout.read().replace('\n',',').strip(",")
        count1 = subprocess.Popen('%s"SELECT COUNT(id) AS page_views FROM (user_action_log) WHERE controller =  \'courses\' AND action =  \'course\' AND course_id=%s"' % (mysql.strip('"'),id) ,shell=True,stdout=subprocess.PIPE).stdout.read().strip('\n')
        #print(count1)
        count2 = subprocess.Popen('%s"SELECT created_at,user_id FROM (user_action_log) WHERE controller =  \'course_api\' AND action =  \'lecture_viewed\' AND course_id=%s"' % (mysql.strip('"'),id) ,shell=True,stdout=subprocess.PIPE).stdout.read().strip('\n')
        count_week1 = subprocess.Popen('%s"SELECT COUNT(id) AS page_views FROM (user_action_log) WHERE controller =  \'courses\' AND action =  \'course\' AND course_id=%s AND created_at > %s AND created_at < %s"' % (mysql.strip('"'),id,starttime,endtime) ,shell=True,stdout=subprocess.PIPE).stdout.read().strip('\n')
        count_week2 = subprocess.Popen('%s"SELECT created_at,user_id FROM (user_action_log) WHERE controller =  \'course_api\' AND action =  \'lecture_viewed\' AND course_id=%s AND created_at > %s AND created_at < %s"' % (mysql.strip('"'),id,starttime,endtime) ,shell=True,stdout=subprocess.PIPE).stdout.read().strip('\n')
        create = chtime(int(create))
        publish = chtime(int(publish))
        count1=int(count1)
        count2=int(oplog(count2))
        count_week1=int(count_week1)
        count_week2=int(oplog(count_week2))
        count=count1+count2
        count_week=count_week1+count_week2
        print count
        print
        print
    
        data.append([u"%s" % title,u"%s" % cl,u"%s" % owner,u"%s" % create,u"%s" % publish,u"%s" % count,u"%s" % count_week,u"%s" % member,u"%s" % rmember,u"%s" % room])

#sys.exit(1)

fobj=open("moore8_%s.csv" % day,"w")
header=[u"标题",u"分类",u"作者名",u"创建时间",u"最新发布时间",u"浏览量 截止邮件发出前",u"上周访问量",u"前台学员数",u"真实学员数",u"直播间ID"]
#header=[u"标题",u"作者名",u"创建时间",u"最新发布时间",u"浏览量",u"学员数",u"直播间ID"]


csvf=unicodecsv.writer(fobj,encoding='gbk')
csvf.writerow(header)
for line in data:
    for sub,item in enumerate(line):
        if u'\xae' in item or u"\u2122" in item or u'\u200b' in item or u'\xa0' in item or u'\u2022' in item:
            line[sub] = item.replace(u'\u200b','').replace(u'\xa0','').replace(u'\u2122','').replace(u'\xae','').replace(u'\u2022','')
    print line
    csvf.writerow(line)
fobj.close()

#sendmail(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","每周moore8课程数据","moore8_%s.csv" % day,"/pub/scripts/moore8/moore8_%s.csv" % day)
sendmail(['yuanyuan.he@cn.supplyframe.com','shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","每周moore8课程数据","moore8_%s.csv" % day,"/pub/scripts/moore8/moore8_%s.csv" % day)
#sendmail(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","每周moore8课程数据","moore8_%s.csv" % day,"/pub/scripts/moore8/moore8_%s.csv" % day)
