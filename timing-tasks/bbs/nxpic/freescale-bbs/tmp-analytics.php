<?php
require_once dirname(__FILE__) . '/mysql.class.php';
require_once dirname(__FILE__) . '/functions.php';
require_once dirname(__FILE__) . '/etc/common.inc.php';

date_default_timezone_set('Asia/Shanghai');
ini_set('pcre.backtrack_limit', 100000000);
set_time_limit(0);

// db info
$db_dz   = new MySQL($db_config_dz['host'], $db_config_dz['username'], $db_config_dz['password'], $db_config_dz['dbname']);
$db_dz->query(sprintf('SET NAMES %s', $db_config_dz['charset']));

$params = array();
$params = parseArgv($argv);
$start  = isset($params['start']) ? $params['start'] : date("Ymd", strtotime("-1 day"));
$end    = isset($params['end']) ? $params['end'] : date('Ymd');

transfer($db_dz, strtotime($start), strtotime($end));

// transfer
function transfer($db, $start, $end) {
    // thread
    $sqlTid = 'SELECT count(*) AS `total` FROM `%s` WHERE `invisible`>=0 AND `first`=1 AND (`dateline`>=%d AND `dateline`<=%d)';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_POST, $start, $end));

    if (is_object($rs_tids)) {
	echo 'threads:' . $rs_tids->rows[0]['total'] . PHP_EOL;
    }
	
    // post
    $sqlTid = 'SELECT count(*) AS `total` FROM `%s` WHERE `invisible`>=0 AND `first`=0 AND (`dateline`>=%d AND `dateline`<=%d)';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_POST, $start, $end));

    if (is_object($rs_tids)) {
	echo 'posts:' . $rs_tids->rows[0]['total'] . PHP_EOL;
    }

    // poster 
    $sqlTid = 'SELECT count(distinct(authorid)) AS `total` FROM `%s` WHERE `invisible`>=0 AND `first`=1 AND (`dateline`>=%d AND `dateline`<=%d)';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_POST, $start, $end));

    if (is_object($rs_tids)) {
	echo 'posters:' . $rs_tids->rows[0]['total'] . PHP_EOL;
    }
	
    // replyer
    $sqlTid = 'SELECT count(distinct(authorid)) AS `total` FROM `%s` WHERE `invisible`>=0 AND `first`=0 AND (`dateline`>=%d AND `dateline`<=%d)';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_POST, $start, $end));

    if (is_object($rs_tids)) {
	echo 'replyers:' . $rs_tids->rows[0]['total'] . PHP_EOL;
    }
}
