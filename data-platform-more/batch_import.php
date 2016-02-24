<?php
/**
*
* $argv1:	Start Date: 2016-01-01
*
* $argv2:	End Date: 2016-01-31
*
* $argv3:	0: import: FALSE, calc  FALSE 
* 			1: import: FALSE, calc TRUE
*			2 and other: import: TRUE, calc TRUE
*/

$argv = $_SERVER['argv'];

if (isset($argv[1]) && isset($argv[2]) && isset($argv[3])){
	$input = trim($argv[1]);
	$input2 = trim($argv[2]);
	$input3 = intval($argv[3]);
}else{
	die('Miss begin day && end day && export');
}

include './config/g_config.php';

$time = strtotime($input);
if(empty($time)){
	die('input day is error');
}

$time2 = strtotime($input2);
if(empty($time2)){
	die('input end day is error');
}

if($time2 < $time){
	die('end is smaller than begin');
}

if($input3 == 0){
	$export = FALSE;
	$export2 = FALSE;
}elseif($input3 == 1) {
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

$days = floor(($time2 - $time)/(3600*24));

$cls = new eef_edm_log($g_db,$g_ndb);
$cls2 = new sendy_edm_log($g_db,$g_sdb);

for($index = $time; $index <= $time2; $index += 3600*24){
	$day = date('Y-m-d',$index);
	$file_day = date('Y_m_d',$index);

	$flag = $cls->clear($day);
	if(!$flag) exit(1);

	$cls->set_output_file(BASEPATH.'output/eef_import_'.$file_day.'.sql');
	$flag = $cls->import($day,$export);
	if(!$flag) exit(1);

	$cls->set_output_file(BASEPATH.'output/eef_calc_'.$file_day.'.sql');
	$flag = $cls->calc_open_click($day,$export2);
	if(!$flag) exit(1);

	$flag = $cls2->clear($day);
	if(!$flag) exit(1);

	$cls2->set_output_file(BASEPATH.'output/sendy_import_'.$file_day.'.sql');
	$flag = $cls2->import($day,$export);
	if(!$flag) exit(1);

	$cls2->set_output_file(BASEPATH.'output/sendy_calc_'.$file_day.'.sql');
	$flag = $cls2->calc_open_click($day,$export2);
	if(!$flag) exit(1);
}



