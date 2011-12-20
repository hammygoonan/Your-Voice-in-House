<?php echo $this->Html->docType(); ?>
<html xmlns="http://www.w3.org/1999/xhtml">
<?php echo $this->Html->charset('ISO-8859-1'); ?>
<head>
	<title><?php echo $title_for_layout?></title>
	<?php echo $this->Html->meta(
	    'keywords',
	    'Democracy, Politics, Politicians, Australia, ACT, NSW, NT, QLD, TAS, SA, VIC, WA, Senate, House, House of Representatives, Legislative Council, Legislative Assembly, Labor, Liberal, Nation, Green, Member, Party, Electorate, State, Federal, Australian Capital Territory, New South Wales, Northern Territory, Queensland, South Australia, Tasmania, Victoria, Western Australia'
	);?>
	<?php echo $this->Html->meta(
	    'description',
	    'Your Voice in House allows you to search for, find and contact every politician in Australia'
	   );?> 
	<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
	<?php echo $this->Html->css(array('grid', 'ui-lightness/jquery-ui', 'style')); ?>
	<?php echo $javascript->link(array('jquery.js', 'jquery-ui.js', 'jquery.validate.min.js', 'javascript.js')); ?>
</head>
<body>
	<div class="container_12">
		<div id="header">
			<a href="/"><?php echo $html->image('head.jpg', array('class' => 'grid_12', 'alt' => 'Your Voice In House')); ?></a>
		</div>
		<div id="content">
			<?php echo $content_for_layout ?>
		</div> <!-- end content -->
		<div id="footer">
			<ul class="footer_list">
				<li><a href="/<?php echo basename(dirname(APP)); ?>">Home</a></li>
				<li><a href="/<?php echo basename(dirname(APP)); ?>/pages/about">About</a></li>
				<li><a href="/latest">Latest</a></li>
				<li><a href="/<?php echo basename(dirname(APP)); ?>/api">API</a></li>
				<li><?php echo $html->link('Spire Software', 'http://spiresoftware.com.au'); ?></li>
			</ul>
		</div>
	</div> <!-- end container_12 -->
</body>
</html>
