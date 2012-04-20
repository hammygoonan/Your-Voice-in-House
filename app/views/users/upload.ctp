<div class="grid_12">
	<h1>File Upload</h1>
	<?php
		echo $this->Session->flash();
		echo $this->Form->create('User', array('type' => 'file'));
		echo $this->Form->input('House');
		echo $this->Form->file('Member.submittedfile');
		echo $this->Form->input('Member.over_ride', array('type' => 'checkbox', 'label' => 'Override current entries'));
		echo $this->Form->submit('Submit');
	?>
	<p><?php echo $this->Html->link('Download CSV file', array('controller' => 'users', 'action' => 'csv_template'));?></a></p>
</div>
<div class="clear"></div>