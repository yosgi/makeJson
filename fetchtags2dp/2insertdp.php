<?php
set_time_limit(0);

date_default_timezone_set('Asia/ShangHai');

$dbConfig = array(
    'host'     => '192.168.2.82',
    'port'     => 3306,
    'dbname'   => 'newsletter',
    'username' => 'wyx',
    'password' => 'yunxiang'
);
$DB = _getDB($dbConfig);

$currentId = 0;
while ($tmpRs = _getTmpUser($currentId, 100)) {
    foreach ($tmpRs as $tmpUser) {
        _log('update user:' . $tmpUser['email']);
        _updateUserTagsByEmail($tmpUser['email'], $tmpUser['tags_hy'], $tmpUser['tags_js']);
    }
    $currentId = $tmpUser['uid'];
}

function _updateUserTagsByEmail($email, $tags_hy, $tags_js) {
    global $DB;

    if (!$tags_hy && !$tags_js) return false;

    // get user by email
    $sql = sprintf("SELECT `id`,`email`,`hy`,`js` FROM `eef_platform_auto_business_edm` WHERE `email` = '%s' LIMIT 1", $email);
    $query = $DB->query($sql);
    if ($rs = $query->fetch(PDO::FETCH_ASSOC)) {
        if ($rs['tags_hy']) {
            $tags_hy = $tags_hy . ',' . trim($rs['tags_hy'], ',');
            $tags_hy = explode(',', trim($tags_hy, ','));
            $tags_hy = implode(',', array_unique($tags_hy));
        }
        if ($rs['tags_js']) {
            $tags_js = $tags_js . ',' . trim($rs['tags_js'], ',');
            $tags_js = explode(',', trim($tags_js, ','));
            $tags_js = implode(',', array_unique($tags_js));
        }

        // update
        $sql = "UPDATE `eef_platform_auto_business_edm` SET `hy`=:HY,`js`=:JS WHERE `id`=:ID";
        $stmt = $DB->prepare($sql);
        $stmt->execute(array(
            ':HY' => $tags_hy,
            ':JS' => $tags_js,
            ':ID' => $rs['id']
        ));
    }
    return;
}

function _getTmpUser($minId, $step = 100) {
    global $DB;
    $sql = sprintf("SELECT `uid`,`email`,`tags_hy`,`tags_js` FROM `tmp_user_tags` WHERE uid>%d ORDER BY uid LIMIT %d", $minId, $step);
    $query = $DB->query($sql);
    return $query->fetchAll(PDO::FETCH_ASSOC);
}

function _log($content = '', $echo = true) {
    static $logDate = null;
    static $logPath = null;
    if (is_null($logDate)) {
        $logDate = date('Ymd');
    }
    if (is_null($logPath)) {
        $logPath = DEFINED('LOG_PATH') ? LOG_PATH : '/tmp';
    }
    $file = rtrim($logPath, '/') . '/edm_user_hyjs_update_' . $logDate . '.log';
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

