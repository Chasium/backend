from sqlalchemy import Column, Integer, String, ForeignKey, Text
from db import db
from db.models.user import UserData



class UserInfoData(db.Model):
    __tablename__ = 'user_info_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    img = Column(String(5000))  # base64编码后的图像
    # name = Column(String(50))
    # last login date
    user_id = Column(Integer, ForeignKey('user_data.id'))
    user = db.relationship(
        'UserData', backref=db.backref('user_info', lazy='dynamic'))

    def __init__(self, img: str, user: UserData):
        self.img = img
        self.user = user