from flask import Flask, request, jsonify
from stl import Mesh
import os

app = Flask(__name__)

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

# 模拟验证码数据库
verification_codes = {}


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    if 'username' in request.json:  # 用户名、密码登录
        username = request.json['username']
        password = request.json['password']
        if username in users and users[username]['password'] == password:
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
    elif 'email' in request.json:  # 邮箱、密码登录
        email = request.json['email']
        password = request.json['password']
        verification_code = request.json['verification_code']
        if verification_code != verification_codes.get(email):
            return jsonify({'success': False, 'message': '验证码错误'})
        if any(user['email'] == email and user['password'] == password for user in users.values()):
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '用户名、邮箱或密码错误'})
    else:
        return jsonify({'success': False, 'message': '无效的登录方式'})


# 发送验证码接口
@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.json['email']

    # 此处可以生成验证码并发送到用户邮箱，这里简单模拟将验证码设置为 1234
    verification_codes[email] = '1234'

    return jsonify({'success': True, 'message': '验证码已发送'})


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
def edit_geometry():
    # 这里可以添加相应的编辑处理逻辑，模拟直接返回成功消息
    return jsonify({'success': True, 'message': '几何形状编辑成功'})


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
