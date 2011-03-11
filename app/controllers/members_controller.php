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
						$this->Member->bindModel(array('hasOne' => array('MembersPortfolio')));
						$this->set('portfolios', $this->Member->find('all', array('conditions' => array('MembersPortfolio.portfolio_id' => 1, 'Electorate.state' => 'Fed'))));
						break;
					case 'pcode':
						$this->set('pcode', $this->Pcode->findByPcode($search_value));
						break;
				}
			}
		}
	}
?>
