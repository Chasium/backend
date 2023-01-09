from apigen.generated.mod.get_mods import GetMyModsRequest, GetMyModsResponse, Mod
from http_api.auth.util import get_user
from db.models.mod import ModData
from typing import List


def get_mods(req: GetMyModsRequest):
    res = GetMyModsResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    mods_list: List[ModData] = user.mods.order_by(ModData.id.desc()).paginate(
        page=req.page, per_page=req.page_size, error_out=False).items
    mods: List[Mod] = []
    for i in mods_list:
        mod = Mod()
        mod.solve__content(i.content)
        mod.solve__name(i.name)
        mod.solve__id(i.id)
        mods.append(mod)
    all_mods = user.mods.count()

    res.solve__mods(value=mods)
    res.solve__pages(all_mods // req.page_size +
                     bool(all_mods % req.page_size))
    res.solve__code(0)
    return res
