<?php
set_time_limit(0);

date_default_timezone_set('Asia/ShangHai');
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/common_helper.php';


$day_start  = isset($argv[1]) ? $argv[1] : '2014-10-01';
$day_end  = isset($argv[2]) ? $argv[2] : '2015-02-01';

$time_start = $current_time = strtotime($day_start);
$time_end   = strtotime($day_end);

while ($current_time <= $time_end) {
    $day = date('Y-m-d', $current_time);
    _log('fetch:'.$day);
    runbyday($day);
    $current_time += 24*60*60;
}

function runbyday($day) {
    global $MongoDB;

    $start_time = strtotime($day);
    $end_time   = $start_time + 24*3600;
    $query = array(
        'date'   => array(
            '$gte'  => $start_time,
            '$lt'   => $end_time
        )
    );

    $edmid2uids = $link2uids = array();

    $cursor = $MongoDB->edms->find($query);

    while($cursor->hasNext()){
        $val = $cursor->getNext();
        // build edmid2uids
        if($val['type'] == 'load') {
            $edm_id = $val['edm_id'];
            if (!isset($edmid2uids[$edm_id])) {
                $edmid2uids[$edm_id] = array();
            }
            if ($val['uids']) {
                $edmid2uids[$edm_id] = array_merge($edmid2uids[$edm_id], $val['uids']);
            }
        }
        // build link2uids
        if($val['type'] == 'jump') {
            if($val['uids']) {
                foreach($val['uids'] as $k=>$v){
                    $link = trim($v['url']);
                    if (!isset($link2uids[$link])) {
                        $link2uids[$link] = array();
                    }
                    $link2uids[$link][] = (int) $v['user'];
                }
            }
        }
    }

    // fetch tags by edm
    foreach ($edmid2uids as $edm_id => $uids) {
        $tags = get_edm_tags($edm_id);
        _log('day:' . $day . '  edm:' . $edm_id);
        if (!$tags && !$tags['hy'] && !$tags['js']) continue;
        insert_user_tags($uids, $tags);
        unset($tags);
    }

    // fetch tags by link
    foreach ($link2uids as $link => $uids) {
        $tags = get_link_tags($link);
        _log('day:' . $day . '  link:' . $link);
        if (!$tags && !$tags['hy'] && !$tags['js']) continue;
        insert_user_tags($uids, $tags);
        unset($tags);
    }
}
