from sqlalchemy import Column, Integer, String, ForeignKey, Text
from db import db
from db.models.card_template import CardTemplateData


class CardScriptData(db.Model):
    __tablename__ = 'card_script_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Text(65535))
    card_id = Column(Integer, ForeignKey('card_template_data.id'))
    card = db.relationship(
        'CardTemplateData', backref=db.backref('scripts', lazy='dynamic'))
    in_card_id = Column(Integer)

    def __init__(self, value: str, card: CardTemplateData, in_card_id: int):
        self.value = value
        self.card = card
        self.in_card_id = in_card_id
