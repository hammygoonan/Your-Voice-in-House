<?php
	class House extends AppModel{
		var $name = 'House';
		var $hasMany = 'Electorate';
	}
?>