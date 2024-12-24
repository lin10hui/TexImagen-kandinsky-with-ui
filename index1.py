import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QMessageBox, QFrame
import subprocess

class TexImagenKandinsky(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TexImagen-kandinsky")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Top bar with buttons
        self.top_bar = QFrame(self)
        self.top_bar.setFrameShape(QFrame.HLine)
        self.top_bar.setFrameShadow(QFrame.Sunken)
        self.top_bar_layout = QHBoxLayout(self.top_bar)

        self.init_button = QPushButton("初始化", self.top_bar)
        self.init_button.setMinimumWidth(80)
        self.init_button.setStyleSheet("""
            background-color: lightgray; 
            border-radius: 10px; 
            padding: 5px;
            margin-right: 10px;
        """)
        self.init_button.setMouseTracking(True)
        self.init_button.setStyleSheet(self.init_button.styleSheet() + "QPushButton:hover { background-color: gray; }")
        self.init_button.clicked.connect(self.confirm_initialize)

        self.exit_button = QPushButton("退出", self.top_bar)
        self.exit_button.setMinimumWidth(80)
        self.exit_button.setStyleSheet("""
            background-color: lightgray; 
            border-radius: 10px; 
            padding: 5px;
        """)
        self.exit_button.setMouseTracking(True)
        self.exit_button.setStyleSheet(self.exit_button.styleSheet() + "QPushButton:hover { background-color: gray; }")
        self.exit_button.clicked.connect(self.close)

        self.top_bar_layout.addWidget(self.init_button)
        self.top_bar_layout.addWidget(self.exit_button)
        self.top_bar_layout.addStretch()
        main_layout.addWidget(self.top_bar)

        # Separation line
        separation_line = QFrame(self)
        separation_line.setFrameShape(QFrame.HLine)
        separation_line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separation_line)

        # Bottom layout
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        # Navigation buttons
        self.nav_widget = QWidget(self)
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)  # Set contents margins to 0 for compactness
        self.nav_layout.setSpacing(5)  # Reduce spacing between buttons

        # Adding buttons with compact spacing
        self.nav_buttons = []
        button_names = ["图像生成", "图像融合", "图像修复"]
        for name in button_names:
            button = QPushButton(name, self.nav_widget)
            button.setMinimumWidth(80)
            button.setStyleSheet("""
                background-color: lightgray; 
                border-radius: 10px; 
                padding: 5px;
                margin-bottom: 2px;  /* Reduced margin for compactness */
            """)
            button.setMouseTracking(True)
            button.setStyleSheet(button.styleSheet() + "QPushButton:hover { background-color: gray; }")
            button.clicked.connect(lambda _, x=len(self.nav_buttons): self.display_page(x))
            self.nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        bottom_layout.addWidget(self.nav_widget)

        # Separation line
        separation_line = QFrame(self)
        separation_line.setFrameShape(QFrame.VLine)
        separation_line.setFrameShadow(QFrame.Sunken)
        bottom_layout.addWidget(separation_line)

        # Stacked widget for pages
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        bottom_layout.addWidget(self.stackedWidget)

        self.initUI()
        self.initialized = False

    def initUI(self):
        # 图像生成页面
        self.page_generation = QWidget()
        self.stackedWidget.addWidget(self.page_generation)
        self.setup_generation_page()

        # 图像融合页面
        self.page_mixing = QWidget()
        self.stackedWidget.addWidget(self.page_mixing)
        self.setup_mixing_page()

        # 图像修复页面
        self.page_inpainting = QWidget()
        self.stackedWidget.addWidget(self.page_inpainting)
        self.setup_inpainting_page()

    def display_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        for i, button in enumerate(self.nav_buttons):
            if i == index:
                button.setEnabled(False)
                button.setStyleSheet("""
                    background-color: darkgray; 
                    border-radius: 10px; 
                    padding: 5px;
                """)
            else:
                button.setEnabled(True)
                button.setStyleSheet("""
                    background-color: lightgray; 
                    border-radius: 10px; 
                    padding: 5px;
                """)

    def confirm_initialize(self):
        if not self.initialized:
            reply = QMessageBox.question(self, '确认初始化',
                '您是否确定初始化？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.initialize_kandinsky()
                self.initialized = True

    def initialize_kandinsky(self):
        subprocess.run(["python", "Kandinsky-2-main/init.py"])

    def setup_generation_page(self):
        layout = QVBoxLayout(self.page_generation)

        desc_layout = QHBoxLayout()
        desc_label = QLabel("图像描述：", self.page_generation)
        self.textEdit_gen = QTextEdit(self.page_generation)
        self.textEdit_gen.setPlaceholderText("输入图像描述")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.textEdit_gen)
        layout.addLayout(desc_layout)

        self.pathButton_gen = QPushButton("选择文件保存位置", self.page_generation)
        self.pathButton_gen.clicked.connect(self.select_save_path_gen)
        layout.addWidget(self.pathButton_gen)

        self.pathLabel_gen = QLabel("未选择路径", self.page_generation)
        layout.addWidget(self.pathLabel_gen)

        self.generateButton_gen = QPushButton("生成", self.page_generation)
        self.generateButton_gen.clicked.connect(self.generate_image)
        layout.addWidget(self.generateButton_gen)

    def select_save_path_gen(self):
        self.save_path_gen, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "", "Images (*.png *.jpg)")
        self.pathLabel_gen.setText(self.save_path_gen if self.save_path_gen else "未选择路径")

    def generate_image(self):
        text = self.textEdit_gen.toPlainText()
        path = self.save_path_gen
        if not text:
            self.show_error_message("请填写图像描述")
            return
        if not path:
            self.show_error_message("请选择文件保存位置")
            return
        subprocess.run(["python", "Kandinsky-2-main/T2I.py", text, path])

    def setup_mixing_page(self):
        layout = QVBoxLayout(self.page_mixing)

        desc_layout1 = QHBoxLayout()
        desc_label1 = QLabel("图像描述1：", self.page_mixing)
        self.textEdit_mix1 = QTextEdit(self.page_mixing)
        self.textEdit_mix1.setPlaceholderText("输入图像描述1")
        desc_layout1.addWidget(desc_label1)
        desc_layout1.addWidget(self.textEdit_mix1)
        layout.addLayout(desc_layout1)

        desc_layout2 = QHBoxLayout()
        desc_label2 = QLabel("图像描述2：", self.page_mixing)
        self.textEdit_mix2 = QTextEdit(self.page_mixing)
        self.textEdit_mix2.setPlaceholderText("输入图像描述2")
        desc_layout2.addWidget(desc_label2)
        desc_layout2.addWidget(self.textEdit_mix2)
        layout.addLayout(desc_layout2)

        self.pathButton_mix = QPushButton("选择文件保存位置", self.page_mixing)
        self.pathButton_mix.clicked.connect(self.select_save_path_mix)
        layout.addWidget(self.pathButton_mix)

        self.pathLabel_mix = QLabel("未选择路径", self.page_mixing)
        layout.addWidget(self.pathLabel_mix)

        self.generateButton_mix = QPushButton("生成", self.page_mixing)
        self.generateButton_mix.clicked.connect(self.mix_images)
        layout.addWidget(self.generateButton_mix)

    def select_save_path_mix(self):
        self.save_path_mix, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "", "Images (*.png *.jpg)")
        self.pathLabel_mix.setText(self.save_path_mix if self.save_path_mix else "未选择路径")

    def mix_images(self):
        text1 = self.textEdit_mix1.toPlainText()
        text2 = self.textEdit_mix2.toPlainText()
        path = self.save_path_mix
        if not text1:
            self.show_error_message("请填写图像描述1")
            return
        if not text2:
            self.show_error_message("请填写图像描述2")
            return
        if not path:
            self.show_error_message("请选择文件保存位置")
            return
        subprocess.run(["python", "Kandinsky-2-main/mixing.py", text1, text2, path])

    def setup_inpainting_page(self):
        layout = QVBoxLayout(self.page_inpainting)

        desc_layout = QHBoxLayout()
        desc_label = QLabel("图像描述：", self.page_inpainting)
        self.textEdit_inpaint = QTextEdit(self.page_inpainting)
        self.textEdit_inpaint.setPlaceholderText("输入图像描述")
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.textEdit_inpaint)
        layout.addLayout(desc_layout)

        self.pathButton_inpaint1 = QPushButton("选择修复文件位置", self.page_inpainting)
        self.pathButton_inpaint1.clicked.connect(self.select_repair_path_inpaint)
        layout.addWidget(self.pathButton_inpaint1)

        self.pathLabel_inpaint1 = QLabel("未选择路径", self.page_inpainting)
        layout.addWidget(self.pathLabel_inpaint1)

        self.pathButton_inpaint2 = QPushButton("选择文件保存位置", self.page_inpainting)
        self.pathButton_inpaint2.clicked.connect(self.select_save_path_inpaint)
        layout.addWidget(self.pathButton_inpaint2)

        self.pathLabel_inpaint2 = QLabel("未选择路径", self.page_inpainting)
        layout.addWidget(self.pathLabel_inpaint2)

        self.generateButton_inpaint = QPushButton("生成", self.page_inpainting)
        self.generateButton_inpaint.clicked.connect(self.inpaint_image)
        layout.addWidget(self.generateButton_inpaint)

    def select_repair_path_inpaint(self):
        self.repair_path_inpaint, _ = QFileDialog.getOpenFileName(self, "选择修复文件", "", "Images (*.png *.jpg)")
        self.pathLabel_inpaint1.setText(self.repair_path_inpaint if self.repair_path_inpaint else "未选择路径")

    def select_save_path_inpaint(self):
        self.save_path_inpaint, _ = QFileDialog.getSaveFileName(self, "选择保存位置", "", "Images (*.png *.jpg)")
        self.pathLabel_inpaint2.setText(self.save_path_inpaint if self.save_path_inpaint else "未选择路径")

    def inpaint_image(self):
        text = self.textEdit_inpaint.toPlainText()
        repair_path = self.repair_path_inpaint
        save_path = self.save_path_inpaint
        if not text:
            self.show_error_message("请填写图像描述")
            return
        if not repair_path:
            self.show_error_message("请选择修复文件位置")
            return
        if not save_path:
            self.show_error_message("请选择文件保存位置")
            return
        subprocess.run(["python", "Kandinsky-2-main/rec.py", text, repair_path, save_path])

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("错误")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TexImagenKandinsky()
    window.show()
    sys.exit(app.exec_())