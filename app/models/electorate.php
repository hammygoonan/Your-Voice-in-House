<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array(
			'Members',
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
		var $order = 'name';
		function return_electorate($name, $state, $house){ // returns electorate ID - either of a new electorate or the existing one
			$electorate['Electorate']['name'] = $name;
			$electorate['Electorate']['state'] = $state;
			$electorate['Electorate']['house'] = $house;
			if($electorate_exists = $this->find('first', array('conditions' => array('name' => $electorate['Electorate']['name'], 'state' => $electorate['Electorate']['state'])))){
				return $electorate_exists['Electorate']['id'];
			}
			else{
				$this->create();
				$this->set(array('name' => $name, 'house' => $house, 'state' => $state));
				$this->save();
				return $this->id;
			}
		}
	}
?>
