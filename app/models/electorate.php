<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array('Members');
		var $hasAndBelongsToMany = array('Pcode');
	}
?>
