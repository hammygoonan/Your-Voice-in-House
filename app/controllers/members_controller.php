<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode');
		var $scaffold;
		function search(){
		}
		function results(){
			foreach($this->params['named'] as $search_param => $search_value){
				switch($search_param){
					case 'member':
						$this->set('members', $this->Member->findById($search_value));
						break;
					case 'electorate':
						$this->set('electorate', $this->Electorate->findById($search_value));
						break;
					case 'portfolio':
						$this->set('portfolios', $this->Member->Portfolio->find('all', array('conditions' => array('Portfolio.id' => 1))));
						break;
					case 'pcode':
						$this->set('pcode', $this->Pcode->findByPcode($search_value));
						break;
				}
			}
		}
	}
?>
