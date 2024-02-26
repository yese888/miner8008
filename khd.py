import subprocess
import importlib
import psutil
import requests
import socket
import time
import random
import hashlib

# 安装 python3-pip
try:
    subprocess.run(['sudo', 'apt', 'install', 'python3-pip', '-y'], check=True)
except subprocess.CalledProcessError as e:
    print(f"安装过程中出现错误：{e}")

# 安装所需库
def install_module(module_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        subprocess.check_call(['pip', 'install', module_name])

# 安装缺失的库
install_module('psutil')
install_module('requests')
install_module('hashlib')


# 导入所需的库
import psutil
import requests
import socket
import time
import random
import hashlib

# 定期向服务端发送信息
def periodic_update(server_url):
    while True:
        try:
            client_info = f'log: {read_last_line()}'
            send_client_info(server_url)
            # 随机等待时间，范围为3到5分钟
            wait_time = random.randint(180, 300)
            time.sleep(wait_time)
        except Exception as e:
            print(f"出错：{e}")
            print("等待10秒后重试...")
            time.sleep(10)

# 读取日志文件的最后一行
def read_last_line():
    file_path = '/run/miner.log'
    with open(file_path, 'rb') as file:
        file.seek(-2, 2)  # 移动到文件倒数第二个字节
        while file.read(1) != b'\n':  # 读取直到找到换行符
            file.seek(-2, 1)  # 继续向前移动两个字节
        last_line = file.readline().decode().strip()  # 读取并解码最后一行
    return last_line

# 获取 CPU 信息
def get_cpu_info():
    cpu_model = None
    try:
        cpu_info = open('/proc/cpuinfo', 'r').read()
        for line in cpu_info.split('\n'):
            if line.strip().startswith('model name'):
                cpu_model = line.split(':')[1].strip()
                break
    except FileNotFoundError:
        pass

    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU:{cpu_model},使用率:{cpu_usage}%"

# 获取本机 MAC 地址
def get_mac():
    mac = ':'.join(['{:02x}'.format((int(sha_byte, 16) ^ 0xAA) & 0xFF) for sha_byte in hashlib.sha256(socket.gethostname().encode()).hexdigest()[::2]])
    return mac

# 获取本机 IP 地址
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

# 生成唯一的 client_id
def generate_client_id():
    return f'client_{get_mac()}'

# 向服务端发送客户端信息
def send_client_info(server_url):
    data = {'client_id': get_ip(), 'client_cpu': get_cpu_info(), 'client_info': read_last_line()}
    response = requests.post(f'{server_url}/update_info', data=data)
    print(response.text)

if __name__ == '__main__':
    # 替换成你的服务端 IP 和端口
    server_url = 'http://43.156.54.199:8008'
    
    # 启动定期更新
    periodic_update(server_url)
