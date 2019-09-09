<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006~2018 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------
use think\facade\Route;

Route::get('think', function () {
    return 'hello,ThinkPHP5!';
});

Route::get('/', 'index/index');
Route::get('index', 'index/index');
Route::get('logout', 'query/logout');
Route::get('getcode', 'query/getcode');
Route::rule('login', 'index/login','POST');
Route::rule('query', 'query/index','GET');
Route::rule('query', 'query/query','POST');