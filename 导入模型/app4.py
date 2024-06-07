# app.py
from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 上传模型文件的存储目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SERVER_NAME'] = 'localhost:5003'

@app.route('/')
def app4_home():
    return render_template('index.html')

# 处理文件上传请求
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

# 提供已上传的模型文件
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
