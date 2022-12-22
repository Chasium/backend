from typing import List
from apigen.generated.card_template.get_mine import GetMyTemplatesRequest, GetMyTemplatesResponse, CardTemplate
from db.models.card_template import CardTemplateData
from db.models.card_script import CardScriptData
from http_api.auth.util import get_user


def get_mine(req: GetMyTemplatesRequest):
    res = GetMyTemplatesResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    template_data_list: List[CardTemplateData] = user.templates.order_by(CardTemplateData.id.desc()).paginate(
        page=req.page, per_page=req.page_size, error_out=False).items

    templates: List[CardTemplate] = []
    for i in template_data_list:
        template = CardTemplate()
        template.solve__id(i.id)
        template.solve__name(i.name)
        template.solve__value(i.content)
        scripts: List[str] = []
        script_data_list: List[CardScriptData] = i.scripts.order_by(
            CardScriptData.in_card_id).all()
        for j in script_data_list:
            scripts.append(j.value)
        template.solve__scripts(scripts)
        templates.append(template)

    all_templates = user.templates.count()

    res.solve__templates(templates)
    res.solve__pages(all_templates // req.page_size +
                     bool(all_templates % req.page_size))
    res.solve__code(0)
    return res
