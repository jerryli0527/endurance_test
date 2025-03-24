import time
import sched
import threading
import paramiko
import re

scheduler = sched.scheduler(time.time, time.sleep)


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


def run_ping_tests():
    print("開始執行 Ping 測試...")

    remote_ips = ['192.168.13.194'] * 3
    remote_DUT_username = 'dnisqa2'
    remote_DUT_password = 'Sqa2sqa2'
    batch_file_paths = ['C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat'] * 3

    ping_loss = PingLoss()
    results = [None] * 3

    def run_test(index):
        result = ping_loss.loss_rate(remote_ips[index], remote_DUT_username, remote_DUT_password,
                                     batch_file_paths[index])
        results[index] = f"{result}"

    threads = []
    for i in range(3):
        thread = threading.Thread(target=run_test, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for result in results:
        print(result)

    print("等待 15 分鐘後再次執行...")
    scheduler.enter(60, 1, run_ping_tests)  # 15 分鐘後再次執行


# 讓 scheduler 在背景執行（不阻塞）
def start_scheduler():
    scheduler.enter(0, 1, run_ping_tests)  # 立即執行第一次
    while True:
        scheduler.run(blocking=False)  # 讓 scheduler 不中斷地檢查排程
        time.sleep(1)  # 避免 CPU 過度使用


# 用 Thread 避免阻塞主程式
threading.Thread(target=start_scheduler, daemon=True).start()

# 讓程式保持運行
while True:
    time.sleep(1)
