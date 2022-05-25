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

#
"""
https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh
标题类别及文件类别
标题类别
财务报表/环境社会及管治资料
所有
    data = {'lang':'ZH', 'category':'0', 'market':'SEHK', 'searchType':'1', 'documentType':'-1', 't1code':'40000', 't2Gcode':'-2', 't2code':'-2', 'from':'20070625', 'to':'20220328', 'MB-Daterange':'0', 'title':''}
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36','Referer': 'http://www.sse.com.cn/'}

bdays = 365

def getid(code):
    code = str(code)
    url = "https://www1.hkexnews.hk/search/partial.do?&callback=callback&lang=ZH&type=A&name=%s&market=SEHK&_=" % code + "{:.0f}".format(time.time()*1000)
    ret = requests.get(url,headers=headers)
    tmp = ret.content.decode('utf8')
    gdata = eval(re.findall("{.*}",tmp)[0].replace('null','"nothing"'))
    mdata = gdata['stockInfo']
    for item in mdata:
        if item['code'] == code:
             return item['stockId']
    return

def opdata(url,data):
    baseurl = "https://www1.hkexnews.hk/"
    startday = (date.today()+timedelta(days=-bdays)).strftime("%Y%m%d")
    #print(data)
    ret = requests.post(url,data=data,headers=headers)
    soup = BeautifulSoup(ret.content,"html.parser")
    text = soup.find(class_="table sticky-header-table table-scroll table-mobile-list")
    rdata = text.find('tbody').find_all('tr')
    stopwords1 = ['作廢','作废']
    stopwords2 = ['社會','環境','治理','社会','环境']
    sdata = []
    for item in rdata:
        mes = item.find(class_="headline").text
        name = item.find(class_='doc-link').find('a').text.strip()
        #print(mes)
        mes1, mes2 = mes.split('[')
        pd1 = list(filter(lambda x: 1 if x in mes1 else 0,stopwords1))
        pd2 = list(filter(lambda x: 1 if x in name else 0,stopwords2))
        if pd1 or pd2:
            continue
        ptime = item.find(class_='text-right release-time').text.strip()
        ptime = ptime.split()[1]
        timeArray = time.strptime(ptime, "%d/%m/%Y")
        ptime = time.strftime("%Y-%m-%d", timeArray)
        #print(ptime)
        link = item.find(class_='doc-link').find('a').get('href')
        sdata.append((name,ptime,urljoin(baseurl,link)))
    return sdata
    

def getpdf(code,dall=None):
    codeid = getid(code)
    if not codeid:
        print('未查询到股票代码')
        return
    print(codeid)
    url = "https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh"
    data = {'lang':'ZH', 'category':'0', 'market':'SEHK', 'searchType':'1', 'documentType':'-1', 't1code':'40000', 't2Gcode':'-2', 't2code':'-2', 'MB-Daterange':'0', 'title':''}
    data['stockId'] = str(codeid)
    if dall:
        print('获取所有报告')
        n = 1
        rdata = []
        while True:
            startday,endday = (date.today()+timedelta(days=-bdays*n)).strftime("%Y%m%d"),(date.today()+timedelta(days=-bdays*(n-1))).strftime("%Y%m%d")
            n += 1
            data['from'] = startday
            data['to'] = endday
            print("\n查询起始时间",startday,endday)
            if "1986" in startday:
                break
            tmp = opdata(url,data)
            if not tmp:
                break
            print(tmp)
            rdata += tmp
        print('1111',rdata)
    else:
        print('获取 %s 天内报告' % bdays)
        startday = (date.today()+timedelta(days=-bdays)).strftime("%Y%m%d")
        endday = time.strftime("%Y%m%d")
        print("\n查询起始时间",startday,endday)
        data['from'] = startday
        data['to'] = endday
        rdata = opdata(url,data)
        print(rdata)

if __name__ == "__main__":
    #print(getpdf('00004',dall=True))
    #print(getpdf('01088'))
    print(getpdf('00700'))
    #print(getpdf('00700',dall=True))
    
