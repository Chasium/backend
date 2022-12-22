from apigen.generated.card_template.create import CreateTemplateRequest, CreateTemplateResponse
from db import db
from db.models.card_template import CardTemplateData
from db.models.card_script import CardScriptData
from http_api.auth.util import get_user


def create(req: CreateTemplateRequest):
    res = CreateTemplateResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    template: CardTemplateData = user.templates.filter_by(
        name=req.name).first()
    if template is not None:
        res.solve__code(2)
        return res
    template = CardTemplateData(req.name, req.template, user)
    db.session.add(template)

    for i, script in enumerate(req.scripts):
        card_script = CardScriptData(script, template, i)
        db.session.add(card_script)

    res.solve__code(0)
    res.solve__id(template.id)
    db.session.commit()
    return res
