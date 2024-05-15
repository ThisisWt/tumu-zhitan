<?php
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $directory = '../信息资源共享/已上传文件/'; // 指定目录
    $filepath = $directory . $file;

    if (file_exists($filepath)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename=' . basename($filepath));
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($filepath));
        ob_clean();
        flush();
        readfile($filepath);
        exit;
    } else {
        echo "文件不存在。";
    }
} else {
    echo "未指定文件。";
}
?>
