from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import logging

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5001'

# 配置日志
logging.basicConfig(level=logging.INFO)

@app.route('/')
def app2_home():
    return render_template('exe.html')

@app.route('/run_exe', methods=['POST'])
def run_exe():
    exe_file = request.files.get('exe_file')
    
    if exe_file is None:
        return jsonify({'status': 'error', 'message': '未上传文件'}), 400
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp_file:
            # 将上传的exe文件内容写入临时文件
            exe_content = exe_file.read()
            tmp_file.write(exe_content)
            tmp_file_path = tmp_file.name  # 获取临时文件路径
            tmp_file.close()  # 关闭文件以便后续使用

        logging.info(f"临时文件路径: {tmp_file_path}")

        # 检查文件是否存在
        if not os.path.exists(tmp_file_path):
            logging.error(f"临时文件未找到: {tmp_file_path}")
            return jsonify({'status': 'error', 'message': '临时文件未找到'}), 500

        # 运行exe文件并捕获输出
        result = subprocess.run(tmp_file_path, check=True, capture_output=True, text=True, shell=True)
        logging.info(f"程序输出: {result.stdout}")

        response = {'status': 'success', 'message': '程序运行成功', 'output': result.stdout}
    except subprocess.CalledProcessError as e:
        logging.error(f"运行程序时出错: {e}")
        response = {'status': 'error', 'message': f'运行程序时出错: {e}', 'output': e.output, 'stderr': e.stderr}
    except Exception as e:
        logging.error(f"其他错误: {e}")
        response = {'status': 'error', 'message': f'其他错误: {e}'}
    finally:
        # 删除临时文件
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            logging.info(f"删除临时文件: {tmp_file_path}")

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
