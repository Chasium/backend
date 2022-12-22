from sqlalchemy import Column, Integer, String
from db import db


class UserData(db.Model):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(120), unique=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password
    def getId(self):
        return self.id
    def getName(self):
        return self.name
