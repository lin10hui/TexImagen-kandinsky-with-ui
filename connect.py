import paramiko
from PyQt5.QtWidgets import QMessageBox
import os

class RemoteServerConnection:
    def __init__(self, ip, username, password):
        """初始化远程服务器连接"""
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None
        self.is_connected = False  # 连接状态

    def connect(self):
        """连接到远程服务器"""
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password)
            self.is_connected = True
            print("连接成功")
            return True
        except Exception as e:
            self.show_error_message(f"连接失败: {str(e)}")
            return False

    def disconnect(self):
        """断开与服务器的连接"""
        if self.client:
            self.client.close()
            self.is_connected = False
            print("已断开连接")

    def execute_command(self, command):
        """在远程服务器上执行命令"""
        if self.client:
            if not self.is_command_safe(command):
                self.show_error_message("不安全的命令")
                return "", "不安全的命令"
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        else:
            self.show_error_message("未连接到服务器")

    def is_command_safe(self, command):

        dangerous_commands = ['rm', 'shutdown', 'reboot', 'mkfs', 'dd']
        return not any(dangerous_command in command for dangerous_command in dangerous_commands)

    def upload_file(self, local_path, remote_path):
        """上传文件到远程服务器"""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"文件 {local_path} 上传成功到 {remote_path}")
        else:
            self.show_error_message("未连接到服务器")

    def download_file(self, remote_path, local_path):
        """从远程服务器下载文件"""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            print(f"文件 {remote_path} 下载成功到 {local_path}")
        else:
            self.show_error_message("未连接到服务器")

    def show_error_message(self, message):
        """显示错误信息对话框"""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("错误")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

    def test_connection(self):
        """测试与服务器的连接"""
        try:
            self.connect()
            self.disconnect()
            QMessageBox.information(None, "测试连接", "连接测试成功！")
        except Exception as e:
            self.show_error_message(f"连接测试失败: {str(e)}")

    def get_server_info(self):
        """获取服务器信息"""
        if self.client:
            command = "uname -a"  # 获取服务器信息的命令
            stdout, stderr = self.execute_command(command)
            if stderr:
                self.show_error_message(f"获取服务器信息失败: {stderr}")
            else:
                return stdout.strip()
        else:
            self.show_error_message("未连接到服务器")

    def list_remote_files(self, remote_path):
        """列出远程目录中的文件"""
        if self.client:
            command = f"ls {remote_path}"
            stdout, stderr = self.execute_command(command)
            if stderr:
                self.show_error_message(f"列出文件失败: {stderr}")
            else:
                return stdout.strip().split('\n')
        else:
            self.show_error_message("未连接到服务器")

    def create_remote_directory(self, remote_path):
        """在远程服务器上创建目录"""
        if self.client:
            command = f"mkdir -p {remote_path}"
            stdout, stderr = self.execute_command(command)
            if stderr:
                self.show_error_message(f"创建目录失败: {stderr}")
            else:
                print(f"目录 {remote_path} 创建成功")
        else:
            self.show_error_message("未连接到服务器")

    def delete_remote_file(self, remote_path):
        """删除远程服务器上的文件"""
        if self.client:
            command = f"rm -f {remote_path}"
            stdout, stderr = self.execute_command(command)
            if stderr:
                self.show_error_message(f"删除文件失败: {stderr}")
            else:
                print(f"文件 {remote_path} 删除成功")
        else:
            self.show_error_message("未连接到服务器")

    def upload_file_with_progress(self, local_path, remote_path):
        """上传文件并显示进度"""
        if self.client:
            sftp = self.client.open_sftp()
            file_size = os.path.getsize(local_path)
            uploaded_size = 0

            def progress_callback(transferred, total):
                nonlocal uploaded_size
                uploaded_size += transferred
                print(f"上传进度: {uploaded_size / file_size * 100:.2f}%")

            sftp.put(local_path, remote_path, callback=progress_callback)
            sftp.close()
            print(f"文件 {local_path} 上传成功到 {remote_path}")
        else:
            self.show_error_message("未连接到服务器")



if __name__ == "__main__":
    # 示例用法
    connection = RemoteServerConnection("192.168.1.1", "user", "password")
    connection.connect()
    connection.disconnect()