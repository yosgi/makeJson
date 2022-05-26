#!/usr/bin/env python
# -*- coding=utf8 -*-

import time
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'172.16.88.42','port':9200}], timeout=3600)

day = time.strftime("%FT%T+08:00")
print(day)

dsl = {
             "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "createTime": '2022-04-24T15:27:02+08:00'
                                }
                            },

                        ]
                    }
                },
                "from":0,
                "size":500
        }

index_name = 'wechat_hot_articles_1'
#index_name = 'wechat_official_account_1'
res = es.search(index = index_name,body=dsl)
#res = es.search(index = 'wechat_official_account_1',body=dsl)


data = res['hits']['hits']
print(len(res['hits']['hits']))

for item in data:
    print(item)
    #print(item['_id'])
    #es.delete(index = 'wechat_official_account_1',id=item['_id'])
    es.delete(index = index_name,id=item['_id'])
