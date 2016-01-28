<?php

include "config/g_config.php";

if(!isset($_POST['m'])){
	die("");
}

$func = trim($_POST['m']);

$cls = new Ajax();

if(!method_exists($cls, $func)){
	die("");
}
	
$cls->$func();


class Ajax {

	public function addfilter(){
		$ret = array('code'=>-1,'result'=>'','message'=>'');
		if(!isset($_POST['ip1'])){
			$ret['message'] = 'no ip1';
			echo json_encode($ret); exit;
		}
		if(!isset($_POST['ip2'])){
			$ret['message'] = 'no ip2';
			echo json_encode($ret); exit;
		}
		if(!isset($_POST['ua'])){
			$ret['message'] = 'no ua';
			echo json_encode($ret); exit;
		}

		$ip1 = $_POST['ip1'];
		$ip2 = $_POST['ip2'];
		$ua = $_POST['ua'];
		if(empty($ip1) && empty($ip2) && empty($ua)){
			$ret['message'] = 'no any filter condition'; 
			echo json_encode($ret); exit;
		}

		if(file_exists("cache/filters")){
			$filters = unserialize(file_get_contents("cache/filters"));
		}else{
			$filters = array();
		}

		$filters[] = array('ip1'=>$ip1,'ip2'=>$ip2,'ua'=>$ua);

		file_put_contents("cache/filters",serialize($filters));

		$ret['code'] = 0;
		$ret['result'] = $filters;
		echo json_encode($ret);
	}

	public function delfilter(){
		$ret = array('code'=>-1,'result'=>'','message'=>'');
		if(isset($_POST['id'])){
			$id = intval($_POST['id']);
		}else{
			echo json_encode($ret); exit;
		}

		$ret = array('code'=>0,'result'=>'','message'=>'');
		if(file_exists("cache/filters")){
			$filters = unserialize(file_get_contents("cache/filters"));
		}else{
			$ret['code'] = -1;
			$ret['message'] = 'filter cache does not exist';
			echo json_encode($ret); exit;
		}

		unset($filters[$id]);

		$new = array();
		foreach($filters as $v){
			$new[] = $v;
		}
		file_put_contents("cache/filters",serialize($new));
		echo json_encode(array('code'=>0,'message'=>'','result'=>$new));
	}

	public function getfilters(){
		if(file_exists("cache/filters")){
			$filters = unserialize(file_get_contents("cache/filters"));
		}else{
			$filters = array();
		}
		echo json_encode(array('code'=>0,'message'=>'','result'=>$filters));
	}

	public function export(){
		global $g_log_dir,$g_filters;
		$ret = array('code'=>-1,'result'=>'','message'=>'');
		if(isset($_POST['date'])){
			$date = $_POST['date'];
		}else{
			$ret['message'] = 'miss date';
			echo json_encode($ret); exit;
		}
		if(isset($_POST['days'])){
			$days = intval($_POST['days']);
		}else{
			$ret['message'] = 'miss days';
			echo json_encode($ret); exit;
		}
		if(isset($_POST['urls'])){
			$urls = $_POST['urls'];
		}else{
			$urls = array();
		}

		$bt = strtotime(date('Y/m/d 00:00:00',strtotime($date)));
		$data = array();

		if(file_exists("cache/filters")){
			$g_filters = unserialize(file_get_contents("cache/filters"));
		}else{
			$g_filters = array();
		}

		for($i = 0;$i< $days;$i++){
			$time = $bt + $i*24*3600;
			$file_path = $g_log_dir."url.eefocus.com.".date("Ymd",$time).".log.gz";
			if(!file_exists($file_path)){
				$ret['message'] = 'miss log '.$file_path;
				echo json_encode($ret); exit;
			}
			$this->_parse($file_path,$urls,$data);
		}

		$fp = new SplFileObject('cache/data.csv',"w");
		$fp->fputcsv(array("From:{$date}  $days days"));
		$fp->fputcsv(array('URL','Time',"IP",'Referer','User Agent'));
		foreach($data as $kk=>$vv){
			//$fp->fputcsv(array($kk,count($vv)));
			foreach($vv as $vvv){
				$fp->fputcsv(array($kk,
					$vvv['time'],
					$vvv['ip'],
					$vvv['referer'],
					$vvv['ua']
					));
			}
		}
		$ret['result'] = 'download.php'; //use relative path
		$ret['code'] = 0;
		echo json_encode($ret);
	}


	private function _parse($file_path,$urls,&$new_data){
		if(empty($file_path)){
			die('');
		}

		if(!empty($urls)){
			$urls = preg_replace("/\r|\n/","$",$urls);
		}

		$fp = new SplFileObject("compress.zlib://".$file_path,"r");
		while(!$fp->eof()){
			$data = $fp->fgetcsv(" ");

			if(!isset($data[2])){
				continue;
			}

			$data[4] = strtotime(preg_replace("/^\[(.*?)\/(.*?)\/(.*?):(.*?)$/","$3-$2-$1 $4",$data[3]));
			
			// $new = array();
			preg_match("/^(.*?) (\/.*?) (.*?)$/",$data[5],$matches);
			// $new['method']=$matches[1];
			$url = $matches[2];
			$filter_url = current(explode("?",$url));
			$filter_url = substr($filter_url,1);
			unset($matches);

			if((preg_match("/^\/([a-zA-Z0-9]+)$/",$url) || preg_match("/^\/[a-zA-Z0-9]+\?[a-zA-Z0-9]+$/",$url))&& $data[6] == 301){
				
				if(!empty($urls)){
					//not in filter urls,ignore
					if(!preg_match("/\/{$filter_url}\\$/",$urls) && !preg_match("/\/{$filter_url}\?[a-zA-Z0-9]+\\$/",$urls)){
						continue;
					}
				}

				if(!is_scalar($data[10])){
					$ip = 'unknown';
				}else{
					if(strpos($data[10],",") !== FALSE){
						$keys = explode(",", $data[10]);
						$ip = trim($keys[0]);
						unset($keys);
					}else{
						$ip = trim($data[10]);
					}
				}

				if($this->_dofilter($ip,$data[8],$data[9]) === FALSE){
					continue;
				}; //ip, referer, ua

				$row = array();
				$row['referer'] = $data[8];
				$row['ua'] = $data[9];
				$row['time'] = date('Y/m/d H:i:s',$data[4]);
				$row['ip'] = $ip;
				
				if(!isset($new_data[$url])){
					$new_data[$url] = array();
				}
				$new_data[$url][] = $row;
				
			}else{
				//not in normal short url ignore
				continue;
			}

		}
	}

	private function _dofilter($ip,$referer,$ua){
		global $g_filters;

		if($ip == 'unknown'){
			return TRUE;
		}

		foreach($g_filters as $f){
			if(!empty($f['ip1']) && !empty($f['ip2']) && !empty($f['ua'])){
				if(ip2long($ip) >= ip2long($f['ip1']) && ip2long($ip) <= ip2long($f['ip2']) && strpos($ua,$f['ua']) !== FALSE){
					return FALSE;
				}
			}else if (!empty($f['ip1']) && !empty($f['ip2'])){
				if(ip2long($ip) >= ip2long($f['ip1']) && ip2long($ip) <= ip2long($f['ip2'])){
					return FALSE;
				}
			}else if (!empty($f['ip1']) && !empty($f['ua'])){
				if($ip == $f['ip1'] && strpos($ua,$f['ua']) !== FALSE){
					return FALSE;
				}
			}else if (!empty($f['ip2']) && !empty($f['ua'])){
				if($ip == $f['ip2'] && strpos($ua,$f['ua']) !== FALSE){
					return FALSE;
				}
			}else if (!empty($f['ip1']) ){
				if($ip == $f['ip1'] ){
					return FALSE;
				}
			}else if (!empty($f['ip2']) ){
				if($ip == $f['ip2'] ){
					return FALSE;
				}
			}else if (!empty($f['ua']) ){
				if(strpos($ua,$f['ua']) !== FALSE){
					return FALSE;
				}
			}
		}

		return TRUE;
	}
}