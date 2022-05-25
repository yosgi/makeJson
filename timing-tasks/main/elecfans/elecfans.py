# -*- coding=utf8 -*-

import re
import os
import sys
import time
import MySQLdb
import datetime
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

proxy_host = 'tps187.kdlapi.com'
proxy_port = 15818


proxyMeta = "http://%(host)s:%(port)s" % {
    "host": proxy_host,
    "port": proxy_port,
}

proxies = {
    'http': proxyMeta,
    'https': proxyMeta,
}

dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_main_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306

replace_dir = "/data/vhosts/main.eefocus.com/"
download_dir = os.path.join(replace_dir,"upload/document/document/")
#download_dir = "C:\\Users\\xu\\Desktop\\main"

year = datetime.datetime.now().strftime("%Y")
mon = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
downloaddir = os.path.join(download_dir,year,mon,day)

sdays = 160
days = [ (datetime.timedelta(days=-item)+datetime.datetime.now()).strftime("%Y-%m-%d") for item in range(sdays)]

def smysql(name):
    sys.stdout.flush()
    print( "查询数据库")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('select * from  eef_document_article where subject="%s"' % name)
        res = cursor.fetchall()
        if res:
            print( "\033[31m 资料 %s 已存在 \033[0m" % name)
            return True

        print( "文章不存在",name)
        db.close()
        return False
    except Exception as e:
        print( "db select wrong")
        return True

def imysql(name,desc,tag,filepath,filename,filetype,filesize):
    sys.stdout.flush()
    print( "数据库插入数据")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('SELECT max(`order`) FROM `eef_document_article`;')
        res = cursor.fetchall()
        num = int(res[0][0])
        print("查询到最大order", num)
        timestamp = round(time.time())
        cursor.execute('insert into eef_document_article (subject,content,markup,uid,category,cluster,status,active,time_submit,time_publish,time_update,user_update,seo_keywords,path,file_name,`type`,size,is_hot,recommended,download_count,`order`) values ("%s","<p>%s</p>","html",3470578,0,2,11,0,%s,%s,%s,0,"%s","%s","%s","%s",%s,0,0,0,%s)' % (name, desc,timestamp,timestamp,timestamp,tag,filepath,filename,filetype,filesize,num+1))
        db.commit()
        cursor.execute('select id from eef_document_article where subject="%s";' % name)
        res = cursor.fetchall()
        aid = int(res[0][0])
        print("eef_document_article数据插入后文章id",aid)
        cursor.execute('insert into eef_document_cluster_article (article,cluster) values (%s,2);' % aid)
        db.commit()
        print( "eef_document_cluster_article数据已插入",name)
        cursor.execute('insert into eef_document_compiled (name, article, type, content) values ("%s-html", "%s", "html","<p>%s</p>")' % (aid,aid,desc))
        db.commit()
        print("eef_document_compiled数据已插入")
        db.close()
        return True
    except Exception as e:
        print( "db select wrong")
        return True



def getpages(num):
    data = []
    url='http://www.elecfans.com/soft/special/soft_New0000++00.html'
    url = url.replace('00++00',str(num))
    ret = requests.get(url,headers=headers)
    soup = BeautifulSoup(ret.content,"html.parser")
    text = soup.find(id="mainContent")
    pages = text.find_all('li')
    for item in pages:
        # print(item)
        tmp = item.find_all('a')
        name = tmp[1].text
        url = tmp[1].get('href')
        # print(name,url)
        tmp = item.find_all('span')
        day = tmp[-1].text
        # print(day,days)
        # print(name,url,day)
        if day not in days:
            print('不在抓取时间内')
            continue
        if smysql(name):
            continue
        data.append(url)
    return data


def getpage(url):
    try:
        ret = requests.get(url,headers=headers)
    except Exception as e:
        return 1
    soup = BeautifulSoup(ret.content,"html.parser")
    name = soup.find('h1').text
    if smysql(name):
        return 0
    try:
        jf = soup.find(class_='info-title jifen').text
    except Exception as e:
        try:
            jf = soup.find(class_='dataParam black').text.split('：')[-1].strip()
        except Exception as e:
            try:
                jf = soup.find(id='J_Jifen').text.replace('分','').strip()
            except Exception as e:
                return 1
    print(jf)
    if int(jf) > 0:
        print('下载需要积分，退出')
        return 1
    tag = []
    ttags = soup.find_all(class_='tags')
    try:
        if not ttags:
            ttags = soup.find(class_='tagDown fl link-blue').find_all('a')
            for item in ttags:
                tag.append(item.text.split('(')[0])
        else:
            for item in ttags:
                tag.append(item.find('a').text)
    except Exception as e:
        print("没有tag")
    tag = ','.join(tag)
    try:
        desc = soup.find(class_='intro-content').text
    except Exception as e:
        try:
            desc = soup.find(id='dataIntro').find('p').text
        except Exception as e:
            desc = ''
    # print(desc)
    if not soup.find(id='df-btnDown'):
        print("页面没有下载地址")
        return 1
    purl = 'http://www.elecfans.com/' + soup.find(id='df-btnDown').get('href')
    # print(purl)
    
    try:
        ret = requests.get(purl,headers=headers)
    except Exception as e:
        return 1
    ftype = ret.history[0].headers['Location'].split('.')[-1].strip()
    ftype = ftype.replace("?filename=","")

    filename = str(hash(name)).replace("-","m") + "." + ftype
    if not os.path.exists(downloaddir):
       print("创建目录 ",downloaddir)
       os.makedirs(downloaddir)
       #os.system("chmod 777 %s" % item)
       os.system("chown -R www: %s" % download_dir)

    filepath = os.path.join(downloaddir,filename)
    # print(ftype)
    with open(filepath,'wb') as f:
       f.write(ret.content) 
    filesize = os.path.getsize(filepath)
    os.system("chown www: %s" % filepath)
    if filesize < 3000:
        print('文件过小,可能存在异常，重试')
        print(filename)
        return 1
    print(desc, tag, filepath, filename, ftype, filesize)
    imysql(name,desc,tag,filepath.replace(replace_dir,""),filename,ftype,filesize)
    time.sleep(2)
    return 0

# getpage('http://www.elecfans.com/code/mcu/202106021628945.html')


for item in range(1,11):
    print("请求页数： ",item)
    n =0 
    while True:
        sys.stdout.flush()
        ret = getpages(item)
        n += 1
        print("起始页第 %s 次下载" % n)
        if n > 3:
            print("尝试次数过多，放弃下载")
            sys.exit()

        if not ret:
            print("第 %s 页请求为空，再次请求" % item)
            # time.sleep(10)
            continue
        else:
            break
    for target in ret:
        n = 0
        while True:
            sys.stdout.flush()
            print()
            print()
            n += 1
            print("第 %s 次下载" % n)
            if n > 3:
                print("尝试次数过多，放弃下载")
                break
            ret = getpage(target)
            if ret == 2:
                sys.exit()
            elif ret == 1:
                continue
            else:
                break


