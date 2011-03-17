<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode');
		var $scaffold;
		var $helpers = array('Form', 'Html');
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
		function upload(){
			if(!empty($this->data)){
				if($this->data['Member']['over_ride'] == 1){
					print('do some shit');
				}
				$file = file($this->data['Member']['submittedfile']['tmp_name']);
				foreach($file as $row){
					$line = explode(';', $row);
					$electorate['name'] = $line[20];
					$electorate['state'] = $this->data['Electorate']['state'];
					$electorate['house'] = $this->data['Electorate']['house'];
					debug($electorate);
				}
			// debug($this->data);
			}
		}
	}
?>
