<?php
	echo "<h1>Results Page</h1>";
?>
<?php if(!empty($members) || !empty($electorate) || !empty($portfolios)): ?>
	<?php echo $form->create('Member', array('action' => 'email')); ?>
	<?php if(!empty($members)): ?>
		<?php echo '<h2>Individual Members</h2>'; ?>
		<table width="100%">
			<?php foreach($members as $member): ?>
				<tr>
					<td><?php echo $form->radio($member['Member']['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false)); ?></td>
					<td><?php echo $this->element('display_member', array('member' => $member['Member'], 'electorate' => $member['Electorate'])); ?></td>
				</tr>
			<?php endforeach; ?>
		</table>
	<?php endif; ?>
	<?php if(!empty($electorate)): ?>
	<?php
		echo '<h2>' . $electorate['Electorate']['name'] . '</h2>';
		echo '<table width="100%">';
		foreach($electorate['Members'] as $member){
			echo "\t<tr>";
			echo "\t\t<td>";
			echo $form->radio($member['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false));
			echo "\t\t</td>";
			echo "\t\t<td>";
			echo $this->element('display_member', array('member' => $member, 'electorate' => $electorate['Electorate']));
			echo "\t\t</td>";
			echo "\t</tr>";
		}
		echo "</table>";
	?>
	<?php endif; ?>
	<?php if(!empty($portfolios)): ?>
	<?php
		echo '<h2>Portfolio</h2>';
		echo '<table width="100%">';
		foreach($portfolios as $portfolio){
			echo "\t<tr>";
			echo "\t\t<td>";
			echo $form->radio($portfolio['Member']['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false));
			echo "\t\t</td>";
			echo "\t\t<td>";
			echo $this->element('display_member', array('member' => $portfolio['Member'], 'electorate' => $portfolio['Electorate']));
			echo "\t\t</td>";
			echo "\t</tr>";
		}
		echo "</table>";
	?>
	<?php endif; ?>
	<?php echo $form->end('Send Email'); ?>
<?php else: ?>
	<h2>Sorry, no results...</h2>
	<p>Please try another search. If you think that this response is wrong, please let us know by <?php echo $html->link('clicking here', array('controller' => 'corrections', 'action' => 'add')); ?>
<?php endif; ?>
