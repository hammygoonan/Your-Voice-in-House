<?php
	class SendEmailsController extends AppController {
		var $name = 'SendEmails';
		var $components = array('Email');
		var $uses = false;
		function index(){
			// debug($this->data);
			if(!eregi("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", $this->data['SendEmail']['from_email'])){
				$this->Session->setFlash('This was not a valid email address');
				$this->redirect($this->referer());
			}
			else{
				$this->Email->from    = $this->data['SendEmail']['from_name'] . ' <no-reply@yourvoiceinhouse.org.au>';
			//	$this->Email->to      = $this->data['SendEmail']['to'];
			//	$this->Email->cc      = $this->data['SendEmail']['cc'];
			//	$this->Email->bcc      = $this->data['SendEmail']['bcc'];
				$this->Email->to      = 'hammy@goonanism.com';
				$this->Email->replyTo    = $this->data['from_name'] . ' <' . $this->data['SendEmail']['from_email'] . '>';
				$this->Email->subject = $this->data['SendEmail']['subject'];
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
				$this->Email->send($this->data['subject']);
			}
		}
	}
?>
