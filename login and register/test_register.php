<?php
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

    // 检查用户名是否已经存在
    $check_query = "SELECT * FROM users WHERE username = '$username'";
    $check_result = $conn->query($check_query);

    if ($check_result->num_rows > 0) {
        // 用户名已存在
        echo "用户名已被使用，请选择其他用户名。";
    } else {
      // 使用参数化查询插入新用户信息到数据库，同时对密码进行哈希处理
      $insert_query = "INSERT INTO users (username, password) VALUES (?, ?)";
      $stmt = $conn->prepare($insert_query);

      // 对密码进行哈希处理
      $hashed_password = password_hash($password, PASSWORD_DEFAULT);

      // 绑定参数并执行插入操作
      $stmt->bind_param("ss", $username, $hashed_password);
      if ($stmt->execute()) {
          // 注册成功
          echo "注册成功！";
          echo "<br><a href='test_login.html'>请重新登录</a>";
      } else {
          // 注册失败
          echo "注册失败，请稍后重试。";
      }
    }

    // 关闭数据库连接
    $conn->close();
}
?>