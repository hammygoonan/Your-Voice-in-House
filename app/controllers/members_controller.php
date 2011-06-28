<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode', 'Party', 'Address', 'Correction');
	//	var $scaffold;
		var $helpers = array('Form', 'Html', 'Session', 'RecaptchaPlugin.Recaptcha', 'Js');
		var $components = array('Email', 'RecaptchaPlugin.Recaptcha');
		function search(){
			$this->set('portfolios', $this->Portfolio->find('list'));
		}
		function results(){
			$this->Member->recursive = 2; // to enable access to the Address Type data
			foreach($this->params['url'] as $search_param => $search_value){
				switch($search_param){
					case 'Member':
						if( !empty($this->params['url']['id']) ){
							$member_ids = explode(',', $this->params['url']['id']);
							foreach($member_ids as $member_id){
								$members[] = $this->Member->findById($member_id);
							}
							$this->set('members', $members);
						}
						elseif( !empty($this->params['url']['Member']) && empty($this->params['url']['id']) ){ // don't search if the Member.id hidden field is set. This search is only done if Javascript is turned off.
							$search_terms = explode(',', $this->params['url']['Member']);
							$member_array = array();
							foreach($search_terms as $last_name){
								$last_name = trim($last_name);
								$member_array = $this->Member->find('all', array('conditions' => array('Member.second_name' => $last_name, 'Electorate.state' => $this->params['url']['State'])));
								foreach($member_array as $ind_arrary){
									$results[] = $ind_arrary;
								}
							}
							$this->set('members', @$results);
						}
						break;
					case 'Electorate':
						if(!empty($this->params['url']['electorate_id'])){
							$this->set('electorate', $this->Member->find('all', array('conditions' => array('Electorate.id' => $this->params['url']['electorate_id']))));
						}
						else{
							$this->set('electorate', $this->Member->find('all', array('conditions' => array('Electorate.name' => $this->params['url']['Electorate'], 'Electorate.state' => $this->params['url']['State']))));
						}
						break;
					case 'Portfolio':
						$portfolios = array(); // to allow for multiple portfolios to be searched
						$this->Member->bindModel(array('hasOne' => array('MembersPortfolio')));
						$portfolios = $this->Member->find('all', array('conditions' => array('MembersPortfolio.portfolio_id' => $this->params['url']['Portfolio'], 'Electorate.state' => $this->params['url']['State']), 'fields' => 'DISTINCT *'));
						$this->set('portfolios', $portfolios);
						break;
				}
			}
			// log search
			
			$portfolio_list = '';
			foreach($this->params['url']['Portfolio'] as $portfolio){
				$portfolio_list .= $portfolio . ', ';
			}
			CakeLog::write('search', "Member: " . $this->params['url']['Member'] . "\tMemer id: " . $this->params['url']['id'] . "\tElectorate: " . $this->params['url']['Electorate'] . "\tElectorate Id: " . $this->params['url']['electorate_id'] . "\tPortfolio: " . $portfolio_list . "\tState: " . $this->params['url']['State']);
			// CakeLog::write('results', '');
		}
		function email(){
			if(preg_match('/members\/results/', $this->referer())){
				foreach($this->data['Member'] as $id => $on){
					switch($on){
						case 'to':
							$to_members[] = $this->Member->findById($id);
							break;
						case 'cc':
							$cc_members[] = $this->Member->findById($id);
							break;
						case 'bcc':
							$bcc_members[] = $this->Member->findById($id);
							break;
					}
				}
				$to_field = '';
				$cc_field = '';
				$bcc_field = '';
				if(!empty($to_members)){
					for($i = 0; $i < sizeof($to_members); $i++){
						$to_field .= $to_members[$i]['Member']['email'];
						if($i < sizeof($to_members) - 1){
							$to_field .= ", ";
						}
					}
				}
				if(!empty($cc_members)){
					for($i = 0; $i < sizeof($cc_members); $i++){
						$cc_field .= $cc_members[$i]['Member']['email'];
						if($i < sizeof($cc_members) - 1){
							$cc_field .= ", ";
						}
					}
				}
				if(!empty($bcc_members)){
					for($i = 0; $i < sizeof($bcc_members); $i++){
						$bcc_field .= $bcc_members[$i]['Member']['email'];
						if($i < sizeof($bcc_members) - 1){
							$bcc_field .= ", ";
						}
					}
				}
				$this->set('to_field', $to_field);
				$this->set('cc_field', $cc_field);
				$this->set('bcc_field', $bcc_field);
			}
			else{
				
				$this->Member->set($this->data); // this is just for the reCAPACTHA plugin
				if(!eregi("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", $this->data['Member']['from_email'])
					|| empty($this->data['Member']['from_name'])
					|| empty($this->data['Member']['from_email'])
					|| empty($this->data['Member']['subject'])
					|| empty($this->data['Member']['msg'])
					|| $this->data['Member']['terms'] == 0
				){;
					$this->Session->setFlash('Either your email address is incorrect or you are missing some manditory fields');
				}
				elseif($this->Member->validates(array('fieldList' => array('recaptcha_response_field')))){ // if recapture is right, then sent the email
					$this->_smtp_send($this->data);
					CakeLog::write('sent_emails', "IP: " . $_SERVER['REMOTE_ADDR'] . "\tTo: " . $this->data['Member']['to'] . "\tCc: " . $this->data['Member']['cc'] . "\tBcc: " . $this->data['Member']['bcc'] . "\tSubject: " . $this->data['Member']['subject']);
					$this->redirect(array('action' => 'send_email'));
				}
			}		
		}
		function send_email(){
		}
		function _smtp_send($data){
			$this->Email->from    = $data['Member']['from_name'] . ' <no-reply@yourvoiceinhouse.org.au>';
		//	$this->Email->to      = $data['Member']['to'];
		//	$this->Email->cc      = $data['Member']['cc'];
		//	$this->Email->bcc      = $data['Member']['bcc'];
			$this->Email->to      = 'hammy@goonanism.com';
			$this->Email->replyTo    = $data['Member']['from_name'] . ' <' . $data['Member']['from_email'] . '>';
			$this->Email->subject = $data['Member']['subject'];
			$this->Email->sendAs = 'both';
			
				/* SMTP Options 
				
			$this->Email->smtpOptions = array(
				'port'=>'25',
				'timeout'=>'30',
				'host' => 'mail.yourvoiceinhouse.org.au',
				'username'=>'your_smtp_username',
				'password'=>'your_smtp_password',
				'client' => 'smtp_helo_hostname'
			);
			$this->Email->delivery = 'smtp';
			*/
			$this->Email->send($data['Member']['msg']);
		}
		function terms(){
			$this->layout = 'ajax';
		}
		function ajax_autocomplete($id = null){
			$this->layout = 'json';
			$this->set('members', $this->Member->find('all', array('conditions' => array(
				'OR' => array(
					'Member.second_name LIKE' => '%' . $id . '%',
					'Electorate.name LIKE' => '%' . $id . '%'
				)
			))));
		}
		function electorate_autocomplete($id = null){
			$this->layout = 'json';
			$this->set('electorates', $this->Electorate->find('all', array('conditions' => array(
				'OR' => array(
					'Electorate.name LIKE' => '%' . $id . '%',
					'Electorate.house LIKE' => '%' . $id . '%',
				)
			), 'fields' => 'DISTINCT *')));
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
		function find(){
			$this->set('house', $this->Electorate->find('all', array('fields' => 'DISTINCT house')));
		}
		function find_results(){
			if(!empty($this->data['Electorate']['house'])){
				$this->set('house', $this->Electorate->find('all', array(
					'conditions' => array(
						'house' => $this->data['Electorate']['house'],
						'state' => $this->data['Electorate']['state']
					)
				)));
				$this->set('search', $this->data['Electorate']['house'] . ' (' . $this->data['Electorate']['state'] .')');
			}
			elseif(!empty($this->data['Member']['id'])){
				$this->redirect(array('controller' => 'members', 'action' => 'edit', 'id' => $this->data['Member']['id']));
			}
			elseif(!empty($this->data['Member']['electorate_id'])){
				$this->set('electorates', $this->Member->findAllByElectorateId($this->data['Member']['electorate_id']));
			}
		}
		function edit($id = null){
			$this->set('member', $this->Member->findById($this->params['named']['id']));
			$this->set('parties', $this->Party->find('list'));
			$this->set('portfolios', $this->Portfolio->find('list'));
		}
	}
?>
