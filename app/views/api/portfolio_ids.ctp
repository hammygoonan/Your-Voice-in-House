<div class="grid_12 api_tables">
	<h1>Portfolio IDs</h1>
	<?php echo $this->element('api_menu'); ?>
	<table>
		<thead>
			<tr>
				<th>Portfolio</th>
				<th>ID</th>
			</tr>
		</thead>
		<tbody>
			<?php foreach($portfolios as $portfolio): ?>
				<tr>
					<td class="first"><?php echo $portfolio['Portfolio']['name']; ?></td>
					<td class="first"><?php echo $portfolio['Portfolio']['id']; ?></td>
				</tr>
			<?php endforeach; ?>
		</tbody>
	</table>
</div>
<div class="clear"></div>