#!/bin/bash
/pub/scripts/freescale-bbs/ftp.sh /pub/scripts/freescale-bbs/context/ eefocus/context eefocus_context_`date -d '-1 day' +%Y%m%d`.txt ftp1.freescale.com eefocus ")8Gl6v%0k" 
/pub/scripts/freescale-bbs/ftp.sh /pub/scripts/freescale-bbs/topic/ eefocus/topic_total eefocus_topic_total_`date -d '-1 day' +%Y%m%d`.txt ftp1.freescale.com eefocus ")8Gl6v%0k" 

gzip /pub/scripts/freescale-bbs/topic/eefocus_topic_total_`date -d '-2 day' +%Y%m%d`.txt
