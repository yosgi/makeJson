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

if (!isset($argv[1]) || $argv[1] != 'confirm'){
	echo 'param error';
	exit;
}

include './config/g_config.php';
/*
0: import: FALSE, calc  FALSE 
1: import: FALSE, calc TRUE
2 and other: import: TRUE, calc TRUE
*/
$export = FALSE;
$export2 = FALSE;

include BASEPATH.'config/mysqli_config.'.G_CODETYPE.'.php';

$g_db = new mysqli_db($g_mysql_config_center);
// $g_ndb = new mysqli_db($g_mysql_config_newsletter);
$g_sdb = new mysqli_db($g_mysql_config_sendy);

include BASEPATH."lib/func.inc.php";
// include BASEPATH."classes/eef_edm_log.php";
include BASEPATH."classes/sendy_edm_log.php";

// $cls = new eef_edm_log($g_db,$g_ndb);

// $flag = $cls->clear($day); 
// if(!$flag) exit(1);

// $cls->set_output_file(BASEPATH.'output/eef_import_'.$file_day.'.sql');
// $flag = $cls->import($day,$export);
// if(!$flag) exit(1);

// $cls->set_output_file(BASEPATH.'output/eef_calc_'.$file_day.'.sql');
// $flag = $cls->calc_open_click($day,$export2);
// if(!$flag) exit(1);

$cls = new sendy_edm_log($g_db,$g_sdb);

$time = strtotime('2016-07-03');
while (1) {
	$day = date('Y-m-d',$time);
	$file_day = date('Y_m_d',$time);

	$time += 86400;
	if ($time == strtotime('20170629') || $time == strtotime('20170630')) {
		continue;
	}
	if ($time >= strtotime('20171128')) {
		break;
	}

	glog("\n\nINFO",'fix sendy edm data begin - ' . date('Y-m-d',$time) . ':');

	$flag = $cls->clear($day);
	if(!$flag) exit(1);

	$cls->set_output_file(BASEPATH.'output/sendy_import_'.$file_day.'.sql');
	$flag = $cls->import($day,$export);
	if(!$flag) exit(1);

	$cls->set_output_file(BASEPATH.'output/sendy_calc_'.$file_day.'.sql');
	$flag = $cls->calc_open_click($day,$export2);
	if(!$flag) exit(1);
	glog("INFO",'fix sendy edm data end - ' . date('Y-m-d',$time) . '.');
	sleep(5);
}

exit(0);
