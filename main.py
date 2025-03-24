import paramiko
import re
import threading


class PingLoss:
    def __init__(self):
        self.ip = None
        self.username = None
        self.password = None

    def loss_rate(self, remote_ip, remote_DUT_username, remote_DUT_password, batch_file_path):
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(remote_ip, port=port, username=remote_DUT_username, password=remote_DUT_password)
            stdin, stdout, stderr = ssh.exec_command(batch_file_path)
            result = stdout.read().decode("Big5")
            stats = re.compile(r"\((\d+)% 遺失\)")
            loss_stats = stats.search(result)

            if loss_stats:
                loss_percent = loss_stats.group(1)
            else:
                loss_percent = "N/A"
        except Exception as e:
            loss_percent = f"錯誤: {str(e)}"
        finally:
            ssh.close()

        return f"{loss_percent}%"


if __name__ == '__main__':
    # 不同的遠端 IP 或不同的測試指令
    remote_ips = [
        '192.168.13.194', '192.168.13.194', '192.168.13.194',
        '192.168.13.194', '192.168.13.194', '192.168.13.194',
        '192.168.13.194', '192.168.13.194'
    ]

    remote_DUT_username = 'dnisqa2'
    remote_DUT_password = 'Sqa2sqa2'

    # 8 個不同的批次檔案（可以執行不同的測試）
    batch_file_paths = [
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat',
        'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat'
    ]

    ping_loss = PingLoss()
    results = [None] * 8  # 建立 8 個空位存放結果


    # 執行 ping 測試的函數
    def run_test(index):
        result = ping_loss.loss_rate(remote_ips[index], remote_DUT_username, remote_DUT_password,
                                     batch_file_paths[index])
        results[index] = f"{result}"


    threads = []

    # 創建 8 個執行緒，每個執行不同的 IP 和批次檔案
    for i in range(8):
        thread = threading.Thread(target=run_test, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有執行緒完成
    for thread in threads:
        thread.join()

    # 顯示所有結果
    for result in results:
        print(result)
