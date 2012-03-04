<div class="grid_12">
	<h1>Export</h1>
	<?php if(isset($members)): ?>
		<?php debug($members); ?>
	<?php else: ?>
		<?php echo $this->Form->create('users'); ?>
		<?php echo $this->Form->input('House'); ?>
		<?php echo $this->Form->end('Submit'); ?>
		<p>The following is assumed:</p>
		<ul>
			<li>Party can be either the abbreviation or the id</li>
			<li>Postal address is boolean</li>
			<li>
		</ul>
	<?php endif; ?>
</div>
<div class="clear"></div>