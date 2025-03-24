import paramiko
import re

class ping_loss():
    def __init__(self):
        pass
    def ipv4_loss(self,remote_DUT_ip,remote_DUT_username,remote_DUT_password):
        port = 22
        batch_file_path = 'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat'
        ssh = paramiko.SSHClient()
        # 自動添加主機密鑰（僅供測試使用，生產環境應謹慎使用）
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # 連接到遠端電腦
            ssh.connect(remote_DUT_ip, port, remote_DUT_username, remote_DUT_password)
            # 執行批次檔
            stdin, stdout, stderr = ssh.exec_command("ping 168.95.1.1\n")

            # # 輸出執行結果
            # print("標準輸出:")
            # print(stdout.read().decode("Big5"))
            # print("標準錯誤:")
            # print(stderr.read().decode())
            # 正規
            stats = re.compile(r"已遺失 = (\d+) \((\d+)% 遺失\)")
            loss_stats = stats.search(stdout.read().decode("Big5"))

            if loss_stats:
                lost, loss_percent = loss_stats.groups()
                print(f"已遺失: {lost}, 遺失百分比: {loss_percent}%")

        finally:
            # 關閉 SSH 連
            ssh.close()

if __name__ == '__main__':
    remote_DUT_ip='192.168.13.194'
    remote_DUT_username='dnisqa2'
    remote_DUT_password = 'Sqa2sqa2'
    ping_loss=ping_loss()
    ping_loss.ipv4_loss(remote_DUT_ip,remote_DUT_username,remote_DUT_password)