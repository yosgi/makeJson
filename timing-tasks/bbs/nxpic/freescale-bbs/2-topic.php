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
$end	= isset($params['end']) ? $params['end'] : date('Ymd');

transfer($db_dz, strtotime($end));

// transfer
function transfer($db, $end) {
    $sqlTid = 'SELECT `tid` FROM `%s` WHERE `displayorder`>=0 AND `dateline`<=%d ORDER BY `tid` DESC';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_THREAD, $end));

    $ids    = array();
    if (is_object($rs_tids)) {
        foreach ($rs_tids->rows as $row) {
            $ids[]  = $row['tid'];
        }
    }
    $ids    = array_unique($ids);

    foreach (array_chunk($ids, CHUNK_SIZE) as $chunk) {
        getThread($db, $chunk, $end);
    }
}

function getThread($db, $tids, $end) {
    $index          = 0;

    $sql    = 'SELECT `tid`, `fid`, `author`, `dateline`, `subject`, `lastpost`, `lastposter`, `views`, `replies`,`displayorder` FROM %s';
    $sql    .= ' WHERE (%s) ORDER BY `tid` DESC';
    $sql    .= ' LIMIT %d,%d';

    do {
        $rs_thread    = $db->query(
            sprintf(
                $sql,
                TABLE_DZ_FORUM_THREAD,
                '`tid`=' . implode(' OR `tid`=', $tids),
                $index,
                CHUNK_SIZE
            )
        );

        if (is_object($rs_thread)) {
            foreach ($rs_thread->rows as $row) {
                $msg    = array(
                    sprintf('article_%d_%d.html', $row['fid'], $row['tid']),
                    _escapestr($row['subject']),
                    _escapestr($row['author']),
                    date('Y-m-d', $row['dateline']),
                    $row['replies'],
                    $row['views'],
                    _escapestr($row['lastposter']),
                    date('Y-m-d H:i', $row['lastpost']),
                    _getTopType($row['displayorder']),
                    date('Y-m-d H:i:s'),
                    $row['fid'],
                    _getThreadUrl($row['tid'])
                );
                write_log($msg, $end);
            }
        }

        $index  += CHUNK_SIZE;
    } while (is_object($rs_thread) && !empty($rs_thread->row));
}
function _getTopType($top) {
    $top    = intval($top);
    $arr    = array(
        0   => '',
        1   => '置顶',
        2   => '置顶',
        3   => '置顶'
    );

    return isset($arr[$top]) ? $arr[$top] : $arr[0];
}
function _getThreadUrl($tid) {
    return sprintf(
        'http://www.freescaleic.org/module/forum/thread-%d-1-1.html',
        $tid
    );
}

function _escapestr($str) {
    $str    = str_replace(array("|", "\r\n","\r","\n"), '', $str);
    return $str;
}

function write_log($str_arr, $end) {
    static $cache;

    if (empty($str_arr)) return;
    $str = implode('|', $str_arr).PHP_EOL;

    // write
    $path   = dirname(__FILE__) . PATH_TOPIC;
    if (!is_dir($path)) mkdir($path);
    $name   = 'eefocus_topic_total_' . date('Ymd', strtotime('-1 day', $end));
    $file   = $path . $name . '.txt';
    $fp = fopen($file, empty($cache['topic']) ? 'w' : 'a');
    fwrite($fp, $str);
    fclose($fp);

    $cache['topic']  = true;
}
