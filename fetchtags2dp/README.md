用户标签分析
=====

## 说明
 - 基于与非edm统计数据，收集用户行业与技术标签

## PHP扩展依赖
 - pdo
 - mongo

## 操作步骤
### 一、线下数据收集
1. 从线上导入newsletter数据库倒出 newsletter_task, newsletter_user 表到开发环境 2.82（可增量导入）
2. 导入目录下db.sql 至 newsletter （tmp_link_tags,tmp_user_tags）
3. 修改config.php中db与mongo部分
   - mongo为与非网日志统计系统（http://stat.local.eefocus.com/）对应库
   - 因此mongodb数据较大，且只存在线上，前面步骤只可在公司环境执行
4. 执行1fetchtags.php
```
# 末尾两位参数为日志分析起至日期
php5 1fetchtags.php 2014-10-01 2014-01-01
```

### 二、线上数据回灌
1. 从线下（2.82）dump出 newsletter 的 tmp_user_tags 表
2. 导入到线上（0.81）的 center_eefocus.center_eefocus 库中
3. 将 2insertdp.php 拷贝到线上服务器，并修改头部db的配置部分
4. 执行2insertdp.php
```
php 2insertdp.php
```

