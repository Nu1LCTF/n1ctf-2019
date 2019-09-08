<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: 流年 <liu21st@gmail.com>
// +----------------------------------------------------------------------
// 应用公共文件
function test_connect($host, $username, $password)
{
    try{
        mysqli_connect($host, $username, $password);
        if (mysqli_connect_errno()) {
            throw new Exception("Connect failed" . mysqli_connect_error());
        }else{
            return true;
        }
    }catch(Exception $e){
        return $e->getMessage();
    }
}

function get_rand($n)
{
    $characters = '0123456789abcdef';
    $randomString = '';
    for ($i = 0; $i < $n; $i++) {
        $index = rand(0, strlen($characters) - 1);
        $randomString .= $characters[$index];
    }
    return $randomString;
}

function check_code($code, $session_code)
{
    if(substr(md5((string)$code."Nu1L"),0,5) == $session_code){
        return true;
    }else{
        return false;
    }
}

function query_sql($conn, $query)
{
    if(preg_match('/sleep|BENCHMARK|processlist|GET_LOCK|information_schema|into.+?outfile|into.+?dumpfile|\/\*.*\*\//is', $query)) {
        die('Go out!!!');
    }
    $result = $conn->query($query);
    if(!$result){
        return mysqli_error($conn);
    }elseif($result->num_rows>0){
        return json_encode($result->fetch_all());
    }else{
        return "no result";
    }
    $conn->close();
}