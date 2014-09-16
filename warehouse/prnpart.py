# coding: utf-8

#import urlparse
from core.sw_base import BaseHandler
from avtuk.avtuk_models import PartyTemp, ExtraPartyTemp
from barcode.zek_model import party, party_size, party2barcode, barcode2party

import os
from settings import ROOT_DIR

from tornado import template



#=== Печать партий ============================================================
class PrintPartHandler(BaseHandler):
    urls = r'/warehouse/prnpart'

    def get(self):
        
        
        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("print_party.js").generate(size=party_size)
       
       
        self.write({'def':[{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_print_party'},
                           {'type':"button", 'text':'Печать Подпартий', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_print_extra_party'},
                           ],
                    'cmd': result
                   })




#=============================================================================#
class PrintParDataHandler(BaseHandler):
    urls = r'/warehouse/prnpart/data'

    def get(self, param):
                
        ids = self.get_argument("ids", None)

        rem = ""

        p = self.get_argument("party", None)
        if p == "extra":
            rem = "ex"

        self.write(party(barcode2party(ids), rem=rem))
        self.set_header("Content-Type", "image/svg+xml")


    def post(self, param):
        
        ids = []        
        for _ in range(10):
            
            if param == "extra_party":
                x = ExtraPartyTemp()
                x.save()
                ids.append(party2barcode(x.id, '8'))
                
            elif param == "party":
                x = PartyTemp()
                x.save()
                ids.append(party2barcode(x.id))
            

        self.write(ids)
