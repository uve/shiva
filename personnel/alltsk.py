# coding: utf-8

import datetime
from core.sw_base import BaseHandler

import cx_Oracle

from core.common_tools import fetchall

import os
from settings import ROOT_DIR
from tornado import template

#=== Все задания ==============================================================
class AllTaskHandler(BaseHandler):
    urls = r'/personnel/alltsk'

    def get(self):
        st = datetime.datetime.now().strftime('%d.%m.%Y')

        loader = template.Loader(os.path.join(ROOT_DIR, 'personnel'))
        
        result = loader.load("alltsk.js").generate()            
    
        self.write({'def':[{'type':"text", 'text':"Дата с:"},
                           {'id':"cal1", 'type':"buttonInput", 'width':60, 'value':st},
                           {'type':"text", 'text':" по:"},
                           {'id':"cal2", 'type':"buttonInput", 'width':60, 'value':st},
                           
                           {'type':"separator"},
                           {'type':"button", 'img':"restart.png", 'action':'do_tool_task_restart', 'title':'Возобновить задачу'},
                           {'type':"button", 'img':"stop.png", 'action':'do_tool_task_close', 'title':'Завершить задачу'},
                           {'type':"button", 'img':"1.png", 'action':'do_tool_task_priority', 'title':'Установить приоритет'},
                           {'type':"separator"},
                           {'type':"button", 'img':"csv.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           ],

                    'cmd': result
                    })


#==============================================================================
class AllTaskDataHandler(BaseHandler):
    urls = r'/personnel/alltsk/data/tasks'

    def get(self, param):
        
        
        if param == "tasks":
            ds = self.get_argument("d1", None)
            if ds:
                ds = datetime.datetime.fromtimestamp(int(ds) / 1000)
                ds = ds.date()
                
            
                
            de = self.get_argument("d2", None)
            if de:
                de = datetime.datetime.fromtimestamp(int(de) / 1000)
                de = de.date()
                
    
            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.proc("shiva_task.GetAllTask", [ds, de, out])
    
            all_results = []
    
            for item in res[-1].fetchall():
                all_results.append({"id": item[0], "data": item })
        
            self.write({"rows": all_results})
            
            
            
            
        if param == "history":
            
            task_id = self.get_argument("task_id", None)

            
            sql = "select sw.task_id, TO_CHAR(sw.datetime, 'MM.DD.YYYY HH24:MI:SS') datetime, sw.description, s.name from sw_task_history sw LEFT JOIN sotrud s ON sw.user_id = s.id WHERE task_id=%s order by datetime desc" % task_id
            
            res = self.execute(sql)
           
            all_results = fetchall(res, count=1)
                    
            self.write(all_results)         
        


    def post(self, param):
        
        
        user_id = self.session.uid
        task_id = self.get_argument("task_id", None)
        
        
        # user_id - пользователь шивы который остановил задачу
        
        if param == 'task_restart':
            self.proc("shiva_task.UserTaskRestart", [task_id, user_id])   
        
        
        if param == 'task_close':
            self.proc("shiva_task.UserTaskClose",   [task_id, user_id])
        
        
        if param == 'task_priority':
            self.proc("shiva_task.SetTaskPriority",   [task_id])
            
            
        
        self.write({'info':'Информация сохранена',  'cmd':"window.do_tool_1()"})
        
        
        
        