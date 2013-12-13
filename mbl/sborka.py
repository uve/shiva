#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cx_Oracle

from core.sw_base import BaseHandler


class Terminal_Sborka(BaseHandler):

    def post(self, param):
        
        count     = self.get_argument("count",     None)
        cell_id   = self.get_argument("cell_id",   None)        
        party_id  = self.get_argument("party_id",  None)
        header_id = self.get_argument("header_id", None)                
        pallet_id = self.get_argument("pallet_id", None)
        

        if param == 'new_sborka_for_shtuka':
                
            out = self.cursor.var(cx_Oracle.STRING)    
            res = self.proc("shiva.NewSborkaForShtuka", [self.session.uid, out])
                
            header_id = res[-1]
            self.write({ 'header_id': header_id})
            
            return
            
            
            
        if param == 'add_factura_for_shtuka':
                
            out = self.cursor.var(cx_Oracle.STRING)    
            self.proc("shiva.AddFacturaForShtuka", [header_id, party_id, count, pallet_id, cell_id])

            return
            
        
            
        if param == 'end_factura_for_shtuka':
                
            out = self.cursor.var(cx_Oracle.STRING)    
            self.proc("shiva.EndFacturaForShtuka", [header_id])
            
            return