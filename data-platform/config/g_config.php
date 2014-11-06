<?php

date_default_timezone_set('Asia/Shanghai');

define ('BASEPATH','F:/brarepos/tools/data-platform/');

define ('G_CODETYPE','development');


if (G_CODETYPE === 'product') {
	define ('G_LOG', FALSE);
}

if (G_CODETYPE === 'development') {
	define ('G_LOG', TRUE);
}


function glog($message,$messageType = ' '){
	$msg = $messageType. ' - '. $message;
	echo $msg."\n";
}


//config for parse log

define ('G_OUT_SQL',true);

define ('G_TIME_LIMIT',90 * 24 * 3600);  //90 days

define ('G_LIMIT',1000);
