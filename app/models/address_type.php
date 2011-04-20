<?php
	class AddressType extends AppModel {
		var $name = 'AddressType';
		var $hasOne = array('Address');
	}
?>
