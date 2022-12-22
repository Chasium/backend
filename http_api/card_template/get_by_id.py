from typing import List
from apigen.generated.card_template.get_by_id import GetTemplateRequest, GetTemplateResponse, CardTemplate
from db.models.card_script import CardScriptData
from http_api.auth.util import get_user
from db.models.card_template import CardTemplateData


def get_by_id(req: GetTemplateRequest):
    res = GetTemplateResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    template_data = CardTemplateData.query.filter_by(id=req.id).first()

    if template_data is None:
        res.solve__code(2)
        return res

    template = CardTemplate()
    template.solve__id(template_data.id)
    template.solve__name(template_data.name)
    template.solve__value(template_data.content)
    scripts: List[str] = []
    script_data_list: List[CardScriptData] = template_data.scripts.order_by(
        CardScriptData.in_card_id).all()
    for i in script_data_list:
        scripts.append(i.value)
    template.solve__scripts(scripts)
    res.solve__code(0)
    res.solve__template(template)
    return res
