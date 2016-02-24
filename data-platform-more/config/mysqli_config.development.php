<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

include BASEPATH.'/lib/mysqli_db.php';


$g_mysql_config_center = array (
		'host' => '192.168.2.82',
		'port' => 3309,
		'username' => 'wyx',
		'password' => 'yunxiang',
		'dbname' => 'center_eefocus',
		'charset' => 'utf8'
);
	       
$g_mysql_config_newsletter = array (
		'host' => '192.168.2.82',
		'port' => 3309,
		'username' => 'wyx',
		'password' => 'yunxiang',
		'dbname' => 'newsletter',
		'charset' => 'utf8'
);    

$g_mysql_config_sendy = array (
		'host' => '192.168.2.82',
		'port' => 3309,
		'username' => 'wyx',
		'password' => 'yunxiang',
		'dbname' => 'sendy',
		'charset' => 'utf8'
);   