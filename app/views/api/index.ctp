<div class="grid_12">
	<h3>Variables:</h3>
	<table>
		<tr>
			<th width="30%">Field</th>
			<th>Options</th>
			<th>Comments</th>
		</tr>
		<tr>
			<td>key</td>
			<td>string (required)</td>
			<td>If you have not already done so you need to sign up for an API key will be emailed to you</td>
		</tr>
		<tr>
			<td>format</td>
			<td>string (either xml or json) (default: json)</td>
			<td>The format of the results. This can be either JSON or XML</td>
		</tr>
		<tr>
			<td>version</td>
			<td>float (required)</td>
			<td>The API version. This field ensures backward compatability.</td>
		</tr>
		<tr>
			<td>member</td>
			<td>comma spearated intiger(s) (optional)</td>
			<td>There must be no gap between the values. Use the URL generator below to determine the ids.</td>
		</tr>
		<tr>
			<td>electorate</td>
			<td>comma spearated intiger(s) (optional)</td>
			<td>There must be no gap between the values. Use the URL generator below to determine the ids.</td>
		</tr>
		<tr>
			<td>house</td>
			<td>comma spearated intiger(s) (optional)</td>
			<td>A single house of parliament id. Use the URL generator below to determine the ids.</td>
		</tr>
		<tr>
			<td>portfolio</td>
			<td>comma spearated intiger(s) (optional)</td>
			There must be no gap between the values. Use the URL generator below to determine the ids.</td>
		</tr>
	</table>
	<p>
	<p>There must be at least one optional variable set (ie member, electorate, portfolio or house)</p>
	
	<h3>Examples</h3>
	
	<p>To retreive a full list of members of the house of representatives in json format you would use this URL:</p>
	
	<code>http://yourvoiceinhouse.org.au/api/query/key:yourkey/version:1/format:json/house:1</code>
	
	<p>To get the details of Julia Gillar and Tony Abbot using the xml format, you would use this URL:</p>
	
	<code>http://yourvoiceinhouse.org.au/api/query/key:yourkey/format:xml/version:1/member:1,54</code>
	
	<p>To find the member for Lalor and the member for Warringah, you would use the following URL (NB the JSON format is used by default):</p>
	
	<code>http://yourvoiceinhouse.org.au/api/query/key:yourkey/version:1/electorate:30,79</code>
	
	<p>To find the leaders of all Australian Governments, you would use the following URL:</p>
	
	<code>http://yourvoiceinhouse.org.au/api/query/key:yourkey/version:1/portfolio:1</code>
	
	<h3>Where do I get the ids?</h3>
	
	<p>A list of of ids can be found here:</p>
	<ul>
		<li><?php echo $html->link('Members', array('controller' => 'api', 'action' => 'member_ids')); ?></li>
		<li><?php echo $html->link('Electorates', array('controller' => 'api', 'action' => 'electorate_ids')); ?></li>
		<li><?php echo $html->link('Houses', array('controller' => 'api', 'action' => 'house_ids')); ?></li>
		<li><?php echo $html->link('Portfolios', array('controller' => 'api', 'action' => 'portfolio_ids')); ?></li>
	</ul>
</div>
<div class="clear"></div>