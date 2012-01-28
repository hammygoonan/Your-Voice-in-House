<?php
	class CorrectionType extends AppModel{
		var $name = 'CorrectionType';
		var $hasOne = array('Correction');
	}
