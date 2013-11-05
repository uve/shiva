# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Menu, User

#=== Меню =====================================================================
class MenuHandler(BaseHandler):
    urls = r'/menu'
    def get(self):
        role = User.get(id=self.session.uid).current_role_cls.id
        self.write(dict([(i.name, (i.caption, i.modules_by_role(role))) for i in Menu.select()]))
