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
class Saldo_GapHandler(BaseHandler):
    urls = r'/revision/auditor'

    def get(self):
                                 

       
                        
        loader = template.Loader(os.path.join(ROOT_DIR, 'revision'))
        result = loader.load("saldo_gap.js").generate()
       
        all_departs = RC.get_current(rc=self.session.rc).depart_cls
        # кнопки с департаментами РЦ
        
        departs = [{"id":"%s" % i.id, "type":"button", "text":i.name} for i in all_departs]       
       
        self.write({'def':[
                           
                           {'type':"text", 'text':"Подразделение:"},
                           {'id':'departs', 'type':"buttonSelect",  'mode':'select', 'selected': all_departs[0].id,  'items':departs},
                     ],

                    'cmd': result
         
            })


#==============================================================================
class Saldo_GapDataHandler(BaseHandler):
    urls = r'/revision/saldo_gap/data/([^/]+)'


    def get(self, param):
        
        departs = self.get_argument("departs", None)
            
            
        if param == 'list':
                
            
            out = self.cursor.var(cx_Oracle.CURSOR) 
            
            res = self.cursor.callproc("shiva.GetSaldoGap", [departs, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
            