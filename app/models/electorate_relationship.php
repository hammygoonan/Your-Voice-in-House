<?php
	class ElectorateRelationship extends AppModel {
		var $name = 'ElectorateRelationship';
		var $belongsTo = array('Electorate' => 
			array('foreignKey' => 'upper_id',
				'foreignKey' => 'lower_id')
		);
	}
?>
