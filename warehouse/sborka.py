# coding: utf-8

import os
from settings import ROOT_DIR
from core.sw_base import BaseHandler


from tornado import template

from core.common_tools import fetchall, fetchall_by_name
import cx_Oracle

#=== Сборка ==================================================================#
class SborkaHandler(BaseHandler):
    urls = r'/warehouse/sborka'
    
 

    def get(self):
 

        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("sborka.js").generate()
       
 
 
        self.write({'def':[ 
                              
                           {'type':"button", 'action':'do_tool_test', 'text':'TEST', 'title':'TEST'}],



                    'one':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_save_extinfo'},
                           {'type':"button", 'text':'Отмена', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_cancel_extinfo'},
                           '<div id="swformextinfo" />'],
                    'two':[{'type':"button", 'text':'Назад', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_cancel_extinfo'},
                           ],
                    'cmd': result
                    })



#==============================================================================
class SborkaDataHandler(BaseHandler):
    urls = r'/warehouse/sborka/data/([^/]+)'

    def get(self, param):


        head = self.get_argument("head", 0)
        
        if param == 'list':


            out = self.cursor.var(cx_Oracle.CURSOR)
                        
            res = self.cursor.callproc("shiva.GetHeaderInwork", [out])                
         
            all_results = fetchall(res[-1])  
                        
            self.write(all_results)         


        elif param == 'messages':

            sql = "select h.id, h.header, h.usr, h.mess, to_char(done,'DD.MM.YYYY') done from header_message h where h.header=%s order by done desc" % head
                        
            res = self.cursor.execute(sql)
            
            all_results = fetchall_by_name(res)
            self.write(all_results)  
        
        
        


