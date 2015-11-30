<?php

$G_FILENAME = '3w5.csv';
$G_MESSAGE = ' Intel视频存储解决方案专题问卷，赢取丰厚礼品（http://www.eeboard.com/intel-iot/）。随着物联网的快速崛起，视频联网的解决方案也在不断推陈出新。回答三个问题，你就有机会免费获得奖品。';
$G_OUTPUT_FILENAME = "message.sql";

//======================================================================================

$fp = new SplFileObject('input/'.$G_FILENAME,'r');

$line = 0;

$time = time();

file_put_contents('output/'.$G_OUTPUT_FILENAME, "SET names utf8;\n");

while (!$fp->eof()){

	$data = $fp->fgetcsv();

	$uid = $data[0];

	if (!empty($uid)) {

		$sql=	"INSERT INTO eef_message_message (`uid_from`,`uid_to`,`content`,`time_send`) VALUES (1,{{UID}},'".addslashes($G_MESSAGE)."',{{TIME}});\n".
				"INSERT INTO eef_core_user_data (`uid`,`module`,`name`,`time`,`value_int`,value_multi) SELECT '{{UID}}','message','message-alert','{{TIME}}','0','[]' FROM eef_core_user_data WHERE NOT EXISTS (SELECT `uid`  FROM eef_core_user_data WHERE `uid` = {{UID}} AND `module` = 'message' AND `name` ='message-alert') LIMIT 1;\n".
				"UPDATE eef_core_user_data SET value_int = value_int + 1  WHERE `uid` = {{UID}} AND `module` = 'message' AND `name` ='message-alert';\n";
		$sql = str_replace("{{TIME}}", $time, $sql);
		$sql = str_replace("{{UID}}", $uid, $sql);

		file_put_contents('output/'.$G_OUTPUT_FILENAME, $sql,FILE_APPEND);

	}
	$line++;
}
