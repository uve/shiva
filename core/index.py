# coding: utf-8
from core.sw_base import BaseHandler
from settings import TEMPLATE_DIR, MOBILE_USER_AGENTS

from tornado import template
from settings import TORNADO_HASH


class MainHandler(BaseHandler):
    urls = r'/'

    def get(self):
        
        #self.cursor.callproc("DBMS_LOCK.sleep", [2])
        
        #self.redirect("http://shiva.ws:12345", True)        
        #return
        

        is_terminal = False
        
        if any(i in self.request.headers.get('User-Agent', '') for i in MOBILE_USER_AGENTS):
            is_terminal = True
            
            
        mobile_template = 'mobile.html'            
                       

        if is_terminal or self.request.path == "/n":
            page_template = mobile_template
        
        else:
            page_template = "index.html"
        
        loader = template.Loader(TEMPLATE_DIR)
        
        default = self.get_template_namespace()
        default.update({ 'is_terminal' : is_terminal,
                         'TORNADO_HASH': TORNADO_HASH })
        
        output = loader.load(page_template).generate(**default)
        
        self.write(output)
