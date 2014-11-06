<?php

$argv = $_SERVER['argv'];

if (isset($argv[1]) && isset($argv[2])){
	$offset = intval($argv[1]);
	$limit = intval($argv[2]);
}else{
	die('Miss number limit');
}

include './config/g_config.php';

include BASEPATH.'config/mysql_config.'.G_CODETYPE.'.php';

$g_db = new mysql_db($g_mysql_config);

include BASEPATH."data_analytics.php";

$cls = new data_analytics($g_db);

$cls->init_params(BASEPATH.'input/hy.csv', 'hy');
$cls->init_params(BASEPATH.'input/js.csv', 'js');

file_put_contents(BASEPATH."output/".date("Y-m-d").".log","START: {$offset} - {$limit} ".date("Y-m-d H:i:s")."\n",FILE_APPEND);

$cls->parse($offset, $limit, G_TIME_LIMIT);

file_put_contents(BASEPATH."output/".date("Y-m-d").".log","END  : {$offset} - {$limit} ".date("Y-m-d H:i:s")."\n",FILE_APPEND);
