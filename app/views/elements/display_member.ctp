<div class="member_display">
	<div class="primary_member_details">
		<?php
			echo $member['Member']['first_name'] . ' ' . $member['Member']['second_name'] . ' (<em>' . $member['Electorate']['name'] . '</em>)';
			if(!empty($member['Member']['job'])){
				echo '<br />' . $member['Member']['job'];
			}
			echo '<br />' . $member['Party']['name'];
		?>
	</div>
	<div class="seconday_member_details">
		<?php
			echo '<br />' . $member['Member']['email'];
			foreach($member['Address'] as $address){
				echo '<div class="address">';
				echo '<br />' . $address['AddressType']['name'] . ' Address';
				if($address['postal'] == 1){echo ' (postal)';}
				echo ':<br />';
				echo $address['address1'];
				if(!empty($address['address2'])){echo '<br />' . $address['address2'];}
				echo '<br />' . $address['suburb'] . '  ' . $address['state'] . '  ' . $address['pcode'];
				echo '</div>';
			}
			
		?>
	<p><?php echo $html->link('Something wrong?', array('controller' => 'corrections', 'action' => 'add_result', $member['Member']['id']), array('class' => 'correction_link grid_2 prefix_7')); ?></p>
	</div>
</div>
