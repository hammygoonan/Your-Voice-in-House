<?php
	class UsersController extends AppController{
		var $name = 'Users';
		var $uses = array('Member', 'Electorate', 'House', 'Portfolio', 'Pcode', 'Party', 'Address');
		var $components = array('Auth');
		var $helpers = array('Html', 'Form', 'Session');
		function index(){
		
		}
		function login(){
		}
		function logout(){
			$this->redirect($this->Auth->logout());
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
						$this->Member->save($member, array('validate' => false));
						$id = $this->Member->id;
						// add addresses
						$k = 9;
						while(is_string($line[$k])){
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
									'phone' => @$line[$k++],
									'tollfree' => @$line[$k++],
									'fax' => @$line[$k++]
								);
								$this->Address->create();
								$this->Address->save($address);
							}
							else{
								$k = $k + 10;
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
		function export(){
			// do export
			$this->redirect($this->referer());
		}
		function mass_action(){
			if($this->data['users']['House']){ // search results
				$this->set('members', $this->Member->find('all', array('conditions' => array('Electorate.house_id' => $this->data['users']['House']))));
			}
			else{
				$houses = $this->House->find('all');
				foreach($houses as $house){
					$house_array[$house['House']['id']] = $house['House']['name'] . ' (' . $house['House']['state'] . ')';
				}
				$this->set('houses', $house_array);
			}
		}
		function mass_delete(){
			foreach($this->data['users'] as $id){
				if($id === 1){
					$this->Member->delete($id);
				}
			}
			$this->redirect($this->referer());
		}
	}
?>
