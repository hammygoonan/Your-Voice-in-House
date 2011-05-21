<h1 class="grid_12">Send your Email</h1>
<div class="clear"></div>
<?php echo $this->Session->flash(); ?>
<?php echo $form->create('Member', array('action' => 'email')); ?>
<label for="MemberFromName" class="grid_6">
	Your name:*
</label>
<?php echo $form->input('from_name', array(
	'label' => false,
	'div' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberFromEmail" class="grid_6">
	Your email address:*
</label>
<?php echo $form->input('from_email', array(
	'label' => false,
	'div' => 'grid_6'
	
)); ?>
<div class="clear"></div>
<label for="MemberTo" class="grid_6">
	To:*
</label>
<?php echo $form->input('to', array(
	'value' => @$to_field,
	'label' => false,
	'div' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberCc" class="grid_6">
	Cc:
</label>
<?php echo $form->input('cc', array(
	'value' => @$cc_field, 
	'label' => false,
	'div' => 'grid_6'
));?>
<div class="clear"></div>
<label for="MemberBcc" class="grid_6">
	Bcc:
</label>
<?php echo $form->input('bcc', array('value' => @$bcc_field, 
	'label' => false,
	'div' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberSubject" class="grid_6">
	Subject:*
</label>
<?php echo $form->input('subject', array(
	'label' => false,
	'div' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberMsg" class="grid_6">
	Message:*
</label>
<?php echo $form->input('msg', array('type' => 'textbox', 
	'label' => false,
	'div' => 'grid_6',
	'rows' => 15
)); ?>
<label for="MemberTerms" class="grid_6">
	I agree to the terms and conditions:*
</label>
<?php echo $form->input('terms', array('type' => 'checkbox', 
	'label' => false,
	'div' => 'grid_6'
)); ?>
<div class="clear"></div>
<?php echo $this->Recaptcha->show(); ?>
<?php echo $this->Recaptcha->error(); ?>
<small>*required fields</small>
<?php echo $form->end('Send Email'); ?>
