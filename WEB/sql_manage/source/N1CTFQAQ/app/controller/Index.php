<?php
namespace app\controller;
use think\facade\Session;

class Index extends Base
{
    public $view;
    public function __construct()
    {
        parent::__construct(False);
    }

    public function index()
    {
        return $this->view->fetch("index");
    }

    public function login()
    {
        $host = $this->request->post("host");
        $username = $this->request->post("username");
        $password = $this->request->post("password");
        $result = test_connect($host, $username, $password);
        if($result === true){
            Session::set("host",$host);
            Session::set("username",$username);
            Session::set("password",$password);
            return "login success";
        }else{
            Session::clear();
            return $result;
        }
    }

}
