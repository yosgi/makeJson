用户标签分析
=====

## 说明
 - 基于现有库中数据，把用户按照访问行为进行行业技术标签分类
     处理表 eef_platform_auto_business_access_log


## PHP扩展依赖
 - MySQL

## 使用说明

 * 配置文件中
 
  G_TIME_LIMIT 定义要处理多少天前到执行时候的数据

  默认写了90天，现在线上已经改为每天跑一次，所以我相应的已经改为8天。(为了避免某天出错以后，第二天能自动补救)

 - php exec_parse.php {OFFSET} {LIMIT} 

   默认G_TIME_LIMIT到现在的数据总数可能很大，为了能让脚本并行处理，所以设置参数
   例如：
       !/bin/bash
       php exec_parse.php 0 10000 &
       php exec_parse.php 10000 10000 &

   在脚本中就可以代表可以同时处理 20000条数据
