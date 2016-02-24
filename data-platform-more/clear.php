<?php

$argv = $_SERVER['argv'];

if (isset($argv[1])){
	$input = trim($argv[1]);
}else{
	die('Miss day');
}

include './config/g_config.php';

$time = strtotime($input);
if(empty($time)){
	die('input day is error');
}
$day = date('Y-m-d',$time);

include BASEPATH.'config/mysqli_config.'.G_CODETYPE.'.php';

$g_db = new mysqli_db($g_mysql_config_center);
$g_ndb = new mysqli_db($g_mysql_config_newsletter);
$g_sdb = new mysqli_db($g_mysql_config_sendy);

include BASEPATH."lib/func.inc.php";

include BASEPATH."classes/eef_edm_log.php";
include BASEPATH."classes/sendy_edm_log.php";

$cls = new eef_edm_log($g_db,$g_ndb);
$flag = $cls->clear($day);
if(!$flag) exit(1);

$cls = new sendy_edm_log($g_db,$g_sdb);

$flag = $cls->clear($day);
if(!$flag) exit(1);
exit(0);
