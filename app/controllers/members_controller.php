<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode', 'Party');
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
				$csv = fopen($this->data['Member']['submittedfile']['tmp_name'], 'r');
				$j = 1;
				while(!feof($csv)){
					$member_keys = array_keys($this->Member->_schema);
					$line = fgetcsv($csv, 0, ';', '"');
					if($line[1] !== NULL){
						$i = 0;
						foreach($member_keys as $key){
							$member['Member'][$key] = $line[$i];
							$i++;
						}
						$member['Member']['electorate_id'] = $this->Electorate->return_electorate($line[20], $this->data['Electorate']['state'], $this->data['Electorate']['house']);
						$member['Member']['party_id'] = $this->Party->return_party($line[21]);
						if($this->data['Member']['over_ride'] == 1){
							$this->Member->deleteAll(array('electorate_id' =>$member['Member']['electorate_id'], 'second_name' => $member['Member']['second_name']));
						}
						$this->Member->save($member);
						$j++;
					}
				}
				$this->Session->setFlash('<p>' . $j . ' lines exicuted');
			}
		}
	}
?>
