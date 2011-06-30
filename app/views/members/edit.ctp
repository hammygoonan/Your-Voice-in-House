<?php echo '<h1>Edit</h1>' ?>
<?php echo $form->create('Member', array('action' => 'edit')); ?>
<table>
	<tr>
		<td>Member ID</td>
		<td>
			<?php echo $member['Member']['id']; ?>
			<?php echo $form->hidden('id', array('value' => $member['Member']['id'])); ?>
		</td>
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
			<?php echo $form->hidden('electorate_id', array('value' => $member['Member']['electorate_id'])); ?>
		</td>
	</tr>
	<tr>
		<td><?php echo $form->input('party_id', array('between' => '</td><td>', 'value' => $member['Party']['id'])); ?></td>
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
	Id: <?php echo $address['id']; ?> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <?php echo $html->link('Edit Address', array('controller' => 'addresses', 'action' => 'edit', 'member_id' => $member['Member']['id'], 'address_id' => $address['id'])); ?><br />
	Postal: <?php echo ($address['postal'] == 1) ? 'Postal' : 'Pysical'; ?><br />
	Address Type: <?php echo $address['AddressType']['name']; ?><br />
	Address Line 1: <?php echo $address['address1']; ?><br />
	Address Line 2: <?php echo $address['address2']; ?><br />
	Suburb: <?php echo $address['suburb']; ?><br />
	State: <?php echo $address['state']; ?><br />
	Postcode: <?php echo $address['pcode']; ?><br />
	Phone: <?php echo $address['phone']; ?><br />
	Tollfree: <?php echo $address['tollfree']; ?><br />
	Fax: <?php echo $address['fax']; ?>
<?php endforeach; ?>

<p><?php echo $html->link('Add Address', array('controller' => 'addresses', 'action' => 'add', 'member_id' => $member['Member']['id'])); ?></p> 
<?php echo $form->end('submit');?>
