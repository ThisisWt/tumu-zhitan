<?php
// 连接数据库
$servername = "localhost"; // 数据库服务器地址
$username = "root"; // 数据库用户名
$password = "123456789"; // 数据库密码
$dbname = "one_schema"; // 数据库名

// 创建数据库连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die(json_encode(array("success" => false, "message" => "数据库连接失败: " . $conn->connect_error)));
}

// 处理表单提交
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 获取表单数据
    $username = $_POST['username'];
    $new_password = $_POST['password'];
    $new_password_again = $_POST['password_again'];

    // 检查新密码是否匹配
    if ($new_password !== $new_password_again) {
        echo json_encode(array("success" => false, "message" => "两次输入的密码不匹配，请重新输入。"));
    } else {
        // 检查用户名是否存在
        $check_user_sql = "SELECT * FROM users WHERE username = ?";
        $stmt = $conn->prepare($check_user_sql);
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            // 用户存在，更新密码
            $hashed_password = password_hash($new_password, PASSWORD_DEFAULT);
            $update_password_sql = "UPDATE users SET password = ? WHERE username = ?";
            $stmt = $conn->prepare($update_password_sql);
            $stmt->bind_param("ss", $hashed_password, $username);

            if ($stmt->execute()) {
                echo json_encode(array("success" => true, "message" => "密码重置成功，请返回登录页面。"));
            } else {
                echo json_encode(array("success" => false, "message" => "密码重置失败: " . $conn->error));
            }
        } else {
            // 用户不存在
            echo json_encode(array("success" => false, "message" => "用户不存在，请确认用户名是否正确。"));
        }
    }
}

// 关闭数据库连接
$conn->close();
?>
