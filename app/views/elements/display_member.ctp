<div class="member_display">
	<div class="primary_member_details">
		<?php
			echo $member['first_name'] . ' ' . $member['second_name'] . '<br />';
			echo '<em>' . $electorate['name'] . '</em>';
		?>
	</div>
	<div class="seconday_member_details">
		<?php
			echo '<br />' . $member['email'];
			if(!empty($member['job'])){
				echo '<br />' . $member['job'];
			}
		?>
			<table>
				<tr>
					<?php
						if(!empty($member['el_address_1'])){
							echo '<td>Electoral Address:<br />';
							echo $member['el_address_1'];
							if(!empty($member['el_address_2'])){echo '<br />' . $member['el_address_2'];}
							echo '<br />' . $member['el_suburb'] . '  ' . $member['el_state'] . '  ' . $member['el_pcode'];
							echo '</td>';
						}
					?>
					<?php
						if(!empty($member['pa_address_1'])){
							echo '<td>Parliamentary Address:<br />';
							echo $member['pa_address_1'];
							if(!empty($member['pa_address_2'])){echo '<br />' . $member['pa_address_2'];}
							echo '<br />' . $member['pa_suburb'] . '  ' . $member['pa_state'] . '  ' . $member['pa_pcode'];
							echo '</td>';
						}
					?>
				</tr>
			</table>
	</div>
</div>
