from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess

import os
import logging
from tkinter import Tk
from tkinter.filedialog import askdirectory

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})  # 启用CORS，允许所有来源

app.config['SERVER_NAME'] = 'localhost:5001'
app.config['EXE_PATH'] = os.path.join(os.getcwd(), 'Instant-NGP-for-RTX-3000-and-4000', 'instant-ngp.exe')
# 配置日志
logging.basicConfig(level=logging.INFO)

def choose_directory():
    root = Tk()
    root.withdraw()
    directory = askdirectory()
    root.destroy()
    return directory
@app.route('/')
def app2_home():
    return app.send_static_file('exe.html')

@app.route('/run_exe', methods=['POST'])
def run_exe():
    exe_path = app.config['EXE_PATH']
    if not os.path.exists(exe_path):
        app.logger.error('文件不存在')
        return jsonify({'message': '文件不存在'}), 400

    # 选择文件夹
    directory = choose_directory()
    if not directory:
        app.logger.error('没有选择文件夹')
        return jsonify({'message': '没有选择文件夹'}), 400

    try:
        # 运行exe文件，并捕获输出和错误信息
        command = f'"{exe_path}" "{directory}"'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        app.logger.info(f'程序运行成功，输出: {result.stdout}, 错误: {result.stderr}')
        return jsonify({'message': '程序运行成功', 'output': result.stdout, 'error': result.stderr})

    except Exception as e:
        app.logger.error(f'程序运行失败: {str(e)}')
        return jsonify({'message': f'程序运行失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)