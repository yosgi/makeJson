用户标签分析
=====

## 说明
 - 老主站的邮件发送数据导入 (加入eef_platform_auto_business_edm_log)
 - Sendy邮件发送数据导入 (加入eef_platform_auto_business_edm_log)
 - 用户退订信息更新 (更新eef_platform_auto_business_edm)
 - 用户邮件打开和点击总数累加 (更新eef_platform_auto_business)


## PHP扩展依赖
 - MySQLi

## 使用说明

 - 配置文件
   
   config/mysqli_config.product.php 配置3个数据库信息

   1. center_eefocus 对应数据平台数据库 （RW)
   2. newsletter  老主站邮件发送数据库 (R)
   3. sendy sendy发送平台数据库 (R)

 - 导入邮件数据
 
    php import.php {DATE} {EXPORT} 

   {DATE}: 2016-02-01 处理某天的edm数据
   {EXPORT}: 0 : 全部直接执行SQL  1: 导入执行SQL,累加open,click导出SQL 2：全部导出处理

   可以并行处理多天 ，定时脚本每天一次就可以
   例如：
       !/bin/bash
       php import.php.php 2016-02-01 0 &

    php batch_import.php {DATE} {DATE2} {EXPORT} 

   {DATE}: 2016-02-01  开始处理某天的edm数据
   {DATE2}: 2016-02-20 结束处理某天的edm数据
   {EXPORT}: 0 : 全部直接执行SQL  1: 导入执行SQL,累加open,click导出SQL 2：全部导出处理

   日志在{ROOT}/output/下

 
 -  清理数据（一般不会用到，import时候，默认会先清理后插入，注意import中更新的open,click总数无法回滚,此方法只清理edm_log表）
 
    php clear.php {DATE}
	{DATE}: 2016-02-01 清理某天的edm数据
   
