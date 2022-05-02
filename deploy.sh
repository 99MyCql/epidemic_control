#!/bin/bash
######
# 部署脚本
#   bash deploy.sh 运行
#   bash deploy.sh -D 后台运行
######

set -uex


HOST=0.0.0.0
PORT=8080
SSL_KEY=./privkey.pem
SSL_CERT=./fullchain.pem


python3 -m venv venv

. venv/bin/activate

pip config set --site global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# flask应用配置文件
export CONFIG_FILE=config_prod.py

if [ $# -gt 0 ]; then
    gunicorn $1 -w 4 -b ${HOST}:${PORT} \
    --keyfile ${SSL_KEY} --certfile ${SSL_CERT} \
    --access-logfile access.log --error-logfile error.log \
    app:app
else
    gunicorn -w 4 -b ${HOST}:${PORT} \
    --keyfile ${SSL_KEY} --certfile ${SSL_CERT} \
    --access-logfile access.log --error-logfile error.log \
    app:app
fi
