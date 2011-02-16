<?php
	class Portfolio extends AppModel {
		var $name = 'Portfolio';
		var $hasAndBelongsToMany = array('Member');
	}
?>
