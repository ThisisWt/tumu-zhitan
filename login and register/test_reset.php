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
    die("数据库连接失败: " . $conn->connect_error);
}

// 处理表单提交
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 获取表单数据
    $username = $_POST['username'];
    $new_password = $_POST['password'];
    $new_password_again = $_POST['password_again'];

    //检查用户名是否存在
    $check_user_sql = "SELECT * FROM users WHERE username = '$username'";
    $result = $conn->query($check_user_sql);
    
    if($result->num_rows>0){

        //用户名存在
        // 检查新密码是否匹配
    if ($new_password !== $new_password_again) {
        echo "两次输入的密码不匹配，请重新输入。";
        echo "<br><a href='test_reset.html'>返回密码重置页面</a><br>";
    } else {
        // 删除旧密码
        $delete_sql = "UPDATE users SET password = NULL WHERE username = '$username'";
        if ($conn->query($delete_sql) === TRUE) {
            // 插入新密码
            $hashed_password = password_hash($new_password, PASSWORD_DEFAULT);
            $insert_sql = "UPDATE users SET password = '$hashed_password' WHERE username = '$username'";
            if ($conn->query($insert_sql) === TRUE) {
                echo "密码重置成功，请返回登录页面。";
                echo "<br><a href='test_login.html'>返回登录页面</a>";
            } else {
                echo "密码重置失败: " . $conn->error;
                echo "<br><a href='test_reset.html'>返回密码重置页面</a><br>";
                echo "<br><a href='test_register.html'>返回账号注册页面</a><br>";
            }
        } else {
            echo "删除旧密码失败: " . $conn->error;
            echo "<br><a href='test_reset.html'>返回密码重置页面</a><br>";
        }
    }
}
else{
    // 用户不存在
    echo "用户不存在，请确认用户名是否正确。";
    echo"<br><a href='test_reset.html'>返回密码重置页面</a><br>";
    echo "<br><a href='test_register.html'>忘记账号，返回账号注册页面</a><br>";
}
}

// 关闭数据库连接
$conn->close();
?>
