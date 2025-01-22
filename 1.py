from PIL import Image
import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                            QSpinBox, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 如果不是打包环境，就使用当前路径
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class ImageConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('图片转换工具')
        self.setFixedSize(400, 300)
        
        # 设置程序图标
        icon_path = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 添加版本信息标签
        version_label = QLabel('版本: 2025/1/22-01')
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # 右对齐
        layout.addWidget(version_label)
        
        # 文件选择部分
        file_layout = QHBoxLayout()
        self.file_label = QLabel('未选择文件')
        self.select_button = QPushButton('选择图片(&O)')
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.select_button)
        
        # 尺寸设置部分
        size_layout = QHBoxLayout()
        width_label = QLabel('宽度(&W):')
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.width_spin.setValue(800)
        width_label.setBuddy(self.width_spin)  # 设置快捷键关联
        size_layout.addWidget(width_label)
        size_layout.addWidget(self.width_spin)
        
        height_label = QLabel('高度(&H):')
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.height_spin.setValue(600)
        height_label.setBuddy(self.height_spin)  # 设置快捷键关联
        size_layout.addWidget(height_label)
        size_layout.addWidget(self.height_spin)
        
        # 格式选择部分
        format_layout = QHBoxLayout()
        format_label = QLabel('输出格式(&F):')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['PNG', 'JPEG', 'BMP', 'GIF', 'ICO', 'WEBP'])
        format_label.setBuddy(self.format_combo)  # 设置快捷键关联
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        
        # 转换按钮
        self.convert_button = QPushButton('转换并保存(&S)')
        self.convert_button.clicked.connect(self.convert_image)
        
        # 添加所有部件到主布局
        layout.addLayout(file_layout)
        layout.addLayout(size_layout)
        layout.addLayout(format_layout)
        layout.addWidget(self.convert_button)
        
        self.input_path = None
        
    def select_file(self):
        # 获取桌面路径
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            desktop_path,  # 设置默认打开位置为桌面
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if file_name:
            self.input_path = file_name
            self.file_label.setText(os.path.basename(file_name))
            
    def convert_image(self):
        if not self.input_path:
            QMessageBox.warning(self, '警告', '请先选择图片文件！')
            return
            
        try:
            # 打开原始图片
            img = Image.open(self.input_path)
            
            # 获取设置的尺寸
            output_size = (self.width_spin.value(), self.height_spin.value())
            
            # 调整图片尺寸
            resized_img = img.resize(output_size, Image.Resampling.LANCZOS)
            
            # 如果是 ICO 格式，需要确保图片是 RGBA 模式
            output_format = self.format_combo.currentText()
            if output_format == 'ICO':
                if resized_img.mode != 'RGBA':
                    resized_img = resized_img.convert('RGBA')
            
            # 获取桌面路径
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            
            # 构建输出文件路径（使用分辨率作为文件名）
            output_filename = f'{output_size[0]}x{output_size[1]}.{output_format.lower()}'
            output_path = os.path.join(desktop_path, output_filename)
            
            # 保存转换后的图片
            resized_img.save(output_path, format=output_format)
            
            QMessageBox.information(self, '成功', f'图片已成功保存到: {output_path}')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'处理图片时出错: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用程序图标
    app_icon = QIcon(resource_path("icon.ico"))
    app.setWindowIcon(app_icon)
    
    window = ImageConverterGUI()
    window.show()
    sys.exit(app.exec())
