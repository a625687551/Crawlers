#!/usr/bin/env bash

. /home/dingyong/zxp/sysenv/bin/activate

cd  /home/dingyong/wangjianfeng/wang/autohome

ps -few | grep "mxspider run $1.py" | grep -v grep | awk '{print $2}' | xargs kill -9

nohup mxspider run $1.py  > ./log/$1.log 2>&1 &