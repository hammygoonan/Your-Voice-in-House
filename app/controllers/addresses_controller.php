<?php
	class AddressesController extends AppController {
		var $name = 'Addresses';
		var $helpers = array('Form', 'Html', 'Session', 'Js');
		var $components = array('Auth');
		var $uses = array('Address', 'AddressType');
	//	var $scaffold;
		function edit($id = null){
			if(!empty($this->data)){
				$this->Address->save($this->data);
				$this->set('address', $this->Address->findById($this->data['Address']['id']));
			}
			else{
				$this->set('address', $this->Address->findById($this->params['named']['address_id']));
			}
			$this->set('address_types', $this->AddressType->find('list'));
		}
		function add(){
			if($this->data){
				$this->Address->save($this->data);
				$this->set('member', $this->data['Address']['member_id']);
			}
			else{
				$this->set('member', $this->params['named']['member_id']);
			}
			$this->set('address_types', $this->AddressType->find('list'));
		}
	}
?>
