<?php

 function get_dir_dirs($dir_path,$only_name = true,$needchangecode = false){
 	$dir_path = rtrim($dir_path,'\/');
 	
 	if (!is_dir($dir_path)){
 		return FALSE;
 	}
 	
 	$t_dir = opendir($dir_path);
 	
 	$result = array();
 	
 	while (($file = readdir($t_dir)) !== false){
 		if ($needchangecode){
 			$file = iconv("GBK", "UTF-8", $file);
 		}
 		if ($file != '.' && $file != '..'){
 			if (is_dir($dir_path.'/'.$file)){
 				if ($only_name){
 					$result[] = $file;
 				}else{
 					$result[] = $dir_path.'/'.$file;
 				}
 			}
 		}
 	}
 	closedir($t_dir);
 	
 	return $result;
 }


 function get_dir_files($dir_path,$only_name = true, $needchangecode = false){
 	
 	$dir_path = rtrim($dir_path,'\/');
 	
 	if (!is_dir($dir_path)){
 		return FALSE;
 	}
 	
	$t_dir = opendir($dir_path);

	$result = array();

	while (($file = readdir($t_dir)) !== false){
		if ($needchangecode){
 			$file = iconv("GBK", "UTF-8", $file);
 		}

		if ($file != '.' && $file != '..'){
			 if (!is_dir($dir_path.'/'.$file)){
			 	 if ($only_name){
			 	 	$result[] = $file;
			 	 }else{
			 	 	$result[] = $dir_path.'/'.$file;
			 	 }
			 }
		}
	}
	closedir($t_dir);
	
	return $result;
}

function curl_post($url, $post = NULL, array $options = array())
{
	if (is_string($post)){
		parse_str($post,$apost);
		foreach($apost as $k=>$v){
			$apost[$k] = stripslashes($v);
		}

	}else{
		$apost = $post;
	}

	$defaults = array(
			CURLOPT_POST => 1,
			CURLOPT_HEADER => 0,
			CURLOPT_URL => $url,
			CURLOPT_FRESH_CONNECT => 1,
			CURLOPT_RETURNTRANSFER => 1,
			CURLOPT_FORBID_REUSE => 1,
			CURLOPT_TIMEOUT => 20,
			CURLOPT_POSTFIELDS => $apost
	);

	$ch = curl_init();
	curl_setopt_array($ch, ($options + $defaults));
	if( ! $result = curl_exec($ch))
	{
		trigger_error(curl_error($ch));
	}
	curl_close($ch);
	return $result;
}

/**
 * Send a GET requst using cURL
 * @param string $url to request
 * @param array $get values to send
 * @param array $options for cURL
 * @return string
 */
function curl_get($url, $get = NULL, array $options = array())
{
	if (is_string($get)){
		parse_str($get,$aget);
		foreach($aget as $k=>$v){
			$aget[$k] = stripslashes($v);
		}

	}else{
		$aget = $get;
	}



	$defaults = array(
			CURLOPT_URL => $url. (strpos($url, '?') === FALSE ? '?' : ''). http_build_query($aget),
			CURLOPT_HEADER => 0,
			CURLOPT_RETURNTRANSFER => TRUE,
			CURLOPT_TIMEOUT => 10
	);

	$ch = curl_init();
	curl_setopt_array($ch, ($options + $defaults));
	if( ! $result = curl_exec($ch))
	{
		echo curl_errno($ch);
	}
	curl_close($ch);
	return $result;
}