<?php if(!empty($members) || !empty($electorate) || !empty($portfolios)): ?>
	<h1 class="grid_12">Results Page</h1>
	<small class="grid_12">Click on a members name for additional detail</small> 
	<div class="clear"></div>
	<?php echo $form->create('Member', array('action' => 'email')); ?>
	<?php if(!empty($members)): ?>
		<h2 class="grid_12">Individual Members</h2>
		<?php foreach($members as $member): ?>
			<div class="grid_2"><?php echo $form->radio('member_' . $member['Member']['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false)); ?></div>
			<div class="grid_10"><?php echo $this->element('display_member', array('member' => $member)); ?></div>
		<?php endforeach; ?>
	<?php endif; ?>
	<?php if(!empty($electorate)): ?>
		<h2 class="grid_12"><?php echo $electorate[0]['Electorate']['name']; ?></h2>
		<?php foreach($electorate as $member): ?>
			<div class="grid_2"><?php echo $form->radio('electorate_' . $member['Member']['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false)); ?></div>
			<div class="grid_10"><?php echo $this->element('display_member', array('member' => $member)); ?></div>
		<?php endforeach; ?>
	<?php endif; ?>
	<?php if(!empty($portfolios)): ?>
		<h2 class="grid_12">Portfolio</h2>
		<?php foreach($portfolios as $portfolio): ?>
			<div class="grid_2"><?php echo $form->radio('portolio_' . $portfolio['Member']['id'], array('to' => 'to', 'cc' => 'cc', 'bcc' => 'bcc'), array('legend' => false)); ?></div>
			<div class="grid_10"><?php echo $this->element('display_member', array('member' => $portfolio)); ?></div>
		<?php endforeach; ?>
	<?php endif; ?>
	<div class="grid_12">
		<?php echo $form->end('Send Email'); ?>
	</div>
	<div class="clear"></div>
<?php else: ?>
	<div class="grid_12">
		<h2>Sorry, no results...</h2>
		<p>Please try another search. If you think that this response is wrong, please let us know by <?php echo $html->link('clicking here', array('controller' => 'corrections', 'action' => 'add_search')); ?>
	</div>
	<div class="clear"></div>
<?php endif; ?>
