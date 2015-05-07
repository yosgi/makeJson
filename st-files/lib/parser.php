<?php if(!defined("BASEPATH")) exit('No direct script access allowed');

class parser  {
		
	protected $template_dir = BASEPATH.'/tpl';
	
	/**
	 *  Parse a template
	 *
	 * Parses pseudo-variables contained in the specified template view,
	 * replacing them with the data in the second param
	 *
	 * @access	public
	 * @param	string
	 * @param	array
	 * @param	bool
	 * @return	string
	 */ 
	public function view($tpl_name, array $tpl_vars, $return = FALSE) {
		
		$tpl_name = rtrim($tpl_name,".php").".php";

		if (!file_exists($this->template_dir. '/' . $tpl_name )) {
			throw new Exception('Unable to load the requested file: ' . $tpl_name);
		}

		extract($tpl_vars);
	
		ob_start();
	
		include($this->template_dir. '/' . $tpl_name ); // include() vs include_once() allows for multiple views with the same name
		
		// Return the file data if requested
		if ($return === TRUE) {
			$buffer = ob_get_contents();
			@ob_end_clean();
			return $buffer;
		}

		ob_end_flush();
	}
	
	
}