<?php
	class Address extends AppModel {
		var $name = 'Address';
		var $belongsTo = array('AddressType', 'Member');
	}
?>
