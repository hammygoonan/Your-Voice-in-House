<?php if(isset($error)): ?>
	<?php if($format == 'xml'): ?>
		<error><?php echo $error; ?></error>
	<?php elseif($format == 'json'): ?>
		<?php echo json_encode($error); ?>
	<?php endif; ?>
<?php else: ?>
	<?php if($format == 'xml'): ?>
		<?php $keys = array_keys($results); ?>
		<results>
			<?php foreach($keys as $key): ?>
				<?php echo '<' . $key . '>'; ?>
					<?php foreach($results[$key] as $member): ?>
						<member id="<?php echo $member['id']; ?>" title="<?php echo $member['title']; ?>" first_name="<?php echo $member['first_name']; ?>" second_name="<?php echo $member['second_name']; ?>" job="<?php echo $member['job']; ?>" email="<?php echo $member['email']; ?>">
							<party id="<?php echo $member['Party']['id']; ?>" abbreviation="<?php echo $member['Party']['abbreviation']; ?>" name="<?php echo $member['Party']['name']; ?>" />
							<electorate id="<?php echo $member['Electorate']['id']; ?>" name="<?php echo $member['Electorate']['name']; ?>">
								<house id="<?php echo $member['Electorate']['House']['id']; ?>" name="<?php echo $member['Electorate']['House']['name']; ?>" state="<?php echo $member['Electorate']['House']['state']; ?>" upperlower="<?php echo $member['Electorate']['House']['upperlower']; ?>"/>
							</electorate>
							<?php foreach($member['Address'] as $address): ?>
								<address id="<?php echo $address['id']; ?>" postal="<?php echo $address['postal']; ?>" address1="<?php echo $address['address1']; ?>" address2="<?php echo $address['address2']; ?>" state="<?php echo $address['state']; ?>" suburb="<?php echo $address['suburb']; ?>" pcode="<?php echo $address['pcode']; ?>" phone="<?php echo $address['phone']; ?>" tollfree="<?php echo $address['tollfree']; ?>" fax="<?php echo $address['fax']; ?>" type="<?php echo $address['type']; ?>" />
							<?php endforeach; ?>
							<?php foreach($member['Portfolio'] as $portfolio): ?>
								<portfolio id="<?php echo $portfolio['id']; ?>" name="<?php echo $portfolio['name']; ?>" />
							<?php endforeach; ?>
						</member>
					<?php endforeach; ?>
				<?php echo '</' . $key . '>'; ?>
			<?php endforeach; ?>
		</results>
	<?php elseif($format == 'json'): ?>
		<?php echo json_encode($results); ?>
	<?php endif; ?>
<?php endif; ?>