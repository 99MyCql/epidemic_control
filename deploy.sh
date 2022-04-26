# 部署脚本
#!/bin/bash

set -uex

. venv/bin/activate

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

gunicorn -D -w 4 -b 0.0.0.0:8080 \
--keyfile privkey.pem --certfile fullchain.pem \
--access-logfile access.log --error-logfile error.log \
app:app