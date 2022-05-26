<?php
function parseArgv($argv)
{
    $params = array();
    array_shift($argv);
    foreach ($argv as $item) {
        list($k, $v) = explode('=', $item, 2);
        $params[$k] = $v;
    }
    return $params;
}

function escapeFieldName($val)
{
    return sprintf('`%s`', $val);
}

function escapeFieldValue($val, $db)
{
    return sprintf("'%s'", $db->escape($val));
}

function getTypeByExt($extension)
{
    $extImages  = array('gif', 'jpg', 'jpeg', 'png', 'bmp');

    return array_search($extension, $extImages) !== false ? 'image' : 'attachment';
}

function create_sql($db, $table, $item_arr, $value_arr, $op="INSERT", $to_file=true) {
    static $cache   = array();

    if (empty($value_arr)) return NULL;

    $sql    = $op == 'REPLACE' ? 'REPLACE INTO ' : 'INSERT INTO ';
    $sql    .= "`{$table}` (";
    $sql    .= '`'.implode('`, `', $item_arr).'`) VALUES ';

    $sql_value  = array();
    foreach ($value_arr as $value) {
        if (is_array($value)) {
            $tmp    = array();
            foreach ($value as $v) {
                if (!is_int($v) && empty($v)) $v='';
                $tmp[]  = is_string($v) ? escapeFieldValue($v, $db) : $v;
            }
            $sql_value[]    = '('.implode(',',$tmp).')';
        }
    }

    $sql    .= implode(',', $sql_value);
    $sql    .= ';'.PHP_EOL;

    // write sql
    if ($to_file) {
        $path       = dirname(__FILE__)."/data/sql/";
        if (!is_dir($path)) mkdir($path, 0777, true);
        $file       = $path . $table . '.sql';
        $fp = fopen($file, empty($cache[$table]) ? 'w' : 'a');
        if (empty($cache[$table])) fwrite($fp, 'SET NAMES UTF8;'.PHP_EOL);
        fwrite($fp, $sql);
        fclose($fp);
        $cache[$table]  = true;

        return true;
    } else {
        $cache[$table]  = true;
        return $sql;
    }
}

function copy_file($src, $dst){
    if (file_exists($src)) {
        $path   = dirname($dst);
        if (!is_dir($path)) mkdir($path, 0777, true);

        copy($src, $dst);
        return true;
    }

    return false;
}

function write_file($table, $str_arr) {
    static $cache   = array();

    if (empty($str_arr)) return;
    $str = implode(PHP_EOL, $str_arr).PHP_EOL;

    // write sql
    $path       = dirname(__FILE__)."/data/log/";
    if (!is_dir($path)) mkdir($path);
    $file       = $path . $table . '.log';
    $fp = fopen($file, empty($cache[$table]) ? 'w' : 'a');
    fwrite($fp, $str);
    fclose($fp);

    $cache[$table]  = true;
}