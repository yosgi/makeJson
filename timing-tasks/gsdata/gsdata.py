#!/usr/bin/env python
# -*- coding=utf8 -*-

import re
import sys
import time
import json
import jinja2
import random
import datetime
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import date,timedelta

# day = time.strftime("%FT%T")
day = time.strftime("%FT%T+08:00")
syesterday = (date.today() + timedelta(days=-1)).strftime("%FT%T+08:00")
es = Elasticsearch([{'host':'172.16.88.42','port':9200}], timeout=3600)
#es = Elasticsearch([{'host':'10.101.12.19','port':9200}],http_auth=('xiao', '123456'), timeout=3600)

data = {"username":"18051092123","password" : "EEFocus=2020"}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

url = "https://u2.gsdata.cn/member/login?url=https%3A%2F%2Fu2.gsdata.cn%2Ftask%2Ftime-limit"

yes = (date.today()+timedelta(days=-1)).strftime("%d")

#ret = requests.post(url,data=data,headers=headers)
#soup = BeautifulSoup(ret.content,"html.parser")
#text = soup.find(id="user-avatar")
#if text:
#    print("登录成功")
#    print(requests.utils.dict_from_cookiejar(ret.cookies))

#cookies = ret.cookies

cookies = {'cookie':'[sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217da34217a329-083f35ba7819488-978153c-2359296-17da34217a4b99%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217da34217a329-083f35ba7819488-978153c-2359296-17da34217a4b99%22%7D; _gsdataCL=WzAsIjE4MDUxMDkyMTIzIiwiMjAyMTEyMTAxNTMzMDYiLCI1ZDA1MzE1ZTk0MzMyYzliYjM0YjlkNWEwN2JhYzViYSIsNDI4MDgzXQ%3D%3D;]'}

urls = {
    "半导体行业观察":
    {
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=aQWBNDiSYJWq5irn",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=aQWBNDiSYJWq5irn&wx=icbank&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=%E5%8D%8A%E5%AF%BC%E4%BD%93%E8%A1%8C%E4%B8%9A%E8%A7%82%E5%AF%9F",
        "need_report":1
    },
    "EETOP":
    {
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=ZQWBVD0SbJ3qAitnMgQ5O0O0O2O0O0O1",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=ZQWBVD0SbJ3qAitnMgQ5O0O0O2O0O0O1&wx=eetop-1&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=EETOP",
        "need_report":1
    },
    "电子发烧友":
    {
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=ZQWBxDlSYJ2qZihnbgn5M2O0O0O1",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=ZQWBxDlSYJ2qZihnbgn5M2O0O0O1&wx=elecfans&sort=",
        "fans":"	https://www.gsdata.cn/tool/ygfsaction?wx_name=%E7%94%B5%E5%AD%90%E5%8F%91%E7%83%A7%E5%8F%8B",
        "need_report":1
    },
    "21ic电子网":{
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=dQ2BVDpSeJGqliunMgj5F2p1YwO0O0OO0O0O",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=dQ2BVDpSeJGqliunMgj5F2p1YwO0O0OO0O0O&wx=weixin21ic&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=21ic%E7%94%B5%E5%AD%90%E7%BD%91",
        "need_report":1
    },
    "电子工程世界":
    {
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=RQUBVD3SbJ3qJisnZgG5J2i1cwO0O0OO0O0O",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=RQUBVD3SbJ3qJisnZgG5J2i1cwO0O0OO0O0O&wx=EEworldbbs&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=%E7%94%B5%E5%AD%90%E5%B7%A5%E7%A8%8B%E4%B8%96%E7%95%8C",
        "need_report":1
    },
    "eefocus":
    {
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=ZQWBUDtSZJmq9ijndgX5M2O0O0O1",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=ZQWBUDtSZJmq9ijndgX5M2O0O0O1&wx=ee-focus&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=%E4%B8%8E%E9%9D%9E%E7%BD%91eefocus",
        "need_report":1
    },
    "AI财经社":{
        "article_data":"https://www.gsdata.cn/rank/wxdetail?wxname=YQWBlDjSaJmq5ilndg35M2O0O0O1",
        "article_top_10":"https://www.gsdata.cn/rank/toparc?wxname=YQWBlDjSaJmq5ilndg35M2O0O0O1&wx=aicjnews&sort=",
        "fans":"https://www.gsdata.cn/tool/ygfsaction?wx_name=AI%E8%B4%A2%E7%BB%8F%E7%A4%BE",
        "need_report":0
    },

}

def qbzs(url,retry=1):
    sys.stdout.flush()
    print(sys._getframe().f_code.co_name,retry)
    if retry >5:
        sys.exit()
    nret = requests.get(url,cookies=cookies,headers=headers)
    soup = BeautifulSoup(nret.content,"html.parser")
    text = soup.find_all(class_="wxData-cont")
    keyword = {'总阅读量':'total_read','头条阅读量':'toutiao_read','排名':'rank','在看数':'reading','点赞数':'praise','平均阅读量':'reading_average'}
    try:
        #print(len(text))
        print("数据获取成功")
        day = text[0].parent.parent.parent.find(class_="wxDetail-tit").text.strip()
        getday = re.findall("\d{2}",day)
        if getday[1] == yes:
            print("获取到昨天日期",yes)
        else:
            print("获取到错误日期",getday[1])
            print("数据不进行插入")
            return
        #print(day)
        data = {}
        data['dataTime'] = day
        for item in text:
            title = item.find_previous_sibling(class_="wxData-txt fl fs16").text
            for key,value in keyword.items():
                if title == key:
                    title = value
            num = item.find(class_="fs28").text
            num = num.lower()
            if "w" in num:
                num = num.split("w")[0]+"0000"
            #print(num)
            data[title]=float(num)
        return data
    except Exception as e:
        time.sleep(50)
        retry += 1
        return qbzs(url,retry)
#print(qbzs(urls["AI财经社"]["article_data"]))
#sys.exit()

def top10(name,url,num,retry=1):
    sys.stdout.flush()
    print(sys._getframe().f_code.co_name,retry)
    if retry >5:
        sys.exit()
    headers["X-Requested-With"] = "XMLHttpRequest"
    ret = []
    print(num[1])
    top10url = url + str(num[0])
    tret = requests.post(top10url,cookies=cookies,headers=headers)
    tdata = tret.content
    #print(tdata)
    try:
        tdata = tdata.decode(encoding="utf8")
        tdata = json.loads(tdata)
        if tdata['error'] and tdata['error_msg']:
            print(tdata['error_msg'])
            return ret
        print('获取数据条数',len(tdata['data']))
        for item in tdata['data']:
            title = item["title"]
            posttime = item["posttime"]
            views = str(item["readnum_newest"]).lower().split('w')[0] + '0000' if 'w' in str(item["readnum_newest"]).lower() else item["readnum_newest"]
            likenum = str(item["likenum_newest"]).lower().split('w')[0] + '0000' if 'w' in str(item["likenum_newest"]).lower() else item["likenum_newest"]
            dz = str(item["old_like_num_newest"]).lower().split('w')[0] + '0000' if 'w' in str(item["old_like_num_newest"]).lower() else item["old_like_num_newest"]
            url = item["url"]
            picurl = item["picurl"]
            original = 1 if item["copyright"] == "有" else 0
#            print(type(views))
            try:
                views = int(views)
            except Exception as e:
                views = 0
            try:
                likenum = int(likenum)
            except Exception as e:
                likenum = 0
            try:
                dz = int(dz)
            except Exception as e:
                dz = 0
            ret.append({"account_name":name,"article_type":num[0],"createTime":day,"displayTime":syesterday,"title":title,"pubTime":posttime,"views":views,"like":likenum,"praise":dz,"url":url,"picurl":picurl,"original":original})
        print(len(ret))
        return ret
    except Exception as e:
        time.sleep(100)
        retry += 1
        return top10(name,url,num,retry)

#print(top10("eefocus",'https://www.gsdata.cn/rank/toparc?wxname=YQ2BND0SdJnqliznYg25o2O0O0O1&wx=cctvyscj&sort=',(-1,"最新")))
#sys.exit()

def fans(url,retry=1):
    print(sys._getframe().f_code.co_name,retry)
    if retry >5:
        sys.exit()
    pret = requests.get(url,cookies=cookies,headers=headers)
    soup = BeautifulSoup(pret.content,"html.parser")
    text = soup.find(class_="num")
    sys.stdout.flush()
    try:
       print("评估数获取成功")
       num = text.text
       num = re.findall("\d+",num)[0]
       print(num)
       if int(num) > 0:
           return int(num)
       else:
           time.sleep(100)
           retry+=1
           return fans(url,retry)
    except Exception as e:
       time.sleep(100)
       retry+=1
       return fans(url,retry)

#print(qbzs(urls["eefocus"]["article_data"]))

#nums = [(-1,"最新"),(-2,"阅读数"),(-3,"在看数"),(-4,"点赞数")]
#ret = []
#for item in nums:
#    ret = top10("eefocus",urls["eefocus"]["article_top_10"],item)
#    print(ret)

#print(fans(urls["eefocus"]["fans"]))


def gettem(data):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    temp = env.get_template('./gstemplate.html')

    render_dict = {}
    dict_table_data = data
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today
    #yesterday=today-oneday 
    render_dict.update({'day': '%s' % yesterday,'dict_table_data': dict_table_data})
    temp_out = temp.render(day=render_dict['day'],dict_table_data=render_dict['dict_table_data'])
    return temp_out

if __name__ =="__main__":
    newdata = []
    for key,value in urls.items():
        sys.stdout.flush()
        print()
        print("-"*10)
        print()
        print(key)
        tmp = {}
        tmp['Name'] = key
        tmp['data'] = []
        article_data = qbzs(urls[key]["article_data"])
        if article_data: 
            time.sleep(random.randint(6,30))
            article_data['Fans'] = fans(urls[key]["fans"])
            article_data['createTime'] = day
            article_data['displayTime'] = syesterday
            article_data['account_name'] = key
            article_data['need_report'] = urls[key]['need_report']
            #print(article_data)
            es.index(index='wechat_official_account_1',document=article_data)
        print()
        time.sleep(random.randint(6,30))
        #nums = [(-1,"最新")]
        nums = [(-1,"最新"),(-2,"阅读数"),(-3,"在看数"),(-4,"点赞数")]
        ret = []
        for item in nums:
            sys.stdout.flush()
            time.sleep(random.randint(6,30))
            ret = top10(key,urls[key]["article_top_10"],item)
            for article in ret:
                es.index(index='wechat_hot_articles_1',document=article)
                if item[0] == -1:
                   tmp['data'].append({'name':article['title'],"url":article['url'],"pubtime":article['pubTime'],"read": '{:,}'.format(article['views']),"original":article['original']})
        newdata.append(tmp)
        #print(ret)
        print()
        print()
    senddata = gettem(newdata)
    from sendmail import sendmail_nofile
    #sendmail_nofile(['shuai.yuan@cn.supplyframe.com'],"自动发送","编辑","最新热门文章",senddata)
    #sys.exit()
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today
    #yesterday=today-oneday 
    print()
    print("begin",time.strftime("%F %T"))
    sendmail_nofile(['shuai.yuan@cn.supplyframe.com','jun.pei@cn.supplyframe.com','lijun.dong@cn.supplyframe.com','yang.gao@cn.supplyframe.com','xiaoquan.he@cn.supplyframe.com', 'xin.wang@cn.supplyframe.com', 'yue.he@cn.supplyframe.com', 'tracy.yu@cn.supplyframe.com', 'awang@supplyframe.com', 'ahong@supplyframe.com', 'nan.lu@cn.supplyframe.com','qingan.liu@cn.supplyframe.com','zhen.xia@cn.supplyframe.com','huijuan.zhang@cn.supplyframe.com','jian.li@cn.supplyframe.com','ziyang.gu@cn.supplyframe.com','dezhi.shi@cn.supplyframe.com','shuncheng.cao@cn.supplyframe.com','jun.zhu@cn.supplyframe.com'],"自动发送","编辑","公众号最新热门文章(%s)" % yesterday,senddata)
    print('end',time.strftime("%F %T"))
    print()
