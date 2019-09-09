<!DOCTYPE html>
<html lang="en" >
<head>
    <meta charset="UTF-8">
    <title>Sql Manage</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
<h1 id="title">Welcome to N1CTF2019!!</h1>
<h1 id="title">You can connect to your mysql to execute SQL statement</h1>
<div class="container">
    <div class="loginBox">
        <div class="userImage">
            <img src="static/img/catFace.png">
        </div>
        <form id="loginForm" action="/login">
            <div class="input-wrapper">
                <label>host:</label>
                <input type="input" name="host" placeholder="127.0.0.1:3306" id="host">
            </div>
            <div class="input-wrapper">
                <label>username:</label>
                <input type="username" name="username" placeholder="root" id="username">
            </div>
            <div class="input-wrapper">
                <label>password:</label>
                <input type="password" name="password" placeholder="root" id="password">
            </div>
            <div class="input-wrapper">
                <p style="color:red" id="news"></p>
            </div>
        </form>
        <input type="button" name="" value="Submit" id="button">
    </div>
</div>

<script src='static/js/jquery.min.js'></script>
<script src="static/js/script.js"></script>
</body>
</html>