<?php
	echo "<h1>Results Page</h1>";
?>

<?php if(!empty($portfolios)){
	echo '<h2>Portfolio</h2>';
	foreach($portfolios as $portfolio){
		echo $this->element('display_member', array('member' => $portfolio));
	}
} ?>

<?php if(!empty($members)){
	echo '<h2>Individual Members</h2>';
	echo $this->element('display_member', array('member' => $members));
}?>
<?php if(!empty($electorate)){
	debug($electorate);
	echo '<h2>' . $electorate['Electorate']['name'] . '</h2>';
	foreach($electorate['Members'] as $member){
		echo $this->element('display_member', array('member' => $member));
	}
}?>
<?php if(!empty($pcode)){debug($pcode);} ?>
