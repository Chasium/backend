from sqlalchemy import Column, Integer, String, ForeignKey, Text
from db import db
from db.models.user import UserData


class CardTemplateData(db.Model):
    __tablename__ = 'card_template_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    content = Column(Text(65535))
    user_id = Column(Integer, ForeignKey('user_data.id'))
    user = db.relationship(
        'UserData', backref=db.backref('templates', lazy='dynamic'))

    def __init__(self, name: str, content: str, user: UserData):
        self.name = name
        self.content = content
        self.user = user
