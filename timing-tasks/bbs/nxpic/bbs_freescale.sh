#!/bin/bash

export LANG="zh_CN.UTF-8"
export LC_ALL="zh_CN.UTF-8"
MIALTO="hao.zhao@cn.supplyframe.com shuai.yuan@cn.supplyframe.com"
#MIALTO="shuai.yuan@supplyframe.cn shuai.yuan@supplyframe.cn"
DATE=`date +%F`
DATE_M=`date -d -1month +%Y%m`
TOTAL=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread'`
IMX=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=175'`
IMX_RT=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1347'`
LPC=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1326'`
KINETIS=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1335'`
S08=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1343'`
DSC=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1046'`
OTHER=`/bin/mysql -hrm-uf65k7yb6oi113324.mysql.rds.aliyuncs.com -upi_sns_eefocus -p'nWxa97#!xW-1' -P 3306 pi_freescale_eefocus -e 'select SUM(views) from eef_forum_thread where fid=1346'`
TOTAL=`/bin/echo $TOTAL|awk -F' ' {'print $2'}`
LPC=`/bin/echo $LPC|awk -F' ' {'print $2'}`
IMX=`/bin/echo $IMX|awk -F' ' {'print $2'}`
IMX_RT=`/bin/echo $IMX_RT|awk -F' ' {'print $2'}`
KINETIS=`/bin/echo $KINETIS|awk -F' ' {'print $2'}`
S08=`/bin/echo $S08|awk -F' ' {'print $2'}`
DSC=`/bin/echo $DSC|awk -F' ' {'print $2'}`
OTHER=`/bin/echo $OTHER|awk -F' ' {'print $2'}`

LAST_MONTH=`/usr/bin/tail -n 1 /pub/scripts/bbs/nxpic/files/bbs_freescale.log`
MAIL=/pub/scripts/bbs/nxpic/files/bbs_freescale_$DATE.mail

TILL_LAST_MONTH_TOTAL=`/bin/echo $LAST_MONTH|awk -F' ' {'print $2'}`
TILL_LAST_MONTH_LPC=`/bin/echo $LAST_MONTH|awk -F' ' {'print $3'}`
TILL_LAST_MONTH_IMX=`/bin/echo $LAST_MONTH|awk -F' ' {'print $4'}`
TILL_LAST_MONTH_IMX_RT=`/bin/echo $LAST_MONTH|awk -F' ' {'print $5'}`
TILL_LAST_MONTH_KINETIS=`/bin/echo $LAST_MONTH|awk -F' ' {'print $6'}`
TILL_LAST_MONTH_S08=`/bin/echo $LAST_MONTH|awk -F' ' {'print $7'}`
TILL_LAST_MONTH_DSC=`/bin/echo $LAST_MONTH|awk -F' ' {'print $8'}`
TILL_LAST_MONTH_OTHER=`/bin/echo $LAST_MONTH|awk -F' ' {'print $9'}`

echo  "$DATE $TOTAL $LPC $IMX $IMX_RT $KINETIS $S08 $DSC $OTHER" >> /pub/scripts/bbs/nxpic/files/bbs_freescale.log

THIS_MONTH_TOTAL=`expr $TOTAL - $TILL_LAST_MONTH_TOTAL`
THIS_MONTH_LPC=`expr $LPC - $TILL_LAST_MONTH_LPC`
THIS_MONTH_IMX=`expr $IMX - $TILL_LAST_MONTH_IMX`
THIS_MONTH_IMX_RT=`expr $IMX_RT - $TILL_LAST_MONTH_IMX_RT`
THIS_MONTH_KINETIS=`expr $KINETIS - $TILL_LAST_MONTH_KINETIS`
THIS_MONTH_S08=`expr $S08 - $TILL_LAST_MONTH_S08`
THIS_MONTH_DSC=`expr $DSC - $TILL_LAST_MONTH_DSC`
THIS_MONTH_OTHER=`expr $OTHER - $TILL_LAST_MONTH_OTHER`


echo -e "Hi,\n$DATE_M月\n总浏览数:$THIS_MONTH_TOTAL\nLPC:$THIS_MONTH_LPC\nIMX_RT:$THIS_MONTH_IMX_RT\nIMX:$THIS_MONTH_IMX\nKINETIS:$THIS_MONTH_KINETIS\nS08:$THIS_MONTH_S08\nDSC:$THIS_MONTH_DSC\n其他:$THIS_MONTH_OTHER" > $MAIL

source /pub/scripts/bbs/python27/bin/activate && python /pub/scripts/bbs/api/smailsimple.py "飞思卡尔社区$DATE_M月份月报数据" $MAIL $MIALTO
#/bin/cat $MAIL |mail -s "飞思卡尔社区$DATE_M月份月报数据" $MIALTO 
#cat $MAIL

#echo -e "Hi,\n$DATE_M月\n总浏览数:$THIS_MONTH_TOTAL\nNXPMCU:$THIS_MONTH_NXPMCU\nIMX:$THIS_MONTH_IMX\nKINETIS:$THIS_MONTH_KINETIS\nS32:$THIS_MONTH_S32\nDSC:$THIS_MONTH_DSC\nLPC:$THIS_MONTH_LPC" > $MAIL
#/bin/cat $MAIL |mail -s "飞思卡尔社区$DATE_M月份月报数据" yanping@eefocus.com
#/bin/cat $MAIL |mail -s "飞思卡尔社区$DATE_M月份月报数据" lupeng@eefocus.com
#/bin/cat $MAIL |mail -s "飞思卡尔社区$DATE_M月份月报数据" xiaoshi@eefocus.com
