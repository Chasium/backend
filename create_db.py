"""
用于快速创建数据库的入口文件
"""
from http_api import http_api
import config
from db import db
from sqlalchemy import create_engine


if __name__ == '__main__':
    root_password = input('Root账号的密码: > ')

    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'information_schema'
    USERNAME = 'root'
    PASSWORD = root_password
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    engine = create_engine(DB_URI, echo=True)
    with engine.connect() as con:
        con.execute(
            "create user if not exists chasium identified by '123456';")
        con.execute("drop database if exists chasium;")
        con.execute("create database if not exists chasium;")
        con.execute(
            "grant all privileges on *.* to chasium@localhost identified by '123456' with grant option;")

    http_api.config.from_object(config)
    db.init_app(http_api)
    http_api.app_context().push()

    with http_api.app_context():
        db.create_all()
