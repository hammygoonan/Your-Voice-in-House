<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode', 'Party', 'Address');
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
				$j = 0;
				while(!feof($csv)){
					$member_keys = array_keys($this->Member->_schema);
					$line = fgetcsv($csv, 0, ';', '"');
					if($line[1] !== NULL){
						$i = 0;
						foreach($member_keys as $key){
							$member['Member'][$key] = $line[$i];
							$i++;
						}
						
						// see if Electorate exists. Create it if it doesn't, return the id if it does
						
						$member['Member']['electorate_id'] = $this->Electorate->return_electorate($line[6], $this->data['Electorate']['state'], $this->data['Electorate']['house']);
						
						// see if Party exists. Create it if it doesn't, return the id if it does
						
						$member['Member']['party_id'] = $this->Party->return_party($line[7]);
						if($this->data['Member']['over_ride'] == 1){
							$this->Member->deleteAll(array('electorate_id' =>$member['Member']['electorate_id'], 'second_name' => $member['Member']['second_name']));
						}
						
						// add portfolos
						
						if($line[8] !== ''){
							$member['Portfolio']['Portfolio'] = explode(',', $line[8]);
						}
						
						// unset member id so that a new record is created
						unset($member['Member']['id']);
						
						// save
						$this->Member->create();
						$this->Member->save($member);
						
						$id = $this->Member->id;
						// add addresses
						$k = 9;
						while(!empty($line[$k])){
							if($line[$k] != ''){
								$address['Address'] = array(
									'member_id' => $id,
									'address_type_id' => $line[$k++],
									'postal' => $line[$k++],
									'address1' => $line[$k++],
									'address2' => $line[$k++],
									'suburb' => $line[$k++],
									'state' => $line[$k++],
									'pcode' => $line[$k++],
									'phone' => $line[$k++],
									'tollfree' => $line[$k++],
									'fax' => $line[$k++]
								);
								$this->Address->create();
								$this->Address->save($address);
							}
						}
						
						// unset member to avoid duplication
						
						unset($member);
						unset($address);
						$j++;
					}
				}
				$this->Session->setFlash('<p>' . $j . ' lines exicuted');
			}
		}
		function test(){
			$this->set('portfolios', $this->Portfolio->find('list'));
			debug($this->data);
		}
	}
?>
