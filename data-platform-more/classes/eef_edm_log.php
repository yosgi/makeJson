<?php

class eef_edm_log {
	
	static public $RMOTE_LOG_URL = "http://stat.local.eefocus.com:8010/search/ajax.html?func=HTableEdm&domain=analytics.eefocus.com&start_time=%s&end_time=%s";
	
	private $_db = null;

	private $_ndb = null;
	
	private $_now = 0;
	
	private $_output_file = null;

	public function __construct($db,$newsletter_db){
		$this->_db = $db;
		$this->_ndb = $newsletter_db;

		$this->_now = time();
	}
	
	public function set_output_file($filepath){
		$this->_output_file = $filepath;
	}
	
	public function import($day,$export=TRUE){
		glog('INFO','start eef_edm_log import day:'.$day. ' EXPORT:'.($export==TRUE?$this->_output_file:'FALSE'));
		$content = curl_get(sprintf(self::$RMOTE_LOG_URL,$day,$day));
		if($content !== FALSE){
			try{
				$result = $this->_parse_data($content,strtotime($day));
				$sqls = $this->_update($result,$export);
				if($export == TRUE){
					if(empty($this->_output_file)){
						throw new Exception('no exist output file definition');
					}
					file_put_contents($this->_output_file,"set names utf8;\n");
					file_put_contents($this->_output_file, implode("\n",$sqls),FILE_APPEND);
				}
			}catch(Exception $e){
				glog('ERROR',$e->getMessage());
				return FALSE;
			}
		}else{
			glog('WARNING','stat.local.eefocus.com empty '.$day);
			return FALSE;
		}
		glog('INFO','complete eef_edm_log import '.$day);
		return TRUE;
	}

	/*clear data*/
	public function clear($day){
		glog('INFO','start eef_edm_log clear '.$day);
		$time = strtotime(date("Y-m-d 00:00:00",strtotime($day)));
		try{
			$this->_db->query(" DELETE FROM eef_platform_auto_business_edm_log WHERE time = $time AND eid>0");
		}catch(Exception $e){
			glog('ERROR',$e->getMessage());
			return FALSE;
		}
		glog('INFO','complete eef_edm_log clear '.$day);
		return TRUE;
	}

	public function  calc_open_click($day,$export = TRUE){
		glog('INFO','start eef_edm_log calc_open_click day:'.$day. ' EXPORT:'.($export==TRUE?$this->_output_file:'FALSE'));
		try{
			$sqls = array();
			$time = strtotime(date("Y-m-d 00:00:00",strtotime($day)));
			$data = $this->_db->query_first("SELECT count(*) as alldata FROM eef_platform_auto_business_edm_log WHERE time = $time AND eid>0");

			$count = ceil($data['alldata']/5000);
			if($export == TRUE && $count > 0){
				if(empty($this->_output_file)){
					throw new Exception('no exist output file definition');
				}
				file_put_contents($this->_output_file,"set names utf8;\n");
			}
			for ($i = 0 ; $i < $count ; $i++){
				$sqls = $this->_deal_open_click($time,$i*5000,5000);
				if($export == TRUE){
					file_put_contents($this->_output_file, implode("\n",$sqls)."\n",FILE_APPEND);
				}else{
					foreach($sqls as $sql){
						$this->_db->query($sql);
					}
				}
			}
		}catch(Exception $e){
			glog('ERROR',$e->getMessage());
			return FALSE;
		}
		glog('INFO','complete eef_edm_log calc_open_click '.$day);
		return TRUE;
	}

	private function _deal_open_click($time,$offset,$limit){
		$sqls = array();
		
		$query = $this->_db->query("SELECT email,open,click FROM eef_platform_auto_business_edm_log WHERE time = $time AND eid>0 LIMIT {$offset},{$limit}");

		$click_count = array();
		while ($row = $this->_db->fetch_row($query)){
			$row['email'] = trim($row['email']);
			if(isset($click_count[$row['email']] )) {
				$click_count[$row['email']]['open_count'] += $row['open'];
				$click_count[$row['email']]['click_count'] += $row['click'];
			}else{
				$click_count[$row['email']] = array();
				$click_count[$row['email']]['open_count'] = $row['open'];
				$click_count[$row['email']]['click_count'] = $row['click'];
			}
		}
		if(!empty($click_count)){
			foreach($click_count as $email => $v){
				$sql = " UPDATE eef_platform_auto_business_edm SET `open_count` = `open_count` + {$v['open_count']}, `click_count` = `click_count` + {$v['click_count']}  WHERE email = '".addslashes($email)."';";
				$sqls[] = $sql;
			}
		}
		return $sqls;
	}

	private function _update($data,$export){
		$count = count($data);
		$limit =0;
		$updatedata = array();
		$uids = array();
		$sqls = array();
		foreach($data as $k=>$v){
			if(empty($v['uid'])) continue;
			$limit ++;
			$updatedata[$v['uid']] = $v;

			$uids[] = $v['uid'];
			if($limit == 100){
				$email_users = $this->_get_email_users($uids);
				if($export == TRUE){
					$sqls = array_merge($sqls,$this->_add_edm_log($updatedata,$email_users));
				}else{
					$tmp_sqls = $this->_add_edm_log($updatedata,$email_users);
					foreach($tmp_sqls as $sql){
						$this->_db->query($sql);
					}
				}
				$limit =0;
				$updatedata = array();
				$uids = array();
			}
		}
		if(!empty($uids)){
			$email_users = $this->_get_email_users($uids);
			if($export == TRUE){
				$sqls = array_merge($sqls,$this->_add_edm_log($updatedata,$email_users));
			}else{
				$tmp_sqls = $this->_add_edm_log($updatedata,$email_users);
				foreach($tmp_sqls as $sql){
					$this->_db->query($sql);
				}
			}
		}
		return $sqls;
	}

	private function _add_edm_log($rawdatas,$email_users){
		$sqls = array();
		$click_count = array();
		foreach($rawdatas as $key=>$row){
			if(isset($email_users[$key])){
				$row['eefocus_uid'] = empty($email_users[$key]['eefocus'])?0:$email_users[$key]['eefocus'];
				$row['email'] = $email_users[$key]['email'];
				$sql = " INSERT INTO eef_platform_auto_business_edm_log(eid,uid,email,`time`,`open`,`click`,time_loaded) VALUES ( '".$row['eid']."','".$row['eefocus_uid']."','".addslashes($row['email'])."','".$row['time']."','".$row['open']."','".$row['click']."','".$this->_now."');";
				$sqls[] = $sql;

				if($email_users[$key]['status'] == 'Q'){
					$sql = " UPDATE eef_platform_auto_business_edm SET unsubscribe = 'Q' WHERE email = '".addslashes($email_users[$key]['email'])."';";
					$sqls[] = $sql;
				}

			}else{
				continue;
			}
		}
		return $sqls;
	}

	private function _get_email_users($uids){
		$sql = " SELECT id,eefocus,email,status FROM newsletter_user WHERE id IN (".implode(",",$uids).")";
		$query = $this->_ndb->query($sql);
		$ret = array();
		while ($row = $this->_ndb->fetch_row($query)){
			$row['email'] = trim($row['email']);
			$row['status'] = trim($row['status']);
			$ret[$row['id']] = $row;
		}
		return $ret;
	}
	
	private function _parse_data($content, $time)
    {
        $result  = array();
        // Parse open counts
        $matches = array();
        preg_match('|name="load">.+</th></tr><tr><td>(.+)</td>|', $content, $matches);
        $opens = array();
        $opens = explode('; ', $matches[1]);
        foreach ($opens as $row) {
            if (strpos($row, ':')) {
                list($eid, $uid) = explode(':', $row);
                $key = $eid . '-' . $uid;
                if (isset($result[$key])) {
                    continue;
                } else {
                    $result[$key] = array(
                        'eid'   => $eid,
                        'uid'   => $uid,
                        'time'  => $time,
                        'open'  => 1,
                        'click' => 0,
                    );
                }
            }
        }
        unset($matches);
        
        // Parse click counts
        $matches = array();
        preg_match('|name="jump">.+</th></tr><tr><td>(.+)</td>|', $content, $matches);
        $clicks = array();
        $clicks = explode('; ', $matches[1]);
        foreach ($clicks as $row) {
            list($eid, $uid) = explode(':', $row);
            $key = $eid . '-' . $uid;
            if (isset($result[$key])) {
                $result[$key]['click']++;
            } else {
                $result[$key] = array(
                    'eid'   => $eid,
                    'uid'   => $uid,
                    'time'  => $time,
                    'open'  => 0,
                    'click' => 1,
                );
            }
        }
        
        unset($matches);
        unset($opens);
        unset($clicks);
        
        return $result;
    }
	
	
	
}
