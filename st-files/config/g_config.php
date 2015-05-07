<?php

date_default_timezone_set('Asia/Shanghai');

define ('BASEPATH','F:/brarepos/tools/st-files/');

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
