<?php
/**
*
* $argv1:	Date: 2016-01-01
*
* $argv2:	0: import: FALSE, calc  FALSE 
* 			1: import: FALSE, calc TRUE
*			2 and other: import: TRUE, calc TRUE
*/

$argv = $_SERVER['argv'];

if (isset($argv[1]) && isset($argv[2])){
	$input = trim($argv[1]);
	$input2 = intval($argv[2]);
}else{
	die('Miss day && export');
	// $input = '2015-02-02';
	// $input2 = 1;
}

include './config/g_config.php';

$time = strtotime($input);
if(empty($time)){
	die('input day is error');
}

$day = date('Y-m-d',$time);
$file_day = date('Y_m_d',$time);
/*
0: import: FALSE, calc  FALSE 
1: import: FALSE, calc TRUE
2 and other: import: TRUE, calc TRUE
*/
if($input2 == 0){
	$export = FALSE;
	$export2 = FALSE;
}elseif($input2 == 1) {
	$export = FALSE;
	$export2 = TRUE;
}else{
	$export = TRUE;
	$export2 = TRUE;
}

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

$cls->set_output_file(BASEPATH.'output/eef_import_'.$file_day.'.sql');
$flag = $cls->import($day,$export);
if(!$flag) exit(1);

$cls->set_output_file(BASEPATH.'output/eef_calc_'.$file_day.'.sql');
$flag = $cls->calc_open_click($day,$export2);
if(!$flag) exit(1);

$cls = new sendy_edm_log($g_db,$g_sdb);

$flag = $cls->clear($day);
if(!$flag) exit(1);

$cls->set_output_file(BASEPATH.'output/sendy_import_'.$file_day.'.sql');
$flag = $cls->import($day,$export);
if(!$flag) exit(1);

$cls->set_output_file(BASEPATH.'output/sendy_calc_'.$file_day.'.sql');
$flag = $cls->calc_open_click($day,$export2);
if(!$flag) exit(1);
exit(0);
