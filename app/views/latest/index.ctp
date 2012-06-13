<h2 class="grid_12">Latest News</h2>
<?php foreach($news as $item): ?>
	<h3 class="grid_12"><?php echo $item['title']; ?></h3>
	<div class="grid_12">
		<small><?php echo date('d M y', strtotime($item['pubDate'])); ?></small>
		<p><?php echo $item['description']; ?></p>
		<a href="<?php echo $item['link']; ?>">Read more</a>
	</div>
<?php endforeach; ?>
<div class="clear"></div>