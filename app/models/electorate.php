<?php
	class Electorate extends AppModel {
		var $name = 'Electorate';
		var $hasMany = array('Members');
		var $hasAndBelongsToMany = array('Pcode');
		var $belongsTo = array('House' => array(
				'className' => 'House',
				'foreignKey' => 'house_id'
			));
		function return_electorate($name, $house){ // returns electorate ID - either of a new electorate or the existing one
			$electorate['Electorate']['name'] = $name;
			$electorate['Electorate']['house_id'] = $house;
			if($electorate_exists = $this->find('first', array('conditions' => array('Electorate.name' => $electorate['Electorate']['name'], 'Electorate.house_id' => $electorate['Electorate']['house_id'])))){
				return $electorate_exists['Electorate']['id'];
			}
			else{
				$this->create();
				$this->set(array('name' => $name, 'house_id' => $house));
				$this->save();
				return $this->id;
			}
		}
	}
?>
