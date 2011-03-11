<?php
	echo "<h1>Results Page</h1>";
?>

<?php if(!empty($portfolios)){
	echo '<h2>Portfolio</h2>';
	foreach($portfolios as $portfolio){
		echo $this->element('display_member', array('member' => $portfolio['Member'], 'electorate' => $portfolio['Electorate']));
	}
} ?>

<?php if(!empty($members)){
	echo '<h2>Individual Members</h2>';
	echo $this->element('display_member', array('member' => $members['Member'], 'electorate' => $members['Electorate']));
}?>
<?php if(!empty($electorate)){
	echo '<h2>' . $electorate['Electorate']['name'] . '</h2>';
	foreach($electorate['Members'] as $member){
		echo $this->element('display_member', array('member' => $member, 'electorate' => $electorate['Electorate']));
	}
}?>
<?php if(!empty($pcode)){debug($pcode);} ?>
