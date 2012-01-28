<?php
	class Member extends AppModel {
		var $name = 'Member';
		var $hasAndBelongsToMany = array('Portfolio');
		var $hasMany = array('Address', 'Correction');
		var $belongsTo = array('Electorate', 'Party');
		var $order = 'second_name';
		var $displayField = 'id';
	}
?>
