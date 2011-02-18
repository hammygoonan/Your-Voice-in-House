<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array('Members');
		var $hasAndBelongsToMany = array('Pcode',
			'Electorate' => 
				array(
					'className' => 'Electorate',
					'joinTable' => 'lower_upper',
					'foreignKey' => 'lower_id',
					'associationForeignKey'  => 'upper_id'
				)
			);
	}
?>
