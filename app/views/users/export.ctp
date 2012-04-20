<?php if(isset($members)): ?>
	<?php foreach($members as $member): ?>
		<?php $csv->addRow($member); ?>
	<?php endforeach; ?>
	<?php echo $csv->render('yhiv.csv'); ?>
<?php else: ?>
	<div class="grid_12">
		<h1>Export</h1>
		<?php echo $this->Form->create('users'); ?>
		<?php echo $this->Form->input('House'); ?>
		<?php echo $this->Form->end('Submit'); ?>
		<p>The following is assumed:</p>
		<ul>
			<li>Party can be either the abbreviation or  the id</li>
			<li>Postal address is boolean</li>
		</ul>
	</div>
	<div class="clear"></div>
<?php endif; ?>