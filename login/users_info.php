<?php
// 模拟用户信息（实际应用中应该从数据库或其他存储中获取）
$valid_username = "john";
$valid_email = "john@example.com";
$valid_password = "password123";

// 检查是否是 POST 请求
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 获取表单提交的数据
    $username = $_POST["name"];
    $email = $_POST["email"];
    $password = $_POST["password"];
    $captcha = $_POST["captcha"]; // 此处应添加后端验证

    // 验证用户名、邮箱和密码
    if ($username === $valid_username && $email === $valid_email && $password === $valid_password) {
        // 登录成功
        echo "<h2>登录成功！</h2>";
        echo "欢迎，" . htmlspecialchars($username) . "！";
    } else {
        // 登录失败
        echo "<h2>登录失败！</h2>";
        echo "请检查您输入的信息是否正确。";
    }
}
?>
