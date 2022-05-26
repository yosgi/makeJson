#!/usr/bin/env python
# -*- coding=utf8 -*-

import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import time
import pymongo
import random
import requests
import urlparse
from multiprocessing import Pool
from bs4 import BeautifulSoup
from proxy import getip

url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=0++0&ie=utf8"
headers = [{"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36"},{"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"},{"user-agent":"Mozilla/5.0 (Linux; Android 9; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.26 SP-engine/2.22.0 baiduboxapp/11.26.5.10 (Baidu; P1 9) NABar/1.0"},{"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"},{"user-agent":"Mozilla/5.0(Linux;Android 5.1.1;OPPO A33 Build/LMY47V;wv) AppleWebKit/537.36(KHTML,link Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 LieBaoFast/4.51.3"}]
logdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"logs")
wfile = os.path.join(logdir,"log.txt")
wdata = os.path.join(logdir,"data.txt")
targetfile = os.path.join(logdir,"xx.txt")



def writefile(words):
    with open(wfile,'a') as f:
        f.write(words)

def writedata(words):
    with open(wdata,'a') as f:
        f.write(words)

def getheader():
    num = len(headers)
    return random.choice(headers)


def getwx(data):
    #data = data.replace("\n","").split("\t")
    #time.sleep(random.randint(1,5))
    sys.stdout.flush()
    mongoid, wx, name = data
    proxy = getip()
    proxies = {'https':'%s:%s' % (proxy['host'],proxy['port'])}
    headers = getheader()
    print
    print
    print proxies
    print "获取公众号名称",name
    print "请求url: ", url.replace("0++0",name)
    try:
        ret = requests.get(url.replace("0++0",name),headers=headers,timeout=7,proxies=proxies)
    except Exception as e:
        return getwx(data)
    rdata = ret.content
    if not rdata:
        print "获取内容为空"
        return getwx(data)
    cookies = ret.cookies
    soup = BeautifulSoup(rdata,"html.parser")
    print "获取sogou内容"
    text = soup.find_all(name='ul', attrs={"class":"news-list2"})
    #print soup
    print len(text)
    if text:
        print "抓取到内容"
        textlist = text[0].find_all(name='li')
        print "抓取条数",len(textlist)
        for item in textlist:
            # 获取到公众号名称
            gname = item.find(name='p',attrs={"class":"tit"}).text.strip('\n')
            #codeurl = item.find(name='a').get('href')
            #print codeurl
            gettime = item.find_all(name="script")
            if gname != name:
                print "公众号名称不一致0++0",name,gname
                continue
            print "获取更新时间"
            print gettime
            gettime = re.findall("\d+",gettime[-1].string)
            if gettime:
                codetime = int(gettime[0])
                print "时间为", codetime
            else:
                print "时间获取失败0++0"
                return getwx(data)
            # 获取到公众号
            gwx = item.find(name='label',attrs={"name":"em_weixinhao"}).text.strip('\n')
            if gwx != wx:
                print "微信号不一致0++0",wx,gwx
                #continue
            tmpcom = item.find_all(name='dd')
            try:
                codeurl = tmpcom[-1].find(name="a").get('href')
            except Exception as e:
                print "未获取到微信 url 0++0", name
                continue
            if codeurl:
                try:
                    retcode = requests.get('https://weixin.sogou.com'+codeurl,headers=headers,timeout=7,cookies=cookies, proxies=proxies)
                except Exception as e:
                    return getwx(data)
                codedata = retcode.content
                if codedata:
                    print "获取到微信url"
                    baseurl = re.findall("var\s*url\s*=\s*'(.*)'\s*;",codedata)[0]
                    allurl = re.findall("url\s*\+=\s*'(.*)'\s*;",codedata)
                    keyword = re.findall('url.replace\("(.*)",\s*"(.*)"\);',codedata)[0]
                    targeturl = (baseurl + "".join(allurl)).replace(keyword[0],keyword[1])
                    print "-"*10
                    print "写入数据"
                    print "-"*10
                    writedata("原始数据1:%s\t原始数据2:%s\t微信url:%s\t获取名称:%s\n" % (name, wx,targeturl,gname))
                    wrmongo({"account_id":mongoid, "userName": wx, "name": name,"timestamp":codetime,"wxurl":targeturl})
                else:
                    print "获取sogou内容失败"
                    writedata("原始数据1:%s\t原始数据2:%s\t微信url:%s\t获取名称:%s\n" % (name, wx,"weixinurl0++0", gname))
            else:
                print "获取sogou url 失败"
    else:
        print "获取title"
        title = soup.find_all(name='title')
        #print dir(title)
        #print title[0].text
        try: 
            if "微信公众号" in title[0].text:
                print "页面抓取为空,请检查微信号是否存在"
                writedata("原始数据1:%s\t原始数据2:%s\t微信url:\t新名称:\n 页面抓取为空,请检查微信号是否存在0++0" % (name, wx))
            else:
                print "没有title存在,重试"
                return getwx(data)
        except Exception as e:
            print "获取title出错,重试"
            return getwx(data)

def getmongo():
    print
    print
    print "---  start  ---"
    myclient = pymongo.MongoClient('mongodb://172.16.88.64')
    db = myclient.wxspider
    my_set = db.account
    totalnum = my_set.count()
    data = my_set.find()
    #data = my_set.find().batch_size(20)
    p = Pool(5)
    for item in data:
        print item["_id"]
        print item['userName']
        print item['name']
        newdata = [item["_id"],item['userName'],item['name']]
        p.apply_async(getwx,args=(newdata,))
        #getwx(newdata)
        #sys.exit()
    p.close()
    p.join()
    print "---   end   ---"

def wrmongo(data):
    myclient = pymongo.MongoClient('mongodb://172.16.88.64')
    db = myclient.wxspider
    my_set = db.newlist
    print 
    gdata = my_set.find({"account_id":data['account_id']})
    print type(gdata)
    print gdata
    #print gdata
    if not gdata:
        print "原始数据不存在,插入数据"
        my_set.insert(data)
    else:
        pd = False
        for item in gdata:
            print "xxxx"
            print item['timestamp'],data['timestamp']
            if item['timestamp'] == data['timestamp']:
                pd = True
                print "timestamp已有，不进行存储"
                break
        if not pd:
            print "111-----"
            print "插入数据"
            my_set.insert(data)
            #print my_set.modified_count


if __name__ == "__main__":
    #fobj = open(targetfile)
    #data = fobj.readlines()
    #for item in data:
    #    time.sleep(random.randint(3,7))
    #    getwx(item)
    #getwx(["芯华社","ChipNews","111"])
    #getwx(["123","汽车电子设计","汽车电子设计"])
    getmongo()
