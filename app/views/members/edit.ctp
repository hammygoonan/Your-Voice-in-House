<div class="grid_12">
	<?= '<h1>Edit</h1>' ?>
	<?= $form->create('Member', array('action' => 'edit')); ?>
	<table>
		<tr>
			<td>Member ID</td>
			<td>
				<?= $member['Member']['id']; ?>
				<?= $form->hidden('id', array('value' => $member['Member']['id'])); ?>
			</td>
		</tr>
		<tr>
			<td><?= $form->input('first_name', array('between' => '</td><td>', 'value' => $member['Member']['first_name'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('second_name', array('between' => '</td><td>', 'value' => $member['Member']['second_name'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('job', array('between' => '</td><td>', 'value' => $member['Member']['job'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('email', array('between' => '</td><td>', 'value' => $member['Member']['email'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('alternative_email', array('between' => '</td><td>', 'value' => $member['Member']['alternative_email'])); ?></td>
		</tr>
		<tr>
			<td>
				<?= $form->input('Electorate', array('between' => '</td><td>', 'value' => $member['Electorate']['name'])); ?>
				<?= $form->hidden('electorate_id', array('value' => $member['Member']['electorate_id'])); ?>
			</td>
		</tr>
		<tr>
			<td><?= $form->input('party_id', array('between' => '</td><td>', 'value' => $member['Party']['id'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('website', array('between' => '</td><td>', 'value' => $member['Member']['website'])); ?></td>
		</tr>
		<tr>
			<td><?= $form->input('twitter', array('between' => '</td><td>', 'value' => $member['Member']['twitter'])); ?></td>
		</tr>
		<tr>
			<td><?php 
				foreach($member['Portfolio'] as $portfolio){
					$portfolio_id[] = $portfolio['id'];
				}
				echo $form->input('Portfolio', array('between' => '</td><td>', 'selected' => @$portfolio_id, 'size' => 10, 'multiple' => true));
			?></td>
		</tr>
	</table>
	<h2>Addresses</h2>
	<?php foreach($member['Address'] as $address): ?>
		<h3>Address</h3>
		Id: <?= $address['id']; ?> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <?= $html->link('Edit Address', array('controller' => 'addresses', 'action' => 'edit', 'member_id' => $member['Member']['id'], 'address_id' => $address['id'])); ?> | <?= $html->link('Delete Address', array('controller' => 'addresses', 'action' => 'delete', 'id' => $member['Member']['id'])); ?><br />
		Postal: <?= ($address['postal'] == 1) ? 'Postal' : 'Pysical'; ?><br />
		Address Type: <?= $address['AddressType']['name']; ?><br />
		Address Line 1: <?= $address['address1']; ?><br />
		Address Line 2: <?= $address['address2']; ?><br />
		Suburb: <?= $address['suburb']; ?><br />
		State: <?= $address['state']; ?><br />
		Postcode: <?= $address['pcode']; ?><br />
		Phone: <?= $address['phone']; ?><br />
		Tollfree: <?= $address['tollfree']; ?><br />
		Fax: <?= $address['fax']; ?>
	<?php endforeach; ?>
	
	<p><?= $html->link('Add Address', array('controller' => 'addresses', 'action' => 'add', 'member_id' => $member['Member']['id'])); ?></p> 
	<?= $form->end('submit');?>
</div>
<div class="clear"></div>