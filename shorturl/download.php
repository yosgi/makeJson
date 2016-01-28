<?php

if(file_exists('cache/data.csv')){
    $content = file_get_contents('cache/data.csv');
}else{
    header('HTTP/1.1 404 Not Found'); 
	header("status: 404 Not Found");
	exit;
}

header("application/vnd.ms-excel","utf-8");   
header("Pragma: public");   
header("Expires: 0");   
header("Cache-Control: must-revalidate, post-check=0, pre-check=0");   
header("Content-Type: application/force-download");   
header("Content-Type: application/octet-stream");   
header("Content-Type: application/download");   
header("Content-Disposition: attachment;filename=all-data.csv ");   
header("Content-Transfer-Encoding: binary ");
echo "\xEF\xBB\xBF".$content;