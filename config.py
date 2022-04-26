# 微信小程序
WEIXIN_APPID = "xxxxxx"
WEIXIN_SECRET = "xxxxxx"

# 数据库
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "epidemic_control"
MYSQL_USERNAME = "ec"
MYSQL_PASSWORD = "123"
SQLALCHEMY_TRACK_MODIFICATIONS = False # 关闭对模型修改的监控
SQLALCHEMY_ECHO = True # 执行时显示SQL语句

# 日志等级：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
LOG_LEVEL = "DEBUG"
# 输出目标：console file
LOG_OUTPUT = "console"
# 若输出到文件，配置日志文件所在目录
LOG_DIR = "./"
# 日志文件的最大字节数，单位为B
LOG_MAX_BYTES = 104857600 # 104857600 = 100 * 1024 * 1024

# session
SECRET_KEY = "xxxxxx"
# cookie 的有效期，单位为秒
PERMANENT_SESSION_LIFETIME = 259200 # 259200 = 72 * 60 * 60