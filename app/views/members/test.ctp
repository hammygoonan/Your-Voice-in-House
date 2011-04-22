<h1>Test</h1>
<?php
	echo $this->Form->create('Member');
	echo $this->Form->input('Member.name');
	echo $this->Form->input('Addresses.0.address1');
	echo $this->Form->submit('Submit');
?>
