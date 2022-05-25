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
IIA资讯

工业电子: SELECT id FROM `eef_channel_channel` where title='工业电子';
--  新闻: SELECT category FROM `eef_channel_page_category` where channel=X and category_title="新闻";


'''
userid = "3470578" #eefocustech
channel_name = "工业电子"
category_title_name = "新闻"
webname = " -- 文章源自IIA资讯"

dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_article_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306

spage = 1 # 访问起始页
sdays = 1 # 允许抓取天数
baseurl = "http://www.iianews.com/"
mainurl = "http://www.iianews.com/ca/news"
url = "http://www.iianews.com/ca/newslistAjax.jsp?_category=001002&keyword=&currentPage=0++0"

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
#    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
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


def inmysql(name,article,tag=[]):
    sys.stdout.flush()
#def inmysql(name,article,summary):
    print(tag)
    tag = str(tag).replace("'",'"')
    print(tag)
    print( "操作数据库")
    name = name.replace("'","\\'")
    article = article.replace("'","\\'")
    tag = tag.replace("'","\\'")
    #summary = summary.replace("'","\\'")
    name = name.replace('"','\\"')
    article = article.replace('"','\\"')
    tag = tag.replace('"','\\"')
    #summary = summary.replace('"','\\"')
    #summary = ''
    print(tag)
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
        cursor.execute('INSERT INTO `eef_article_draft` (`subject`, `subtitle`, `author`, `user`, `source`, `poll_url`, `content`, `category`, `related_type`, `related`, `time_publish`, `time_update`, `slug`, `seo_title`, `seo_keywords`, `seo_description`, `recommended`, `channel`, `partnumber`, `manufacturer`, `watermark_check`, `autoplay`, `has_catelog`, `summary`, `tag`, `pages`, `time_save`, `status`) VALUES ("%s", "", "", "%s", "EEFOCUS", "", "%s", "%s", "1", "[]", "0", "0", "", "", "", "", "0", "%s", "[]", "[]", "0", "0", "0", "", "%s", "1", "%s", "2")' % (name,userid,article,category_title,channel,tag,int(time.time())))
        db.commit()
        db.close()
    except Exception as e:
        print( "db insert wrong")
        with open("wrong.data","ab") as f:
            f.write('INSERT INTO `eef_article_draft` (`subject`, `subtitle`, `author`, `user`, `source`, `poll_url`, `content`, `category`, `related_type`, `related`, `time_publish`, `time_update`, `slug`, `seo_title`, `seo_keywords`, `seo_description`, `recommended`, `channel`, `partnumber`, `manufacturer`, `watermark_check`, `autoplay`, `has_catelog`, `summary`, `tag`, `pages`, `time_save`, `status`) VALUES ("%s", "", "", "%s", "EEFOCUS", "", "%s", "%s", "1", "[]", "0", "0", "", "", "", "", "0", "%s", "[]", "[]", "0", "0", "0", "", "%s", "1", "%s", "2")' % (name,userid,article,category_title,channel,tag,int(time.time())))

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
            name_thumb = "%s-thumb.%s" % (sname,imgtype)
            outfile_thumb = os.path.join(fimgpath, name_thumb)
            img_thumb = Image.open(os.path.join(downloaddir,spic))
            out_thumb = img_thumb.resize((260,195),Image.ANTIALIAS)
            if imgtype.lower() == "jpg":
                out_thumb.save(outfile_thumb, "jpeg")
            else:
                out_thumb.save(outfile_thumb, imgtype)
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
            #
            print("出错后尝试转为png 尺寸 260*195")
            name_thumb = "%s-thumb.%s" % (sname,imgtype)
            outfile_thumb = os.path.join(fimgpath, name_thumb)
            img_thumb = Image.open(os.path.join(downloaddir,spic))
            out_thumb = img_thumb.resize((260,195),Image.ANTIALIAS)
            out_thumb.save(outfile_thumb, imgtype)
            return (True,data[-1],imgtype)
    except Exception as e:
        return (False,)
        

def getheader():
    num = len(headers)
    return random.choice(headers)


def level1(ourl=None,cookies=None,headers=None):
    sys.stdout.flush()
    try:
         print()
         if ourl:
            lurl = ourl
         else:
            lurl = url.replace("0++0",str(spage))
         if not headers:
             headers = getheader()
         print( "开始获首页分类")
         #ip = getip()
         #print( "获取到ip",ip)
         #proxies = {'http':':'.join(ip)}
         print(lurl)
         if cookies:
             #ret = requests.get(lurl,proxies=proxies,headers=headers,cookies=cookies,timeout=10)
             ret = requests.get(lurl,headers=headers,cookies=cookies,timeout=10)
         else:
             #ret = requests.get(lurl,proxies=proxies,headers=headers,timeout=10)
             ret = requests.get(lurl,headers=headers,timeout=10)
             cookies = ret.cookies
         rdata = ret.content
         if not rdata:
             return level1(lurl,cookies,headers)

         alltitle = []
         
         soup = BeautifulSoup(rdata,"html.parser")
         print( "IIA资讯")
         text = soup.find_all(name='div', attrs={"class":"info_item clearfix"})
         if text:
             for item in text:
                 tmp = item.find(name='h3')
                 turl = tmp.find(name="a").get("href")
                 tname = tmp.find(name="a").text
                 print(tname,turl)
                 if selmysql(tname):
                    continue 
                 alltitle.append(turl)
             return (alltitle,cookies)
         else:
             print( "页面获取为空，重试")
             return level1(lurl,cookies,headers)
    except Exception as e:
         print( e)
         return level1(lurl,cookies,headers)


def target(url,count=1):
    sys.stdout.flush()
    try:
        print("第 %s 次下载文章内容" % count)
        print(url)
        if count > 5:
            print("下载文章内容超过20次,放弃下载")
            return
        count += 1
        print( "开始获文章内容")
        #ip = getip()
        #print( "获取到ip",ip)
        #proxies = {'http':':'.join(ip)}
        #ret = requests.get(urljoin(baseurl,url),proxies=proxies,headers=getheader(),timeout=10)
        ret = requests.get(urljoin(baseurl,url),headers=getheader(),timeout=10)
        rdata = ret.content
        if not rdata:
            print("获取内容为空")
            return target(url,count)

        imgsurl = []
        allimgsurl = []
        articles = ""
        soup = BeautifulSoup(rdata,"html.parser")
        title = soup.find(name='h1', attrs={"id":"main_title"})
        article = soup.find(name='div', attrs={"id":"content"})
        date = soup.find(name='div',attrs={"class":"artile_attr"}).text
        date = date.replace("年","-").replace("月","-").replace("日","")
        date = date.split()[0]
        tag = soup.find(name="div",attrs={"id":"keysSearchDiv"}).text
        if date not in days:
            print("文章不在抓取时间范围内")
            return date
        
        print(date)
        
        if title and article:
            print( "获取到文章")
            name = title.text
            print( "文章名",name)
            body = article.find_all(name="p")
            print( "文章内容")
            for item in body:
                #print( item)
                titem = str(item)
                titem = re.sub("<a.*?>","",titem)
                titem = re.sub("</a>","",titem)
                articles += titem
            onlychars = articles
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
            p = Pool(3)
            for item in allimgsurl:
                #print( name)
                #dimag(item)
                p.apply_async(dimag,args=(item,))
            p.close()
            p.join()
            if tag:
                tag = tag.replace("标签：","").replace("我要反馈","").split()
                print(tag)
                inmysql(name,articles,tag)
            else:
                inmysql(name,articles)
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
                            os.makedirs(fimgpath)
                        ret = opspic(spic)
                        if len(ret) > 1:
                            upmysql_spic(name,spic.replace(ret[1],ret[2]))
                        else:
                            if ret[0]:
                               upmysql_spic(name,spic)
                    else:
                        print( "首张图不存在")
            return date
        else:
            print( "未获取到,重试")
            return target(url,count)
    except Exception as e:
        print( e)
        return target(url,count)

def dimag(arg, count=1):
    sys.stdout.flush()
    try:
        imgname = arg[0]
        imgurl = arg[1]
        print( "开始下载图片")
        if not os.path.exists(downloaddir):
            print( "目录不存在,创建",downloaddir)
            os.makedirs(downloaddir)
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
            return True
        else:
            print( "图片内容获取为空")
            return dimag(arg,count)
    except Exception as e:
        print( e)
        return dimag(arg,count)

def getnext(url,cookies):
    global spage
    if not url:
        sys.exit()
    ret = target(url)
    print("获取到的日期",ret)
    if ret in days:
        spage += 1
        data = level1(cookies=cookies)
        urls = data[0]
        cookies = data[1]
        if len(urls) >= 1:
            endurl = urls.pop()
        else:
            endurl = ''
            urls = []
        getnext(endurl,cookies)
        for item in urls:
            target(item)
    else:
        print("超出时间范围")
        

if __name__ == "__main__":
    print("-- start --")
    createdirs(downloaddir1)
    createdirs(featherdir)
    #print(level1(ourl=mainurl))
    data = level1(ourl=mainurl)
    urls = data[0]
    cookies = data[1]
    if len(urls) >= 1:
        endurl = urls.pop()
    else:
        endurl = ''
        urls = []
    getnext(endurl,cookies)
    for item in urls:
        target(item)
           
    #target(u'/ca/_01-ABC00000000000306065.shtml')
    #inmysql('1','1','1','1')
    #opspic("8411193015529754084-0.jpg")
    print("--  end  --")
