<div class="grid_12">
	<?php 
		echo $form->create('Address', array('action' => 'edit'));
		echo $form->hidden('id', array('value' => $address['Address']['id']));
		echo $form->hidden('member_id', array('value' => $address['Address']['member_id']));
	?>
	<table>
		<tr>
			<td>Address Type</td>
			<td><?php echo $form->select('address_type_id', $address_types, array('value' => $address['Address']['address_type_id'])); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('postal', array('value' => $address['Address']['postal'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('address1', array('value' => $address['Address']['address1'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('address2', array('value' => $address['Address']['address2'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('suburb', array('value' => $address['Address']['suburb'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('state', array('value' => $address['Address']['state'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('pcode', array('value' => $address['Address']['pcode'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('phone', array('value' => $address['Address']['phone'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('tollfree', array('value' => $address['Address']['tollfree'], 'between' => '</td><td>')); ?></td>
		</tr>
		<tr>
			<td><?php echo $form->input('fax', array('value' => $address['Address']['fax'], 'between' => '</td><td>')); ?></td>
		</tr>
	</table>
	<?php echo $form->end('Submit'); ?>
	<p><?php echo $html->link('Back to member', array('controller' => 'members', 'action' => 'edit', $address['Address']['member_id'])); ?>
</div>
<div class="clear"></div>