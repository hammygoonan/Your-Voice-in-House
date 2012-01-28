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
	<?php foreach($results as $result => $electorates): ?>
		<h2><a name="<?php echo $result; ?>"><?php echo $result; ?></a></h2>
		<table>
			<thead>
				<tr>
					<th>Electorate</th>
					<th>House</th>
					<th>State</th>
					<th>id</th>
				</tr>
			</thead>
			<tbody>
				<?php usort($electorates, function($a, $b){
					return strcmp($a['name'], $b['name']);
				}); ?>
				<?php foreach($electorates as $electorate): ?>
					<tr>
						<td class="first"><?php echo $electorate['name']; ?></td>
						<td class="second"><?php echo $electorate['house']; ?></td>
						<td class="third"><?php echo $electorate['state']; ?></td>
						<td class="fourth"><?php echo $electorate['id']; ?></td>
					</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
		<p><a href="#top">Back to top</a></p>
	<?php endforeach; ?>
</div>
<div class="clear"></div>