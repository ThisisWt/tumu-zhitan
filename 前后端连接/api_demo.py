from flask import Flask, request, jsonify, redirect, url_for
from stl import Mesh
import os
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # 允许所有域进行跨域请求

# 设置文件上传目录
UPLOAD_FOLDER = '/path/to/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 模拟用户数据库
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# 模拟材料库
materials = {
    'material1': {'density': 2.7, 'elastic_modulus': 70e9, 'yield_strength': 250e6},
    'material2': {'density': 7.9, 'elastic_modulus': 200e9, 'yield_strength': 300e6}
}



# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        if username in users and users[username]['password'] == password:
            # 登录成功，重定向到首页
            return redirect(url_for('homepage'))
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
    else:
        return jsonify({'success': False, 'message': '无效的登录方式'})


@app.route('/homepage')
def homepage():
    # 这里应该返回您的首页HTML页面
    return '<h1>Welcome to the Homepage!</h1>'



# 上传模型接口
@app.route('/upload_model', methods=['POST'])
def upload_model():
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    # 将上传的文件保存到服务器
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'message': 'File uploaded successfully', 'filename': filename})


# 编辑几何形状接口
@app.route('/edit_geometry', methods=['POST'])
def edit_geometry_shape(translate, scale, rotate):
    shape = np.random.rand(10, 3)  # 假设的原始点集

    # 缩放
    scaled_shape = shape * scale

    # 平移
    translated_shape = scaled_shape + np.array(translate)

    # 旋转
    angle = np.deg2rad(rotate['angle'])  # 角度转弧度
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    rotation_matrix = np.array([
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ])
    rotated_shape = np.dot(translated_shape, rotation_matrix.T)

    return rotated_shape.tolist()


def edit_geometry():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    transform = data.get('transform', {})
    translate = transform.get('translate', [0, 0, 0])
    scale = transform.get('scale', 1)
    rotate = transform.get('rotate', {'angle': 0, 'axis': [0, 1, 0]})

    try:
        result = edit_geometry_shape(translate, scale, rotate)
        return jsonify({'success': True, 'message': 'Geometry edited successfully', 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 设置材料属性接口
@app.route('/set_material', methods=['POST'])
def set_material():
    material_name = request.json['material_name']
    if material_name in materials:
        # 如果材料存在于材料库中，可以将其属性应用到几何体中
        return jsonify({'success': True, 'message': '材料属性设置成功'})
    else:
        return jsonify({'success': False, 'message': '未找到该材料'})


# 调整分析需求接口
@app.route('/adjust_analysis', methods=['POST'])
def adjust_analysis():
    # 这里可以添加相应的分析需求调整处理逻辑，模拟直接返回成功消息
    return jsonify({'success': True, 'message': '分析需求调整成功'})


# 模型查看和验证接口
@app.route('/view_and_verify_model', methods=['GET'])
def view_and_verify_model():
    # 这里可以返回模型的三维图形数据，供前端展示和交互
    return jsonify({'success': True, 'message': '模型数据获取成功'})


# DXF转换为STL接口
@app.route('/convert_dxf_to_stl', methods=['POST'])
def convert_dxf_to_stl():
    # 获取上传的DXF文件路径
    dxf_file_path = request.json['dxf_file_path']

    # 设置STL输出路径
    stl_file_path = "/path/to/output/file.stl"  # 这里需要设置输出路径

    try:
        # 读取DXF文件并转换为STL
        stl_mesh = Mesh.from_file(dxf_file_path)
        stl_mesh.save(stl_file_path)

        return jsonify({'success': True, 'message': 'DXF文件转换为STL成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
