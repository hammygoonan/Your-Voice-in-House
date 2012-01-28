<div class="api_tables grid_12">
	<h1><a name="top">House Ids</a></h1>
	<ul>
		<?php
			foreach($results as $letter => $restofit){
				print("<li><a href=\"#" . $letter . "\">" . $letter . "</a></li>");
			}
		?>
	</ul>
	<?php echo $this->element('api_menu'); ?>
	<?php foreach($results as $result => $members): ?>
		<h2><a name="<?php echo $result; ?>"><?php echo $result; ?></a></h2>
		<table>
			<thead>
				<tr>
					<th>Name</th>
					<th>Electorate</th>
					<th>State</th>
					<th>id</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach($members as $member): ?>
					<tr>
						<td class="first"><?php echo $member['first_name'] . ' ' . $member['second_name']; ?></td>
						<td class="second"><?php echo $member['electorate']; ?></td>
						<td class="third"><?php echo $member['state']; ?></td>
						<td class="fourth"><?php echo $member['id']; ?></td>
					</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
		<p><a href="#top">Back to top</a></p>
	<?php endforeach; ?>
</div>
<div class="clear"></div>