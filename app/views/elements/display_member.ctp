<div class="member_display">
	<div class="primary_member_details">
		<?= $member['Member']['first_name']; ?> <?= $member['Member']['second_name']; ?> (<em><?= $member['Electorate']['name']; ?></em>)
		<?php if(!empty($member['Member']['job'])): ?>
			<br /><?= $member['Member']['job']; ?>
		<?php endif; ?>
		<br /><?= $member['Party']['name']; ?>
	</div>
	<div class="seconday_member_details">
		<br /><?= $member['Member']['email']; ?>
		<?php if(!empty($member['Member']['alternative_email'])): ?>
			<br /><?= $member['Member']['alternative_email']; ?>
		<?php endif; ?>
		<?php if(!empty($member['Member']['twitter'])): ?>
			<br /><a href="http://twitter/<?= $member['Member']['twitter']; ?>">@<?= $member['Member']['twitter']; ?></a>
		<?php endif; ?>
		<?php if(!empty($member['Member']['website'])): ?>
			<br /><a href="<?= $member['Member']['website']; ?>"><?= $member['Member']['website']; ?></a>
		<?php endif; ?>
		<?php foreach($member['Address'] as $address): ?>
			<div class="address">
				<br /><?= $address['AddressType']['name']; ?> Address <?php if($address['postal'] == 1): ?> (postal)<?php endif; ?>:
				<br /><?= $address['address1']; ?>
				<?php if(!empty($address['address2'])): ?><br /><?= $address['address2']; ?><?php endif; ?>
				<br /><?= $address['suburb']; ?> <?= $address['state']; ?> <?= $address['pcode']; ?>
			</div>
		<?php endforeach; ?>
		<p><?= $html->link('Something wrong?', array('controller' => 'corrections', 'action' => 'add_result', $member['Member']['id']), array('class' => 'correction_link grid_2 prefix_7')); ?></p>
		<?php if($session->check('Auth.User.id')): ?>
			<p><?= $html->link('edit', array('controller' => 'members', 'action' => 'edit', $member['Member']['id'])); ?>
		<?php endif; ?>
	</div>
</div>
