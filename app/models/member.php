<?php
	class Member extends AppModel {
		var $name = 'Member';
		var $hasAndBelongsToMany = array('Portfolio');
		var $belongsTo = array('Electorate', 'Party');
		var $order = 'second_name';
	}
?>
