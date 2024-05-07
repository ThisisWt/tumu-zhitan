from flask import Flask, request, jsonify, render_template, send_from_directory
import tkinter as tk
from tkinter import filedialog
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)


class StructuralModelingApp:
    def __init__(self):
        self.filename = None

    def process_action(self, action, dimensions):
        try:
            print("Action:", action)
            print("Dimensions:", dimensions)
            if action == '矩形梁' and len(dimensions) == 3:
                self.plot_beam(*map(float, dimensions))
                return "矩形梁绘制完成"
            elif action == '圆柱体' and len(dimensions) == 2:
                self.plot_cylinder(*map(float, dimensions))
                return "圆柱体绘制完成"
            elif action == '球体' and len(dimensions) == 1:
                self.plot_sphere(float(dimensions[0]))
                return "球体绘制完成"
            elif action.startswith('导入') and action.endswith('DXF'):
                return self.import_dxf()
            elif self.filename and action.endswith('DXF'):
                return getattr(self, action.lower().replace(' ', '_'))()
            else:
                return "无法处理的操作"
        except ValueError as e:
            print("Error:", e)
            return "参数错误，请检查输入值"

    def plot_beam(self, length, width, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z, color='blue')
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        plt.show()

    def plot_cylinder(self, radius, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        z = np.linspace(0, height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius * np.cos(theta_grid)
        y_grid = radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color='red')
        ax.set_xlabel('Radius')
        ax.set_ylabel('Height')
        plt.show()

    def plot_sphere(self, radius):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='green')
        ax.set_xlabel('Radius')
        plt.show()

    def import_dxf(self):
        self.filename = filedialog.askopenfilename(title="选择DXF模型文件", filetypes=[("DXF files", "*.dxf")])
        if self.filename:
            return f"文件已加载: {self.filename}"
        else:
            return "未选择任何文件"

    def analyze_dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        entity_types = {}
        for entity in msp:
            entity_type = entity.dxftype()
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        result = "分析结果:\n"
        for entity_type, count in entity_types.items():
            result += f"{entity_type}: {count}\n"
        return result

    def modify_dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        for entity in msp.query('LINE'):
            entity.dxf.color = 1
        doc.saveas('modified_dxf.dxf')
        return "修改已保存到 'modified_dxf.dxf'"

    def visualize_dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for entity in msp.query('LINE'):
            start = entity.dxf.start
            end = entity.dxf.end
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], 'gray')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def export_dxf(self):
        doc = ezdxf.readfile(self.filename)
        doc.saveas('exported_dxf.dxf')
        return "文件已导出为 'exported_dxf.dxf'"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    data = request.json
    action = data.get('action')
    dimensions = data.get('dimensions')

    if action and dimensions:
        app_instance = StructuralModelingApp()
        result = app_instance.process_action(action, dimensions)

        if result:
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to process request.'}), 500
    else:
        return jsonify({'error': 'Action and dimensions are required.'}), 400


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
