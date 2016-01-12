<?php

$G_FILENAME = 'uid.csv';
$G_OUTPUT_FILENAME = "disable_user.sql";

//======================================================================================

$fp = new SplFileObject('input/'.$G_FILENAME,'r');

$line = 0;

$time = time();

file_put_contents('output/'.$G_OUTPUT_FILENAME, "SET names utf8;\n");

while (!$fp->eof()){

	$data = $fp->fgetcsv();

	$uid = $data[0];

	if (!empty($uid)) {

		$sql=	"update eef_core_user_account set time_disabled=1450800000 where id =".$uid.";\n";

		file_put_contents('output/'.$G_OUTPUT_FILENAME, $sql,FILE_APPEND);
		
	}
	$line++;
}
echo $line;
