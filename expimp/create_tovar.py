# coding: utf-8

from core.sw_base import BaseHandler


class CreateTovarHandler(BaseHandler):    


    def post(self):
                    
        code = self.get_argument("code", None)
        name = self.get_argument("name", None)
        articul = self.get_argument("articul", None) 
                   
        self.proc("shiva.AddTovIQ", [code, articul, name])
