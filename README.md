# epidemic_control

疫情防控小程序后端

## Getting Start

环境：

- python >= 3.7
- MySQL 8.0

代码规范：[PEP8](https://peps.python.org/pep-0008)

安装依赖（建议使用虚拟环境）：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

修改默认配置文件 `./config.py` ，或者自定义配置文件（格式参照config.py），并通过环境变量 `CONFIG_FILE` 指定：

```bash
# windows: set CONFIG_FILE=config_dev.py
export CONFIG_FILE=config_dev.py
```

数据库迁移：

```bash
flask db migrate
flask db upgrade
```

运行:

```bash
# windows: set FLASK_ENV=development
export FLASK_ENV=development

# flask run -p 8080
flask run
```

or

```bash
python app.py
```
