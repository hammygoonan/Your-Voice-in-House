<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array(
			'Upper' => array(
				'className' => 'ElectorateRelationship',
				'foreignKey' => 'upper_id'
			),
			'Lower' => array(
				'className' => 'ElectorateRelationship',
				'foreignKey' => 'lower_id'
			)
		);
		var $hasAndBelongsToMany = array('Pcode');
		var $hasOne = 'Members';
		var $order = 'name';
	}
?>
