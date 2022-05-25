# -*- coding=utf8 -*-

# 动态验证码无法绕过，使用登录后的cookie进行下载

import re
import os
import sys
import time
import MySQLdb
import datetime
import requests
from bs4 import BeautifulSoup



dbhost = "rm-uf603bo2vwhndskwc.mysql.rds.aliyuncs.com"
dbname = "pi_main_eefocus"
dbuser = "pi_eefocus"
dbpswd = "ES#)8#3jN_DM+"
dbport = 3306
# 
# select * from eef_document_cluster_article where article=4503\G;
# SELECT * FROM `eef_document_article` WHERE `id` = '4503'\G;
# select * from eef_document_compiled where article=4503\G;

#SELECT max(`order`) FROM `eef_document_article`;
#insert into eef_document_article (subject,content,markup,uid,category,cluster,status,active,time_submit,time_publish,time_update,user_update,path,file_name,`type`,size,is_hot,recommended,download_count,`order`) values ('5555','<p>jjjj</p>','html',3470578,0,2,11,0,1622182200,1622182200,1622182200,0,'upload/document/document/2021/05/28/93b1fed31d292d8a4bb1127ad55ce1f4.pdf','21ic下载_机器视觉系统概述模板.pdf','pdf',4570870,0,0,0,4502)
#insert into eef_document_cluster_article (article,cluster) values (4506,2);



start_page = "http://download.eeworld.com.cn/eeplp--00--00--.html"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

proxy_host = 'tps187.kdlapi.com'
proxy_port = 15818

proxyMeta = "http://%s:%s" % (proxy_host,proxy_port)

proxies = {
    'http': proxyMeta,
    'https': proxyMeta,
}

replace_dir = "/data/vhosts/main.eefocus.com/"
download_dir = os.path.join(replace_dir,"upload/document/document/")

year = datetime.datetime.now().strftime("%Y")
mon = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
downloaddir = os.path.join(download_dir,year,mon,day)

#‘20210527 15：30’ 公司 cookie
cookies = {'cookie':'[_ga=GA1.3.1888341863.1622769389; advx=z; eew_uid=1234879; eew_username=%B5%E7%D7%D3%D0%D0%D2%B5%B0%AE%BA%C3%D5%DF; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221234879%22%2C%22first_id%22%3A%22179d497c7921bc-029a8e27261288-2363163-2359296-179d497c79347c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22179d497c7921bc-029a8e27261288-2363163-2359296-179d497c79347c%22%7D; a_r=yes; __utmz=87464263.1623286998.1.1.utmcsr=download.eeworld.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/eeplp3.html; __utma=87464263.1888341863.1622769389.1623286998.1623286998.1; acw_tc=2760824316242444222696472edd493e21b205387426f6dcbf2493b8d5ecfa; Hm_lvt_5dda3e9bf25d76518183b98aa932e329=1623285150,1623287024,1623402066,1624244424; _gid=GA1.3.1079130750.1624244425; ABGP_7fe6_pc_size_c=0; ABGP_7fe6_saltkey=xt3p3D55; ABGP_7fe6_lastvisit=1624240830; ABGP_7fe6_sendmail=1; ABGP_7fe6_referer=http%253A%252F%252Fbbs.eeworld.com.cn; ABGP_7fe6_ulastactivity=5577LwRrP7jsIgigVfdwUIwm5BuiIQT90FD87L%2FQLL8%2BTWbXPDRn; ABGP_7fe6_auth=36b7SFWvw%2FTW6mQh5he2Prw%2FQF9OkTSdgSzqeEH%2BJNa4sxZD9%2FlDK1VmEHElKOKNTd5Mxpe%2FQteWa3S0881vpiLcTrAD; ABGP_7fe6_lastcheckfeed=1234879%7C1624244439; ABGP_7fe6_eew_news=5490zVdZiKDfHZkAVS2KvUbe4DeHyWpPdoh%2Bu8kaBnMiziexCn%2BWBk56W4FrRR2mWB6DKWR%2FKzE%2Fsg; csdn_auth=59923eMvYw0uEct4oXx%2Fppb4vCdFHZ2o1mF5FLc1oh26ozL7azHX6rrXj%2FgKKNeE1mNh48KKa2l1ZJlsr2jb10CZ5Srs; csdn_user=%E7%94%B5%E5%AD%90%E8%A1%8C%E4%B8%9A%E7%88%B1%E5%A5%BD%E8%80%85; REMEMBERME=VG9weGlhXFNlcnZpY2VcVXNlclxDdXJyZW50VXNlcjpZMmhsYm1jdWVXRnVaMEJqYmk1emRYQndiSGxtY21GdFpTNWpiMjA9OjE2NTU3ODA0Mzk6YjZlNGFlMmY0NWM2OTMwNmI2N2NmYjA0ZWI3MGRhZTIyNzFkYTA0NTU3MTljODdlYWViOTI5MTM4MThmM2Y3ZQ%3D%3D; ABGP_7fe6_sid=nJHyl8; ABGP_7fe6_lip=218.4.226.238%2C1624244441; ABGP_7fe6_lastact=1624244441%09ck.php%09; _gat=1; __fanvt=1624244679868; Hm_lpvt_5dda3e9bf25d76518183b98aa932e329=1624244680]'}

sdays = 160
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
        db.close()
        return True
    except Exception as e:
        print( "db select wrong")
        return True

def getpages(page):
# getall 为 True 不按时间限制，全部下载	False 按时间限制下载
    sys.stdout.flush()
    try:
        rdata = []
        #print(page)
        #print(proxies)
        ret = requests.get(start_page.replace('--00--00--',str(page)),headers=headers)
        #ret = requests.get(start_page.replace('--00--00--',str(page)),proxies=proxies,headers=headers)
        #print(ret.content)
        soup = BeautifulSoup(ret.content,"html.parser")
        # 获取首页内容
        text = soup.find(class_="dwc_mlistxtloop")
        # print(text)
        targets = text.find_all(class_="dwc_sorde")
        # print(page)
        return targets
    except Exception as e:
        print(e)
        return

def getpage(item):
    sys.stdout.flush()
    # for item in targets:
    # print(item)
    rdata = []
    ftype = item.find(class_='sorde_ico').text
    # print(ftype)
    tmp = item.find(class_="dsc").find_all('span')
    jf = tmp[0].text.split('：')[-1]
    day = tmp[-1].text.split('：')[-1].strip()
    print(jf,day)
    if int(jf) > 0:
        print("下载需要积分")
        return 0
    #print(jf,day,days)
    if day not in days:
        print('不在抓取时间内')
        return 2
    tmp = item.find(href=re.compile("detail"))
    name = tmp.text
    if smysql(name):
        return 0
    print(tmp.get('href'))
    try:
        tdata = requests.get('http:' + tmp.get('href'),headers=headers)
        #tdata = requests.get('http:' + tmp.get('href'),headers=headers,proxies=proxies)
    except Exception as e:
        return 1
    tsoup = BeautifulSoup(tdata.content,"html.parser")
    ttext = tsoup.find(class_="dwc_maldesc")
    if not ttext:
        return 1
    desc = ttext.find_all('p')[1].text

    purl = tmp.get('href').split('/')
    fid = purl[-1]
    author = purl[-2]
    purl = 'http://download.eeworld.com.cn/index.php/source/do_download/%s/%s/' % (fid,author)
#    purl = "http://download.eeworld.com.cn/index.php/source/do_download/618805/%E5%A4%A9%E5%9C%B0%E8%8B%B1%E9%9B%84/"
    ttags = item.find(class_="tag").find_all('a')
    tags = []
    for item in ttags:
        tags.append(item.text.split('：')[-1])
    tag = ",".join(tags)
    print(tag)
    #if int(jf) > 0:
    #    print('下载需要积分，pass')
    #    return 0
    #imysql(name)
    #return
    data = {'ds':'dx'}
    print('start download')
    try:
        ret = requests.post(purl,data,cookies=cookies,headers=headers)
        #ret = requests.post(purl,data,cookies=cookies,headers=headers,proxies=proxies)
    except Exception as e:
        return 1
    filename = str(hash(name)).replace("-","m") + "." + ftype
    if not os.path.exists(downloaddir):
       print("创建目录 ",downloaddir)
       os.makedirs(downloaddir)
       # os.system("chmod 777 %s" % item)
       os.system("chown -R www: %s" % download_dir)

    filepath = os.path.join(downloaddir,filename)
    print(ftype)
    with open(filepath,'wb') as f:
        f.write(ret.content)
    filesize = os.path.getsize(filepath)
    os.system("chown www: %s" % filepath)
    if filesize < 3000:
        print('文件过小,可能存在异常，重试',filename)
        return 1
    print(desc, tag, filepath, filename, ftype, filesize)
    # time.sleep(10)
    imysql(name,desc,tag,filepath.replace(replace_dir,""),filename,ftype,filesize)
    return 0


#print(getpage(getpages(1)[3]))
#sys.exit()        
for item in range(1,100):
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
            print("第 %s 次下载" % n)
            if n > 2:
                print("尝试次数过多，放弃下载")
                break
            ret = getpage(target)
            if ret == 2:
                sys.exit()
            elif ret == 1:
                continue
            else:
                break

        
