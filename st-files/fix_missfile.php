<?php

##偶尔能用 ，因为大部分文件为zip和pdf 得一一处理对应

require './config/g_config.php';

require BASEPATH.'config/mysql_config.'.G_CODETYPE.'.php';

$g_db_comm = new mysqli_db($g_mysql_config_comm);

$ctx = file_get_contents(BASEPATH."output/missfiles");

$lines = explode("\n",$ctx);
file_put_contents(BASEPATH.'output/sql.sql', "");


foreach($lines as $line){
	if (empty($line)){
		continue;
	}
	$name = basename($line);

	$sql = "select * from eef_media_doc where path like '%{$name}'";

	$data = $g_db_comm->query_first($sql);

	$newpath = str_replace($name,$name."pdf",$data['path']);
	$newpath = addslashes($newpath);

	$sql = " UPDATE eef_media_doc SET path = '{$newpath}' WHERE id = {$data['id']} ";
	file_put_contents(BASEPATH.'output/sql.sql', $sql.";\n",FILE_APPEND);

}