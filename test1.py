import paramiko
import re

# SSH 連線資訊
hostname = '192.168.13.194'
port = 22
username = 'dnisqa2'
password = 'Sqa2sqa2'
file_path = "C:\\Users\\dnisqa2\\Desktop\\ping_ipv6_google.txt"

# 建立 SSH 連線
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)

# 執行命令抓取檔案內容 (Windows 使用 type)
stdin, stdout, stderr = client.exec_command(f'type "{file_path}"')

# 讀取並輸出檔案內容
file_content = stdout.read().decode("Big5")

# 正規表達式 - 抓取遺失率
loss_pattern = r"\((\d+)% 遺失\)"

loss_matches = re.findall(loss_pattern, file_content)
loss_rates = list(map(int, loss_matches))
# 計算平均值
average_loss = sum(loss_rates) / len(loss_rates)

print(f"平均遺失率: {average_loss}%")
# 關閉 SSH 連線
client.close()
