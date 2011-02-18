<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array('Members', 'ElectorateRelationship' => array('foreignKey' => 'upper_id', 'foreignKey' => 'lower_id'));
		var $hasAndBelongsToMany = array('Pcode');
	}
?>
