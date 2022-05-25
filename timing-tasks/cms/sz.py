#!/usr/bin/env python
# -*- coding=utf8 -*-

import re
import sys
import time
import json
import random
import requests
from functools import reduce
from urllib.parse import urljoin
from datetime import date,timedelta

#深圳证券交易所
# http://www.szse.cn/disclosure/listed/fixed/index.html
#seDate: ["2022-03-01", "2022-03-25"] 时间范围
#stock 股票代码
#data = {"seDate":["2022-03-01","2022-03-25"],"stock":["000001"],"channelCode":["fixed_disc"],"pageSize":"50","pageNum":"1"}
data = {"seDate":["",""],"stock":[],"channelCode":["fixed_disc"]}
pageSize = 50
pageNum = 1

data['pageSize'] = pageSize
data['pageNum'] = pageNum

bdays = 182

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36','Content-Type': 'application/json','Origin': 'http://www.szse.cn','Referer': 'http://www.szse.cn/disclosure/listed/fixed/index.html','Accept-Language': 'zh-CN,zh;q=0.9','Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache','Accept': 'application/json, text/javascript, */*; q=0.01','X-Request-Type': 'ajax','X-Requested-With': 'XMLHttpRequest'}

baseurl = "http://disc.static.szse.cn/download/"

def opdata(url,data):
    ret = requests.post(url,headers=headers,data=json.dumps(data))
    gdata = json.loads(ret.content)
    mdata = gdata['data']
    rdata = []
    for item in mdata:
        title = item['title']
        ptime = item['publishTime'].split()[0]
        durl = urljoin(baseurl,item['attachPath'])
        rdata.append((title,ptime,durl))
    return rdata

def getpdf(code,dall=None):
    url = 'http://www.szse.cn/api/disc/announcement/annList?random=0.%s' % reduce(lambda x,y:x+y,[ str(random.randint(0,9)) for i in range(16) ])
    data['stock'] = [code]
    if dall:
        print('获取所有报告')
        n = 1
        rdata = []
        while True:
            startday,endday = (date.today()+timedelta(days=-bdays*n)).strftime("%F"),(date
.today()+timedelta(days=-bdays*(n-1))).strftime("%F")
            n += 1
            print("\n查询起始时间",startday,endday)
            data['seDate'] = [startday,endday]
            if "1989" in startday:
                break
            tmp = opdata(url,data)
            if not tmp:
                break
            print(tmp)
            rdata += tmp
        print(rdata)
    else:
        startday = (date.today()+timedelta(days=-bdays)).strftime("%F")
        endday = time.strftime("%F")
        print("\n查询起始时间",startday,endday)
        data['seDate'] = [startday,endday]
        rdata = opdata(url,data)
        print(rdata)


if __name__ == "__main__":
    #getpdf("300750")
    getpdf("300750",dall=True)
    #getpdf("000001")
    #getpdf("000001",dall=True)
