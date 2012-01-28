<h1 class="grid_12">Search for Members of Parliament</h1>
<div class="clear"></div>
<strong class="grid_12">You can search in as many fields as you like</strong>
<?php echo $form->create('Member', array('action' => 'results', 'type' => 'get')); ?>
	<h3 class="grid_12">Search for a politician by name</h3>
	<div class="clear"></div>
	<div class="search_field">
		<label for="MemberMember" class="grid_6">
			<h4>Surname</h4>
		</label>
		<?php echo $form->input('Member', array(
			'type' => 'text', 
			'label' => false,
			'div' => 'grid_6'
		)); ?>
		<?php echo $form->hidden('Member.id'); ?>
		<small class="grid_12">Search by surname, and separate multiple names by a comma</small>
	<div class="clear"></div>
	</div>
	
	<h3 class="grid_12">Search by Electorate</h3>
	<div class="clear"></div>
	<div class="search_field">
		<label for="MemberElectorate" class="grid_6">
			<h4>Electorate</h4>
		</label>
		<?php echo $form->input('Electorate', array(
			'label' => false,
			'div' => 'grid_6'
		)); ?>
		<?php echo $form->hidden('electorate_id'); ?>
		<small class="grid_12">You can search by electorate name or the name of the house of parliament (ie House of Representatives)</small>
	<div class="clear"></div>
	</div>
	
	<h3 class="grid_12">Search by Portfolio</h3>
	<div class="clear"></div>
	<div class="search_field">
		<label for="PortfolioPortfolio" class="grid_6">
			<h4>Portfolio</h4>
		</label>
		<?php echo $form->input('Portfolio', array(
			'label' => false,
			'div' => 'grid_6',
			'size' => 10
		));?>
		<div class="clear"></div>
		<label for="MemberState" class="grid_6">
			<h4>State/Federal</h4>
		</label>
		<?php echo $form->input('State', array('options' =>
			array(
				'Fed' => 'Federal',
				'ACT' => 'Australian Capitol Territory',
				'NSW' => 'New South Wales',
				'NT' => 'Norther Territory',
				'Qld' => 'Queensland',
				'SA' => 'South Australia',
				'Tas' => 'Tasmania',
				'Vic' => 'Victoria',
				'WA' => 'West Australia'
			),
			'label' => false,
			'div' => 'grid_6'
		)); ?>
	<div class="clear"></div>
	</div>
<div class="prefix_7 grid_3">
	<?php echo $form->end('Submit'); ?>
</div>
<div class="grid_12">
	<div class="grid_1">
		<a href="http://twitter.com/share" class="twitter-share-button" data-url="http://yourvoiceinhouse.org.au" data-text="I just found and contacted politicians using Your Voice in House" data-count="vertical" data-via="spiresoft">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
	</div>
	<div id="fb-root" class="grid_2"></div><script src="http://connect.facebook.net/en_US/all.js#xfbml=1"></script><fb:like-box href="https://www.facebook.com/pages/Your-Voice-in-House/204204789616697" width="100" show_faces="true" border_color="" stream="false" header="true"></fb:like-box>
</div>
<div class="clear"></div>
