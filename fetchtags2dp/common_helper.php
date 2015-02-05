<?php
if (!isset($_config)) {
    require_once __DIR__ . '/config.php';
}
$DB         = _getDB($_config['db']);
$MongoDB    = _getMongo($_config['mongo']);

function _log($content = '', $echo = true) {
    static $logDate = null;
    static $logPath = null;
    if (is_null($logDate)) {
        $logDate = date('Ymd');
    }
    if (is_null($logPath)) {
        $logPath = DEFINED('LOG_PATH') ? LOG_PATH : '/tmp';
    }
    $file = rtrim($logPath, '/') . '/edm_analyse_' . $logDate . '.log';
    $content = $content . PHP_EOL;
    if ($echo) echo $content;
    @file_put_contents($file, $content, FILE_APPEND);
}

function _getDB($config) {
    $dsn = sprintf('mysql:host=%s;port=%s;dbname=%s', $config['host'], $config['port'], $config['dbname']);
    $db  = new PDO($dsn, $config['username'], $config['password'], array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8'));
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $db;
}

function _getMongo($config) {
    $mongo   = new Mongo($config['connection']);
    $mongoDB = new MongoDB($mongo, $config['dbname']);
    return $mongoDB;
}

// insert tmp user tags
function insert_user_tags($uids, $tags) {
    global $DB;
    $uid_map = _get_uid_map($uids); // tmp_uid -> eef_uid

    $tags_hy = !empty($tags['hy']) ? $tags['hy'] : '';
    $tags_js = !empty($tags['js']) ? $tags['js'] : '';
    if (!$tags_hy && !$tags_js) return false;

    foreach ($uid_map as $uid => $eef_user) { // todo: inset branch ?
        $user_tags_hy = $tags_hy;
        $user_tags_js = $tags_js;
        // get
        $sql = sprintf("SELECT `uid`,`tags_hy`,`tags_js`,`created` FROM `tmp_user_tags` WHERE `uid` = %d LIMIT 1", $uid);
        $query = $DB->query($sql);
        $created = $updated = time();
        if ($rs = $query->fetch(PDO::FETCH_ASSOC)) {
            if ($rs['tags_hy']) {
                $user_tags_hy = $tags_hy . ',' . trim($rs['tags_hy'], ',');
                $user_tags_hy = explode(',', trim($user_tags_hy, ','));
                $user_tags_hy = implode(',', array_unique($user_tags_hy));
            }
            if ($rs['tags_js']) {
                $user_tags_js = $tags_js . ',' . trim($rs['tags_js'], ',');
                $user_tags_js = explode(',', trim($user_tags_js, ','));
                $user_tags_js = implode(',', array_unique($user_tags_js));
            }
            $created = $rs['created'];
        }

        // update
        $sql = "REPLACE INTO `tmp_user_tags` (`uid`,`eefocus_uid`,`email`,`tags_hy`,`tags_js`,`created`,`updated`) VALUES (:p1, :p2, :p3, :p4, :p5, :p6, :p7)";
        $stmt = $DB->prepare($sql);
        $stmt->execute(array(
            ':p1' => $uid,
            ':p2' => $eef_user['eef_uid'],
            ':p3' => $eef_user['email'],
            ':p4' => $user_tags_hy,
            ':p5' => $user_tags_js,
            ':p6' => $created,
            ':p7' => $updated
        ));
    }
    return true;
}

// get eef uid map with tmp uid
function _get_uid_map($uids) {
    global $DB;
    $uid_map = array();
    $uids = (array) $uids;
    $uids = array_unique($uids);
    foreach ($uids as $k => $uid) {
        if (!$uid) unset($uids[$k]);
    }

    if (count($uids)) {
        $sql = sprintf("SELECT `id`,`eefocus`,`email` FROM `newsletter_user` WHERE `id` IN (%s)", implode(',', $uids));
        $query = $DB->query($sql);
        if ($rs = $query->fetchAll(PDO::FETCH_ASSOC)) {
            foreach ($rs as $k => $v) {
                $uid_map[$v['id']] = array(
                    'eef_uid'   => $v['eefocus'],
                    'email'     => $v['email']
                );
            }
        }
    }
    return $uid_map;
}

// get edm tags by edm id
function get_edm_tags($edm_id) {
    global $DB, $_config;
    $tags = array('js'=>'','hy'=>'');
    if ($edm_id) {
        $sql = sprintf("SELECT `id`,`technical_field` AS js,`industry` AS hy FROM `newsletter_task` WHERE `id` = %d LIMIT 1", $edm_id);
        $query = $DB->query($sql);
        if ($rs = $query->fetch(PDO::FETCH_ASSOC)) {
            // $tags['js'] = explode(',', preg_replace("/\s|　/","", $rs['js']));
            // $tags['hy'] = explode(',', preg_replace("/\s|　/","", $rs['hy']));
            $tags['js'] = _filter_tags($rs['js'], 'js');
            $tags['hy'] = _filter_tags($rs['hy'], 'hy');
        }
    }
    return $tags;
}

// get link tags
function get_link_tags($link) {
    global $DB, $_config;
    $tags = array('js'=>'','hy'=>'');
    $hash = md5($link);
    // get by hash in tmp db
    $sql = sprintf("SELECT `id`,`hash`,`tags_hy`,`tags_js` FROM `tmp_link_tags` WHERE `hash` = '%s' LIMIT 1", $hash);
    $query = $DB->query($sql);
    if ($rs = $query->fetch(PDO::FETCH_ASSOC)) {
        if ($rs['tags_js']) {
            $tags['js'] = trim($rs['tags_js'], ',');
        }
        if ($rs['tags_hy']) {
            $tags['hy'] = trim($rs['tags_hy'], ',');
        }
    } else {
        $page_info = _get_page_info($link);
        if ($page_info) {
            $page_info_str = implode(',', $page_info);

            if ($tags_js = _filter_tags($page_info_str, 'js')) {
                $tags['js'] = $tags_js;
            }
            if ($tags_hy = _filter_tags($page_info_str, 'hy')) {
                $tags['hy'] = $tags_hy;
            }

            // cache to db
            if ($page_info['title']) {
                $sql = "INSERT INTO `tmp_link_tags` (`hash`,`link`,`title`,`description`,`keywords`,`tags_js`,`tags_hy`, `created`) VALUES (:p1, :p2, :p3, :p4, :p5, :p6, :p7, :p8)";
                $stmt = $DB->prepare($sql);
                $stmt->execute(array(
                    ':p1' => $hash,
                    ':p2' => $link,
                    ':p3' => $page_info['title'],
                    ':p4' => $page_info['description'],
                    ':p5' => $page_info['keywords'],
                    ':p6' => $tags['js'],
                    ':p7' => $tags['hy'],
                    ':p8' => time()
                ));
            }
        }
    }

    return $tags;
}

// init tags map
function _init_tags_map() {
    $tags_map = array();
    foreach (array('hy', 'js') as $type) {
        $file = __DIR__ . '/' . $type . '.csv';
        $fp = fopen($file, "r");

        $map = array();
        while (!feof($fp)){
            $data = fgetcsv($fp);

            if (empty($data)){
                continue;
            }

            foreach ($data as $k => $v){
                $v = strtoupper(trim($v));
                if (empty($data[0]) || empty($v)){
                    break;
                }
                $map[$v] = $data[0];
            }
        }
        fclose($fp);
        $tags_map[$type] = $map;
    }

    return $tags_map;
}

function _filter_tags($tag_str, $type = 'hy') {
    static $tags_map = null;
    if (is_null($tags_map)) {
        $tags_map = _init_tags_map();
    }

    $tags = array();
    $map  = isset($tags_map[$type]) ? $tags_map[$type] : array();
    if ($tag_str && $map) {
        foreach ($map as $k=>$v) {
            if (stripos($tag_str, $k) !== false)    $tags[] = $v;
        }
    }

    return $tags ? implode(',', array_unique($tags)) : '';
}

// get remote page info
function _get_page_info($link) {

    $html = _curl_get_contents($link, 10);

    $doc = new DOMDocument();
    $meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>';
    @$doc->loadHTML($meta . $html);

    $nodes = $doc->getElementsByTagName('title');

    $title = $nodes->item(0)->nodeValue;

    $metas = $doc->getElementsByTagName('meta');

    for ($i = 0; $i < $metas->length; $i++){
        $meta = $metas->item($i);
        if($meta->getAttribute('name') == 'description')
            $description = $meta->getAttribute('content');
        if($meta->getAttribute('name') == 'keywords')
            $keywords = $meta->getAttribute('content');
    }

    return array(
        'title'         => !empty($title) ? $title : '',
        'keywords'      => !empty($keywords) ? $keywords : '',
        'description'   => !empty($description) ? $description : ''
    );
}

function _curl_get_contents($url = '', $timeout = '') {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0)");
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip,deflate');

    if (!empty($timeout)) {
        curl_setopt($ch, CURLOPT_TIMEOUT, intval($timeout));
    }
    $html = curl_exec($ch);
    curl_close($ch);

    return empty($html) ? null : $html;
}