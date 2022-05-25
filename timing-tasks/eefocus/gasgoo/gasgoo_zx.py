#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import re
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
import json
import time
import random
import MySQLdb
import datetime
import requests
from PIL import Image
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from proxy import getip
from opredis import OpRedis
from multiprocessing import Pool

'''
盖世汽车 资讯

'''
userid = "3470578" #eefocustech
channel_name = "汽车电子"
category_title_name = "新闻"
webname = " -- 文章源自盖世汽车"

dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_article_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306

spage = 1 # 访问起始页
sdays = 1 # 允许抓取天数
baseurl = "https://auto.gasgoo.com/"

urls = ["https://auto.gasgoo.com/industry/C-108/0++0","https://auto.gasgoo.com/parts-news/C-103/0++0","https://auto.gasgoo.com/nev/C-501/0++0","https://auto.gasgoo.com/sales/C-110/0++0","https://auto.gasgoo.com/automaker/C-109/0++0","https://auto.gasgoo.com/smart-connected/C-601/0++0","https://auto.gasgoo.com/new-tech/C-409/0++0","https://auto.gasgoo.com/interview/C-303/0++0", "https://auto.gasgoo.com/industry/C-108/0++0"]

downloaddir1 = "/data/vhosts/upload.semidata.info/new.eefocus.com/article/image/"
featherdir = "/data/vhosts/upload.semidata.info/new.eefocus.com/article/feature/"

year = datetime.datetime.now().strftime("%Y")
mon = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
downloaddir = os.path.join(downloaddir1,year,mon,day)




baseimgurl = "https://upload.semidata.info/new.eefocus.com/article/image/%s/%s/%s" % (year,mon,day) # 图片存储路径
fimgpath = os.path.join(featherdir,year,mon,day) # 图片存储路径

days = [ (datetime.timedelta(days=-item)+datetime.datetime.now()).strftime("%Y-%m-%d") for item in range(sdays)]


#headers = [{"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36"},{"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"},{"user-agent":"Mozilla/5.0 (Linux; Android 9; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.26 SP-engine/2.22.0 baiduboxapp/11.26.5.10 (Baidu; P1 9) NABar/1.0"},{"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"},{"user-agent":"Mozilla/5.0(Linux;Android 5.1.1;OPPO A33 Build/LMY47V;wv) AppleWebKit/537.36(KHTML,link Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 LieBaoFast/4.51.3"}]
headers = [{"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36"},{"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"},{"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"},{"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"},{"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}]

def createdirs(dirname):
    dirs = [os.path.join(dirname,year),os.path.join(dirname,year,mon),os.path.join(dirname,year,mon,day)]
    #print(dirs)
    for item in dirs:
        print(item)
        if not os.path.exists(item):
            print("创建目录 ",item)
            os.makedirs(item)
            os.system("chmod 777 %s" % item)
            os.system("chown www: %s" % item)


def selmysql(name):
    sys.stdout.flush()
    print( "查询数据库")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    if name.endswith('…'):
        print("\033[31m 名称不完全 \033[0m")
        name = name.replace('…','')
    #else:
    #    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        if name.endswith(webname):
            print(1111)
            cursor.execute('select * from eef_article_article where subject="%s"' % name)
            res1 = cursor.fetchall()
            cursor.execute('select * from eef_article_draft where subject="%s"' % name)
            res2 = cursor.fetchall()
        else:
            print(22222)
            cursor.execute('select * from eef_article_article where subject like "%s%%"' % name)
            res1 = cursor.fetchall()
            cursor.execute('select * from eef_article_draft where subject like "%s%%"' % name)
            res2 = cursor.fetchall()
        if res1 or res2:
            print( "\033[31m 文章 %s 已存在 \033[0m" % name)
            return True
        else:
            print( "文章不存在",name)
            return False
    except Exception as e:
        print( "db select wrong")
        with open("wrong.data","ab") as f:
            f.write('\n select * from eef_article_article where subject="%s"\n select * from eef_article_draft where subject="%s"' % (name,name))


def selmysql_spic(name,spic):
    sys.stdout.flush()
    print( "查询数据库 特征图")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('select image from eef_article_draft where subject="%s"' % name)
        res1 = cursor.fetchall()
        print( res1)
        if res1[0][0]:
            print( "\033[31m %s 特征图已存在 \033[0m" % name)
            return True
        else:
            print( "特征图不存在",name)
            return False
    except Exception as e:
        print( "db select feather wrong")
        with open("wrong.data","ab") as f:
            f.write('\n select image from eef_article_draft where subject="%s"' % (name,name))

def upmysql_spic(name,spic):
    sys.stdout.flush()
    print( "修改数据库 特征图")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('update eef_article_draft set image="upload/article/feature/%s/%s/%s/%s" where subject="%s"' % (year,mon,day,spic,name))
        db.commit()
        db.close()
        return True
    except Exception as e:
        print( "db update feather wrong")
        with open("wrong.data","ab") as f:
            f.write('\n update eef_article_draft set image="upload/article/feature/%s/%s/%s/%s" where subject="%s"' % (year,mon,day,spic,name))


def inmysql(name,article):
    sys.stdout.flush()
#def inmysql(name,article,summary):
    print( "操作数据库")
    name = name.replace("'","\\'")
    article = article.replace("'","\\'")
    #summary = summary.replace("'","\\'")
    name = name.replace('"','\\"')
    article = article.replace('"','\\"')
    #summary = summary.replace('"','\\"')
    #summary = ''
    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('SELECT id FROM `eef_channel_channel` where title="%s";' % channel_name)
        channel = int(cursor.fetchall()[0][0])
        print( channel_name,channel)
        cursor.execute('SELECT category FROM `eef_channel_page_category` where channel=%s and category_title="%s";' % (channel, category_title_name))
        category_title = int(cursor.fetchall()[0][0])
        print( category_title_name,category_title)
        print( "插入数据")
        cursor.execute('INSERT INTO `eef_article_draft` (`subject`, `subtitle`, `author`, `user`, `source`, `poll_url`, `content`, `category`, `related_type`, `related`, `time_publish`, `time_update`, `slug`, `seo_title`, `seo_keywords`, `seo_description`, `recommended`, `channel`, `partnumber`, `manufacturer`, `watermark_check`, `autoplay`, `has_catelog`, `summary`, `tag`, `pages`, `time_save`, `status`) VALUES ("%s", "", "", "%s", "EEFOCUS", "", "%s", "%s", "1", "[]", "0", "0", "", "", "", "", "0", "%s", "[]", "[]", "0", "0", "0", "", "[]", "1", "%s", "2")' % (name,userid,article,category_title,channel,int(time.time())))
        db.commit()
        db.close()
    except Exception as e:
        print( "db insert wrong")
        with open("wrong.data","ab") as f:
            f.write('INSERT INTO `eef_article_draft` (`subject`, `subtitle`, `author`, `user`, `source`, `poll_url`, `content`, `category`, `related_type`, `related`, `time_publish`, `time_update`, `slug`, `seo_title`, `seo_keywords`, `seo_description`, `recommended`, `channel`, `partnumber`, `manufacturer`, `watermark_check`, `autoplay`, `has_catelog`, `summary`, `tag`, `pages`, `time_save`, `status`) VALUES ("%s", "", "", "%s", "EEFOCUS", "", "%s", "%s", "1", "[]", "0", "0", "", "", "", "", "0", "%s", "[]", "[]", "0", "0", "0", "", "[]", "1", "%s", "2")' % (name,userid,article,category_title,channel,int(time.time())))

def opspic(spic):
    sys.stdout.flush()
    try:
        try:
            print("尺寸 400*300")
            data = spic.split(".")
            imgtype = data[-1]
            sname = data[0]
            outfile = os.path.join(fimgpath,spic)
            img = Image.open(os.path.join(downloaddir,spic))
            out = img.resize((400,300),Image.ANTIALIAS)
            if imgtype.lower() == "jpg":
                out.save(outfile, 'jpeg')
            else:
                out.save(outfile, imgtype)
            #
            print("尺寸 260*195")
            os.system("chown -R www: %s" % outfile)
            name_thumb = "%s-thumb.%s" % (sname,imgtype)
            outfile_thumb = os.path.join(fimgpath, name_thumb)
            img_thumb = Image.open(os.path.join(downloaddir,spic))
            out_thumb = img_thumb.resize((260,195),Image.ANTIALIAS)
            if imgtype.lower() == "jpg":
                out_thumb.save(outfile_thumb, "jpeg")
            else:
                out_thumb.save(outfile_thumb, imgtype)
            os.system("chown -R www: %s" % outfile_thumb)
            return (True,)
        except Exception as e:
            print("出错后尝试转为png 尺寸 400*300")
            data = spic.split(".")
            imgtype = "png"
            sname = data[0]
            outfile = os.path.join(fimgpath,spic.replace(data[-1],imgtype))
            img = Image.open(os.path.join(downloaddir,spic))
            out = img.resize((400,300),Image.ANTIALIAS)
            out.save(outfile, imgtype)
            os.system("chown -R www: %s" % outfile)
            #
            print("出错后尝试转为png 尺寸 260*195")
            name_thumb = "%s-thumb.%s" % (sname,imgtype)
            outfile_thumb = os.path.join(fimgpath, name_thumb)
            img_thumb = Image.open(os.path.join(downloaddir,spic))
            out_thumb = img_thumb.resize((260,195),Image.ANTIALIAS)
            out_thumb.save(outfile_thumb, imgtype)
            os.system("chown -R www: %s" % outfile_thumb)
            return (True,data[-1],imgtype)
    except Exception as e:
        return (False,)
        

def getheader():
    num = len(headers)
    return random.choice(headers)


def level1(ourl=None,odays=None):
    sys.stdout.flush()
    try:
         global spage
         print()
         if ourl and odays:
            lurl = ourl
            ldays = odays
         else:
            lurl = url.replace("0++0",str(spage))
            ldays = days
         print( "获取日期列表",ldays)
         print( lurl)
         print( "开始获首页分类")
         #ip = getip(types="https")
         #print( "获取到ip",ip)
         #proxies = {'http':':'.join(ip)}
         #ret = requests.get(lurl,proxies=proxies,headers=getheader(),timeout=16)
         ret = requests.get(lurl,headers=getheader(),timeout=20)
         rdata = ret.content

         alltitle = []
         
         soup = BeautifulSoup(rdata,"html.parser")
         print( "盖世汽车 行业")
         text = soup.find_all(name='div', attrs={"class":"contentList"})
         if text:
             for item in text:
                 turl = item.find(name='a')
                 #print(turl)
                 tdate = item.find(name='span',attrs={"class":"time"})
                 #print(tdate)
                 tori = item.find(name='span',attrs={"class":"original"})
                 tdate = tdate.text.split()[0]
                 print(tdate)
                 if tdate in ldays:
                     tname = item.find(name='h2',attrs={"class":"bigtitle"}).text
                     print(tname)
                     if selmysql(tname):
                         continue 
                     if tori:
                         print("原创")
                         alltitle.append((turl.get('href'),"original"))
                     else:
                         print("非原创")
                         alltitle.append((turl.get('href'),))
             eday = text[-1].find(name='span',attrs={"class":"time"}).text.split()[0]
             print(eday)
             if eday in ldays:
                 print(ldays)
                 print("末尾日期为",eday)
                 #print("允许抓取范围缩减一天",ldays)
                 #global spage
                 spage += 1
                 print("请求下一页")
                 oldtitle = level1(url.replace("0++0",str(spage)),ldays)
                 alltitle += oldtitle
             return alltitle
         else:
             return level1(url.replace("0++0",str(spage)),ldays)
    except Exception as e:
         print( e)
         return level1(url.replace("0++0",str(spage)),ldays)


def target(arg,count=1):
    sys.stdout.flush()
    try:
        print(arg)
        print("第 %s 次下载文章内容" % count)
        if count > 20:
            print("下载文章内容超过20次,放弃下载")
            return
        count += 1
        ori = ''
        turl = arg[0]
        if len(arg) > 1:
            ori = arg[1]
        print( "开始获文章内容")
        #ip = getip()
        #print( "获取到ip",ip)
        #proxies = {'http':':'.join(ip)}
        #ret = requests.get(urljoin(baseurl,turl),proxies=proxies,headers=getheader(),timeout=10)
        ret = requests.get(urljoin(baseurl,turl),headers=getheader(),timeout=10)
        rdata = ret.content

        imgsurl = []
        allimgsurl = []
        articles = ""
        soup = BeautifulSoup(rdata,"html.parser")
        text = soup.find(name="div",attrs={"class":"detailed"})
        title = text.find(name='h1')
        print(title)
        keytxt = soup.find(name='div',attrs={"class":"keytxt"})
        article = soup.find(name='div', attrs={"id":"ArticleContent"})
        if title and article:
            print( "获取到文章")
            name = title.text
            print( "文章名 " , name)
            body = article.find_all(name="p")
            print( "文章内容")
            for item in body:
                #print( item)
                titem = str(item)
                titem = re.sub("<a.*?>","",titem)
                titem = re.sub("</a>","",titem)
                articles += titem
            #print( articles)
            #sys.exit()
            onlychars = articles
            #print( "去除html")
            #print( re.sub("<.*?>","",onlychars))
            #print( article.text.replace("\n",""))
            #summary = article.text.replace("\n","")[:255]
            #num = summary.rfind("。")
            #summary = summary[:num+1]
            #print( summary)
            print()
            imgs = article.find_all(name="img")
            for img in imgs:
                imgsurl.append(urljoin(baseurl,img.get('src')))
            for sub,item in enumerate(imgsurl):
                print( item)
                imgtype = item.split(".")[-1]
                if imgtype.lower() not in ['bmp','jpg','png','tif','gif','pcx','tga','exif','fpx','svg','psd','cdr','pcd','dxf','ufo','eps','ai','raw','wmf','webp','jpeg','avif']:
                    #print( "图片原格式",imgtype)
                    imgtype = "png"
                #print( imgtype)
                imgname =  "%s-%s.%s" % (str(hash(name)).replace("-","w"),sub,imgtype)
                articles = articles.replace(item,"%s/%s" % (baseimgurl,imgname))
                allimgsurl.append((imgname,item))
            if ori:
                print("添加作者")
                user = text.find(name='div',attrs={"class":"userInfo"}).find_all(name='a')[-1].text
                print("\033[35m %s \033[0m" % user)
                print()
                articles += '<br><span style="box-sizing: border-box; color: rgb(51, 51, 51); letter-spacing: 0px; font-size: 16px; font-family: 微软雅黑; text-align: justify; text-indent: 24px;">来源：盖世汽车<br>作者：%s</span></p>' % user
            else:
                articles += '<br><span style="box-sizing: border-box; color: rgb(51, 51, 51); letter-spacing: 0px; font-size: 16px; font-family: 微软雅黑; text-align: justify; text-indent: 24px;">来源：盖世汽车</span></p>'
            p = Pool(3)
            for item in allimgsurl:
                #print( name)
                #dimag(item)
                p.apply_async(dimag,args=(item,))
            p.close()
            p.join()
            inmysql(name,articles)
            #inmysql(name,articles,summary)
            print( "处理特征图")
            if len(allimgsurl) >= 1:
                spic = allimgsurl[0][0]
                print( spic)
                if selmysql_spic(name,spic):
                    print( "特征图已存入数据库",name)
                else:
                    print( "特征图未入库",name)
                    if os.path.exists(os.path.join(downloaddir,spic)):
                        print( "首张图存在")
                        if not os.path.exists(fimgpath):
                            os.makedirs(fimgpath,mode=777)
                            os.system("chmod -R 777 %s" %  fimgpath)
                            os.system("chown -R www: %s" % fimgpath)
                        ret = opspic(spic)
                        if len(ret) > 1:
                            upmysql_spic(name,spic.replace(ret[1],ret[2]))
                        else:
                            if ret[0]:
                               upmysql_spic(name,spic)
                    else:
                        print( "首张图不存在")

        else:
            print( "未获取到,重试")
            return target(arg,count)
    except Exception as e:
        print( e)
        return target(arg,count)

def dimag(arg, count=1):
    sys.stdout.flush()
    try:
        imgname = arg[0]
        imgurl = arg[1]
        print( "开始下载图片")
        if not os.path.exists(downloaddir):
            print( "目录不存在,创建",downloaddir)
            os.makedirs(downloaddir,mode=777)
            os.system("chmod -R 777 %s" % downloaddir)
            os.system("chown -R www: %s" % downloaddir)
        if os.path.exists(os.path.join(downloaddir,imgname)):
            print( "图片已存在,不再下载")
            return True
        #print( imgurl)
        #print( imgname)
        print( "图片下载次数",count)
        if count > 30:
            print( "图片下载次数超过 30 次,放弃下载")
            return True
        #ip = getip()
        count += 1
        #print( "获取到ip",ip)
        #proxies = {'http':':'.join(ip)}
        #ret = requests.get(imgurl,proxies=proxies,headers=getheader(),timeout=10)
        ret = requests.get(imgurl,headers=getheader(),timeout=10)
        print( ret.status_code)
        if ret.status_code not in  [200]:
            return dimag(arg,count)
        rdata = ret.content
        print( downloaddir)
        if rdata:
            print( "图片不存在,本地写入")
            with open(os.path.join(downloaddir,imgname),'wb') as f:
                f.write(rdata)
            os.system("chown -R www: %s" % downloaddir)
            return True
        else:
            print( "图片内容获取为空")
            return dimag(arg,count)
    except Exception as e:
        print( e)
        return dimag(arg,count)


if __name__ == "__main__":
    print("-- start --")
    createdirs(downloaddir1)
    createdirs(featherdir)
    for url in urls:
        spage = 1
        #print(level1())
        print(url)
        data = level1()
        for item in data:
            target(item)
        print("停顿")
        time.sleep(random.randint(5,9))
        print()
    #target(('news/202103/1I70243556C108.shtml',))
    print("--  end  --")
    #inmysql('1','1','1','1')
    #opspic("8411193015529754084-0.jpg")
