<h1>Search for Members of Parliament</h1>
<?php echo $form->create('Member', array('action' => 'results', 'type' => 'get')); ?>
<table width="100%">
	<tr>
		<td><?php echo $form->input('Member', array('between' => '</td><td>', 'type' => 'text')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('Portfolio', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('Electorate', array('between' => '</td><td>')); ?></td>
	</tr>
	<tr>
		<td><?php echo $form->input('State', array('between' => '</td><td>', 'options' =>
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
			))); ?></td>
	</tr>
	<tr>
		<td></td>
		<td><?php echo $form->end('Submit'); ?></td>
	</tr>
</table>
