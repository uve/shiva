# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Menu

#=== Меню =====================================================================
class MenuHandler(BaseHandler):
    urls = r'/menu'
    def get(self):
                
        role = self.session.role#User.get(id=self.session.uid).current_role_cls.id
        
        all_modules = []
        for i in Menu.select():
            item = (i.name, (i.caption, i.modules_by_role(role)))
            
            all_modules.append(item)
            
        res = dict(all_modules)
        self.write(res)
