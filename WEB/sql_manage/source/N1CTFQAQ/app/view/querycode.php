<!DOCTYPE html>
<html lang="en" >
<head>
    <meta charset="UTF-8">
    <title>Login form with confirmation!</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
<a href="#"id="logout">logout</a>
<h1 id="title">Welcome to N1CTF2019!!</h1>
<h1 id="title">You can connect to your mysql to execute SQL statement</h1>
<div class="container">
    <div class="loginBox">
        <div class="userImage">
            <img src="static/img/catFace.png">
        </div>
        <form id="loginForm">
            <div class="input-wrapper">
                <label>query:</label>
                <input type="input" name="query" placeholder="select 1;" id="query">
            </div>
            <div class="input-wrapper">
                <label id="verify">Code:</label>
                <input type="code" name="code" placeholder="" id="code">
            </div>
            <div class="input-wrapper">
                <label>result:</label>
                <br>
            </div>
            <div class="input-wrapper">
                <p id="news"></p>
            </div>
        </form>
        <input type="button" name="" value="Submit" id="button">
    </div>
</div>

<script src='static/js/jquery.min.js'></script>
<script src="static/js/querycode.js"></script>
</body>
</html>