<div class="member_display">
	<div class="primary_member_details">
		<?php
			echo $member['Member']['first_name'] . ' ' . $member['Member']['second_name'] . '<br />';
			echo '<em>' . $member['Electorate']['name'] . '</em>';
		?>
	</div>
	<div class="seconday_member_details">
		<?php
			echo '<br />' . $member['Member']['email'];
			if(!empty($member['Member']['job'])){
				echo '<br />' . $member['Member']['job'];
			}
		?>
			<table>
				<tr>
					<?php
						if(!empty($member['Member']['el_address_1'])){
							echo '<td>Electoral Address:<br />';
							echo $member['Member']['el_address_1'];
							if(!empty($member['Member']['el_address_2'])){echo '<br />' . $member['Member']['el_address_2'];}
							echo '<br />' . $member['Member']['el_suburb'] . '  ' . $member['Member']['el_state'] . '  ' . $member['Member']['el_pcode'];
							echo '</td>';
						}
					?>
					<?php
						if(!empty($member['Member']['pa_address_1'])){
							echo '<td>Parliamentary Address:<br />';
							echo $member['Member']['pa_address_1'];
							if(!empty($member['Member']['pa_address_2'])){echo '<br />' . $member['Member']['pa_address_2'];}
							echo '<br />' . $member['Member']['pa_suburb'] . '  ' . $member['Member']['pa_state'] . '  ' . $member['Member']['pa_pcode'];
							echo '</td>';
						}
					?>
				</tr>
			</table>
	</div>
</div>
