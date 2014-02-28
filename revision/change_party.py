#!/usr/bin/env python
# -*- coding: utf8 -*- 

from core.sw_base import BaseHandler


import os
from settings import ROOT_DIR


from tornado import template
import cx_Oracle


from core.common_tools import fetchall#, fetchone, fetchall_by_name

from avtuk.avtuk_models import RC
#===  =========================================================
class Change_party(BaseHandler):

    def get(self):
                                 

       
                        
        loader = template.Loader(os.path.join(ROOT_DIR, 'revision'))
        result = loader.load("change_party.js").generate()
              
        self.write({'def':[
                           {'type':"button", 'text':'Печать',         'action':'do_print',  'img':"print.gif", 'imgdis':"print_dis.gif"},
                           {'type':"button", 'text':'Добавить',       'action':'do_add',    'img':"add24.png", 'imgdis':"add24g.png"},
                           {'type':"button", 'text':'Удалить',        'action':'do_delete', 'img':"delete24.png", 'imgdis':"delete24g.png"},
                       
                     ],

                    'cmd': result         
            })



#==============================================================================
class Change_party_data(BaseHandler):

    def get(self, param):
                
        if param == 'list':
                            
            out = self.cursor.var(cx_Oracle.CURSOR) 
            
            res = self.proc("tehno_utils.change_party_list", [out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
            