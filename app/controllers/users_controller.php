<?php
	class UsersController extends AppController{
		var $name = 'Users';
		var $components = array('Auth');
		var $helpers = array('Html', 'Form', 'Session');
		function login(){
		}
		function logout(){
			$this->redirect($this->Auth->logout());
		}
	}
?>
