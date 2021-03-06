# coding: utf-8

from core.sw_base import BaseHandler

import cx_Oracle

from core.common_tools import fetchall, fetchone, fetchall_by_name

from barcode.zek_model import party2barcode

import os
from settings import ROOT_DIR, TEMPLATE_DIR
from tornado import template

#==============================================================================
class BTKConfirmIn(BaseHandler):

    def get(self):
        
        loader = template.Loader(os.path.join(ROOT_DIR, 'btk'))
        
        
        out = self.cursor.var(cx_Oracle.CURSOR)
        res = self.proc("shiva.Get_Iq_Status", [2, out])  
        all_status = fetchall_by_name(res[-1])
         
        
        
        result = loader.load("btkconfirmin.js").generate(all_status=all_status)            
        
        self.write({'def': [ {'type':"button", 'enabled' : 'false', 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'id': 'id_print', 'action':'do_print'},
                             {'type':"button", 'text':'Подтвердить', 'id': 'id_confirm', 'action':'do_confirm'} ],
                   'cmd': result })


#==============================================================================
class BTKConfirmInData(BaseHandler):

    def get(self, param):
          
        header_id = self.get_argument("head",  None)
        party_id  = self.get_argument("party", None)
        status  = self.get_argument("status", None)
        
        out = self.cursor.var(cx_Oracle.CURSOR)  



        if param == "change_status":
            
            res = self.proc("tehno.shiva.SetIqStatusParty", [header_id, party_id, status])           
            return 
            
          
        if param == "head":
            
            res = self.proc("shiva.GetHeaderInputList", [self.session.uid, out])  
            
         
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return 
        

        if param == "list":
            
            res = self.proc("shiva.GetFacturaPartyList", [header_id, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
        
        
        if param == "print":


            res = self.proc("tehno.shiva.GetPartyInfo", [party_id, header_id, out])  
            
            info = fetchone(res[-1])
            

            res = self.proc("tehno.shiva.extra_party_barcode_for_party", [party_id, out])


            pages = fetchall_by_name(res[-1])

            #results["ids"] = party2barcode(results["party"])

                        
            loader = template.Loader(TEMPLATE_DIR)         
            output = loader.load("tovar_label.html").generate(results=info, pages=pages)
            #self.write(output) 
            #return     
        
            output = output.replace('\n', '').replace('\r', '')

            self.write({"cmd": "self.Incunable(function(doc){ doc.write('%s') })" % output})
            #self.write(output)
            
            return


    def post(self, param):

        header_id = self.get_argument("head",  None)

        
        if param == "confirm":
            
            res = self.proc("shiva.OkInputBtk", [header_id])  
     
            return        
        
        