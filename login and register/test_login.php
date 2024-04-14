<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 处理表单提交的用户名和密码
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 建立数据库连接
    $hostname = 'localhost';
    $db_username = 'root';
    $db_password = '123456789';
    $database = 'one_schema';

    $conn = new mysqli($hostname, $db_username, $db_password, $database);

    // 检查连接是否成功
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }

    // 查询数据库中是否有匹配的用户
    $sql = "SELECT * FROM users WHERE username = '$username'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // 用户存在，验证密码
        $user = $result->fetch_assoc();
        if (password_verify($password, $user['password'])) {
            // 密码验证成功，设置会话变量
            $_SESSION['username'] = $username;
            // 重定向到受保护的页面
            header('Location: ../土木智探前端/首页.html');
            exit;
        } else {
            // 密码错误
            echo "用户名或密码错误，请重试。";
            echo "<br><a href='test_login.html'>返回登录页面</a>";
        }
    } else {
        // 用户不存在
        echo "用户名或密码错误，请重试。";
        echo "<br><a href='test_login.html'>返回登录页面</a>";
    }

    // 关闭数据库连接
    $conn->close();
}
?>