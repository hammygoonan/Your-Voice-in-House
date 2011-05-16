<?php
	echo "<h1>Results Page</h1>";
?>
<?php echo $form->create('Member', array('action' => 'email')); ?>
<?php if(!empty($members)): ?>
	<?php echo '<h2>Individual Members</h2>'; ?>
	<table width="100%">
		<tr>
			<td><?php echo $form->input($members['Member']['id'], array('type' => 'checkbox', 'label' => false)); ?></td>
			<td><?php echo $this->element('display_member', array('member' => $members['Member'], 'electorate' => $members['Electorate'])); ?></td>
		</tr>
	</table>
<?php endif; ?>
<?php if(!empty($electorate)){
	echo '<h2>' . $electorate['Electorate']['name'] . '</h2>';
	echo '<table width="100%">';
	foreach($electorate['Members'] as $member){
		echo "\t<tr>";
		echo "\t\t<td>";
		echo $form->input($member['id'], array('type' => 'checkbox', 'label' => false));
		echo "\t\t</td>";
		echo "\t\t<td>";
		echo $this->element('display_member', array('member' => $member, 'electorate' => $electorate['Electorate']));
		echo "\t\t</td>";
		echo "\t</tr>";
	}
	echo "</table>";
}?>
<?php if(!empty($portfolios)){
	echo '<h2>Portfolio</h2>';
	echo '<table width="100%">';
	foreach($portfolios as $portfolio){
		echo "\t<tr>";
		echo "\t\t<td>";
		echo $form->input($portfolio['Member']['id'], array('type' => 'checkbox', 'label' => false));
		echo "\t\t</td>";
		echo "\t\t<td>";
		echo $this->element('display_member', array('member' => $portfolio['Member'], 'electorate' => $portfolio['Electorate']));
		echo "\t\t</td>";
		echo "\t</tr>";
	}
	echo "</table>";
} ?>
<?php echo $form->end('Send Email'); ?>
