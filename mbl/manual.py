  #!/usr/bin/env python
# -*- coding: utf-8 -*-

import cx_Oracle

from core.sw_base import BaseHandler

from datetime import datetime


from core.common_tools import fetchall_by_name

class InventoryHandler(BaseHandler):
    '''
    Все, что нужно для инвентаризации
    '''
    urls = r'/mbl/inventory/([^/]+)'

    #@gen.coroutine
    def post(self, param):
                
        delivery_id = self.get_argument("delivery_id", default=None)
        cell_id     = self.get_argument("cell_id",     default=None)
        pallet_id   = self.get_argument("pallet_id",   default=None)
        party_id    = self.get_argument("party_id",    default=None)
        target_id   = self.get_argument("target_id",   default=None)
        
        
        count_inbox  = self.get_argument("count_inbox",  default=None)        
        product_id   = self.get_argument("product_id",   default=None)        
        party_number = self.get_argument("party_number", default=None)             
        plus         = self.get_argument("plus",         default=0)
        
        party_status = self.get_argument("party_status", default=None)        
        header_id    = self.get_argument("header_id",    default=None) 
        client_id    = self.get_argument("client_id",    default=None)
                 
        count        = self.get_argument("count",        default=None)
        
        # if count:
        #    count = float(count)
            
        product_code = self.get_argument("product_code", default=None)
                       
                                
        goden_do = self.get_argument("goden_do", default=None)
        
        if goden_do:
            goden_do = datetime.fromtimestamp(float(goden_do)).strftime('%d.%m.%Y')
            

        
        if param == 'setparty':
 
            self.cursor.callproc("shiva.SetPartyCell", [pallet_id, party_id, product_id, count_inbox,
                                                 goden_do, party_number,
                                                 cell_id, count, plus, party_status])
            return
        
        

        if param == 'add_product_to_input':
  
            self.cursor.callproc("shiva.AddProductToInput", [header_id, pallet_id, party_id, product_id, count_inbox,
                                                 goden_do, party_number,
                                                 cell_id, count, plus, party_status])
                        
            return
        
        
        if param == 'add_product':
 
            self.cursor.callproc("shiva.AddProductToOutput", [header_id, cell_id, party_id, count])                
            return
        
        
        if param == 'end_input':
                      
            self.cursor.callproc("shiva.EndInputProduct", [header_id])                
            return
        
        if param == 'end_output':
                      
            self.cursor.callproc("shiva.EndOutputProduct", [header_id])                
            return



        if param == 'start_input':            
            out = self.cursor.var(cx_Oracle.NUMBER)
            
            res = self.cursor.callproc("shiva.StartInputProduct", [out])
            
            self.write({'header_id' : int(res[-1])})
            return
        
        
        

        if param == 'start_output':            
            out = self.cursor.var(cx_Oracle.NUMBER)
            
            res = self.cursor.callproc("shiva.StartOutputProduct", [client_id, out])
            
            self.write({'header_id' : int(res[1])})
            return
        
        

        
        
        if param == 'all_clients':
                     
            self.cursor.execute("select client_id as id, name from distribution_center where type=1")
            
            all_results = []
            
            for item in self.cursor.fetchall():
                node = {}
                node["id"], node["name"] = item
                all_results.append(node)
                
            self.write(all_results)
                
            return
        
        
        if param == 'get_from_cell':
            
            self.cursor.callproc("shiva.TakeValFromCell", [pallet_id, party_id, cell_id, count, target_id])
            return
        
        
        
        if param == 'empty_cell':
        
            if not cell_id:
                raise Exception('Неправильный номер ячейки')
                        
            self.cursor.callproc("shiva.EmptyCell", [cell_id])

 
            return

  
  
        if param == 'block_cell':
        
            if not cell_id:
                raise Exception('Неправильный номер ячейки')
            
            self.cursor.callproc("shiva.BlockCell", [cell_id])

            return          
    
    
    
        if param == 'unblock_cell':
        
            if not cell_id:
                raise Exception('Неправильный номер ячейки')
            
            self.cursor.callproc("shiva.UnBlockCell", [cell_id])
            
 
            return
        
        
        
        if param == 'checkparty':        
            
            if not party_id:
                raise Exception('Неправильный номер партии')
            
                        
            self.cursor.execute("select count(*) from sw_party where id=:party", party=party_id)
            value = self.cursor.fetchone()[0]
            
            if int(value) > 0:
                self.write({"is_new": True})
                return
            else:
                self.write({"is_new": False})
                return



        if param == 'get_product':
                       
            out = self.cursor.var(cx_Oracle.CURSOR)
            
            res = self.cursor.callproc("shiva.getlistbycode", [product_code, out])
            
            result = res[1].fetchall()
            
            if not result:
                raise Exception('Не найден товар в справочнике')
            
            
            all_tovars = []
            for item in result:
                node = {}
                node["id"], node["code"], node["name"] = item
                
                all_tovars.append(node)
            self.write(all_tovars)
            
            return
        
        
        
        if param == 'all_party_status':              

            res = self.cursor.execute("select id,name from vw_iq_status_cell")
            
            result = res.fetchall()
            
            if not result:
                raise Exception('Не найдены статусы в справочнике')
            
            
            all_items = []
            for item in result:
                node = {}
                node["id"], node["name"] = item
                
                all_items.append(node)
                
            self.write(all_items)
            
            return



        if param == 'clear_tovar':
                        
            # 3) позовем хранимую процедуру

            
            self.cursor.callproc("shiva.ClearTovarInProduction", [product_id, 77, count_inbox])
            
 
            return
        
        
        # Отправка клиенту 
        if param == 'set_pallet_delivery':
            
            self.cursor.callproc("shiva.SetPalletDelivery", [delivery_id])
            
            return
        
        
        # Перемещение со штучного
        if param == 'send_from_item_to_delivery':
        
            value_cursor = self.cursor.var(cx_Oracle.CURSOR)           
            cell_cursor = self.cursor.var(cx_Oracle.CURSOR)
            
            
            res = self.cursor.callproc("shiva.setfromitemtodelivery", [delivery_id, cell_cursor, value_cursor])  
            
            count = res[-1].fetchone()[0]
        
            cell_id, cell_name = res[-2].fetchone()
            
                        
            self.write({'cell_name' : cell_name,
                        'cell_id':    cell_id,
                        'count':      count})            
            
                        
            return   
        
        
        
        if param == 'get_cell_info':
        
                       
            value_cursor = self.cursor.var(cx_Oracle.CURSOR)
            
            
            res = self.cursor.callproc("shiva.GetCellInfo", [cell_id, value_cursor])  
            
            
            results = fetchall_by_name(res[-1])
                                
            self.write(results)            
                        
            return           
        
        
class ManualIncrease(BaseHandler):
    '''
    Ручная подтоварка
    '''
    urls = r'/mbl/increase/([^/]+)'

    
    def post(self, param):
        
        
        user_id = self.session.uid
        
        if param == 'add':
                     
            cell_id = self.get_argument("cell_id", default=None)   
            self.cursor.callproc("shiva.AddNeedMove", [user_id, cell_id])
            return        
        
        
        
        if param == 'complete':

            self.cursor.callproc("shiva.CreateHeaderNeedMove", [user_id])
            return            



class ManualValidation(BaseHandler):
    '''
    Ручная валидация
    запуск функции shiva.IsPartyCellValid()
    '''
    urls = r'/mbl/valid'

    
    def post(self):
                
        cell_id = self.get_argument("cell_id", None)
        party_id = self.get_argument("party_id", None)
        pallet_id = self.get_argument("pallet_id", None)
        
        self.cursor.callproc("shiva.IsPartyCellValid", [party_id, cell_id, pallet_id])
                 


