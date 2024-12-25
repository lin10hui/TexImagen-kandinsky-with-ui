import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QMessageBox, QFrame, QRadioButton, QLineEdit, QDialog
from PyQt5.QtGui import QPalette, QBrush
import subprocess
from connect import RemoteServerConnection

class TexImagenKandinsky(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TexImagen-kandinsky")
        self.setGeometry(100, 100, 1200, 800)

        # 设置背景图片自适应铺满整个窗口
        self.set_background()

        # 主布局
        main_layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 顶部工具栏
        self.top_bar = QFrame(self)
        self.top_bar.setFrameShape(QFrame.HLine)
        self.top_bar.setFrameShadow(QFrame.Sunken)
        self.top_bar_layout = QHBoxLayout(self.top_bar)

        # 初始化按钮
        self.init_button = QPushButton("初始化", self.top_bar)
        self.init_button.setMinimumWidth(100)
        self.init_button.setFixedHeight(50)
        self.init_button.setStyleSheet(self.get_button_style())
        self.init_button.clicked.connect(self.confirm_initialize)

        # 退出按钮
        self.exit_button = QPushButton("退出", self.top_bar)
        self.exit_button.setMinimumWidth(100)
        self.exit_button.setFixedHeight(50)
        self.exit_button.setStyleSheet(self.get_button_style())
        self.exit_button.clicked.connect(self.close)

        # 设置按钮
        self.settings_button = QPushButton("设置", self.top_bar)
        self.settings_button.setMinimumWidth(100)
        self.settings_button.setFixedHeight(50)
        self.settings_button.setStyleSheet(self.get_button_style())
        self.settings_button.clicked.connect(self.do_nothing)

        # 帮助按钮
        self.help_button = QPushButton("帮助", self.top_bar)
        self.help_button.setMinimumWidth(100)
        self.help_button.setFixedHeight(50)
        self.help_button.setStyleSheet(self.get_button_style())
        self.help_button.clicked.connect(self.show_help_info)

        # 将按钮添加到顶部布局
        self.top_bar_layout.addWidget(self.init_button)
        self.top_bar_layout.addWidget(self.exit_button)
        self.top_bar_layout.addWidget(self.settings_button)
        self.top_bar_layout.addWidget(self.help_button)
        self.top_bar_layout.addStretch()
        main_layout.addWidget(self.top_bar)

        # 顶部与中部的分隔线
        separation_line_top = QFrame(self)
        separation_line_top.setFrameShape(QFrame.HLine)
        separation_line_top.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separation_line_top)

        # 中部布局
        middle_layout = QHBoxLayout()
        main_layout.addLayout(middle_layout)

        # 中左导航按钮区域
        self.nav_widget = QWidget(self)
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(10)

        # 添加导航按钮
        self.nav_buttons = []
        button_names = ["图像生成", "图像融合", "图像修复"]
        for name in button_names:
            button = QPushButton(name, self.nav_widget)
            button.setMinimumWidth(80)
            button.setFixedHeight(50)
            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(lambda _, x=len(self.nav_buttons): self.display_page(x))
            self.nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        # 中左区域占 20%
        middle_layout.addWidget(self.nav_widget, stretch=1)

        # 中左与中右之间的分隔线
        separation_line_middle = QFrame(self)
        separation_line_middle.setFrameShape(QFrame.VLine)
        separation_line_middle.setFrameShadow(QFrame.Sunken)
        middle_layout.addWidget(separation_line_middle)

        # 中右内容区域
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        middle_layout.addWidget(self.stackedWidget, stretch=4)

        # 初始化页面
        self.initUI()

        # 中部与底部的分隔线
        separation_line_bottom = QFrame(self)
        separation_line_bottom.setFrameShape(QFrame.HLine)
        separation_line_bottom.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separation_line_bottom)

        # 底部布局
        self.bottom_layout = QHBoxLayout()
        main_layout.addLayout(self.bottom_layout)

        # 本地运行和服务器运行的单选按钮
        self.local_run_radio = QRadioButton("本地运行")
        self.server_run_radio = QRadioButton("服务器运行")
        self.local_run_radio.setChecked(True)
        self.bottom_layout.addWidget(self.local_run_radio)
        self.bottom_layout.addWidget(self.server_run_radio)

        # 连接服务器按钮
        self.connect_button = QPushButton("连接服务器")
        self.connect_button.clicked.connect(self.show_connection_dialog)
        self.bottom_layout.addWidget(self.connect_button)

        # 设置顶部和底部的高度
        self.top_bar.setFixedHeight(70)
        self.bottom_layout.setSpacing(20)

    def set_background(self):
        """设置背景图片自适应铺满整个窗口"""
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QtGui.QPixmap('img/background.png').scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 0.8);
            }
            QPushButton:disabled {
                background-color: rgba(150, 150, 150, 0.8);
            }
        """

    def initUI(self):
        # 初始化页面
        self.page_generation = QWidget()
        self.stackedWidget.addWidget(self.page_generation)
        self.setup_generation_page()

        self.page_mixing = QWidget()
        self.stackedWidget.addWidget(self.page_mixing)
        self.setup_mixing_page()

        self.page_inpainting = QWidget()
        self.stackedWidget.addWidget(self.page_inpainting)
        self.setup_inpainting_page()

    def show_help_info(self):
        """显示帮助信息"""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("帮助")
        help_dialog.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(help_dialog)

        help_label = QLabel("<b>请联系邮箱: 1749057435@qq.com</b>", help_dialog)
        layout.addWidget(help_label)

        copy_button = QPushButton("复制邮箱", help_dialog)
        copy_button.clicked.connect(self.copy_email_to_clipboard)
        layout.addWidget(copy_button)

        help_dialog.exec_()

    def copy_email_to_clipboard(self):
        """复制邮箱到剪切板"""
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText("1749057435@qq.com")
        QMessageBox.information(self, "复制成功", "邮箱已复制到剪切板！")

    def do_nothing(self):
        """设置按钮点击无反应"""
        pass

    def show_connection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("连接服务器")
        dialog.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(dialog)

        ip_label = QLabel("服务器 IP 地址:", dialog)
        self.ip_input = QLineEdit(dialog)
        self.ip_input.setStyleSheet("border-radius: 10px;")  # 圆角输入框
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)

        username_label = QLabel("用户名:", dialog)
        self.username_input = QLineEdit(dialog)
        self.username_input.setStyleSheet("border-radius: 10px;")  # 圆角输入框
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        password_label = QLabel("密码:", dialog)
        self.password_input = QLineEdit(dialog)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("border-radius: 10px;")  # 圆角输入框
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        test_button = QPushButton("测试连接", dialog)
        test_button.clicked.connect(self.test_connection)
        layout.addWidget(test_button)

        confirm_button = QPushButton("确认", dialog)
        confirm_button.clicked.connect(lambda: self.connect_to_server(dialog))
        layout.addWidget(confirm_button)

        dialog.exec_()

    def test_connection(self):
        ip = self.ip_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        self.remote_connection = RemoteServerConnection(ip, username, password)
        if self.remote_connection.connect():
            QMessageBox.information(self, "连接成功", "成功连接到服务器！")
        else:
            QMessageBox.critical(self, "连接失败", "无法连接到服务器，请检查IP和密码。")

    def connect_to_server(self, dialog):
        ip = self.ip_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        self.remote_connection = RemoteServerConnection(ip, username, password)
        if self.remote_connection.connect():
            QMessageBox.information(self, "连接成功", "成功连接到服务器！")
            dialog.accept()  # Close the dialog
            self.update_button_states()  # Update button states after connection
        else:
            QMessageBox.critical(self, "连接失败", "无法连接到服务器，请检查IP和密码。")

    def update_button_states(self):
        for i, button in enumerate(self.nav_buttons):
            button.setEnabled(i != self.stackedWidget.currentIndex())
            button.setStyleSheet(self.get_button_style() if button.isEnabled() else "background-color: darkgray;")

    def display_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.update_button_states()

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
        if self.server_run_radio.isChecked():
            command = "python Kandinsky-2-main/init.py"
            stdout, stderr = self.remote_connection.execute_command(command)
            if stderr:
                self.show_error_message(f"错误: {stderr}")
            else:
                QMessageBox.information(self, "成功", "初始化成功！")
        else:
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
        if self.server_run_radio.isChecked():
            command = f"python Kandinsky-2-main/T2I.py '{text}' '{path}'"
            stdout, stderr = self.remote_connection.execute_command(command)
            if stderr:
                self.show_error_message(f"错误: {stderr}")
            else:
                QMessageBox.information(self, "成功", "图像生成成功！")
        else:
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
        if self.server_run_radio.isChecked():
            command = f"python Kandinsky-2-main/mixing.py '{text1}' '{text2}' '{path}'"
            stdout, stderr = self.remote_connection.execute_command(command)
            if stderr:
                self.show_error_message(f"错误: {stderr}")
            else:
                QMessageBox.information(self, "成功", "图像混合成功！")
        else:
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
        if self.server_run_radio.isChecked():
            command = f"python Kandinsky-2-main/rec.py '{text}' '{repair_path}' '{save_path}'"
            stdout, stderr = self.remote_connection.execute_command(command)
            if stderr:
                self.show_error_message(f"错误: {stderr}")
            else:
                QMessageBox.information(self, "成功", "图像修复成功！")
        else:
            subprocess.run(["python", "Kandinsky-2-main/rec.py", text, repair_path, save_path])

    def show_error_message(self, message):
        """显示错误信息对话框"""
        error_dialog = QMessageBox()
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