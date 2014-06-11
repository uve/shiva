#!/usr/bin/env python
# -*- coding: utf8 -*- 

from core.sw_base import BaseHandler


import os
from settings import ROOT_DIR


from tornado import template
import cx_Oracle


from core.common_tools import fetchall, fetchall_by_count

#, fetchone, fetchall_by_name

from avtuk.avtuk_models import RC
#===  =========================================================
class Saldo_GapHandler(BaseHandler):
    urls = r'/revision/auditor'

    def get(self):

        loader = template.Loader(os.path.join(ROOT_DIR, 'revision'))
        result = loader.load("saldo_gap.js").generate()
       
        all_departs = RC.get_current(rc=self.session.rc).depart_cls
        # кнопки с департаментами РЦ
        
        departs = [{"id":"%s" % i.id, "type":"button", "text":i.name, "action":"change_depart"} for i in all_departs]
       
        self.write({'def':[
                           #{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_print'},
                           #{'type':"separator"},

                           {'type':"button", 'text':'Excel (кратко)',    'action':'do_csv', 'img':"excel24.png", 'imgdis':"excel24g.png"},
                           {'type':"button", 'text':'Excel (подробно)',  'action':'do_csv_full', 'img':"excel24.png", 'imgdis':"excel24g.png"},
                           {'type':"separator"},
                           {'type':"text", 'text':"Подразделение:"},
                           {'id':'departs', 'type':"buttonSelect",  'mode':'select', 'selected': all_departs[0].id,  'items':departs},

                           '''<table style='width:100%'>

                                <tr><td colspan="2"><div id='sw_grid1' style="width:100%; height:250px;"></div></td></tr>
                                <tr><td colspan="2"><span>Детализация:</span></td></tr>
                                <tr><td colspan="2"><div id='sw_grid2' style="width:100%; height:300px;"></div></td></tr>

                              </table>
                           '''],

                    'cmd': result
         
            })


#==============================================================================
class Saldo_GapDataHandler(BaseHandler):
    urls = r'/revision/saldo_gap/data/([^/]+)'


    def get(self, param):
        
        departs = self.get_argument("departs", None)
        code    = self.get_argument("code", None)
            
            
        if param == 'list':
                
            
            out = self.cursor.var(cx_Oracle.CURSOR) 
            
            res = self.proc("shiva.GetSaldoGap", [departs, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return



        if param == 'csv':


            out = self.cursor.var(cx_Oracle.CURSOR)

            res = self.proc("shiva.GetSaldoGap", [departs, out])

            all_results = fetchall_by_count(res[-1])

            self.write(all_results)
            return



        if param == 'csv_full':


            out = self.cursor.var(cx_Oracle.CURSOR)

            res = self.proc("shiva.dif_saldo_tehno_shiva", [departs, out])

            all_results = fetchall_by_count(res[-1])

            self.write(all_results)
            return




        if param == 'detail':


            out = self.cursor.var(cx_Oracle.CURSOR)

            res = self.proc("shiva.tovar_address", [departs, code, out])

            all_results = fetchall(res[-1])

            self.write(all_results)
            return