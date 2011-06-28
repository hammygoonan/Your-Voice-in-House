<?php echo $form->create('Member', array('action' => 'find_results')); ?>

<h2>Members</h2>
<label for="MemberMember" class="grid_3">Surname</label>
<?php echo $form->input('Member', array(
	'type' => 'text', 
	'label' => false,
	'div' => 'grid_6 suffix_3'
)); ?>
<?php echo $form->hidden('Member.id'); ?>
<h2>Electorate</h2>
<label for="MemberElectorate" class="grid_3">Electorate</label>
<?php echo $form->input('Electorate', array(
	'label' => false,
	'div' => 'grid_6 suffix_3'
)); ?>
<?php echo $form->hidden('electorate_id'); ?>


<h2>House</h2>

<label for="ElectorateHouse" class="grid_3">House</label>

<?php echo $form->input('Electorate.house', array(
	'type' => 'text', 
	'label' => false,
	'div' => 'grid_6 suffix_3'
)); ?>

<label for="ElectorateState" class="grid_3">State/Federal</label>
<?php echo $form->input('Electorate.state', array('options' =>
	array(
		'Fed' => 'Federal',
		'ACT' => 'Australian Capitol Territory',
		'NSW' => 'New South Wales',
		'NT' => 'Norther Territory',
		'Qld' => 'Queensland',
		'SA' => 'South Australia',
		'Tas' => 'Tasmania',
		'Vic' => 'Victoria',
		'WA' => 'West Australia'
	),
	'label' => false,
	'div' => 'grid_6 suffix_3'
)); ?>

<?php echo $form->end('Submit'); ?>
