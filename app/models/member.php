<?php
	class Member extends AppModel {
		var $name = 'Member';
		var $belongsTo = 'Electorate';
		var $hasAndBelongsToMany = array('Portfolio');
	}
?>
