<?php

include BASEPATH.'lib/IP.class.php';


class data_analytics {
	
	private $_map_hy = array();
	
	private $_map_js = array();
	
	private $_db = null;
	
	private $_nowday = 0;
	
	private $_output_file = "output/sql.sql";

	public function __construct($db){
		$this->_db = $db;
		
		$day = date('Y-m-d 00:00:00');
		$this->_nowday = strtotime($day);
	}
	
	public function set_output_file($filepath){
		$this->_output_file = $filepath;
	}
	
	public function init_params ($file_path, $type){
		$fp = new SplFileObject($file_path,'r');
	
		$ret = array();
		while (!$fp->eof()){	
			$data = $fp->fgetcsv();
			
			if (empty($data)){
				continue;
			}
	
			foreach ($data as $k=>$v){
				$v = strtoupper(trim($v));
				if (empty($v)){
					break;
				}
				if ($k == 0 ){
					$value = $v;
				}else{
					$ret[$v] = $value;
				}
			}
		}
		
		switch ($type){
			case 'hy':
				$this->_map_hy = $ret;
				break;
			case 'js':
				$this->_map_js = $ret;
				break;
			default:
				throw new Exception(' Error type ');
				break;
		}
	}
	
	
	private function _run ($key,$type){
		$key = strtoupper(trim($key));
		switch ($type){
			case 'hy':
				$data = $this->_map_hy;
				break;
			case 'js':
				$data = $this->_map_js;
				break;
			default:
				throw new Exception(' Error type ');
				break;
		}
	
		$map = array_keys($data);
		
		$result = array();
		
		foreach ($map as $v){
			if (strpos($key,$v) !== false){
				$result[$data[$v]] = 'h';
			}
		}
		
		if (!empty($result)){
			return array_keys($result);
		}else{
			return array();
		}
	}
	/**
	 * db key :
	 * hy
	 * js
	 * domain
	 * ip
	 * 
	 * 
	 * @param unknown $offset
	 * @param unknown $limit
	 * @param unknown $time_limit
	 */
	public function parse($offset,$limit,$time_limit){

		$time = $this->_nowday - $time_limit;
		
		$sql = " SELECT time,param1,param2,param3, uid, domain,ip FROM eef_platform_auto_business_access_log WHERE uid <> 0 and time >= {$time} ORDER BY time ASC LIMIT {$offset}, {$limit};";
		
		$query = $this->_db->query($sql);
		
// 		if ($file === true){
// 			file_put_contents($this->_output_file, " set names utf8;\n");
// 		}
		
		while ($row = $this->_db->fetch_row($query)){
			
			$hy_tags = $js_tags = array();
			
			if (!empty($row['param1'])){
				$hy_tags = $this->_run($row['param1'],'hy');
			}
			
			if (!empty($row['param2'])){
				$hy_tags = array_merge($hy_tags,$this->_run($row['param2'],'hy'));
			}
			
			if (!empty($row['param3'])){
				$hy_tags = array_merge($hy_tags,$this->_run($row['param3'],'hy'));
			}
			$hy_tags = array_unique($hy_tags);
			
			
			if (!empty($row['param1'])){
				$js_tags = $this->_run($row['param1'],'js');
			}
				
			if (!empty($row['param2'])){
				$js_tags = array_merge($js_tags,$this->_run($row['param2'],'js'));
			}
				
			if (!empty($row['param3'])){
				$js_tags = array_merge($js_tags,$this->_run($row['param3'],'js'));
			}
			$js_tags = array_unique($js_tags);
			
			$uid = $row['uid'];
			
			$user_data = $this->_db->query_first(" SELECT * FROM eef_platform_auto_business_edm WHERE uid = {$uid} ");

			$origin_hy = explode(",",$user_data['hy']);
			$new_hy = array_unique(array_merge($origin_hy,$hy_tags));
			$new_hy = array_filter($new_hy);
			
			$origin_js = explode(",",$user_data['js']);
			$origin_js = explode(",",$user_data['js']);
			$new_js = array_unique(array_merge($origin_js,$js_tags));
			$new_js = array_filter($new_js);
			

			$origin_domain = explode(",",$user_data['domain']);
			$domain = preg_replace("/^.*:\/\/([a-zA-Z\-_\.]+).*$/", "\\1",  $row['domain']);
			$origin_domain[] = $domain;
			$new_domain = array_unique($origin_domain);
			$new_domain = array_filter($new_domain);

			if (!empty($row['ip'])){
				$new_ip = $row['ip'];
			}else{
				$new_ip = $user_data['ip'];
			}
			
			if ($user_data['time'] >= $row['time']){
				$time = $user_data['time'];
			}else{
				$time = $row['time'];
			}
			
			
			$location = IP::find($new_ip);
			
			//IP exist(location found) , update database
			if (is_array($location)){
				$country = $location[0];
				$province = $location[1];
				$city = $location[2];
				$update_sql = " UPDATE ignore eef_platform_auto_business_edm SET ".
						" hy = '".addslashes(implode(",", $new_hy))."' , ".
						" js = '".addslashes(implode(",", $new_js))."' , ".
						" domain = '".addslashes(implode(",", $new_domain))."' , ".
						" ip = '".addslashes( $new_ip)."',  ".
						" visit_country = '".addslashes($country)."', ".
						" visit_province = '".addslashes($province)."', ".
						" visit_city = '".addslashes($city)."', ".
						" time = {$time} ".
						" WHERE uid = {$uid};";
			}else{
			//location not found, do nothing, previous location(city) remain.
				$update_sql = " UPDATE ignore eef_platform_auto_business_edm SET ".
						" hy = '".addslashes(implode(",", $new_hy))."' , ".
						" js = '".addslashes(implode(",", $new_js))."' , ".
						" domain = '".addslashes(implode(",", $new_domain))."' , ".
						" ip = '".addslashes( $new_ip)."',  ".
						" time = {$time} ".
						" WHERE uid = {$uid};";
			}
			
//			echo $update_sql."\n";
// 			if ($file === true){
// 				file_put_contents($this->_output_file, $update_sql."\n", FILE_APPEND);
// 			}else{
				$this->_db->query($update_sql);
//			}
					      
		}	
	}
}

	