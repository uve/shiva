  #!/usr/bin/env python
# -*- coding: utf-8 -*-


import cx_Oracle

from core.sw_base import BaseHandler

#=============================================================================


class AllocationHandler(BaseHandler):
    '''
    Обработка сообщений с ТСД при размещении паллет карщиком
    '''
    urls = r'/mbl/alloc'


    def post(self, param):

        cell_id   = self.get_argument("cell_id",   None)
        pallet_id = self.get_argument("pallet_id", None)

        if param == 'get_place':
                
            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.cursor.callproc("shiva.GetPlaceForPallet", [pallet_id, out])
                
            target_id, target_name = res[-1].fetchone()
            self.write({ 'target_name': target_name, 'target_id': target_id})
            

        elif param == 'set_place':
            
            # if inp.cellbarcode == 'BTC': Place = 0; # режим БТК - он такой, да
            
            self.cursor.callproc("shiva.SetPalletToPlace", [pallet_id, cell_id])


class MovingHandler(BaseHandler):
    '''
    Обработка сообщений с ТСД в режиме перемещения паллеты
    
    параметры:
        source_cell_barcode - ШК исходной ячейки
        target_cell_barcode - ШК ячейки назначения
        pallet - id паллеты.
        
    команды(приходят по ключу в cmd):
        SETCELL - запуск Shiva.SetCellStoreError()
        OKPALLET - запуск Shiva.OkPalletMove() 
    '''
    urls = r'/mbl/moving'


    def post(self, param):

        
            
        cell_id = self.get_argument("cell_id", None)
        target_id = self.get_argument("target_id", None)
        
        party_id = self.get_argument("party_id", None)
        value    = self.get_argument("value", None)
        

        user_id = self.session.uid


        if param == 'next_cell':
            out = self.cursor.var(cx_Oracle.CURSOR)            
            res = self.cursor.callproc("shiva.SetCellStoreError", [user_id, cell_id, target_id, out])
            
            target_id, target_name = res[-1].fetchone()
            self.write({ 'target_name': target_name, 'target_id': target_id})


        if param == 'moved':                         
 
            self.cursor.callproc("shiva.MovePalete", [cell_id, target_id])            


        if param == 'GetCellForPartyFromBox':
            out = self.cursor.var(cx_Oracle.CURSOR)          
            res = self.cursor.callproc("shiva.GetCellForPartyFromBox", [party_id, value, out])      

            code = res[-1].fetchone()
            
            if code:                
                self.write({ 'code': code})
            else:
                self.write({ 'error': "Код не найден"})
                

class BatchingOrders(BaseHandler):
    '''
    Сборка заказа покоробочно

    '''
    urls = r'/mbl/batching'


    def post(self, param):
        
        
        
        count = self.get_argument("count", None)
        task_id = self.get_argument("task_id", None)
        cell_id = self.get_argument("cell_id", None)                 
        pallet_id = self.get_argument("pallet_id", None)        
        target_id = self.get_argument("target_id", None)     
        
        
        # Для сборки сырья
        
        party_id = self.get_argument("party_id", None)   
        extra_party_id = self.get_argument("extra_party_id", None)  
        

                    
        if param == "bind_pallet":

            self.cursor.callproc("shiva.PalletToPackList", [task_id, pallet_id])                
            return
        
        

        if param == 'get_cell':
            
            
            value_cursor = self.cursor.var(cx_Oracle.CURSOR)            
            cell_cursor = self.cursor.var(cx_Oracle.CURSOR)
            target_cursor = self.cursor.var(cx_Oracle.CURSOR)
            
            
            res = self.cursor.callproc("shiva.GetCellValFromPackList", [pallet_id, value_cursor, cell_cursor, target_cursor])  
            
            
            value, count, count_total, product_name = res[-3].fetchone()
            
            cell_id, cell_name = res[-2].fetchone()
            target_id, target_name = res[-1].fetchone()
                        
                        
            self.write({ 'value':       value,
                         'count':       count,
                         'count_total': count_total,
                         'cell_id':     cell_id,
                         'cell_name':   cell_name,
                         'target_id':   target_id,
                         'target_name': target_name,
                         'product_name': product_name,
                         })
            
            return

     
        if param == 'ok_cell':
                        
            out = self.cursor.var(cx_Oracle.CURSOR)            
            res = self.cursor.callproc("shiva.OkCellValFromPackList", [pallet_id, cell_id, count, party_id, extra_party_id, out])    
            
            info = res[-1].fetchone()
            if info and info[0]:
                self.write({'info': info[0]});
                         
            return
                        
            
        if param == 'set_pallet':
            
            self.cursor.callproc("shiva.SetPalletToDelivery", [pallet_id, target_id])                 
            return
            
                
        

class CellFail(BaseHandler):
    '''
    Приём ошибок от пользователя
    
    0 - иная ошибка
    1 - неизвестная ячейка
    2 - ячейка пустая или заблокированная
    3 - ячейка занята
    4 - нет привязки паллеты к ячейке
    5 - паллета не соответствует ячейке
    6 - нет такой партии в ячейке
    7 - неизвестная партия
    8 - неверное количество коробок на паллете

    '''
    urls = r'/mbl/fail'


    def post(self):
        inp = self.input(party=0, cell_barcode=False, pallet=0, real_count=0, errcode=0, task=0)
        try:
            

            # 1) узнаем ID исходной ячейки по её ШК - если её передали от клиента, разумеется
            if inp.cell_barcode:
                # cell_tuple = barcode2cellinfo(inp.cell_barcode)
                cell_tuple = inp.cell_barcode
                
                self.cursor.execute("select shiva.GetCellFromAddress(:Dep, :C1, :C2, :C3) from dual",
                         Dep=cell_tuple[0],
                         C1=cell_tuple[1],
                         C2=cell_tuple[2],
                         C3=cell_tuple[3])

                rec = self.cursor.fetchone()
                if not rec[0]:
                    self.write(['ERROR', 'Неправильный адрес исходной ячейки'])
                    return

                cell_id = rec[0]

            else:
                # ШК ячейки не передавали
                cell_id = 0

            # 2) собственно, вызов функции
            self.cursor.execute("begin shiva.SetFailCell(:SOTRUD, :CELL, :PALLET, :PARTY, :VALUME, :TYPEBLOCK); end;",
                            SOTRUD=self.session.uid,
                            PALLET=inp.pallet,
                            CELL=cell_id,
                            PARTY=inp.party,
                            VALUME=inp.real_count,
                            TYPEBLOCK=inp.errcode)

            self.write(['OK'])

        except Exception, err:
            self.write(['ERROR', str(err)])




class TaskHandler(BaseHandler):
   
   
    def get(self, status):
        self.write({'error' : "Method Not Allowed"})   
        
        

    def post(self, status):
        user_id = self.session.uid
        
        if not user_id:
            return
        
        
        out = self.cursor.var(cx_Oracle.CURSOR)
        task_id = self.get_argument("task_id", None)
        
  
        
        if status == "check":
            res = self.cursor.callproc("shiva_task.UserTaskGet", [user_id, out])            
            task_id, type_id, description, header_id = res[-1].fetchone()
            
            if task_id:                       
                self.write({'task_id'    : task_id,
                            'type_id'    : type_id,
                            'header_id'  : header_id,
                            'description': description})            
            return


        if status == "abort":
            res = self.cursor.callproc("shiva_task.UserTaskAbort", [task_id, user_id])                      
            return

        if status == "apply":
            res = self.cursor.callproc("shiva_task.UserTaskApply", [task_id, user_id])                      
            return

        if status == "cancel":
            res = self.cursor.callproc("shiva_task.UserTaskCancel", [task_id, user_id])                      
            return
        
        if status == "complete":
            res = self.cursor.callproc("shiva_task.UserTaskComplete", [task_id, user_id])                      
            return    
   
        if status == "getcelldestination":
            res = self.cursor.callproc("shiva_task.GetCellDestination", [task_id, out])   
            result = res[-1].fetchone()

            if not result:
                raise Exception('Ячейка не определена')
            
            
            cell_name, cell_id, target_name, target_id = result
            
            self.write({'cell_name' :     cell_name,
                        'cell_id':        cell_id,
                        'cell_barcode':   cell_id,
                        'target_name':    target_name,
                        'target_id':      target_id,
                        'target_barcode': target_id})                        
            return       
