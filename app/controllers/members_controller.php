<?php
	class MembersController extends AppController{
		var $name = 'Members';
		var $uses = array('Member', 'Electorate', 'Portfolio', 'Pcode', 'Party', 'Address', 'Correction');
		var $scaffold;
		var $helpers = array('Form', 'Html', 'Session', 'RecaptchaPlugin.Recaptcha');
		var $components = array('Email', 'RecaptchaPlugin.Recaptcha');
		function search(){
			$this->set('portfolios', $this->Portfolio->find('list'));
		}
		function results(){
			$portfolios = array();
			foreach($this->params['url'] as $search_param => $search_value){
				switch($search_param){
					case 'Member':
						if((int)$search_value){
							$this->set('members', $this->Member->findAllById($search_value));
						}
						else{
							$this->set('members', $this->Member->find('all', array('conditions' => array('Member.second_name' => $this->params['url']['Member'], 'Electorate.state' => $this->params['url']['State']))));
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
			// in case we need to make a correction, we need to know what the search was:
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
						$to_field .= $to_members[$i]['Member']['first_name'] . ' ' . $to_members[$i]['Member']['second_name'] . ' <' . $to_members[$i]['Member']['email'] . '>';
						if($i < sizeof($to_members) - 1){
							$to_field .= ", ";
						}
					}
				}
				if(!empty($cc_members)){
					for($i = 0; $i < sizeof($cc_members); $i++){
						$cc_field .= $cc_members[$i]['Member']['first_name'] . ' ' . $cc_members[$i]['Member']['second_name'] . ' <' . $cc_members[$i]['Member']['email'] . '>';
						if($i < sizeof($cc_members) - 1){
							$cc_field .= ", ";
						}
					}
				}
				if(!empty($bcc_members)){
					for($i = 0; $i < sizeof($bcc_members); $i++){
						$bcc_field .= $bcc_members[$i]['Member']['first_name'] . ' ' . $bcc_members[$i]['Member']['second_name'] . ' <' . $bcc_members[$i]['Member']['email'] . '>';
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
				){
					$this->Session->setFlash('Either your email address is incorrect or you are missing some manditory fields');
				}
				elseif($this->Member->validates(array('fieldList' => array('recaptcha_response_field')))){ // if recapture is right, then sent the email
					$this->_smtp_send($this->data);
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
