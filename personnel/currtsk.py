# coding: utf-8

from core.sw_base import BaseHandler


import os
from settings import ROOT_DIR
from tornado import template


#=== Текущие задания =========================================================
class CurrentTaskHandler(BaseHandler):
    urls = r'/personnel/currtsk'

    def get(self):
        
        loader = template.Loader(os.path.join(ROOT_DIR, 'personnel'))
        
        result = loader.load("alltsk.js").generate(calendar=False)   
        
        
        self.write({'def':[{'type':"button", 'img':"restart.png", 'action':'do_tool_task_restart', 'title':'Возобновить задачу'},
                           {'type':"button", 'img':"stop.png", 'action':'do_tool_task_close', 'title':'Завершить задачу'},
                           {'type':"button", 'img':"1.png", 'action':'do_tool_task_priority', 'title':'Установить приоритет'},
                           {'type':"separator"},
                           {'type':"button", 'img':"csv.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],
                    
                     'cmd': result})        
                    

