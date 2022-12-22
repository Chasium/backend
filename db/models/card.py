from sqlalchemy import Column, Integer, ForeignKey, Text, String
from db import db
from db.models.user import UserData
from db.models.card_template import CardTemplateData


class CardData(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    value = Column(Text(65535))
    user_id = Column(Integer, ForeignKey('user_data.id'))
    user = db.relationship(
        'UserData', backref=db.backref('cards', lazy='dynamic'))
    template_id = Column(Integer, ForeignKey('card_template_data.id'))
    template = db.relationship(
        'CardTemplateData', backref=db.backref('cards', lazy='dynamic'))

    def __init__(self, name: str, value: str, user: UserData, template: CardTemplateData):
        self.name = name
        self.value = value
        self.user = user
        self.template = template
