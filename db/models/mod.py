from sqlalchemy import Column, Integer, String, ForeignKey
from db import db
from db.models.user import UserData
import random


class ModData(db.Model):
    __tablename__ = 'mod_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    content = Column(String(5000), unique=False)
    user_id = Column(Integer, ForeignKey('user_data.id'))
    user = db.relationship(
        'UserData', backref=db.backref('mods', lazy='dynamic'))

    def __init__(self, name, content, user: UserData):
        self.name = name
        self.content = content
        self.user = user

    def getId(self):
        return self.id

    def getName(self):
        return self.name
