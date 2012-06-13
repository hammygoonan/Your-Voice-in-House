<?php
	class LatestController extends AppController{
		var $name = 'Latest';
		var $uses = array();
		function index(){
			$xml = $this->importXml('http://spiresoftware.com.au/blog/category/your-voice-in-house/feed/');
			$this->set('news', $xml['Rss']['Channel']['Item']);
		}
		function importXml($import){
			App::import('Xml');
			$xml = new Xml($import);
			$xml = $xml->toArray();
			return $xml;
		}
	}