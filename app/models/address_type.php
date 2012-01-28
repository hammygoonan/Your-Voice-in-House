<?php
	class AddressType extends AppModel {
		var $name = 'AddressType';
		var $hasMany = array('Address');
	}
?>
