<?php

date_default_timezone_set("Asia/Shanghai");

$tm = "2016/05";
$minday = 1;
$maxday = 25;

led();

function led() {
	global $tm,$minday,$maxday;
	//ams
	$uids = array(
			2099900,2099907,2100105,2102019,2102028,2102047,2102148,2102565,2102574,2102722,2103156,2103568,2104164,2107132,2107768,2108106,2108633,2108875,2109036,2110052,2110187,2110562,2111785,2112114,2115024,2115031,2115049,2115162,2116855,3053816,3055146,3055922,3056242,3056578,3056913,3057158,3059235,3059961,3066297

	);
	
	$outputfile = "output/led.sql";
	
	file_put_contents($outputfile,"SET names utf8;\n");
	
	$sql1 = " INSERT ignore INTO eef_member_member(uid,time) VALUES(##UID##,##TIME##);";
	
	$sql2 = " INSERT ignore INTO eef_member_profile(uid,level) VALUES (##UID##,1);";
	
	
	foreach ($uids as $uid){
		$t = $tm."/".rand($minday,$maxday)." ".rand(7,22).":".rand(1,59).":".rand(1,59);
		$s_time = strtotime($t);
	
	
		$sql = str_replace("##UID##", $uid, $sql1);
		$sql = str_replace("##TIME##",$s_time,$sql)."\n";
	
		$sqlx = str_replace("##UID##", $uid, $sql2)."\n";
	
		file_put_contents($outputfile,$sql.$sqlx,FILE_APPEND);
	}
}


function fairchild() {
	global $tm;
	$uids = array(
			412175,1609418,125964,127296,221909,257372,360516,364428,416988,133291,135369,136214,345604,394616,1647331,338600,374692,390651,1657617,144646,305426,398253,1671519,1675012,150034
	);
	
	$sql1 = " INSERT ignore INTO eef_member_member(uid,time) VALUES(##UID##,##TIME##);";
	
	$sql2 = " INSERT ignore INTO eef_member_profile(uid,level) VALUES (##UID##,1);";
	
	$outputfile = "output/fairchild.sql";
	
	file_put_contents($outputfile,"SET names utf8;\n");
	
	foreach ($uids as $uid){
		$t = $tm."/".rand(1,28)." ".rand(7,22).":".rand(1,59).":".rand(1,59);
		$s_time = strtotime($t);
		$sql = str_replace("##UID##", $uid, $sql1);
		$sql = str_replace("##TIME##",$s_time,$sql)."\n";
		
		$sqlx = str_replace("##UID##", $uid, $sql2)."\n";
		
		file_put_contents($outputfile,$sql.$sqlx,FILE_APPEND);
	}
}

function ams() {
	global $tm;
	//ams
	$uids = array(
			2099900,2099907,2100105,2102019,2102028,2102047,2102148,2102565,2102574,2102722,2103156,2103568,2104164,2107132,2107768,2108106,2108633,2108875,2109036,2110052,2110187,2110562,2111785,2112114,2115024,2115031,2115049,2115162,2116855,3053816,3055146,3055922,3056242,3056578,3056913,3057158,3059235,3059961,3066297

	);
	
	$outputfile = "output/ams.sql";
	
	file_put_contents($outputfile,"SET names utf8;\n");
	
	$sql1 = " INSERT ignore INTO eef_member_member(uid,time) VALUES(##UID##,##TIME##);";
	
	$sql2 = " INSERT ignore INTO eef_member_profile(uid,level) VALUES (##UID##,1);";
	
	
	foreach ($uids as $uid){
		$t = $tm."/".rand(1,28)." ".rand(7,22).":".rand(1,59).":".rand(1,59);
		$s_time = strtotime($t);
	
	
		$sql = str_replace("##UID##", $uid, $sql1);
		$sql = str_replace("##TIME##",$s_time,$sql)."\n";
	
		$sqlx = str_replace("##UID##", $uid, $sql2)."\n";
	
		file_put_contents($outputfile,$sql.$sqlx,FILE_APPEND);
	}
}

function analog() {
	
	global $tm;
// 	
    $uids = array(
    		"34","4484","8859","9029","10528","21701","40787","44057","47177","60064","60118","77409","89001","98611","114378","133587","158954","178197","178953","180310","191368","191590","192046","205404","210474","214908","224480","236914","242923","251541","252169","252755","253130","254274","255427","255908","256789","258898","259431","267357","269831","270132","273008","275159","281280","281652","282066","291960","294031","295455","296078","300773","302051","302675","303762","305415","305426","306085","306530","307273","308658","312803","312949","315402","316560","318008","318144","319522","320451","320668","322215","324867","327137","327674","328244","328605","329383","329645","333257","334888","338496","338816","340160","342234","345861","350584","362300","378221","378265","387631","390132","425268","1844678","1894651","2005330","2026512","2034770","2036571","2038436","2071165"
    );

	$outputfile = "output/analog.sql";
	
	file_put_contents($outputfile,"SET names utf8;\n");
	
	$sql1 = " INSERT ignore INTO eef_member_member(uid,time) VALUES(##UID##,##TIME##);";
	
	$sql2 = " INSERT ignore INTO eef_member_profile(uid,level) VALUES (##UID##,1);";
	
	
	foreach ($uids as $uid){
		$t = $tm."/".rand(1,28)." ".rand(7,22).":".rand(1,59).":".rand(1,59);
		$s_time = strtotime($t);
	
		$sql = str_replace("##UID##", $uid, $sql1);
		$sql = str_replace("##TIME##",$s_time,$sql)."\n";
	
		$sqlx = str_replace("##UID##", $uid, $sql2)."\n";
	
		file_put_contents($outputfile,$sql.$sqlx,FILE_APPEND);
	}
}




