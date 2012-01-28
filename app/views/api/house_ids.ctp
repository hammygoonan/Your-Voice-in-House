<div class="api_tables grid_12">
	<h1>House IDs</h1>
	<ul>
		<li><a href="#fed">Federal</a></li>
		<li><a href="#act">Australian Capital Territory</a></li>
		<li><a href="#nsw">New South Wales</a></li>
		<li><a href="#nt">Northern Territory</a></li>
		<li><a href="#qld">Queensland</a></li>
		<li><a href="#tas">Tasmania</a></li>
		<li><a href="#sa">South Australia</a></li>
		<li><a href="#vic">Victoria</a></li>
		<li><a href="#wa">Western Australia</a></li>
	</ul>
	<?php echo $this->element('api_menu'); ?>
	<h3><a name="fed">Federal</a></h3>
	<?php display_house($results['Fed']); ?>

	<h3><a name="act">Australian Capital Territory</a></h3>
	<?php display_house($results['ACT']); ?>
	
	<h3><a name="nsw">New South Wales</a></h3>
	<?php display_house($results['NSW']); ?>
	
	<h3><a name="nt">Northern Territory</a></h3>
	<?php display_house($results['NT']); ?>
	
	<h3><a name="qld">Queensland</a></h3>
	<?php display_house($results['Qld']); ?>
	
	<h3><a name="tas">Tasmania</a></h3>
	<?php display_house($results['Tas']); ?>
	
	<h3><a name="sa">South Australia</a></h3>
	<?php display_house($results['SA']); ?>
	
	<h3><a name="vic">Victoria</a></h3>
	<?php display_house($results['Vic']); ?>
	
	<h3><a name="wa">Western Australia</a></h3>
	<?php display_house($results['WA']); ?>
</div>
	<div class="clear"></div>
	<?php 
		function display_house($house){
			print("<table>
				<thead>
					<tr>
						<th>House</th>
						<th>id</th>
					</tr>
				</thead>		
				<tbody>");
			foreach($house as $cell){
				print("<tr>");
				display_cells($cell);
				print("</tr>");
			}
			print("</tbody>
			</table>
			<p><a href=\"#top\">Back to top</a></p>");
		}
		function display_cells($cell){
			print("<td class=\"first\">" . $cell['name'] . "</td>
			<td class=\"first\">" . $cell['id'] . "</td>");
		}
	
	?>