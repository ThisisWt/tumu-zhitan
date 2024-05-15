<?php

// 指定文件存储的目录
$directory = '../信息资源共享/已上传文件/';

// 确保目录存在且可读
if (!is_dir($directory) || !is_readable($directory)) {
    http_response_code(500);
    exit('无法访问文件目录');
}

// 打开目录并读取文件
try {
    $files = array_diff(scandir($directory), array('.', '..')); // 排除'.'和'..'两个特殊目录
    $response = array('files' => $files);
    http_response_code(200);
} catch (Exception $e) {
    http_response_code(500);
    $response = array('error' => '读取文件列表时发生错误');
}

// 输出JSON响应
header('Content-Type: application/json');
echo json_encode($response);
exit;

?>