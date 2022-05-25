#!/usr/bin/env python
# -*- coding=utf8 -*-

import re
import sys
import time
import json
import random
import requests
from functools import reduce
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import date,timedelta

#上海证券交易所
"""
http://www.sse.com.cn/disclosure/listedinfo/regular/
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36','Referer': 'http://www.sse.com.cn/'}

url = "http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?jsonCallBack=jsonpCallback46857&isPagination=true&productId=code&securityType=0101%2C120100%2C020100%2C020200%2C120200&reportType2=DQBG&reportType=ALL&beginDate=startday&endDate=endday&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=" + "{:.0f}".format(time.time()*1000)

baseurl = "http://www.sse.com.cn/"

bdays = 182
#startday = (date.today()+timedelta(days=bdays)).strftime("%F")

def opdata(url,code,startday,endday):
    url = url.replace("code",code).replace("startday",startday).replace("endday",endday)
    #print(url)
    ret = requests.get(url,headers=headers)
    tmp = ret.content.decode('utf8')
    gdata = eval(re.findall("{.*}",tmp)[0].replace('null','"nothing"'))
    mdata = gdata['pageHelp']['data']
    count = len(mdata)
    print("查询到报告数量",count)
    if not count:
        return
    rdata = []
    for item in mdata:
        title = item['TITLE']
        ptime = item['SSEDATE']
        durl = urljoin(baseurl,item['URL'].replace("\\",''))
        rdata.append((title,ptime,durl))
    return rdata


# 查询日期需要指定，最长时间为3年
# 即第一季报在四月份，第三季报在十月份
def getpdf(code,dall=None):
    if dall:
        print('获取所有报告')
        n = 1
        data = []
        while True:
            startday,endday = (date.today()+timedelta(days=-bdays*n)).strftime("%F"),(date.today()+timedelta(days=-bdays*(n-1))).strftime("%F")
            n += 1
            print("\n查询起始时间",startday,endday)
            if "1989" in startday:
                break
            tmp = opdata(url,code,startday,endday)
            if not tmp:
                break
            print(tmp)
            data += tmp
        print(data)
    else:
        startday = (date.today()+timedelta(days=-bdays)).strftime("%F")
        endday = time.strftime("%F")
        print("\n查询起始时间",startday,endday)
        data = opdata(url,code,startday,endday)
        print(data)

if __name__ == "__main__":
    getpdf("600000")
    #getpdf("600000",True)
    #getpdf("600519",True)
