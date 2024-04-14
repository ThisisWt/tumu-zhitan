import sys
import pyvista as pv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from pyvistaqt import QtInteractor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('结构模型输入与编辑')
        self.setGeometry(100, 100, 800, 600)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建PyVista绘图控件
        self.plotter = QtInteractor(self)
        self.plotter.set_background('white')  # 设置背景为白色
        layout.addWidget(self.plotter)

        # 创建一个按钮用于导入模型
        btn_import = QPushButton("导入模型")
        btn_import.clicked.connect(self.import_model)
        layout.addWidget(btn_import, alignment=Qt.AlignTop)

    def import_model(self):
        # 弹出文件选择对话框
        filepath, _ = QFileDialog.getOpenFileName(self, "选择3D模型文件", "", "Mesh Files (*.stl *.ply *.obj);;All Files (*)")
        if filepath:
            self.load_model(filepath)

    def load_model(self, filepath):
        # 读取模型并显示
        mesh = pv.read(filepath)
        self.plotter.add_mesh(mesh, color='lightblue', show_edges=True)  # 显示网格边界
        self.plotter.reset_camera()  # 重置摄像机视角以适应新加载的模型

# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

import FreeCAD
import Import
import Mesh

def convert_dxf_to_stl(dxf_file, stl_file):
    # 创建一个新的文档
    doc = FreeCAD.newDocument()

    # 导入DXF文件
    Import.insert(dxf_file, doc.Name)

    # 将所有可视对象导出为STL
    objs = [obj for obj in doc.Objects if hasattr(obj, 'ViewObject') and obj.ViewObject.Visibility]
    Mesh.export(objs, stl_file)
    print(f"Exported STL to {stl_file}")

    # 关闭文档
    FreeCAD.closeDocument(doc.Name)

# 示例用法
dxf_file_path = "/path/to/your/file.dxf"
stl_file_path = "/path/to/output/file.stl"
convert_dxf_to_stl(dxf_file_path, stl_file_path)
import sys
sys.path.append('/usr/share/freecad/lib')
