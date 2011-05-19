<?php echo $this->Html->docType(); ?>
<html xmlns="http://www.w3.org/1999/xhtml">
<?php echo $this->Html->charset('ISO-8859-1'); ?>
<head>
	<title><?php echo $title_for_layout?></title>
	<?php echo $this->Html->meta(
	    'keywords',
	    'enter any meta keyword here'
	);?>
	<?php echo $this->Html->meta(
	    'description',
	    'enter any meta description here'
	   );?> 
	<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
	<?php echo $this->Html->css(array('rest', 'grid', 'style')); ?> 
</head>
<body>
	<div class="container_12">
		<div id="header">
			<h1>Header</h1>
		</div>
		<div id="content">
			<?php echo $content_for_layout ?>
		</div>
		<div id="footer">
			Designed and developed by Spire Software
		</div>
	</div> <!-- end container_12 -->
</body>
</html>
