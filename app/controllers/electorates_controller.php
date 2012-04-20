<?php
	class ElectoratesController extends AppController{
		var $helpers = array('Js');
		var $name = 'Electorates';
		function ajax_autocomplete($id = null){
			$this->layout = 'json';
			$this->set('electorates', $this->Electorate->find('all'));
		}
	}
?>
