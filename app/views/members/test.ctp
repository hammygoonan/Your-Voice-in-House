<h1>Test</h1>
<?php
	echo $this->Form->create('Member');
	echo $this->Form->input('Member.name');
	echo $this->Form->input('Portfolio');
	echo $this->Form->submit('Submit');
?>
