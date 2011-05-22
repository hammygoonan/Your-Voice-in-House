<div class="grid_12">
	<h1>Something wrong?</h1>
	<p>Thanks for letting us know that there is something wrong with the details we have.</p>
	<p>Please give us as much as you want but the more you provide the easier it will be for us to check the data.</p>
	<p>It's up to you whether you leave your name and emails address. We will only use it to contact you to clarify your comments and it will not be stored or passed on to anyone else.</p>
</div>
<?php echo $form->create('Correction', array('action' => 'add_result')); ?>
<label for="CorrectionName" class="grid_6">
	Your Name
</label>
<?php echo $form->input('name', array('div' => 'grid_6', 'label' => false)); ?>
<div class="clear"></div>
<label for="CorrectionEmail" class="grid_6">
	Your Email Address
</label>
<?php echo $form->input('email', array('div' => 'grid_6', 'label' => false)); ?>
<div class="clear"></div>
<label for="CorrectionComment" class="grid_6">
	Any Comments?
</label>
<?php echo $form->input('comment', array('div' => 'grid_6', 'label' => false)); ?>
<div class="clear"></div>
<label for="CorrectionCorrectionTypeId" class="grid_6">
	Type of error?
</label>
<?php echo $form->input('correction_type_id', array('div' => 'grid_6', 'label' => false, 'options' => $correction_types)); ?>
<?php echo $form->hidden('search_fields', array('value' => $referer)); ?>
<?php echo $form->hidden('member_id', array('value' => $member_id)); ?>
<div class="clear"></div>
<div class="grid_12">
	<?php echo $form->end('Submit'); ?>
</div>
<div class="clear"></div>
