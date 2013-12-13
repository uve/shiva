# coding: utf-8

from core.sw_base   import BaseHandler
from avtuk.executor import Executor

from core.common_tools import fetchall
import os
from settings import ROOT_DIR
from tornado import template

import cx_Oracle

#=== Заблокированные ячейки ===================================================
class BlockCellHandler(BaseHandler):
    urls = r'/revision/blockcell'

    def get(self):
        loader = template.Loader(os.path.join(ROOT_DIR, 'revision'))
        result = loader.load("blockcell.js").generate()            
        
        self.write({'def':[{'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'} ],
                    'cmd': result })
      

#==============================================================================
class BlockCellDataHandler(BaseHandler):
    urls = r'/revision/blockcell/data'

    def get(self, param):
        
        if param == "list":
            
            sql = '''select fc.id, tp.name addr, to_char(fc.dstart,'DD.MM.YYYY') dstart, fct.name, s1.name name1, fc.palete, fc.valume, fc.party
                      from sw_failcell fc
                      join tovar_place tp on fc.tovar_place = tp.id
                      join sw_failcelltypes fct on fc.typeblock = fct.id
                      join sotrud s1 on fc.sotrud = s1.id
                     where dend is Null 
                     order by tp.name'''
    
            self.execute(sql)
    
            all_results = fetchall(self.cursor)
            
            self.write(all_results)  
            return
        
        
        
        if param == "history":
            
            cell_id = self.get_argument("cell_id",  None)
            out = self.cursor.var(cx_Oracle.CURSOR) 
            
            res = self.proc("shiva.GetPalletHistory", [cell_id, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
