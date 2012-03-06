<div class="grid_12">
	<?php echo $this->Session->flash('auth'); ?>
	<?php echo $this->Form->create('User'); ?>
	<?php echo $this->Form->input('username'); ?>
	<?php echo $this->Form->input('password'); ?>
	<?php echo $this->Form->end('Login'); ?>
</div>