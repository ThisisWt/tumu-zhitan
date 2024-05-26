<?php
session_start();

$response = array();

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
        $response['success'] = false;
        $response['message'] = "连接失败: " . $conn->connect_error;
    } else {
        // 查询数据库中是否有匹配的用户
        $sql = "SELECT * FROM users WHERE username = '$username'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // 用户存在，验证密码
            $user = $result->fetch_assoc();
            if (password_verify($password, $user['password'])) {
                // 密码验证成功，设置会话变量
                $_SESSION['username'] = $username;
                $response['success'] = true;
                $response['message'] = "登录成功";
            } else {
                // 密码错误
                $response['success'] = false;
                $response['message'] = "用户名或密码错误，请重试。";
            }
        } else {
            // 用户不存在
            $response['success'] = false;
            $response['message'] = "用户名或密码错误，请重试。";
        }

        // 关闭数据库连接
        $conn->close();
    }
    // 返回 JSON 数据
    echo json_encode($response);
}
?>
