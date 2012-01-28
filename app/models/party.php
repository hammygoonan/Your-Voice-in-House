<?php
	class Party extends AppModel {
		var $name = 'Party';
		var $hasMany = array('Member');
		var $order = 'name';
		function return_party($abb){ // returns electorate ID - either of a new electorate or the existing one
			if($party = $this->find('first', array('conditions' => array('abbreviation' => $abb)))){
				return $party['Party']['id'];
			}
			else{
				return false;
			}
		}
	}
?>
