<?php
	class ElectorateRelationship extends AppModel {
		var $name = 'ElectorateRelationship';
		var $belongsTo = array(
			'UpperHouse' => 
				array(
					'className' => 'Electorate',
					'foreignKey' => 'upper_id'),
			'LowerHouse' => 
				array(
					'className' => 'Electorate',
					'foreignKey' => 'lower_id')
		);
	}
?>
