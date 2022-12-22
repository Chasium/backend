from apigen.generated.card_template.edit import EditTemplateRequest, EditTemplateResponse
from db import db
from db.models.card_template import CardTemplateData
from db.models.card_script import CardScriptData
from http_api.auth.util import get_user


def edit(req: EditTemplateRequest):
    res = EditTemplateResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    template: CardTemplateData = CardTemplateData.query.filter_by(
        id=req.id).first()
    if template is None:
        res.solve__code(2)
        return res
    scripts = template.scripts.all()
    for i in scripts:
        db.session.delete(i)
    for i, script in enumerate(req.scripts):
        card_script = CardScriptData(script, template, i)
        db.session.add(card_script)

    template.content = req.template
    db.session.add(template)
    db.session.commit()
    res.solve__code(0)
    return res
