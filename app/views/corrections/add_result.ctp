<?php echo $form->create('Correction', array('action' => 'add_result')); ?>
<table width="100%">
<?php
	echo "\t<tr>";
	echo "\t\t<td>";
	echo $form->input('name', array('between' => '</td><td>'));
	echo "\t\t</td>";
	echo "\t</tr>";
	echo "\t<tr>";
	echo "\t\t<td>";
	echo $form->input('email', array('between' => '</td><td>'));
	echo "\t\t</td>";
	echo "\t</tr>";
	echo "\t<tr>";
	echo "\t\t<td>";
	echo $form->input('comment', array('between' => '</td><td>'));
	echo "\t\t</td>";
	echo "\t</tr>";
	echo "\t<tr>";
	echo "\t\t<td>";
	echo $form->input('correction_type_id', array('between' => '</td><td>', 'options' => $correction_types));
	echo "\t\t</td>";
	echo "\t</tr>";
?>
</table>
<?php echo $form->hidden('search_fields', array('value' => $referer)); ?>
<?php echo $form->hidden('member_id', array('value' => $member_id)); ?>
<?php echo $form->end('Submit'); ?>
	
