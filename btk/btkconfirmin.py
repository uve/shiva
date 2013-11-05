# coding: utf-8

from core.sw_base import BaseHandler

import cx_Oracle

from core.common_tools import fetchall, fetchone

from barcode.zek_model import party2barcode

import os
from settings import ROOT_DIR, TEMPLATE_DIR
from tornado import template

#==============================================================================
class BTKConfirmIn(BaseHandler):

    def get(self):
        
        loader = template.Loader(os.path.join(ROOT_DIR, 'btk'))
        result = loader.load("btkconfirmin.js").generate()            
        
        self.write({'def': [ {'type':"button", 'enabled' : 'false', 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'id': 'id_print', 'action':'do_print'} ],
                   'cmd': result })


#==============================================================================
class BTKConfirmInData(BaseHandler):

    def get(self, param):
          
        header_id = self.get_argument("head",  None)
        party_id  = self.get_argument("party", None)
        
        out = self.cursor.var(cx_Oracle.CURSOR)  
          
        if param == "head":
            
            res = self.cursor.callproc("shiva.GetHeaderInputList", [self.session.uid, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return 
        

        if param == "list":
            
            res = self.cursor.callproc("shiva.GetFacturaPartyList", [header_id, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
        
        
        if param == "print":
            
            res = self.cursor.callproc("tehno.shiva.GetPartyInfo", [party_id, header_id, out])  
            
            results = fetchone(res[-1])
            results["ids"] = party2barcode(results["party"])
            
            pages = 1
                        
            loader = template.Loader(TEMPLATE_DIR)         
            output = loader.load("tovar_label.html").generate(results=results, pages=pages)    
            #self.write(output) 
            #return     
        
            output = output.replace('\n', '').replace('\r', '')        
            self.write({"cmd": "self.Incunable(function(doc){ doc.write('%s') })" % output})
            
            return     