<?php 
	echo $form->create('Address', array('action' => 'add'));
	echo $form->hidden('member_id', array('value' => $member));
?>
<table>
	<tr>
		<td>Address Type</td>
		<td><?php echo $form->select('address_type_id', $address_types, array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('postal', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('address1', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('address2', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('suburb', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('state', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('pcode', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('phone', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('tollfree', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('fax', array('between' => '</td><td>')); ?></td>
	</tr>
</table>
<?php echo $form->end('Submit'); ?>
