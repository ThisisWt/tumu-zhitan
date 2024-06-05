from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile

app = Flask(__name__)

@app.route('/app2/')
def app2_home():
    return render_template('exe.html')

@app.route('/run_exe', methods=['POST'])
def run_exe():
    exe_file = request.files['exe_file']
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # 将上传的exe文件内容写入临时文件
            exe_content = exe_file.read()
            tmp_file.write(exe_content)
            # 获取临时文件路径
            exe_path = tmp_file.name

            # 运行exe文件
            subprocess.run([exe_path], check=True)
            response = {'status': 'success', 'message': '程序运行成功'}
    except subprocess.CalledProcessError as e:
        response = {'status': 'error', 'message': f'运行程序时出错: {e}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
