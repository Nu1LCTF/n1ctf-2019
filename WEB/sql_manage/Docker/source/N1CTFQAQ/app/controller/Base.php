<?php
namespace app\controller;
use think\Controller;
use think\View;

class Base extends Controller
{
    public $view;
    public $host;
    public function __construct($checkLogin = True)
    {
        parent::__construct(new \think\App());
        $this->view = new View;
        if ($checkLogin) {
            $this->isLogin();
        }
    }

    public function isLogin()
    {
        $this->host = session('host');
        if(empty($this->host)){
            $this->redirect("/index");
        }
    }
}