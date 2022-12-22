from apigen.generated.card_template.delete import DeleteTemplateRequest, DeleteTemplateResponse
from db import db
from db.models.card_template import CardTemplateData
from http_api.auth.util import get_user


def delete(req: DeleteTemplateRequest):
    res = DeleteTemplateResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    template: CardTemplateData = user.templates.filter_by(
        id=req.id).first()
    if template is None:
        res.solve__code(2)
        return res
    scripts = template.scripts.all()
    for i in scripts:
        db.session.delete(i)
    db.session.delete(template)
    db.session.commit()
    res.solve__code(0)
    return res
