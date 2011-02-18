<?php
	class Party extends AppModel {
		var $name = 'Party';
		var $hasMany = array('Member');
		var $order = 'name';
	}
?>
