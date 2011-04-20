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
						$member['Member']['electorate_id'] = $this->Electorate->return_electorate($line[20], $this->data['Electorate']['state'], $this->data['Electorate']['house']);
						$member['Member']['party_id'] = $this->Party->return_party($line[21]);
						if($this->data['Member']['over_ride'] == 1){
							$this->Member->deleteAll(array('electorate_id' =>$member['Member']['electorate_id'], 'second_name' => $member['Member']['second_name']));
						}
						if($line[22] !== ''){
							$member['Portfolio']['Portfolio'] = explode(',', $line[22]);
						}
						unset($member['Member']['id']);
						$this->Member->create();
						$this->Member->save($member);
						unset($member['Portfolio']['Portfolio']);
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
	/*	function addresses(){
			$members = $this->Member->find('all');
			foreach($members as $member){
				if(!empty($member['Member']['el_address_1'])){
					$address['member_id'] = $member['Member']['id'];
					$address['address_type_id'] = 1;
					$address['postal'] = 0;
					$address['address1'] = $member['Member']['el_address_1'];
					$address['address2'] = $member['Member']['el_address_2'];
					$address['state'] = $member['Member']['el_state'];
					$address['suburb'] = $member['Member']['el_suburb'];
					$address['pcode'] = $member['Member']['el_pcode'];
					$address['phone'] = $member['Member']['el_phone'];
					$address['fax'] = $member['Member']['el_fax'];
					$this->Address->create();
					$this->Address->save($address);
					print('<p>New Address saved for ' . $member['Member']['first_name'] . ' ' . $member['Member']['second_name'] . '</p>');
					unset($address);
				}
				if(!empty($member['Member']['pa_address_1'])){
					$address['member_id'] = $member['Member']['id'];
					$address['address_type_id'] = 1;
					$address['postal'] = 0;
					$address['address1'] = $member['Member']['pa_address_1'];
					$address['address2'] = $member['Member']['pa_address_2'];
					$address['state'] = $member['Member']['pa_state'];
					$address['suburb'] = $member['Member']['pa_suburb'];
					$address['pcode'] = $member['Member']['pa_pcode'];
					$address['phone'] = $member['Member']['pa_phone'];
					$address['fax'] = $member['Member']['pa_fax'];
					$this->Address->create();
					$this->Address->save($address);
					print('<p>New Address saved for ' . $member['Member']['first_name'] . ' ' . $member['Member']['second_name'] . '</p>');
					unset($address);
				}
			}
		} */
	}
?>
