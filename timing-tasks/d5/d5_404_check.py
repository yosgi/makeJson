#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys
import time
import random
import pymongo
import datetime
import requests
from sendmail import sendmail_nofile
from multiprocessing import Pool
from multiprocessing import Manager

from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

host = "172.16.88.64"
# host = "192.168.0.196"
port = 27017
db = "d5"

# 并发共用全局变量
error_data = Manager().list()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

params_to_remove = [
    "utm_source",  
    "utm_medium",  
    "utm_campaign",
    "utm_term",
    "utm_content",
    "cid", # nxp tracking param:
    "/?cid" # special case when there's # in url https://www.nxp.com/part/LPC802M001JDH20#/?cid=ad_product l_tac818600_38
]


# 记录已访问的链接, 有些广告链接是重复的
allRet = {}
# http请求函数
def getcode(url,key,name1,name2):

    try:
        ret = {}
        if url in allRet:
            print("Visited Before: ", url)
            ret = allRet[url]
        else:
            time.sleep(random.randint(3,5))
            ret = requests.get(url,headers=headers,timeout=20)
            allRet[url] = ret
        print('\n',url,ret.status_code)
        sys.stdout.flush()
        # http code 返回值，放入列表内将不记录
        if ret.status_code not in [200]:
            print("error",len(error_data))
            sys.stdout.flush()
            error_data.append((str(ret.status_code),name1,name2,key,url))
    except Exception as e:
#        print('\nerror',url)
        sys.stdout.flush()
        # 请求错误设置为 15555
        error_data.append(('15555',name1,name2,key,url))

def remove_tracker_params(query_string):
    """
    Given a query string from a URL, strip out the known trackers
    >>> remove_tracker_params("utm_campaign=2018-05-31&utm_medium=email&utm_source=courtside-20180531")
    ''
    >>> remove_tracker_params("a=b&utm_campaign=2018-05-31&utm_medium=email&utm_source=courtside-20180531")
    'a=b'
    >>> remove_tracker_params("type=test&type=test2")
    'type=test&type=test2'
    """

    params = []
    for param, values in parse_qs(query_string).items():
        if param not in params_to_remove:
            # value will be a list, extract each one out
            for value in values:
                params.append((param, value))
    return urlencode(params)

myclient = pymongo.MongoClient("mongodb://%s:%s/" %(host,port))
mydb = myclient[db]


mycol = mydb['campaigns']

allid = {}
for item in mycol.find({'end' : {'$gt' :datetime.datetime.utcfromtimestamp(time.time())}}):
    allid[item['_id']] = item['title']

# 并发数量
p = Pool(8)

mycol = mydb['banners']

for item in mycol.find({'campaign':{'$in':list(allid.keys())}}, {'_id': -1, 'links':1, 'title':1, 'campaign':1}):
    #print(allid[item['campaign']],item['title'],item['links'])
    
    for key,value in item['links'].items():
        # if 'https://www.nxp.com/part/JN5189HN' in value:
        # print(key,value)
        parsed = urlparse(value)
        parsed = parsed._replace(query=remove_tracker_params(parsed.query))
        parsed = parsed._replace(fragment=remove_tracker_params(parsed.fragment))
        url = parsed.geturl()
        print(url)
        #ret = requests.get(url, prefetch=False)
        #print(ret.status_code)
        p.apply_async(getcode,args=(url,key,allid[item['campaign']],item['title']))

p.close()
p.join()

# 发送邮件内容
senddata = '<html><table border="1"><tr><th>code</th><th>campaign</th><th>banner</th><th>类型</th><th>url</th></tr>'
for err in error_data:
    print(err)
    senddata += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (err[0],err[1],err[2],err[3],err[4])
print(senddata)

senddata += '</table></html>'

# 发送邮件函数
sendmail_nofile(['shuai.yuan@cn.supplyframe.com','xiaoshi.xu@cn.supplyframe.com','fengyu.tian@cn.supplyframe.com'],"自动发送","运维","d5问题链接",senddata)
