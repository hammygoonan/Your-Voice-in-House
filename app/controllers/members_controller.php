<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode', 'Party', 'Address');
		var $scaffold;
		var $helpers = array('Form', 'Html');
		function search(){
			$this->set('portfolios', $this->Portfolio->find('list'));
		}
		function results(){
			$portfolios = array();
			foreach($this->params['url'] as $search_param => $search_value){
				switch($search_param){
					case 'Member':
						if((int)$search_value){
							$this->set('members', $this->Member->findById($search_value));
						}
						else{
							$this->set('members', $this->Member->findBySecondName($search_value));
						}
						break;
					case 'Electorate':
						if((int)$search_value){
							$this->set('electorate', $this->Electorate->findById($search_value));
						}
						else{
							$this->set('electorate', $this->Electorate->find('first', array('conditions' => array('name' => $this->params['url']['Electorate'], 'state' => $this->params['url']['State']))));
						}
						break;
					case 'Portfolio': // need to make it work for multipule portfolios
						$this->Member->bindModel(array('hasOne' => array('MembersPortfolio')));
						$portfolios = $this->Member->find('all', array('conditions' => array('MembersPortfolio.portfolio_id' => $this->params['url']['Portfolio'], 'Electorate.state' => $this->params['url']['State'])));
						$this->set('portfolios', $portfolios);
						break;
				}
			}
		}
		function email(){
		//	$recipients = array();
			foreach($this->data['Member'] as $id => $on){
				if($on == 1){
					$recipients[] = $this->Member->findById($id);
				}
			}
			$to_field = '';
			for($i = 0; $i < sizeof($recipients); $i++){
				$to_field .= $recipients[$i]['Member']['first_name'] . ' ' . $recipients[$i]['Member']['second_name'] . ' <' . $recipients[$i]['Member']['email'] . '>';
				if($i < sizeof($recipients) - 1){
					$to_field .= ", ";
				}
			}
			$this->set('to_field', $to_field);
		}
		function email_send(){
			debug($this->data);
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
					//	var_dump(is_string($line[$k]));
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
									'phone' => $line[$k++],
									'tollfree' => $line[$k++],
									'fax' => $line[$k++]
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
		function test(){
			$this->set('portfolios', $this->Portfolio->find('list'));
			debug($this->data);
		}
	}
?>
