<?php
	class CorrectionsController extends AppController{
		var $name = "Corrections";
		var $uses = array("Correction", "Member", "CorrectionType");
		var $components = array('Auth');
		var $helpers = array('Form');
		var $scaffold;
		function add_search(){
			if($this->data){
				$this->Correction->save($this->data);
				$this->redirect('thanks');
			}
			else{
				$this->set('correction_types', $this->CorrectionType->find('list'));
				$this->set('referer', $this->referer());
			}
		}
		function add_result($id = null){
			if($this->data){
				$this->Correction->save($this->data);
				$this->redirect('thanks');
			}
			else{
				$this->set('referer', $this->referer());
				$this->set('correction_types', $this->CorrectionType->find('list'));
				$this->set('member_id', $id);
			}
		}
		function thanks(){
		}
		function beforeFilter(){
			$this->Auth->allow('add_search', 'add_result', 'thanks');
		}
	}
