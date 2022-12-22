"""
后端配置文件
"""
SQL_HOST = '127.0.0.1'
SQL_PORT = '3306'
SQL_DATABASE = 'chasium'
SQL_USERNAME = 'chasium'
SQL_PASSWORD = '123456'

DB_URI = \
    "mysql+pymysql://" + \
    f"{SQL_USERNAME}:" + \
    f"{SQL_PASSWORD}@" + \
    f"{SQL_HOST}:" + \
    f"{SQL_PORT}/" + \
    f"{SQL_DATABASE}?" + \
    "charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = './project_storage/@upload'
