<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class stdoc {

	private $_db_home;

	private $_db_media;

	private $_categories = null;

	public function __construct($db1,$db2){
		$this->_db_home = $db1;
		$this->_db_media = $db2;
	}

	public function get_categories(){
		if (empty($this->_categories)){
			$this->_categories = $this->_get_categories();
		}
		return $this->_categories;
	}


	private function _get_categories(){
		$sql = " select * from eef_document_category order by `left` asc";

		$res = $this->_db_home->query($sql);

		$rowset = array();
		while($row = $this->_db_home->fetch_row($res)){
			$rowset[] = $row;
		}

		$root = null;
		$result = array();

		foreach ($rowset as $row) {
            // Initialize a tree or start a new tree when last tree finishes
            if (is_null($root) || $row['left'] > $root['right']) {
                if (!empty($ret)) {
                    $result += $ret;
                }
                unset($ret);
                $root = $row;
                $root_id = $root['id'];
                $item = $row;
                $ret[$root_id] = $item;
                $stack = array();
                continue;
            }

            $parent =& $ret[$root_id];
            if (!empty($stack)) {
                // remove nodes with right smaller than current node,
                // which means not ancestors anymore
                $count = count($stack);
                while ($count && $stack[$count - 1]['right'] < $row['right']) {
                    array_pop($stack);
                    $count = count($stack);
                }
                if (($count_stack = count($stack)) > 0) {
                    for($i = 0; $i < $count_stack; $i ++) {
                        $parent =& $parent['child'][$stack[$i]['id']];
                    }
                }
            }

            // add this node to the stack for next node
            $stack[] = array('id' => $row['id'], 'right' => $row['right']);

            //continue;
            // store the node
            $item = $row;
            $parent['child'][$row['id']]= $item;
            
        }

        if (!empty($ret)) {
            $result += $ret;
        }

        return $result[1]['child'];
	}

	private function _get_mime_icon($mimetype){
		$type = '';
		switch ($mimetype) {
			case 'application/pdf':
				$type = 'pdf.gif';
				break;
			case 'application/zip':
				$type = 'zip.gif';
				break;
			case 'text/html':
				$type = 'html.gif';
				break;
			case 'application/msword':
				$type = 'html.gif';
				break;
			case 'application/octet-stream':
				$type = 'other.gif';
				break;
			case 'application/x-rar':				
			case 'application/x-rar-compressed':
				$type = 'rar.gif';
				break;
			case 'text/plain':
				$type = 'txt.gif';
				break;
			case 'image/jpeg':
				$type = 'jpeg.gif';
				break;
			case 'application/x-shockwave-flash':
				$type = 'swf.gif';
				break;
			case 'image/png':
				$type = 'png.gif';
				break;
			default:
				$type = 'other.gif';
				break;
		}
		return $type;
	}

	public function get_category_doc($cid){
		$sql = "select * from eef_document_detail where category = $cid and active = 1 order by title ASC";

		$res = $this->_db_home->query($sql);

		$result = array();

		while ($row = $this->_db_home->fetch_row($res)){
			$files  = $this->_get_docs($row['id']);
			$version = '';
			$row['file_en'] = $row['file_attachment'] = $row['file_cn'] = array();
			$row['version'] = $row['att_version']  ='';
			foreach ($files as $k=>$v){

				$v['ico'] = $this->_get_mime_icon($v['mimetype']);

				if ($v['language'] == 'en'){
					$row['file_en'][] = $v;
					if (!empty($v['version'] && empty($row['version']))){
                		$row['version'] = $v['version'];
                	}
                }else if ($v['language'] == 'zh'){
					$row['file_cn'][] = $v;
					if (!empty($v['version'] && empty($row['version']))){
                		$row['version'] = $v['version'];
                	}
                }else{
					$row['file_attachment'][] = $v;
					if (!empty($v['version'] && empty($row['att_version']))){
                		$row['att_version'] = $v['version'];
                	}
                }
			}
			$result[] = $row;
		}

		return $result;
	}

	private function _get_media($mid){
		$data = $this->_db_media->query_first("select * from eef_media_doc where id = {$mid}");

		$result = array();
		$result['filename'] = $data['filename'];
		$result['path'] = $data['path'];
		$result['title'] = $data['title'];
		if (empty($result['path'])){
			$result['url'] = $data['url'];
		}else{
			$result['url'] = '';
		}
		
		return $result;
	}

	private function _get_docs($doc_id){
		$sql = " select * from eef_document_doc where document = {$doc_id} and active = 1";

		$res = $this->_db_home->query($sql);

		$result = array();
		while($row = $this->_db_home->fetch_row($res)){
			$data = array(
				"id"=>$row['id'],
				"subject"=>$row['subject'],
				"language" =>$row['language'],
				"version" => $row['version'],
				"mimetype"=>$row['mimetype']
			);

			if (!empty($row['link'])){
				$data['link'] = $row['link'];
				$data['title'] = $data['subject'];
				$result[] = $data;
			}else{
				$media = $this->_get_media($row['media']);
				$result[] = array_merge($media,$data);
			}
		}

		return $result;
	}
}