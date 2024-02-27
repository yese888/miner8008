#!/bin/bash

screen -wipe
pkill -9 qli-runner
pkill -9 qli-Client
pkill -9 check.sh

sudo apt-get update
apt install vim screen curl wine -y
echo "deb http://cz.archive.ubuntu.com/ubuntu jammy main" | sudo tee -a /etc/apt/sources.list &&
sudo apt install libc6 -y
sleep 3
sudo apt-get update
sudo apt install g++-11 -y

rm -rf /run/miner*.log
mkdir ~/g
mkdir ~/c


cd ~/g
wget https://dl.qubic.li/downloads/qli-Client-1.8.6-Linux-x64.tar.gz &&
tar -xvf qli-Client-1.8.6-Linux-x64.tar.gz
echo "软件下载成功，等待启动GPU"
#wget http://150.158.140.31/while.sh
#wget http://150.158.140.31/qli-Client &&


name=$(curl ifconfig.me)

json_data='{
  "Settings": {
    "baseUrl": "https://ai.diyschool.ch/",
    "amountOfThreads": 1,
    "payoutId": null,
        "overwrites": {"cuda": "12"},
    "accessToken": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjMxMzIxNmU4LTlkZjEtNDA4OC04Nzk0LWZhMmFlMTA4ODcwNiIsIk1pbmluZyI6IiIsIm5iZiI6MTcwNjcwNDYyNCwiZXhwIjoxNzM4MjQwNjI0LCJpYXQiOjE3MDY3MDQ2MjQsImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.049at1qfEWGaWFMq0y_M8K1HugT83hZMulj63bI6eUz1EQkuQXgRt_QztPOODBxbjYg1QPtEhp182KGN-k7OnA",
    "alias": "nameys",
    "allowHwInfoCollect": true
  }
}'


# 将JSON数据保存到appsettings.json文件
echo -e "$json_data"  >  ~/g/appsettings.json

chmod 777 *

screen -L -Logfile /run/minerg.log -dmS g ./qli-Client $name

echo "复制软件到目录c"
cp ~/g/qli-Client ~/c
echo "GPU启动成功，等待CPU"
sleep 10

# tail -f /run/minerq.log




#sed -i 's/nameys/7941475/g' /root/appsettings.json
#screen -dmS q ./qli-Client
#screen -r


cd ~/c

c=$(cat /proc/cpuinfo| grep "processor"| wc -l)
i=$((c/2))
name=$(curl ifconfig.me)
namec="${name}c"

json_data_c='{
  "Settings": {
    "baseUrl": "https://ai.diyschool.ch/",
    "amountOfThreads": 1,
    "payoutId": null,
    "accessToken": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjMxMzIxNmU4LTlkZjEtNDA4OC04Nzk0LWZhMmFlMTA4ODcwNiIsIk1pbmluZyI6IiIsIm5iZiI6MTcwNjcwNDYyNCwiZXhwIjoxNzM4MjQwNjI0LCJpYXQiOjE3MDY3MDQ2MjQsImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.049at1qfEWGaWFMq0y_M8K1HugT83hZMulj63bI6eUz1EQkuQXgRt_QztPOODBxbjYg1QPtEhp182KGN-k7OnA",
    "alias": "nameys",
    "allowHwInfoCollect": false

  }
}'

#将JSON数据保存到appsettings.json文件
echo -e "$json_data_c"  >  ~/c/appsettings.json

chmod 777 *

screen -L -Logfile /run/minerc.log -dmS c ./qli-Client "$namec" "$i"

echo "CPU启动成功"
sleep 10


# echo "nohup守护------------------"
# rm ~/check.sh
# sleep 2
# check='#!/bin/bash
# while true; do
    # if ! ps aux | grep qli-Client | grep -v grep > /dev/null || ! screen -ls | grep g | grep -v grep > /dev/null; then
    # echo "程序不存在 准备运行。"
    # cd ~
    # rm -rf ~/g ~/c ~/aaa.sh && wget http://150.158.140.31/aaa.sh && chmod 777 aaa.sh && ./aaa.sh
    # else
		# echo "程序运行中 无需重开。"
# fi
    # sleep 300
# done'

# echo -e "$check"  >  ~/check.sh
# chmod 777 ~/check.sh
# nohup ./check.sh > check.log 2>&1 &
# echo "nohup守护运行中---------------"
# sleep 2

tail -f /run/miner*


# cd /root
# screen -dmS while ./while.sh
# tail -f /run/miner*
