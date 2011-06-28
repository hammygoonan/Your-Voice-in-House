<?php echo '<h1>Edit</h1>' ?>
<?php echo $form->create('Member', array('action' => 'edit')); ?>
<table>
	<tr>
		<td>Member ID</td>
		<td><?php echo $member['Member']['id']; ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('first_name', array('between' => '</td><td>', 'value' => $member['Member']['first_name'])); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('second_name', array('between' => '</td><td>', 'value' => $member['Member']['second_name'])); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('job', array('between' => '</td><td>', 'value' => $member['Member']['job'])); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('email', array('between' => '</td><td>', 'value' => $member['Member']['email'])); ?></td>
	</tr>
	<tr>
		<td>
			<?php echo $form->input('Electorate', array('between' => '</td><td>', 'value' => $member['Electorate']['name'])); ?>
			<?php echo $form->hidden('electorate_id'); ?>
		</td>
	</tr>
	<tr>
		<td><?php echo $form->input('party', array('between' => '</td><td>', 'value' => $member['Party']['id'])); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('portfolios', array('between' => '</td><td>', 'size' => 10, 'multiple' => true)); ?></td>
	</tr>
</table>
<?php foreach($member['Address'] as $address): ?>
	<?php echo 'address<br />'; ?>
<?php endforeach; ?>



<?php echo $form->end('submit');?>
