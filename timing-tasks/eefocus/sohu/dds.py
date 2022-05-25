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
from qn import opqn
from PIL import Image
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from multiprocessing import Pool

'''


'''
userid = "3470578" #eefocustech
channel_name = "通信/网络"
category_title_name = "新闻"
webname = " -- 文章源自搜狐号：易天光通信"
author = "邓德尚"
sohuid = 99938783

dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_article_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306
#dbhost = "192.168.2.82"
#dbname = "pi_article_eefocus"
#dbuser = "root"
#dbpswd = "root"
#dbport = 6033

proxy_host = 'tps187.kdlapi.com'
proxy_port = 15818

proxyMeta = "http://%s:%s" % (proxy_host,proxy_port)

proxies = {
    'http': proxyMeta,
    'https': proxyMeta,
}

sdays = 2 # 允许抓取天数
#colnum_name = "jishu"

downloaddir1 = "/data/vhosts/upload.semidata.info/new.eefocus.com/article/image/"
featherdir = "/data/vhosts/upload.semidata.info/new.eefocus.com/article/feature/"

year = datetime.datetime.now().strftime("%Y")
mon = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
downloaddir = os.path.join(downloaddir1,year,mon,day)




baseimgurl = "https://upload.semidata.info/new.eefocus.com/article/image/%s/%s/%s" % (year,mon,day) # 图片存储路径
fimgpath = os.path.join(featherdir,year,mon,day) # 图片存储路径

#days = [ (datetime.timedelta(days=-item)+datetime.datetime.now()).strftime("%Y%m%d") for item in range(sdays)]
#days += [ str(num) for num in range(1,sdays+1) ]
#print(days)
#sys.exit()

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
        cursor.execute('SELECT * from eef_article_author WHERE name="%s"' % author)
        author_id = int(cursor.fetchall()[0][0])
        print( "插入数据")
        cursor.execute('INSERT INTO `eef_article_draft` (`subject`, `subtitle`, `author`, `user`, `source`, `poll_url`, `content`, `category`, `related_type`, `related`, `time_publish`, `time_update`, `slug`, `seo_title`, `seo_keywords`, `seo_description`, `recommended`, `channel`, `partnumber`, `manufacturer`, `watermark_check`, `autoplay`, `has_catelog`, `summary`, `tag`, `pages`, `time_save`, `status`) VALUES ("%s", "", %s, "%s", "EEFOCUS", "", "%s", "%s", "1", "[]", "0", "0", "", "", "", "", "0", "%s", "[]", "[]", "0", "0", "0", "", "[]", "1", "%s", "2")' % (name,author_id,userid,article,category_title,channel,int(time.time())))
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

def invideo(fkey,fsize,mimetype,ctime,jtname):
    sys.stdout.flush()
    print( "video操作数据库")
    extra = {"vframe":jtname}
    extra = json.dumps(extra)
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('INSERT INTO `eef_article_fileinfo` (fname,fkey,fsize,mime_type,time_create,storage,bucket,extra) values ("%s","%s",%s,"%s",%s,"qiniu","eefocus-article",\'%s\')' % (fkey,fkey,fsize,mimetype,ctime,extra))
        db.commit()
        cursor.execute('SELECT id FROM `eef_article_fileinfo` where fkey="%s" and fsize=%s and time_create=%s;' % (fkey,fsize,ctime))
        vid = int(cursor.fetchall()[0][0])
        db.close()
        print(vid)
        return vid
    except Exception as e:
        print("video插入出错",e)
        return

def selvideo(name):
    sys.stdout.flush()
    print( "查询articleid操作数据库")
    name = name.replace("'","\\'")
    name = name.replace('"','\\"')
    name += webname
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset='utf8')
        cursor = db.cursor()
        cursor.execute('select id from eef_article_draft where subject="%s"' % name)
        articleid = int(cursor.fetchall()[0][0])
        db.close()
        return articleid
    except Exception as e:
        return

def invdraft(articleid,file_id):
    sys.stdout.flush()
    print( "操作数据库")
    try:
        db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser,passwd=dbpswd,port=dbport,charset=
'utf8')
        cursor = db.cursor()
        cursor.execute('insert into eef_article_draft_file (draft,file_id,type) values (%s,%s,"video")' % (articleid,file_id))
        db.commit()
        db.close()
        return True
    except Exception as e:
        return

def getvideo(title,url):
    print("开始下载视频")
    url = 'https://' +  url
    title += "-视频-"
    headers = getheader()
    rdata = requests.get(url,headers=headers)
    rdata = str(rdata.content)
    data = re.findall("url:\s*\"(.*_%s..*?)\"" % sohuid,rdata)
    if not data:
        print("非固定格式视频，请注意")
        data = re.findall("\s+url:\s*\"(.*?)\s*\"\s*,",rdata)
    video = data[0]
    print(video)
    filename = video.split('/')[-1]
    print(filename)
    fpath = os.path.dirname(os.path.realpath(__file__))
    dpath = os.path.join(fpath,'download')
    if not os.path.exists(dpath):
        os.mkdir(dpath)
    
    print('cd %s && wget -O %s --header="user-agent:%s" %s' % (dpath,filename,headers["user-agent"],video))
    if os.system('cd %s && wget -O %s --header="user-agent:%s" %s' % (dpath,filename,headers["user-agent"],video)):
        print("文章下载出现异常")
        return
    print("视频上传七牛")
    qndata = opqn(filename,os.path.join(dpath,filename))
    if not qndata:
        print("七牛处理失败，返回")
        return
    print(qndata)
    vid = invideo(*qndata)
    if not vid:
        print("视频操作数据库失败")
        return
    inmysql(title,'')
    articleid = selvideo(title)    
    if not articleid:
        print('文章插入失败')
        return
    print(articleid)
    invdraft(articleid,vid)
   
    
    

def level1(num):
    sys.stdout.flush()
    url = "https://v2.sohu.com/author-page-api/author-articles/pc/99938783?pNo=00++00"
    try:
        print()
        #print( "获取日期列表",days)
        print( "开始获首页分类")
        print()
        headers = getheader()
        alltitle = []
        surl = url.replace("00++00",str(num))
        print("获取 %s " % surl)
        
        ret = requests.get(surl,headers=headers)
        rdata = ret.content
        rdata = json.loads(rdata)
        #print(rdata)
        print()
        print()
        if rdata['code'] != 200:
            print('页面返回值不为200',rdata['code'])
            return
        else:
            print('页面返回值为200')
        jdata = rdata['data']['pcArticleVOS']
        for item in jdata:
            print()
            day = item['publicTimeStr'].strip()
            print(day)
            if '刚刚' in day or '分钟前' in day or '小时前' in day or '今天' in day:
            #if '刚刚' in day or '分钟前' in day or '小时前' in day or '昨天' in day or '今天' in day:
                print("时间范围内")
            else:
                print("时间范围之外")
                continue
            title = item['title'].strip()
            if selmysql(title):
                continue
            atype = item['type']
            if atype == 4:
               print("判断为视频")
               print(item['link'])
               getvideo(title,item['link'])
               continue
            aurl = "https://" + item['link']
            alltitle.append((title,aurl))
        #print(alltitle)
        return alltitle
    except Exception as e:
         print(e)
         return


def target(arg,count=0):
    sys.stdout.flush()
    try:
        print(arg)
        print("第 %s 次下载文章内容" % count)
        if count > 4:
            print("下载文章内容超过次数,放弃下载")
            return
        count += 1
        turl = arg[1]
        print( "开始获文章内容")
        ret = requests.get(turl,headers=getheader())
        rdata = ret.content
        #print(rdata)

        imgsurl = []
        allimgsurl = []
        articles = ""
        soup = BeautifulSoup(rdata,"html.parser")
        title = arg[0]
        article = soup.find(id='mp-editor')
        if not article:
            print("旧版")
            article = soup.find(class_='article-text')
        #print(article)
        #sys.exit()
        if title and article:
            print( "获取到文章")
            name = title
            print( "文章名 " , name)
            body = article.find_all(name="p")
            print( "文章内容")
            #print(body)
            for item in body:
                #print( item)
                if item.get("data-role") == "editor-name":
                    continue
                titem = str(item)
                #titem = re.sub('text-indent:\s*\d*em\s*;',"",titem)
                titem = re.sub('<span class="backword"><i class="backsohu"></i>返回搜狐，查看更多</span>','',titem)
                titem = re.sub("<a.*?>","",titem)
                titem = re.sub("</a>","",titem)
                articles += titem
            #print( articles)
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
            #print(imgs)
            #sys.exit()
            for img in imgs:
                imgsurl.append(img.get('src'))
            for sub,item in enumerate(imgsurl):
                #print( item)
                imgtype = item.split(".")[-1]
                if imgtype.lower() not in ['bmp','jpg','png','tif','gif','pcx','tga','exif','fpx','svg','psd','cdr','pcd','dxf','ufo','eps','ai','raw','wmf','webp','jpeg','avif']:
                    #print( "图片原格式",imgtype)
                    imgtype = "png"
                #print( imgtype)
                imgname =  "%s-%s.%s" % (str(hash(name)).replace("-","w"),sub,imgtype)
                articles = articles.replace(item,"%s/%s" % (baseimgurl,imgname))
                allimgsurl.append((imgname,item))
            #print(articles)
            #print("添加作者")
            #user = text.find(name='span',attrs={"class":"author"}).text
            #print("\033[35m %s \033[0m" % user)
            #print()
            #articles += '<br><span style="box-sizing: border-box; color: rgb(51, 51, 51); letter-spacing: 0px; font-size: 16px; font-family: 微软雅黑; text-align: justify; text-indent: 24px;">来源：通信产业网<br>作者：%s</span></p>' % user
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
        if imgurl.startswith('//'):
            imgurl = "https:" + imgurl
        print( imgurl)
        print( "开始下载图片")
        if not os.path.exists(downloaddir):
            print( "目录不存在,创建",downloaddir)
            os.makedirs(downloaddir,mode=777)
            os.system("chmod -R 777 %s" % downloaddir)
            os.system("chown -R www: %s" % downloaddir)
        if os.path.exists(os.path.join(downloaddir,imgname)):
            print( "图片已存在,不再下载")
            return True
        #print( imgname)
        print( "图片下载次数",count)
        if count > 5:
            print( "图片下载次数超过 5 次,放弃下载")
            return True
        #ip = getip()
        count += 1
        #print( "获取到ip",ip)
        #proxies = {'http':':'.join(ip)}
        #ret = requests.get(imgurl,proxies=proxies,headers=getheader(),timeout=10)
        
        ret = requests.get(imgurl,headers=getheader())
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
        time.sleep(10)
        print( e)
        return dimag(arg,count)


if __name__ == "__main__":
    print("-- start --")
    createdirs(downloaddir1)
    createdirs(featherdir)
    #level1(1)
    #sys.exit()
    #target(('40G/100G光模块和10G有源光缆在数据中心光网络中的应用 ','https://www.sohu.com/a/472156285_99938783'))
    #for item in level1():
    #    print(item)
    for num in range(1,10):
        print("请求 %s 页" % num)
        tmp = level1(num)
        if not tmp:
            print("首页获取为空，退出")
            sys.exit()
        for item in tmp:
            target(item)
