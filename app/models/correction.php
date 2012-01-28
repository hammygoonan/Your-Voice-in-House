<?php
	class Correction extends AppModel{
		var $name = 'Correction';
		var $belongsTo = array('Member', 'CorrectionType');
	}
