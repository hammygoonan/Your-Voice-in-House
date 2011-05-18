<?php
	class CorrectionsController extends AppController{
		var $name = "Corrections";
		var $uses = array("Correction", "Member");
		var $scaffold;
		function add_search(){
			if($this->data){
				$this->Correction->save($this->data);
				$this->redirect($this->referer());
			}
			else{
				$this->set('referer', $this->referer());
			}
		}
		function add_result(){
			if($this->data){
				$this->Correction->save($this->data);
				$this->redirect($this->referer());
			}
			else{
				$this->set('referer', $this->referer());
			}
		}
	}
