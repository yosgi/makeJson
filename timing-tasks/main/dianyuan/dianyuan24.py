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

# cookies = {'cookie':'[__yjs_duid=1_58397096e76941495215ab91277c138e16226974563221; cookie_uid=wbc2mcltjx1; UM_distinctid=179d04e35af9a5-0a0e40b09b8e9f-2363163-240000-179d04e35b0bc51; CNZZDATA5781160=cnzz_eid%3D1129602721-1622696414-%26ntime%3D16226964141; Hm_lvt_dd2486feb652190c6d492457baf80d7b=1622697457; _ga=GA1.2.1908502405.1622697457; _gid=GA1.2.576583942.1622697457; _version_up_temp=1; CNZZDATA2637227=cnzz_eid%3D1218853652-1622692698-%26ntime%3D1622698153; __gads=ID=49d43b13219b0e07-22d3ef1926c90017:T=1622701294:RT=1622701294:S=ALNI_MaEOCk3azZSaSKp1htegIlw8maMUA; __site_info__=a9bddb041ed2f74610a1e5d7bf83560b; __time_a_=8709399409; _user_account_=c96a6099998c3997b9a20d744afeb190; _uid___=142875; username=dy-UW9B5mp2; Hm_lpvt_dd2486feb652190c6d492457baf80d7b=1622701415]'}
now = int(round(time.time())) - 10 
cookies = {}
# cookies['__yjs_duid']='1_58397096e76941495215ab91277c138e1622697456322'
# cookies['cookie_uid']='wbc2mcltjx'
# cookies['UM_distinctid']='179d04e35af9a5-0a0e40b09b8e9f-2363163-240000-179d04e35b0bc5'
# cookies['Hm_lvt_dd2486feb652190c6d492457baf80d7b']='%s' % now
# cookies['_ga']='GA1.2.1908502405.1622697457'
# cookies['_gid']='GA1.2.576583942.1622697457'
cookies['_version_up_temp']='1'
# cookies['CNZZDATA2637227']='cnzz_eid%%3D1218853652-%s-%%26ntime%%3D%s' % (now-4759,now+696)
# cookies['CNZZDATA2664271']='cnzz_eid%3D899561588-1622701923-https%253A%252F%252Fwww.dianyuan.com%252F%26ntime%3D1622701923'
# cookies['CNZZDATA5781160']='cnzz_eid%3D1129602721-1622696414-%26ntime%3D1622702224'
cookies['_gat_gtag_UA_39990293_1']='1'
cookies['__gads']='ID=38cea80b49e9a53f-2210a66d2ec900b8:T=1622702525:RT=1622702525:S=ALNI_MZtQRUcRwktVReSTlYbwf0uhnw7jQ'
cookies['__site_info__']='a9bddb041ed2f74610a1e5d7bf83560b'
cookies['__time_a_']='8709399409'
cookies['_user_account_']='4dd2304f7a953d266fff00ab4ad2667c'
cookies['_uid___']='652560'
cookies['username']='dy-UW9B5mp2'
cookies['_gat_gtag_UA_118658118_1']='1'
# cookies['Hm_lpvt_dd2486feb652190c6d492457baf80d7b']='1622702572'

dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_main_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306

replace_dir = "/data/vhosts/main.eefocus.com/"
download_dir = os.path.join(replace_dir,"upload/document/document/")

year = datetime.datetime.now().strftime("%Y")
mon = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
downloaddir = os.path.join(download_dir,year,mon,day)

sdays = 180
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
        print( "db select wrong",e)
        return True



def getpages(num):
# getall 为 True 不按时间限制，全部下载 False 按时间限制下载
    data = []
    url='https://www.dianyuan.com/index.php?do=download_file_list&cateid=24&rc_start=00++00'
    url = url.replace('00++00',str(num*10))
    print(url)
    ret = requests.get(url,headers=headers)
    # print(cookies)
    # print(requests.utils.dict_from_cookiejar(ret.cookies))
    soup = BeautifulSoup(ret.content,"html.parser")
    text = soup.find(class_="leftMain").find(class_='r2').find_all('li')
    # print(text)
    # sys.exit()
    for item in text:
        # print(item)
        tmp = item.find('a')
        url = tmp.get('href')
        name = tmp.text.strip()
        name = name.replace("\\","\\\\").replace('(','\\(').replace(')','\\)')
        if smysql(name):
            continue
        day = item.find('span').text
        if day not in days:
            print('不在抓取时间内',day)
            continue
        tag = []
        tags = item.find(class_='p3').find_all('a')
        for tmp in tags:
            tag.append(tmp.text) 
        tag = ','.join(tag)
        print(url)
        # data.append((name,'https://mbb.eet-china.com' + url,ftype,tag))
        data.append((name,url,tag))
    print(data)
    return data

def getpage(name,url,tag):
    try:
        ret = requests.get(url,headers=headers)
    except Exception as e:
        return 1
    soup = BeautifulSoup(ret.content,"html.parser")
    text = soup.find('h3',string=re.compile(name)).parent
    desc = text.find('p').text.strip()
    ftype = text.find('li').find('span').text.strip()
    pid = re.split('[/.]',url)[-2]
    headers['referer'] = url
    print(pid)
    # print(text)
    filename = str(hash(name)).replace("-","m") + "." + ftype
    if not os.path.exists(downloaddir):
       print("创建目录 ",downloaddir)
       os.makedirs(downloaddir)
       # os.system("chmod 777 %s" % item)
       os.system("chown -R www: %s" % download_dir)

    filepath = os.path.join(downloaddir,filename)
    # print(ftype)
    try:
        ret = requests.get('https://www.dianyuan.com/index.php?do=download_file_download&id=%s' % pid,cookies=cookies,headers=headers)
    except Exception as e:
        return 1
    with open(filepath,'wb') as f:
       f.write(ret.content) 
    filesize = os.path.getsize(filepath)
    os.system("chown www: %s" % filepath)
    if filesize < 3000:
        print('文件过小,可能存在异常，重试')
        return 1
    print(desc, tag, filepath, filename, ftype, filesize)
    imysql(name,desc,tag,filepath.replace(replace_dir,""),filename,ftype,filesize)
    time.sleep(10)
    return 0

# getpage('838单端9瓦单声道功率放大器', 'https://www.dianyuan.com/download/62409.html', 'EMC,EMI')
# getpage('用于汽车外部照明的 DLP® 动态地面投影技术', 'https://www.dianyuan.com/download/62482.html', 'EMC,EMI')
for item in range(0,100):
    print("请求页数： ",item)
    n = 0
    while True:
        sys.stdout.flush()
        ret = getpages(item)
        n += 1
        print("起始页第 %s 次下载" % n)
        if n > 3:
            print("尝试次数过多，放弃下载")
            sys.exit()
            #break

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
            print("内容页第 %s 次下载" % n)
            if n > 4:
                print("尝试次数过多，放弃下载")
                break
            ret = getpage(*target)
            if ret == 2:
                sys.exit()
            elif ret == 1:
                continue
            else:
                break
