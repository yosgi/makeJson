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

//$cls->set_output_file(BASEPATH."output/out_{$offset}_{$limit}.sql");

$cls->parse($offset, $limit, G_TIME_LIMIT);
