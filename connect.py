import paramiko
from PyQt5.QtWidgets import QMessageBox

class RemoteServerConnection:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password)
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def execute_command(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        return None, "未连接到服务器"

    def close(self):
        if self.client:
            self.client.close() 