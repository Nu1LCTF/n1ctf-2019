<?php
$file = file_get_contents('waf_tmp');
$ok = false;
try{
    $tokens = token_get_all($file,TOKEN_PARSE);

    foreach ($tokens as $tt) {
        if ($tt[0] == 379) 
        {
            $ok = true;
        
        }
        if($tt[0] == 380)
        {
            $ok = true;
        }
   
    }
}
catch(\Throwable $e){
    fwrite(STDOUT, "check error"); 
   exit(0);
}
if($ok == true){
    fwrite(STDOUT, "check ok"); 
    exit(0);
}