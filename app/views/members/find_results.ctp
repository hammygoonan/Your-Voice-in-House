<?php print('<h1>Find Results</h1>'); ?>
<?php if(!empty($house)): ?>
	<h2><?php echo $search; ?></h2>
	<table>
		<?php $house_members = 0; ?>
		<?php foreach($house as $electorate): ?>
			<?php foreach($electorate['Members'] as $member): ?>
				<tr>
					<td><?php echo $member['first_name'] . ' ' . $member['second_name'] . ' (' . $electorate['Electorate']['name'] . ')'; ?></td>
					<td><?php echo $this->Html->link('edit', array('controller' => 'members', 'action' => 'edit', 'id' => $member['id'])); ?> | 
					<?php echo $this->Html->link('delete', array('controller' => 'members', 'action' => 'delete', 'id' => $member['id'])); ?></td>
				</tr>
				<?php $house_members++ ?>
			<?php endforeach; ?>
		<?php endforeach; ?>
	</table>
	<?php echo '<h2>' . $house_members . ' Results</h2>'; ?>
<?php endif; ?>
<?php if(!empty($electorates)): ?>
	<table>
		<?php foreach($electorates as $electorate): ?>
			<tr>
				<td><?php echo $electorate['Member']['first_name'] . ' ' . $electorate['Member']['second_name'] . ' (' . $electorate['Electorate']['name'] . ')'; ?></td>
				<td><?php echo $this->Html->link('edit', array('controller' => 'members', 'action' => 'edit', 'id' => $electorate['Member']['id'])); ?> | 
				<?php echo $this->Html->link('delete', array('controller' => 'members', 'action' => 'delete', 'id' => $electorate['Member']['id'])); ?></td>
			</tr>
		<?php endforeach; ?>
	<table>
	<?php echo '<h2>' . sizeof($electorates) . ' Results</h2>'; ?>
<?php endif; ?>
