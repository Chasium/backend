from sqlalchemy import Column, Integer, String, Text
from db import db
import random


class UserData(db.Model):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(120), unique=False)
    img = Column(Text(65535))  # base64编码后的图像
    nickname = Column(String(50))

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.img = ''
        self.nickname = '路人' + str(random.randint(0, 100))

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def modifyImage(self, img: str):
        self.img = img

    def modifyNickname(self, nickname: str):
        self.nickname = nickname
