<h1 class="grid_12">Search for Members of Parliament</h1>
<div class="clear"></div>
<?php echo $form->create('Member', array('action' => 'results', 'type' => 'get')); ?>
	<label for="MemberMember" class="grid_6">
		Search for a specific politican<br /><small>(search by surname, and separate multiple names by a comma)</small>
	</label>
	<?php echo $form->input('Member', array(
		'type' => 'text', 
		'label' => false,
		'div' => 'grid_6'
	)); ?>
	<?php echo $form->hidden('Member.id'); ?>
	<div class="clear"></div>
	<label for="PortfolioPortfolio" class="grid_6">
		Search by portfolio
	</label>
	<?php echo $form->input('Portfolio', array(
		'label' => false,
		'div' => 'grid_6',
		'size' => 10
	));?>
	<div class="clear"></div>
	<label for="MemberElectorate" class="grid_6">
		Search by electorate
	</label>
	<?php echo $form->input('Electorate', array(
		'label' => false,
		'div' => 'grid_6'
	)); ?>
	<div class="clear"></div>
	<label for="MemberState" class="grid_6">
		State/Federal
	</label>
	<?php echo $form->input('State', array('options' =>
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
		'div' => 'grid_6'
	)); ?>
	<div class="clear"></div>
<div class="grid_12">
	<?php echo $form->end('Submit'); ?>
</div>
<div class="clear"></div>
