<h1>File Upload</h1>
<?php
	echo $this->Session->flash();
	echo $this->Form->create('Member', array('type' => 'file'));
	echo $this->Form->input('Electorate.state');
	echo $this->Form->input('Electorate.house');
	echo $this->Form->file('Member.submittedfile');
	echo $this->Form->input('Member.over_ride', array('type' => 'checkbox', 'label' => 'Override current entries'));
	echo $this->Form->submit('Submit');
?>
