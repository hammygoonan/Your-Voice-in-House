<?php
	class ApiController extends AppController {
		var $name = 'Api';
		var $uses = array('Api', 'Member', 'Address', 'Electorate', 'Party', 'House', 'AddressType', 'Portfolio');
		var $helpers = array('Html', 'Form', 'Session');
		var $components = array('Session', 'Email');
		var $scaffold;
		function index(){
			//how to use
		}
		function signup(){
			if(!empty($this->data)){
				$this->data['Api']['version'] = 1.0;
				$this->data['Api']['key'] = $this->genRandomString(20);
				$this->data['Api']['valid'] = 1;
				if($this->Api->save($this->data)){ // validate
					$this->Session->setFlash('Your key has been emailed to you');
				}
				else{
					$this->Session->setFlash('Sorry, something has gone arye. Your key was not generate. Please try again', 'default', array('class' => 'error'));
				}
				//send email
			}
		}
		function query(){
			if( !isset($this->params['named']['key']) || !isset($this->params['named']['version']) ){ // check that the key and format are set, if false, return an error
				$this->layout = 'ajax';
				$this->set('error', 'Error: some required fields are missing');
			}
			elseif( !isset($this->params['named']['member']) && !isset($this->params['named']['electorate']) && !isset($this->params['named']['house']) && !isset($this->params['named']['portfolio']) ){
				$this->layout = 'ajax';
				$this->set('error', 'Error: some required fields are missing');
			}
/*			elseif( !is_numeric(@$this->params['named']['member']) && !is_numeric(@$this->params['named']['electorate']) && !is_numeric(@$this->params['named']['house']) && !is_numeric(@$this->params['named']['portfolio']) ){
				$this->layout = 'ajax';
				$this->set('error', 'Error: some required fields are incorrect');
			} */
			else{ // if key are format are set
				$api = $this->Api->find('first', array('conditions' => array('Api.key' => $this->params['named']['key'])));
				if( !isset($api['Api']['valid']) ){ // check to see that API key is in the database and valid
					$this->layout = 'ajax';
					$this->set('error', 'Error: Invalid key');
				}
				else{
					$address = $this->neat_address_types();
					$house_type = $this->neat_houses();
					foreach($this->params['named'] as $param => $value){ // get results
						switch($param){
							case 'member':
								$member_ids = split(',', $value);
								$members = $this->Member->find('all', array('conditions' => array('Member.id' => $member_ids)));
								$member_results = array();
								foreach($members as $member){
									$member_results[] = $this->generateApiArray($member, $house_type, $address);
								}
								break;
							case 'electorate':
								$electorate_id = split(',', $value);
								$electorates = $this->Member->find('all', array('conditions' => array('Member.electorate_id' => $electorate_id)));
								$electorate_results = array();
								foreach($electorates as $electorate){
									$electorate_results[] = $this->generateApiArray($electorate, $house_type, $address);
								}
								break;
							case 'house':
								$houses = $this->Member->find('all', array('conditions' => array('Electorate.house_id' => $value)));
								$house_results = array();
								foreach($houses as $house){
									$house_results[] = $this->generateApiArray($house, $house_type, $address);
								}
								break;
							case 'portfolio':
								$this->Member->bindModel(array('hasOne' => array('MembersPortfolio')));
								$portfolios = $this->Member->find('all', array('conditions' => array('MembersPortfolio.portfolio_id' => $this->params['named']['portfolio']), 'fields' => 'DISTINCT *'));
								foreach($portfolios as $portfolio){
									$this->Party->recursive = 0;
									$this->Electorate->recursive = 0;
									$party = $this->Party->findById($portfolio['Member']['party_id']);
									$electorate = $this->Electorate->findById($portfolio['Member']['electorate_id']);
									$portfolio['Party'] = $party['Party'];
									$portfolio['Electorate'] = $electorate['Electorate'];
									$portfolio_results[] = $this->generateApiArray($portfolio, $house_type, $address);
								}
								break;
						}
					}
					if(isset($member)) $results['Member'] = $member_results;
					if(isset($electorate_results)) $results['Electorate'] = $electorate_results;
					if(isset($house_results)) $results['House'] = $house_results;
					if(isset($portfolio_results)) $results['Portfolio'] = $portfolio_results;
					if(isset($results)){
						$this->set('results', $results);
					}
					else{
						$this->set('error', 'Error: no results');
					}
				}
			}
			switch(@$this->params['named']['format']){
				case 'xml':
					$this->layout = 'xml';
					$this->set('format', 'xml');
					break;
				case 'json':
					$this->layout = 'json';
					$this->set('format', 'json');
					break;
				default:
					$this->layout = 'json';
					$this->set('format', 'json');
					break;
			}
		}
		function member_ids(){
			$members = $this->Member->find('all');
			$houses = $this->neat_houses();
			foreach($members as $member){
				$results[strtoupper(substr($member['Member']['second_name'], 0, 1))][] = array(
					'id' => $member['Member']['id'],
					'first_name' => $member['Member']['first_name'],
					'second_name' => $member['Member']['second_name'],
					'electorate' => $member['Electorate']['name'],
					'state' => $houses[ $member['Electorate']['house_id'] ]['state']
				);
			}
			$this->set('results', $results);
		}
		function house_ids(){
			$houses = $this->House->find('all');
			foreach($houses as $house){
				$results[$house['House']['state']][] = array('name' => $house['House']['name'], 'id' => $house['House']['id']);
			}
			$this->set('results', $results);
		}
		function electorate_ids(){
			$electorates = $this->Electorate->find('all');
			foreach($electorates as $electorate){
				$results[strtoupper(substr($electorate['Electorate']['name'], 0, 1))][] = array(
					'id' => $electorate['Electorate']['id'],
					'name' => $electorate['Electorate']['name'],
					'house' => $electorate['House']['name'],
					'state' => $electorate['House']['state']
				);
			}
			ksort($results);
			$this->set('results', $results);
		}
		function portfolio_ids(){
			$portfolios = $this->Portfolio->find('all');
			$this->set('portfolios', $portfolios);
		}
		function generator(){
		}
		function generateApiArray($member, $houses, $addresses){
			unset($member['Correction']);
			unset($member['Member']['electorate_id']);
			unset($member['Member']['party_id']);
			$member['Member']['Party'] = $member['Party'];
			
			#electorates - including adding house details
			$member['Member']['Electorate'] = $member['Electorate'];
			$member['Member']['Electorate']['House'] = $houses[$member['Member']['Electorate']['house_id']];
			$member['Member']['Electorate']['House']['id'] = $member['Member']['Electorate']['house_id'];
			unset($member['Member']['Electorate']['house_id']);
			
			#addresses - including adding address type
			$member['Member']['Address'] = $member['Address'];
			for($i = 0; sizeof($member['Member']['Address']) > $i; $i++){
				$member['Member']['Address'][$i]['type'] = $addresses[$member['Member']['Address'][$i]['address_type_id']]['name'];
				unset($member['Member']['Address'][$i]['address_type_id']);
				unset($member['Member']['Address'][$i]['member_id']);
			}

			$member['Member']['Portfolio'] = $member['Portfolio'];
			unset($member['Party']);
			unset($member['Electorate']);
			unset($member['Address']);
			unset($member['Portfolio']);
			for($i = 0; sizeof($member['Member']['Portfolio']) > $i; $i++){
				unset($member['Member']['Portfolio'][$i]['MembersPortfolio']);
			}
			return $member['Member'];
		}
		function neat_houses(){
			$houses = $this->House->find('all');
			$neat_houses = array();
			foreach($houses as $house){
				$neat_houses[$house['House']['id']] = array('name' => $house['House']['name'], 'state' => $house['House']['state'], 'upperlower' => $house['House']['upperlower']);
			}
			return $neat_houses;
		}
		function neat_address_types(){
			$address_types = $this->AddressType->find('all');
			$neat_address_types = array();
			foreach($address_types as $address_type){
				$neat_address_types[$address_type['AddressType']['id']] = array('name' => $address_type['AddressType']['name']);
			}
			return $neat_address_types;
		}
		function genRandomString($length) {
			$characters = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ';
			$string = '';
			for ($p = 0; $p < $length; $p++) {
				$string .= $characters[mt_rand(0, strlen($characters) - 1)];
			}
			return $string;
		}
	}
?>