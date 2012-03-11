<div class="grid_12">
	<h1>Administration</h1>
	<ul>
		<li><?php echo $this->Html->link('Search / Edit', array('controller' => 'members', 'action' => 'search')); ?></li>
		<li><?php echo $this->Html->link('Import', array('action' => 'upload')); ?></li>
		<li><?php echo $this->Html->link('Export', array('action' => 'export')); ?></li>
		<li><?php echo $this->Html->link('Mass Action', array('action' => 'mass_action')); ?></li>
		<li><?php echo $this->Html->link('Corrections', array('controller' => 'corrections', 'action' => 'index')); ?></li>
	</ul>
</div>
<div class="clear"></div>