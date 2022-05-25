# -*- coding=utf8 -*-

# 地址 https://dl.21ic.com/list.html
# 用户名/密码 spee2021/eefocus2021
# 需要cookie 和 referer

# 0601 list.html 页面访问不了


import random
import re
import os
import sys
import time
import MySQLdb
import datetime
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'Referer': 'https://dl.21ic.com/download/ic-486509.html'}

proxy_host = 'tps187.kdlapi.com'
proxy_port = 15818
#proxy_username = 't12312827165733'
#proxy_pwd = "f5daui7a"

#proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#    "host": proxy_host,
#    "port": proxy_port,
#    "user": proxy_username,
#    "pass": proxy_pwd,
#}
proxyMeta = "http://%s:%s" % (proxy_host,proxy_port)

proxies = {
    'http': proxyMeta,
    'https': proxyMeta,
}

login_url = 'https://my.21ic.com/member.php?mod=logging_normal&action=login&loginsubmit=yes&loginhash=LcHYh&inajax=1'
data = {'formhash': '4f5f7b9e', 'referer': 'https://dl.21ic.com/list.html','username': 'spee2021','password': 'eefocus2021','questionid': 0,'answer': ''}
ret = requests.post(login_url,data,headers=headers,proxies=proxies)
cookies = requests.utils.dict_from_cookiejar(ret.cookies)
#print(cookies)
#sys.exit()

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

sdays = 120
days = [ (datetime.timedelta(days=-item)+datetime.datetime.now()).strftime("%Y-%m-%d") for item in range(sdays)]
# print(days)

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


# cookies = {}
# headers['referer'] = 'https://dl.21ic.com/download/ic-486509.html'
cookies['__fansid'] = str(round(int(time.time()*1000)))+str(365*10)

def getpages(page):
# getall 为 True 不按时间限制，全部下载	False 按时间限制下载
    data = []
    url='https://dl.21ic.com/list.html?inl=1&page=00++00'
    url = url.replace('00++00',str(page))
    ret = requests.get(url,cookies=cookies,headers=headers,proxies=proxies)
    # print(cookies)
    # print(requests.utils.dict_from_cookiejar(ret.cookies))
    soup = BeautifulSoup(ret.content,"html.parser")
    text = soup.find(class_="items")
    pages = text.find_all('li')
    for item in pages:
    
        # print(name,url)

        tmp = item.find(class_='hotlist_cont').find_all('p')[0].find_all('span')
        jf = tmp[2].text.split('：')[-1].replace('分','')
        if int(jf) > 0:
            print("下载需要积分")
            continue
        day = tmp[1].text.split('：')[-1]
        if day not in days:
            print('不在抓取时间内')
            continue
        name = item.find('h3').text
        if smysql(name):
            continue
        url = item.find('a').get('href')
        data.append((name,'https://dl.21ic.com' + url))
        # data.append((name,'https://dl.21ic.com' + url,day,jf))
    return data

def getpage(name,url):
    #now = int(round(time.time()))
    #print(name,url)
    #cookies['Hm_lvt_22332d78648b7586de15b4542cb6f7ae']='%s' % (now-10)
    #cookies['_gid']='GA1.2.1006918765.%s' % (now-10)
    #cookies['aSr_connect_is_bind']='0'
    #cookies['__utmz']='39547766.%s.1.1.utmcsr=my.21ic.com|utmccn=(referral)|utmcmd=referral|utmcct=/' % (now-10)
    #cookies['__utma']='39547766.87081149.%s.%s.%s.1' % (now-10,now-10,now-10)
    #cookies['__utmc']='39547766'
    #cookies['aSr_seccode']='1228.3f4021621524963c10'
    #cookies['Hm_lvt_77b58db1e4bc572516ab5fe31529b92e']='%s,%s,%s,%s' % (now-10,now+55,now+55+65,now+55+65*2) 
    ## cookies['PHPSESSID']='iqvmf0nans2pfa1p7hqa0js2a2'
    #cookies['Hm_lpvt_77b58db1e4bc572516ab5fe31529b92e']='%s' % (now+217)
    #cookies['__utmt']='1'
    #cookies['__utmb']='39547766.6.10.%s' % (now-10)
    #cookies['__fanvt']='1622512223271'
    #cookies['_ga_8R2MPCQQZ0']='GS1.1.%s.7.1.%s.0' % (now-10,now+216)
    #cookies['_ga']='GA1.2.1426173338.%s' % (now-10)
    # print(cookies)

    cookies = {'cookie':'[__utmz=39547766.1622524217.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __fansid=1622524217136132202; aSr_saltkey=1; aSr_lastvisit=1622520726; aSr_connect_is_bind=0; __utmc=39547766; __utma=39547766.1031329486.1622524217.1623305394.1623717636.7; __utmt=1; _gid=GA1.2.1265070672.1623717636; aSr_pc_size_c=0; aSr_seccode=564.7ed68300fae5415c4e; aSr_sid=jz2DG1; aSr_ulastactivity=e353PhDFBe2YWXJ5MGYRQfNzkMRD1xIPeRKSw%2B0q1kW4G81z454N; aSr_auth=8299%2F0b6j9FlAfOtFsrQcwq1%2BjAC4ezp0YQN0KqLM6CWGBKHNlno6PCQM%2FPxrVHlYLqDDdrjWOg7qt4EXbNdkDRhqeZEON0Z1n%2B4XmkBoA; aSr_ic21_user=spee2021%093235128; www_username=spee2021; bbs_username=spee2021; ic21_bbsuser=spee2021%093235128; aSr_lastcheckfeed=3235128%7C1623717642; PHPSESSID=u4jf3msub68rjs5bee14j6s1u6; Hm_lvt_77b58db1e4bc572516ab5fe31529b92e=1623305394,1623717636,1623717641,1623717654; aSr_lastact=1623717655%09api.php%09member%3Apms; Hm_lpvt_77b58db1e4bc572516ab5fe31529b92e=1623717699; __utmb=39547766.5.10.1623717636; __fanvt=1623717698996; _ga_8R2MPCQQZ0=GS1.1.1623717636.7.1.1623717699.0; _ga=GA1.2.1426173338.1622524217; _gat_gtag_UA_197335059_1=1]'}
 


    try:
        print(2,name,url)
        ret = requests.get(url,cookies=cookies,headers=headers,proxies=proxies)
    except Exception as e:
        print(e)
        return 1
    # print(ret.content)
    #print(requests.utils.dict_from_cookiejar(ret.cookies))
#    try:
#        print('1尝试获取session')
#        print(requests.utils.dict_from_cookiejar(ret.cookies))
#        cookies['PHPSESSID'] = requests.utils.dict_from_cookiejar(ret.cookies)['PHPSESSID']
#    except Exception as e:
#        try:
#            print('2尝试获取session')
#            ret = requests.get(url,cookies=cookies,headers=headers,proxies=proxies)
#            cookies['PHPSESSID'] = requests.utils.dict_from_cookiejar(ret.cookies)['PHPSESSID']
#        except Exception as e:
#            print('尝试获取session失败')
#            return 1
#    #print( requests.utils.dict_from_cookiejar(ret.cookies)['PHPSESSID'])
#    cookies['PHPSESSID']='ks40oc1qlrsnvi0ing7k1pk7n4'
#    #time.sleep(6)

    soup = BeautifulSoup(ret.content,"html.parser")
    alltag = soup.find(class_='tags').find_all('a')
    tags = []
    for item in alltag:
        tags.append(item.text)
    tag = ",".join(tags)
    desc = soup.find(class_='zljs_infor').find('p').text
    #print(desc)
    #print(requests.utils.dict_from_cookiejar(ret.cookies))
    
    # sys.exit()

    durl = soup.find(class_='link1').find('a').get('href')
    durl = 'https://dl.21ic.com/download/index/%s?isvip=' % durl.split('/')[-1]
    print(durl)

    tftype = soup.find(class_='files_cont')
    if not tftype:
        print('资料为空')
        return 0
    ftype = tftype.find_all('td')[2].text
    nftype = ftype.split('.')
    ftype = nftype[-1]
    if len(nftype) < 2:
        ftype = soup.find('h1').find('span').get('class')[-1].replace('2','')
    if len(ftype) > 10:
        print('文件格式存在错误')
        return 0
    headers['Referer'] = url
    # print(headers)
    try:
        ret = requests.get(durl,cookies=cookies,headers=headers,proxies=proxies)
    except Exception as e:
        return 1

    filename = str(hash(name)).replace("-","m") + "." + ftype
    if not os.path.exists(downloaddir):
       print("创建目录 ",downloaddir)
       os.makedirs(downloaddir)
       # os.system("chmod 777 %s" % item)
       os.system("chown -R www: %s" % download_dir)

    filepath = os.path.join(downloaddir,filename)
    wdata = ret.content
    if '</html>' in str(wdata):
        print('error')
        return 1
    #sys.exit()
    print(filepath)
    #print(wdata)
    with open(filepath,'wb') as f:
      f.write(wdata)
    filesize = os.path.getsize(filepath)
    os.system("chown www: %s" % filepath)
    if filesize < 3000:
        print('文件过小,可能存在异常，重试')
        return 1
    print(desc, tag, filepath, filename, ftype, filesize)
    # print(filepath)
    # print(filename)
    imysql(name,desc,tag,filepath.replace(replace_dir,""),filename,ftype,filesize)
    return 0


for item in range(7,120):
    print("请求页数： ",item)
    n = 0
    while True:
        sys.stdout.flush()
        ret = getpages(item)
        n += 1
        print("起始页第 %s 次下载" % n)
        if n > 2:
            print("尝试次数过多，放弃下载")
            #sys.exit()
            break

        if not ret:
            print("第 %s 页请求为空，再次请求" % item)
            # time.sleep(10)
            continue
        else:
            break
    for target in ret:
        n = 0
        while True:
            time.sleep(random.randint(10,30))
            sys.stdout.flush()
            print()
            print()
            n += 1
            print("第 %s 次下载" % n)
            if n > 3:
                print("尝试次数过多，放弃下载")
                break
            ret = getpage(target[0],target[1])
            if ret == 2:
                sys.exit()
            elif ret == 1:
                continue
            else:
                break


sys.exit()
getpage('通信原理知识点的归纳', 'https://dl.21ic.com/download/pptx-470641.html')


