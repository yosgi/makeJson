<?php

$argv = $_SERVER['argv'];

if (isset($argv[1]) && !empty($argv[1])){
	$file_path = trim($argv[1]);
	if(!file_exists($file_path)){
		exit(2);
	}
}else{
	exit(1);
}

include './IP.class.php';

$fp = new SplFileObject($file_path,"r");

$uv = 0;
$source = array();

while(!$fp->eof()){    
		    
		$data = $fp->fgets();
		$data = trim($data);
		if(!isset($data[1])){
			continue;
		}
		$uv++;
		$data= explode(" ",$data);
		$ip = trim($data[1]);
		$ip = trim($ip,",");
		$location = IP::find($ip);

		if(is_array($location)){
			$country = $location[0];
			$province = $location[1];
			$city = $location[2];
			$key = (empty($city)?'':$city.'-').(empty($province)?'':$province.'-').(empty($country)?'':$country);
		}else{
			$key = '未知';
		}
		$source[$key] = isset($source[$key])?$source[$key]+1: 1;
}

asort($source);
$source = array_reverse($source);

echo 'UV:'.$uv."\n";
foreach($source as $k=>$v){
	echo $k.':'.$v."\n";
}
exit(0);