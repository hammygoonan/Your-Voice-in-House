<?php
	class SendEmailsController extends AppController {
		var $name = 'SendEmails';
		var $components = array('Email');
//		var $uses = array('SendEmail');
		function index(){
			debug($this->data);
			$this->SendEmail->set($this->data);
			if($this->SendEmail->validates()){
				$this->Email->from    = $this->data['from_name'] . ' <no-reply@yourvoiceinhouse.org.au>';
			//	$this->Email->to      = $this->data['to'];
				$this->Email->to      = 'hammy@goonanism.com';
				$this->Email->replyTo    = $this->data['from_name'] . ' <' . $this->data['from_email'] . '>';
				$this->Email->subject = $this->data['subject'];
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
			else{
				debug($this->SendEmail->invalidFields());
			}
		}
	}
?>
