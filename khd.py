import subprocess
import importlib
客户标识='ys'
地区='A组'
def install_pip():
    try:
        print("检查是否已安装")
        # 检查是否已安装 pip
        subprocess.run(['pip3', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("Python 3 pip 已经安装.")
    except Exception as e:
        # 如果没有安装 pip，则安装
        print("开始安装")
        try:
            subprocess.run(['sudo', 'apt', 'install', 'python3-pip', '-y'], check=True)
            print("成功安装 Python 3 pip.")
        except subprocess.CalledProcessError as e:
            print(f"安装过程中出现错误：{e}")
        except Exception as e:
            print(f"安装过程中出现未知错误：{e}")

# 安装缺失的库
def install_module(module_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        subprocess.check_call(['pip', 'install', module_name])

# 检查并安装所需库
def setup_environment():
    install_pip()
    install_module('psutil')
    install_module('requests')
    install_module('hashlib')
    install_module('datetime')
    install_module('re')
setup_environment()
import re
import requests
import psutil
import socket
import time
import random
import hashlib
import datetime
def 获取内存大小():
    result = subprocess.run(['cat', '/proc/meminfo'], capture_output=True, text=True)
    mem_total_match = re.search(r'MemTotal:\s+(\d+)', result.stdout)
    if mem_total_match:
        mem_size = int(mem_total_match.group(1)) // 1031000  # 将内存大小从KB转换为GB
        return mem_size
    return None
def 获取内存位置信息():
    # 检查CPU型号是否为7B13
    cpu_info = subprocess.check_output("lscpu", shell=True).decode()
    if "7B13" in cpu_info:
        # 如果是7B13，检查主板型号是否为R5218、TYAN或Ramaxel
        baseboard_info = subprocess.check_output("dmidecode -t baseboard", shell=True).decode()
        if any(board in baseboard_info for board in ["R5218", "TYAN", "Ramaxel"]):
            # 如果主板型号符合条件，则提取内存位置信息
            memory_info = subprocess.check_output("dmidecode -t memory | grep -B3 DDR4 | grep 'Bank Locator' | awk '{print $5}'", shell=True).decode().replace("\n", "").replace("1", "")
        else:
            # 如果主板型号不符合条件，则提取内存位置信息
            memory_info = subprocess.check_output("dmidecode -t memory | grep -B3 DDR4 | grep 'Locator:' | grep 'Locator: CPU[01]_' | awk '{print substr($0,length($0)-1)}'", shell=True).decode().replace("\n", "").replace("1", "")
    else:
        # 如果CPU型号不是7B13，则提取内存位置信息
        memory_info = subprocess.check_output("dmidecode -t memory | grep -B3 DDR4 | grep 'Bank Locator:' | awk '/Locator/ {printf $NF} END {print \"\"}'", shell=True).decode().replace(" ", "").replace("\n", "").replace("1", "")

    return memory_info
def 获取自定义2():
    # 初始化变量
    getcustom2 = None
    # 获取自定义2
    try:
        with open('/proc/cpuinfo', 'r') as file:
            for line in file:
                if 'cpu MHz' in line:
                    getcustom2 = line.split()[3]  # 提取第四列的值
                    break  # 找到后跳出循环
    except FileNotFoundError:
        getcustom2 = '000'

    return getcustom2
# 获取运行时间
def get_boot_time():
    with open('/proc/uptime', 'r') as file:
        uptime_str = file.readline().split()[0]  # 读取第一行并提取第一个字段
        uptime_sec = float(uptime_str.split('.')[0])  # 将字符串转换为浮点数，并去除小数部分
        days, hours, minutes, seconds = 格式化秒数(int(uptime_sec))
        return f"{days}天{hours}时{minutes}分{seconds}秒"  # 将浮点数转换为整数并返回
def 格式化秒数(秒数):
    天 = 秒数 // (24 * 3600)
    剩余秒数 = 秒数 % (24 * 3600)
    小时 = 剩余秒数 // 3600
    剩余秒数 %= 3600
    分钟 = 剩余秒数 // 60
    秒数 %= 60
    return 天, 小时, 分钟, 秒数
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

    # 提取前三个段落
    if cpu_model:
        cpu_model_parts = cpu_model.split()
        if len(cpu_model_parts) >= 3:
            cpu_model = ' '.join(cpu_model_parts[:3])
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"{cpu_model}",f"{cpu_usage}%"

def 获取算力值():
    file_path = '/run/miner.log'
    matched_text = ''
    with open(file_path, 'rb') as file:
        lines = []
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        for i in range(1, 11):
            # 逐行向前读取
            file.seek(-i, 2)
            if file.tell() <= 0:  # 已经读到文件开头
                break
            file.seek(-i, 2)  # 再次移动
            while file.read(1) != b'\n':  # 读取直到找到换行符
                file.seek(-2, 1)  # 继续向前移动两个字节
            lines.append(file.readline().decode().strip())  # 读取并解码一行
        # 倒序处理
        lines.reverse()

        # 逐行匹配，找到符合条件的行即可
        for line in lines:
            match = re.search(r'.*\|(.+?)it/s', line)
            if match:
                matched_text = match.group(1)
                break

    if matched_text:
        return matched_text
    else:
        return '000'

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

if __name__ == '__main__':
    # 设置服务端 URL
    server_url = 'http://43.156.54.199:8009/update_info'

    # 设置环境并检查/安装所需库
    mac=get_mac()
    ip=get_ip()
    while True:
        try:
            # 构造要发送的数据
            g2=获取自定义2()

            cpu_model,cpu_usage=get_cpu_info()
            data = {
                'client_id':mac ,  # 使用 MAC 地址作为客户端ID
                'region': 地区,
                'model': cpu_model,
                'online': 1,  # 在线状态，1表示在线
                'custom_sum1': 获取算力值(),
                'custom_sum2': g2,
                'cpu_usage': cpu_usage+"%",
                'runtime': get_boot_time(),
                'cpu_memory_custom': 获取内存大小(),
                'region_time': 客户标识,
                'ip_address': ip,
                'memory_address': 获取内存位置信息(),
            }

            # 发送 POST 请求到服务端
            response = requests.post(server_url, data=data)
            #print(response.text)  # 输出服务端返回的信息

            # 随机等待时间，范围为3到5分钟
            wait_time = random.randint(180, 300)
            time.sleep(wait_time)
        except Exception as e:
            print(f"出错：{e}")
            print("等待10秒后重试...")
            time.sleep(10)
