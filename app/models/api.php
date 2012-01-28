<?php
	class Api extends AppModel {
		var $name = 'Api';
		var $useTable = 'api';
		var $displayName = 'Api';
		var $validate = array(
			'email' => 'email',
			'url' => 'url'
		);
		
	}
?>