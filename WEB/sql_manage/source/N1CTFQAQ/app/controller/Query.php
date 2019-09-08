<?php
namespace app\controller;
use think\facade\Session;

class Query extends Base
{
    public $host;
    public $conn;
    public $session_code;
    public function __construct()
    {
        parent::__construct(True);

        if (!session("code")){
            $this->session_code = get_rand(5);
            Session::set("code",$this->session_code);
        }else{
            $this->session_code = session("code");
        }
    }

    public function index()
    {
        return $this->view->fetch("querycode");
    }

    public function getcode()
    {
        $code_str = "substr(md5(?+'Nu1L'), 0, 5) === $this->session_code";
        return $code_str;
    }

    public function query()
    {
        $query = $this->request->post("query");
        $code = $this->request->post("code");
        $db_name = $this->request->post("dbname") ? $this->request->post("dbname") : "Nu1L";
        $conn = mysqli_connect($this->host, session("username"), session("password"), $db_name);

        if (check_code($code, $this->session_code)) {
            $result = query_sql($conn, $query);
            Session::delete("code");
            return htmlentities($result);
        } else {
            Session::delete("code");
            return "code error";
        }
    }

    public function logout()
    {
        Session::clear();
    }
}
