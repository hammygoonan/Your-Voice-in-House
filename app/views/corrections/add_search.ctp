<?php echo $form->create('Correction', array('action' => 'add_search')); ?>
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
	echo $form->input('correction_type_id', array('between' => '</td><td>', 'options' => $correction_types, 'default' => 5));
	echo "\t\t</td>";
	echo "\t</tr>";
?>
</table>
<?php echo $form->hidden('search_fields', array('value' => $referer)); ?>
<?php echo $form->end('Submit'); ?>
	
