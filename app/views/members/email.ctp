<h1 class="grid_12">Send your Email</h1>
<div class="clear"></div>
<?php echo $this->Session->flash(); ?>
<?php echo $form->create('Member', array('action' => 'email')); ?>
<label for="MemberFromName" class="grid_5">
	Your name:*
</label>
<?php echo $form->input('from_name', array(
	'label' => false,
	'class' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberFromEmail" class="grid_5">
	Your email address:*
</label>
<?php echo $form->input('from_email', array(
	'label' => false,
	'class' => 'grid_6'
	
)); ?>
<div class="clear"></div>
<label for="MemberTo" class="grid_5">
	To:*
</label>
<?php echo $form->input('to', array(
	'value' => @$to_field,
	'label' => false,
	'class' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberCc" class="grid_5">
	Cc:
</label>
<?php echo $form->input('cc', array(
	'value' => @$cc_field, 
	'label' => false,
	'class' => 'grid_6'
));?>
<div class="clear"></div>
<label for="MemberBcc" class="grid_5">
	Bcc:
</label>
<?php echo $form->input('bcc', array('value' => @$bcc_field, 
	'label' => false,
	'class' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberSubject" class="grid_5">
	Subject:*
</label>
<?php echo $form->input('subject', array(
	'label' => false,
	'class' => 'grid_6'
)); ?>
<div class="clear"></div>
<label for="MemberMsg" class="grid_5">
	Message:*
</label>
<?php echo $form->input('msg', array('type' => 'textbox', 
	'label' => false,
	'class' => 'grid_6',
	'rows' => 15
)); ?>
<div class="clear"></div>
<?php echo $this->Recaptcha->show(); ?>
<?php echo $this->Recaptcha->error(); ?>
<small>*required fields</small>
<?php echo $form->end('Send Email'); ?>
