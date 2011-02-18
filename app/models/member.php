<?php
	class Member extends AppModel {
		var $name = 'Member';
		var $hasAndBelongsToMany = array('Portfolio');
		var $belongsTo = 'Electorate';
	}
?>
