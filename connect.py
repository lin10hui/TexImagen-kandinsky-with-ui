import paramiko
from PyQt5.QtWidgets import QMessageBox

class RemoteServerConnection:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        """连接到远程服务器"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password)
            print("连接成功")
        except Exception as e:
            self.show_error_message(f"连接失败: {str(e)}")

    def disconnect(self):
        """断开与服务器的连接"""
        if self.client:
            self.client.close()
            print("已断开连接")

    def execute_command(self, command):
        """在远程服务器上执行命令"""
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        else:
            self.show_error_message("未连接到服务器")

    def upload_file(self, local_path, remote_path):
        """上传文件到远程服务器"""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"文件 {local_path} 上传成功到 {remote_path}")

    def download_file(self, remote_path, local_path):
        """从远程服务器下载文件"""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            print(f"文件 {remote_path} 下载成功到 {local_path}")

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

# 额外的功能示例
def additional_functionality():
    """示例额外功能"""
    print("执行额外功能")

if __name__ == "__main__":
    # test
    connection = RemoteServerConnection("192.168.1.1", "user", "password")
    connection.connect()
    connection.disconnect() 