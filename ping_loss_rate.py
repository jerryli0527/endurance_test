import paramiko
import re

class ping_loss():
    def __init__(self):
        self.ip=None
        self.username=None
        self.password=None
    def loss_rate(self,remote_ip,remote_DUT_username,remote_DUT_password,batch_file_path):
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(remote_ip, port, remote_DUT_username, remote_DUT_password)
            stdin, stdout, stderr = ssh.exec_command(batch_file_path)
            result=stdout.read().decode("Big5")
            stats = re.compile(r"\((\d+)% 遺失\)")
            loss_stats = stats.search(result)
            if loss_stats:
                loss_percent = loss_stats.group(1)  # ✅ Correct way to extract the first group
        finally:
            ssh.close()
        return f"{loss_percent}%"

if __name__ == '__main__':
    remote_ip='192.168.13.194'
    remote_DUT_username='dnisqa2'
    remote_DUT_password = 'Sqa2sqa2'
    batch_file_path = 'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat'
    ping_loss=ping_loss()
    result=ping_loss.loss_rate(remote_ip,remote_DUT_username,remote_DUT_password,batch_file_path)
    print(result)