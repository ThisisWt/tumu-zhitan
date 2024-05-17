<?php
$uploadDir = "../信息资源共享/已上传文件/";

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['file'])) {
    $fileName = $_GET['file'];

    // 检查文件是否存在
    if (file_exists($uploadDir . $fileName)) {
        echo json_encode(array('found' => true));
    } else {
        echo json_encode(array('found' => false));
    }
} else {
    $response = array('message' => '无效的请求。');
    http_response_code(400);
    echo json_encode($response);
}
?>
