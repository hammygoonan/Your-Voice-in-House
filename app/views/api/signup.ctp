<div class="grid_12">
	<h1>Sign up for API key</h1>
	<p>To use the Your Voice in House API you need to register a key for each domain name you are using.</p>
	<p>Please enter your email address and the domain name you wish to use the API on.</p>
	<p>There are no real restrictions on the use of the API, however we would appreciate some forwarning if you intend heavy usage.</p>
</div>
<div class="clear"></div>
<?php echo $this->Session->flash(); ?>
<?php echo $this->Form->create('Api', array('controller' => 'api', 'action' => 'signup')); ?>
<div class="search_field">
	<label class="grid_6" for="ApiEmail">
		<h4>Email</h4>
	</label>
	<div class="grid_6">
		<?php echo $this->Form->input('email', array('label' => false, 'class' => 'email required')); ?>
	</div>
	<div class="clear"></div>
</div>
<div class="search_field">
	<label class="grid_6" for="ApiUrl">
		<h4>Url</h4>
	</label>
	<div class="grid_6">
		<?php echo $this->Form->input('url', array('label' => false, 'class' => 'url required')); ?>
		<small>include the prefix (ie http:// or https://)</small>
	</div>
	<div class="clear"></div>
</div>
<div class="prefix_7 grid_3">
	<div class="submit">
		<?php echo $this->Form->end('Generate Key'); ?>
	</div>
</div>
<div class="clear"></div>