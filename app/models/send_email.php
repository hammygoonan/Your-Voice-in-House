<?php
	class SendEmail extends AppModel{
		var $name = 'Send Email';
		var $useTable = false;
		var $_schema = array(
			'to' => array(
				'type' => 'text'
			),
			'from_email' => array(
				'type' => 'string', 
				'length' => 255 
			),
			'from_name' => array(
				'type' => 'string',
				'length' => 255
			),
			'msg' => array(
				'type' => 'text'
			),
			'subject' => array(
				'type' => 'string',
				'length' => 255
			),
		);

		var $validate = array(
			'to' => 'email',
			'from_email' => 'email',
		//	'from_name' => array(
		//		'required' => true
		//	),
			'msg' => array(
				'required' => true
			),
		//	'subject' => array(
		//		'required' => true
		//	)
		);	
	}
