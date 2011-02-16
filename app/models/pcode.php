<?php
	class Pcode extends AppModel {
		var $name = 'Pcode';
		var $hasAndBelongsToMany = array('Electorate');
	}
?>
