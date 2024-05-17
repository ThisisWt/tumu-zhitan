<?php
header('Content-Type: application/json');

// 定义上传目录路径
$uploadDirectory = "../信息资源共享/已上传文件/"; // 替换为实际的上传目录路径

// 准备响应数组
$response = array();

if (isset($_FILES["fileToUpload"]) && $_FILES["fileToUpload"]["error"] === UPLOAD_ERR_OK) {
    // 获取上传文件的信息
    $fileName = basename($_FILES["fileToUpload"]["name"]);

    // 确保上传目录存在
    if (!is_dir($uploadDirectory)) {
        mkdir($uploadDirectory, 0777, true);
    }

    // 将文件移动到上传目录
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $uploadDirectory . $fileName)) {
        // 文件上传成功
        $response['message'] = "文件上传成功: " . htmlspecialchars($fileName);
    } else {
        // 文件上传失败
        $response['message'] = "文件上传失败，请重试。";
    }
} else {
    // 没有选择文件或文件上传过程中出错
    $response['message'] = "请选择要上传的文件。";
}

// 获取目录下的所有文件
$files = array();
if (is_dir($uploadDirectory)) {
    if ($handle = opendir($uploadDirectory)) {
        while (false !== ($entry = readdir($handle))) {
            if ($entry != "." && $entry != "..") {
                $file_extension = pathinfo($entry, PATHINFO_EXTENSION);
                $files[] = $entry . " (" . $file_extension . ")";
            }
        }
        closedir($handle);
    }
}

// 将文件列表添加到响应
$response['files'] = $files;

// 返回 JSON 格式的响应
echo json_encode($response);
?>
