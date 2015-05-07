<?php

require './config/g_config.php';

require BASEPATH.'config/mysql_config.'.G_CODETYPE.'.php';

include BASEPATH."lib/parser.php";

$g_db_community = new mysqli_db($g_mysql_config_community);

$g_db_comm = new mysqli_db($g_mysql_config_comm);

include BASEPATH."stdoc.php";

$g_docs = new stdoc($g_db_community,$g_db_comm);
$g_parser = new Parser();

$g_maps = array();
if (file_exists(BASEPATH.'input/outlink.csv')){
	$csvfile = file_get_contents(BASEPATH.'input/outlink.csv');
	$lines = explode("\n",$csvfile);
	foreach($lines as $line){
		$dt = explode(",",trim($line));
		if(count($dt) == 3){
			$g_maps[$dt[0]] = trim($dt[2]).".zip";
		}
	}
}

gen_homepage();
//gen_categories(1);
gen_categories(2);


function gen_homepage(){
	global $g_parser,$g_docs;
	$cates = $g_docs->get_categories();
	$dispdata = array();
	$dispdata['cates'] = $cates[466]['child'];
	$dispdata['content'] = '<img style="vertical-align: top;" src="images/content.jpg" width="700">';
	$dispdata['c1'] = $dispdata['c2'] = 0;
	$view = $g_parser->view('main.php',$dispdata,TRUE);
	file_put_contents(BASEPATH.'output/home.html', $view);
}

function find_filename($link){
	global $g_maps;
	$data = array();
	if (isset($g_maps[$link])){
		$data['name'] = $g_maps[$link];
		$data['fileurl'] = 'file/other/'.$data['name'];
		$data['ico'] = 'zip.gif';
	}else{
		die("error $link");
	}
	return $data;
}

function _deal_files(&$files,$flag,$category){
	foreach($files as &$vvv){
			if (empty($vvv['link'])) {
				if (empty($vvv['filename'])){
					$vvv['filename'] = basename($vvv['path']);
				}
				if (!empty($vvv['url'])){
					if (strpos($vvv['url'],'pan.baidu.com') > 0){
						if ($flag == 1) {
							$vvv['filename'] = md5($vvv['url']);
							$vvv['fileurl'] = $vvv['url'];
							$vvv['ico'] = 'link.gif';
							file_put_contents(BASEPATH.'output/outlink.csv', '"'.$vvv['url']."\",{$vvv['filename']}\n",FILE_APPEND);

						}
						if ($flag == 2){
							$find = find_filename($vvv['url']);
							$vvv['filename'] = $find['name'];
							$vvv['ico'] = $find['ico'];
							$vvv['fileurl'] = $find['fileurl'];
						}
					}else{
						$vvv['fileurl'] = $vvv['url'];
						$vvv['ico'] = 'link.gif';
					}					
				}else{
					if (!empty($vvv['path'])) {
						if ($flag == 1){
							file_put_contents(BASEPATH.'output/cp.sh', "cp \"{$vvv['path']}\" \"\$HOME/file/{$category}/{$vvv['filename']}\"\n",FILE_APPEND);
						}
						$vvv['fileurl'] = "file/{$category}/{$vvv['filename']}";
					}else{
						file_put_contents(BASEPATH.'output/error.csv', $s_doc['id'].','.$vvv['id'].','.$vvv['filename']."\n",FILE_APPEND);
					}	
				}
			}else{
				if (strpos($vvv['link'],'pan.baidu.com') > 0){
					if ($flag == 1) {
						$vvv['filename'] = md5($vvv['link']);
						$vvv['ico'] = 'link.gif';
						$vvv['fileurl'] = $vvv['link'];
						file_put_contents(BASEPATH.'output/outlink.csv', '"'.$vvv['link']."\",{$vvv['filename']}\n",FILE_APPEND);
					}

					if ($flag == 2){
						$find = find_filename($vvv['link']);
						$vvv['filename'] = $find['name'];
						$vvv['ico'] = $find['ico'];
						$vvv['fileurl'] = $find['fileurl'];
					}
				}else{
					$vvv['fileurl'] = $vvv['link'];
					$vvv['ico'] = 'link.gif';
				}
			}
		}
}

function deal_docs(&$docs,$flag){
	foreach($docs as &$s_doc){
		_deal_files($s_doc['file_cn'],$flag,$s_doc['category']);
		_deal_files($s_doc['file_en'],$flag,$s_doc['category']);
		_deal_files($s_doc['file_attachment'],$flag,$s_doc['category']);
	}
}

/**
* @param $flag  1: save log 2: change outlink to local filename 
*/
function gen_categories($flag = 1){

	global $g_parser,$g_docs;
	$cates = $g_docs->get_categories();
	$cates = $cates[466]['child'];

	if ($flag  == 1) {
		file_put_contents(BASEPATH.'output/cp.sh', "#!/bin/sh\n");
		file_put_contents(BASEPATH.'output/cp.sh', "HOME=/home/\n\n",FILE_APPEND);
		file_put_contents(BASEPATH.'output/outlink.csv',"");
	}

	file_put_contents(BASEPATH.'output/error.csv',"");

	foreach ($cates as $k=>$level1){
		$dispdata = array();
		$dispdata['cates'] = $cates;
		$dispdata['content'] = '';
		$dispdata['c1'] =  $level1['id'];
		$dispdata['c2'] =  0;
		
		foreach ($level1['child'] as $kk=>$level2){
			$dt = array();
			$dt['c2_id'] = $level2['id'];
			$dt['c2_name'] = $level2['title'];
			$dt['c3_docs'] = array();

			foreach ($level2['child'] as $kkk=>$level3){
				$ddt = array();
				$ddt['c1_id'] = $level1['id'];
				$ddt['c2_id'] = $level2['id'];
				$ddt['c3_id'] = $level3['id'];
				$ddt['c3_name'] = $level3['title'];

				$docs = $g_docs->get_category_doc($level3['id']);
				if ($flag == 1){
					file_put_contents(BASEPATH.'output/cp.sh', "mkdir -p \$HOME/file/{$level3['id']}\n", FILE_APPEND);
				}

				deal_docs($docs,$flag);

				$ddt['c3_docs'] = $docs;

				$dt['c3_docs'][] = $g_parser->view('doc_block.php',$ddt,TRUE);
			}
			$dispdata['content'] .= $g_parser->view('cate_block.php',$dt,TRUE);
		}
		$view = $g_parser->view('main.php',$dispdata,TRUE);
		file_put_contents(BASEPATH.'output/'.$level1['id'].'.html', $view);
	}


	if(empty(file_get_contents(BASEPATH.'output/error.csv'))){
		unlink(BASEPATH.'output/error.csv');
	}
}

