from db.models.card_template import CardTemplateData


def get_template(id: int) -> CardTemplateData:
    return CardTemplateData.query.filter_by(id=id).first()
