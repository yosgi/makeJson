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
	
	private function _deal_domain($domain,&$type){
		/*	
									技术类别
			ams社区	ams.eefocus.com		传感/MEMS		
			飞兆技术社区	www.fairchildic.org		电源/电器管理		
			LED社区	ledlight.eefocus.com		光电/显示		
			美信技术中心	maximmini.eefocus.com		电源/电器管理		
			凌力尔特技术社区	linear.eefocus.com		RF/微波，电源/电器管理		
			模拟与电源技术社区	analog.eefocus.com		电源/电器管理		
			射频微波技术社区	rf.eefocus.com		RF/微波		
			英飞凌技术社区	www.infineonic.org		控制器/处理器/DSP		
			Atmel技术社区	atmel.eefocus.com		控制器/处理器/DSP		
			飞思卡尔技术社区	www.freescaleic.org		控制器/处理器/DSP		
			意法半导体STM8/STM32社区	www.stmuc.org		控制器/处理器/DSP		
			嵌入式社区	mcu.eefocus.com		控制器/处理器/DSP		
			OpenHW开源硬件社区	openhw.eefocus.com		数字/可编程逻辑		
			与非网测试测量社区	tm.eefocus.com		测试测量		
		 */
		 $type = -1;
		 
		 $map = array();
		 $map['ams.eefocus.com'] =array("传感/MEMS");
		 $map['www.fairchildic.org'] =array("电源/电器管理");
		 $map['ledlight.eefocus.com'] =array("光电/显示");
		 $map['maximmini.eefocus.com'] =array("电源/电器管理");
		 $map['linear.eefocus.com'] =array("RF/微波","电源/电器管理");
		 $map['analog.eefocus.com'] =array("电源/电器管理");
		 $map['rf.eefocus.com'] =array("RF/微波");
		 $map['www.infineonic.org'] =array("控制器/处理器/DSP");
		 $map['atmel.eefocus.com'] =array("控制器/处理器/DSP");
		 $map['www.freescaleic.org'] =array("控制器/处理器/DSP");
		 $map['www.stmuc.org'] =array("控制器/处理器/DSP");
		 $map['mcu.eefocus.com'] =array("控制器/处理器/DSP");
		 $map['openhw.eefocus.com'] =array("数字/可编程逻辑");
		 $map['tm.eefocus.com'] =array("测试测量");
		
		 foreach ($map as $k=>$v){
		 	if (strpos($domain,$k) !== false){
		 		$type = 1;
		 		return $v;
		 	}
		 }
		 
		
		 /*						行业类别
			汽车电子互动社区	automotive.eefocus.com				汽车电子		
			英飞凌汽车电子生态圈	www.infineon-ecosystem.org				汽车电子
		 */
		 $map2 = array();
		 $map2['automotive.eefocus.com'] =array("汽车电子");
		 $map2['www.infineon-ecosystem.org'] =array("汽车电子");
		
		 foreach ($map2 as $k=>$v){
		 	if (strpos($domain,$k) !== false){
		 		$type = 2;
		 		return $v;
		 	}
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
			
			$domain = preg_replace("/^.*:\/\/([a-zA-Z\-_\.]+).*$/", "\\1",  $row['domain']);
			$type = -1;
			$domain_tags = $this->_deal_domain($domain, $type);
		
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
			if ($type == 2 ){
				$hy_tags = array_merge($hy_tags,$domain_tags);
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
			if ($type == 1 ){
				$js_tags = array_merge($js_tags,$domain_tags);
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
			
			$origin_domain[] = $domain;
			$new_domain = array_unique($origin_domain);
			$new_domain = array_filter($new_domain,'filter_domain');

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
/**
 *
 * @param unknown $v
 * @return boolean
 */
function filter_domain($v){
	if (empty($v)) return false;
	
	if (preg_match("/sso\.eefocus/", $v)){
		return false;
	}
	
	if (preg_match("/account\.eefocus/", $v)){
		return false;
	}

	return true;
}
	