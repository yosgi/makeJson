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
    $sqlTid = 'SELECT `tid` FROM `%s` WHERE `invisible`>=0 AND (`dateline`>=%d AND `dateline`<=%d)';
    $rs_tids   = $db->query(sprintf($sqlTid, TABLE_DZ_FORUM_POST, $start, $end));

    $ids    = array();
    if (is_object($rs_tids)) {
        foreach ($rs_tids->rows as $row) {
            $ids[]  = $row['tid'];
        }
    }
    $ids    = array_unique($ids);

    foreach (array_chunk($ids, CHUNK_SIZE) as $chunk) {
        getPost($db, $chunk, $start, $end);
    }
}

function getPost($db, $tids, $start, $end) {
    $arr_subjects   = array();
    $index          = 0;

    $sql    = 'SELECT `tid`, `fid`, `first`, `author`, `dateline`, `subject`, `message` FROM %s';
    $sql    .= ' WHERE (%s) AND `invisible`>=0';
    $sql    .= ' ORDER BY `tid` ASC, `pid` ASC';
    $sql    .= ' LIMIT %d,%d';

    do {
        $rs_post    = $db->query(
            sprintf(
                $sql,
                TABLE_DZ_FORUM_POST,
                '`tid`=' . implode(' OR `tid`=', $tids),
                $index,
                CHUNK_SIZE
            )
        );

        if (is_object($rs_post)) {
            foreach ($rs_post->rows as $row) {
                if ($row['first']==1) {
                    $arr_subjects[$row['tid']]['subject']   = _escapestr($row['subject']);
                    $arr_subjects[$row['tid']]['position']  = 1;
                } else {
                    $arr_subjects[$row['tid']]['position']++;
                }

                if ($row['dateline']>=$start && $row['dateline']<=$end) {
                    $msg    = array(
                        $arr_subjects[$row['tid']]['subject'],
                        $row['author'],
                        date('Y-m-d H:i:s', $row['dateline']),
                        _escapestr($row['message']),
                        date('Y-m-d H:i:s'),
                        _getThreadUrl($row['tid'], $arr_subjects[$row['tid']]['position']),
                        $arr_subjects[$row['tid']]['position'] . '#',
                        $row['fid']
                    );
                    write_log($start, $msg);
                }
            }
        }

        $index  += CHUNK_SIZE;
    } while (is_object($rs_post) && !empty($rs_post->row));
}

function _getThreadUrl($tid, $position, $pagelimit=10) {
    return sprintf(
        'http://www.freescaleic.org/module/forum/thread-%d-%d-1.html',
        $tid,
        ceil($position / $pagelimit)
    );
}

function _escapestr($str) {
    $str    = str_replace(array("|", "\r\n","\r","\n"), '', $str);
    return $str;
}

function write_log($date, $str_arr) {
    static $cache;

    if (empty($str_arr)) return;
    $str = implode('|', $str_arr).PHP_EOL;

    // write
    $path   = dirname(__FILE__) . PATH_CONTEXT;
    if (!is_dir($path)) mkdir($path);
    $name   = 'eefocus_context_' . date('Ymd', $date);
    $file   = $path . $name . '.txt';
    $fp = fopen($file, empty($cache[$date]) ? 'w' : 'a');
    fwrite($fp, $str);
    fclose($fp);

    $cache[$date]  = true;
}
