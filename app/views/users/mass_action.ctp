<div class="grid_12">
	<h1>Mass Action</h1>
	<?php if(isset($members)): ?>
		<p><?php echo $this->Html->link('export', array('action' => 'export')); ?>
		<?php echo $this->Form->create('users', array('action' => 'mass_delete', 'onsubmit'=>'return confirm("are you sure?");')); ?>
		<table>
			<thead>
				<tr>
					<th></th>
					<th>Name</th>
					<th>Electorate</th>
					<th>Job</th>
					<th></th>
				</tr>
			</thead>
			<tbody>
				<?php foreach($members as $member): ?>
					<tr>
						<td><?php echo $this->Form->checkbox($member['Member']['id']); ?></td>
						<td><?php echo $member['Member']['first_name'] . ' ' . $member['Member']['second_name']; ?></td>
						<td><?php echo $member['Electorate']['name']; ?></td>
						<td><?php if(isset($member['Member']['job'])) echo $member['Member']['job']; ?></td>
						<td><?php echo $this->Html->link('edit', array('controller' => 'members', 'action' => 'edit', $member['Member']['id'])); ?></td>
					</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
		<?php echo $this->Form->end('Delete'); ?>
	<?php else: ?>
		<?php echo $this->Form->create('users'); ?>
		<?php echo $this->Form->input('House'); ?>
		<?php echo $this->Form->end('Submit'); ?>
	<?php endif; ?>
</div>
<div class="clear"></div>