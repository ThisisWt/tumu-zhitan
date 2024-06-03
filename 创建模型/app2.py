from flask import Flask, render_template, request, jsonify
import subprocess

app= Flask(__name__)

@app.route('/app2/')
def app2_home():
    return render_template('exe.html')

@app.route('/run_exe', methods=['POST'])
def run_exe():
    exe_path = request.form['exe_path']
    # 这里需要修改为从表单中获取文件路径的方式
    folder_path = request.files['folder_file'].filename
    
    try:
        subprocess.run([exe_path, folder_path], check=True)
        response = {'status': 'success', 'message': '程序运行成功'}
    except subprocess.CalledProcessError as e:
        response = {'status': 'error', 'message': f'运行程序时出错: {e}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
