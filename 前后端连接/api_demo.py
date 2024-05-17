from flask import Flask, request, jsonify, redirect, url_for
from stl import Mesh
import os
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Set file upload directory
UPLOAD_FOLDER = '/path/to/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mock user database
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# Mock materials library
materials = {
    'material1': {'density': 2.7, 'elastic_modulus': 70e9, 'yield_strength': 250e6},
    'material2': {'density': 7.9, 'elastic_modulus': 200e9, 'yield_strength': 300e6}
}

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        if username in users and users[username]['password'] == password:
            # Login successful, redirect to homepage
            return redirect(url_for('homepage'))
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    else:
        return jsonify({'success': False, 'message': 'Invalid login credentials'})

@app.route('/homepage')
def homepage():
    # Return your homepage HTML here
    return '<h1>Welcome to the Homepage!</h1>'

# Upload model endpoint
@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'message': 'File uploaded successfully', 'filename': filename})

# Geometry editing helper function
def edit_geometry_shape(translate, scale, rotate):
    shape = np.random.rand(10, 3)  # Mock original point set

    # Scaling
    scaled_shape = shape * scale

    # Translation
    translated_shape = scaled_shape + np.array(translate)

    # Rotation (around Z-axis for simplicity)
    angle = np.deg2rad(rotate['angle'])
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    rotation_matrix = np.array([
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ])
    rotated_shape = np.dot(translated_shape, rotation_matrix.T)

    return rotated_shape.tolist()

# Edit geometry endpoint
@app.route('/edit_geometry', methods=['POST'])
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

# Set material properties endpoint
@app.route('/set_material', methods=['POST'])
def set_material():
    material_name = request.json.get('material_name')
    if material_name in materials:
        return jsonify({'success': True, 'message': 'Material properties set successfully'})
    else:
        return jsonify({'success': False, 'message': 'Material not found'})

# Adjust analysis requirements endpoint
@app.route('/adjust_analysis', methods=['POST'])
def adjust_analysis():
    return jsonify({'success': True, 'message': 'Analysis requirements adjusted successfully'})

# View and verify model endpoint
@app.route('/view_and_verify_model', methods=['GET'])
def view_and_verify_model():
    return jsonify({'success': True, 'message': 'Model data retrieved successfully'})

# Convert DXF to STL endpoint
@app.route('/convert_dxf_to_stl', methods=['POST'])
def convert_dxf_to_stl():
    dxf_file_path = request.json.get('dxf_file_path')
    stl_file_path = "/path/to/output/file.stl"  # Set output path

    try:
        stl_mesh = Mesh.from_file(dxf_file_path)
        stl_mesh.save(stl_file_path)
        return jsonify({'success': True, 'message': 'DXF file converted to STL successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
