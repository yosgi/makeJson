<?php

require './config/g_config.php';

include BASEPATH."lib/func.inc.php";

// $dirs = get_dir_dirs("K:/files/file",false,true);

// ############## scan all files ###############3
// $files = array();

// foreach($dirs as $k=>$dir){
// 	$fls = get_dir_files($dir,false,true);
// 	foreach($fls as $v){
// 		$vv = iconv("UTF-8","GBK",$v);
// 		$files[$v] = filesize($vv);
// 	}
// }


// file_put_contents(BASEPATH."output/files",serialize($files));

###################################################

#################### filter same files ####################

// $ctx = file_get_contents(BASEPATH."output/files");

// $files = unserialize($ctx); 

// asort($files);

// $ct = count($files);
// $samefiles = array();
// $files2 = $files;
// foreach($files as $fpath => $size){
// 	unset($files2[$fpath]);
// 	if (isset($samefiles[$fpath])){
// 		continue;
// 	}
// 	foreach($files2 as $fpath2=>$size2){
// 		if(basename($fpath) == basename($fpath2) && $size == $size2){
// 			$samefiles[$fpath2] = array();
// 			$samefiles[$fpath2]['change2'] = $fpath;
// 			$samefiles[$fpath2]['size'] = $size;
// 			$vvv = iconv("UTF-8","GBK",$fpath2);
// 			//echo $kk."\t".$vv['change2']."\n";
// 			//unlink($vvv);
// 		}
// 	}
// }


// file_put_contents(BASEPATH."output/samefiles",serialize($samefiles));

// $ct = file_get_contents(BASEPATH."output/samefiles");

// $samefiles = unserialize($ct);

// foreach ($samefiles as $kk=>$vv){
// 	echo $kk."\t".$vv['change2']."\n";
// 	if ($kk == $vv['change2']){
// 		continue;
// 	}
// 	$path = iconv("UTF-8","GBK",$kk);
// 	unlink($path);
// }


###########################################################


