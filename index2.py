import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QMessageBox, QFrame, QRadioButton, QLineEdit, QDialog
import subprocess
from connect import RemoteServerConnection

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
        self.init_button.setStyleSheet(self.get_button_style())
        self.init_button.clicked.connect(self.confirm_initialize)

        self.exit_button = QPushButton("退出", self.top_bar)
        self.exit_button.setMinimumWidth(80)
        self.exit_button.setStyleSheet(self.get_button_style())
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

        # Middle layout for navigation buttons
        middle_layout = QHBoxLayout()
        main_layout.addLayout(middle_layout)

        # Navigation buttons
        self.nav_widget = QWidget(self)
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(5)

        # Adding navigation buttons
        self.nav_buttons = []
        button_names = ["图像生成", "图像融合", "图像修复"]
        for name in button_names:
            button = QPushButton(name, self.nav_widget)
            button.setMinimumWidth(80)
            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(lambda _, x=len(self.nav_buttons): self.display_page(x))
            self.nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        middle_layout.addWidget(self.nav_widget)

        # Right side for content area
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        middle_layout.addWidget(self.stackedWidget)

        self.initUI()

        # Bottom layout for options
        self.bottom_layout = QHBoxLayout()
        main_layout.addLayout(self.bottom_layout)

        # Radio buttons for local and server run
        self.local_run_radio = QRadioButton("本地运行")
        self.server_run_radio = QRadioButton("服务器运行")
        self.local_run_radio.setChecked(True)  # Default to local run
        self.bottom_layout.addWidget(self.local_run_radio)
        self.bottom_layout.addWidget(self.server_run_radio)

        # Connect button for server run
        self.connect_button = QPushButton("连接服务器")
        self.connect_button.clicked.connect(self.show_connection_dialog)
        self.bottom_layout.addWidget(self.connect_button)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: lightgray; 
                border-radius: 10px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: gray;
            }
            QPushButton:disabled {
                background-color: darkgray;
            }
        """

    def initUI(self):
        # Initialize pages
        self.page_generation = QWidget()
        self.stackedWidget.addWidget(self.page_generation)
        self.setup_generation_page()

        self.page_mixing = QWidget()
        self.stackedWidget.addWidget(self.page_mixing)
        self.setup_mixing_page()

        self.page_inpainting = QWidget()
        self.stackedWidget.addWidget(self.page_inpainting)
        self.setup_inpainting_page()

    def show_connection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("连接服务器")
        dialog.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(dialog)

        ip_label = QLabel("服务器 IP 地址:", dialog)
        self.ip_input = QLineEdit(dialog)
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)

        username_label = QLabel("用户名:", dialog)
        self.username_input = QLineEdit(dialog)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        password_label = QLabel("密码:", dialog)
        self.password_input = QLineEdit(dialog)
        self.password_input.setEchoMode(QLineEdit.Password)
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
