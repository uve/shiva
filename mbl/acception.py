  #!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime 

import cx_Oracle

from core.sw_base import BaseHandler


class AcceptionHandler(BaseHandler):
    '''
    Прием команд пользователя о этапах приёмки:
    принята партия, принята паллета, приёмка завершена etc.
    
    команды (приходят по ключу в cmd):
        CHECKCELL - проверка приёмочной ячейки
        CHECKPALLET - проверка корректности паллеты (вызов shiva.IsPalletValid())
        ADDPALLET - добавить паллету (вызов shiva.AddNewPallet())
        GETVALUME - узнать сколько принято штук по данной фактуре
        ENDHEADER - завершение всей приёмки по некой фактуре (вызов shiva.OkInput())
        DROPPALLET - Откат паллеты в процессе приёмки (вызов shiva.DropPallet())
     
    параметры:
        party - id партии
        itemcode - код товара, который шестизначный
        header - id фактуры
        pallet - id паллеты
        onpallet - сколько коробок на паллете (VALUME)
        inbox - количество товара в коробке
        datado - срок годности (из JS передаётся как *строка*)
        btk - признак БТК (1-БТК, 0-нет)
        mode - просто флаг режима выполнения команды, может быть разным для разных cmd 
        pnum - номер партии
    '''

    def post(self, param):

            
        cell_id   = self.get_argument("cell_id",   None)
        party_id  = self.get_argument("party_id",  None)
        pallet_id = self.get_argument("pallet_id", None)
        header_id = self.get_argument("header_id", None)
        
        party_number  = self.get_argument("party_number",  None)
        
        count = self.get_argument("count", None)
        #if count:
        #    count = int(count)
        count_inbox = self.get_argument("count_inbox", None)
        
        
        count_all = self.get_argument("count_all", None)
        #if count_all:
        #    count_all = int(count_all)
                    
        is_btk = self.get_argument("is_btk", 0)
        
        product_id = self.get_argument("product_id", None)
         
        
        
        goden_do = self.get_argument("goden_do", default=None)
        
        if goden_do:
            goden_do = datetime.fromtimestamp(float(goden_do)).strftime('%d.%m.%Y')
  
        if param == 'check_cell':
            
            self.execute("select depart from depart where rc=:RC and depart_type=1", RC=self.session.rc)                        

            rec = self.cursor.fetchone()
            if not rec[0]:
                raise Exception('Не найден департамент')
            
            depart_id = int(rec[0])                  
            self.proc("shiva.IsCellValid", [cell_id, depart_id, header_id])
            return
        
        
            
        if param == 'check_pallet':
                        
            self.proc("shiva.IsPalletValid", [header_id, pallet_id])            
            return                 
                            



        if param == 'check_party':
                
           
            party_mode = self.func('shiva.IsPartyNew', returnType=cx_Oracle.NUMBER, parameters=[party_id])
            party_mode = int(party_mode)
                       
            # 0 - старая, известная партия, 1 - новая партия, неизвестная системе

            if party_mode == 0:  # если это старая партия - узнаем кол-во в коробке
                
                count_inbox = self.func('shiva.GetPartyInBox', returnType=cx_Oracle.NUMBER, parameters=[party_id])
                count_inbox = int(count_inbox)  # узнаем, сколько штук в коробке у этой партии
                
                self.write({"party_mode" : party_mode, 'count_inbox': count_inbox})  # отдадим результат обратно
            else:
                self.write({"party_mode" : party_mode})  # отдадим результат обратно            
                
            return
            
                
        if param == 'end_header':
            self.proc("shiva.OkInput", [header_id])
            return
        
        
            
        if param == 'addnewpallet':        
            # Добавить сушествующую паллету, не бтк            
            self.proc("shiva.AddNewPallet", [header_id, product_id, count, pallet_id, count_inbox, party_id, party_number,
                                                goden_do, is_btk, cell_id])
            return

            
        if param == 'addnewpallet_oldparty':        
            # Добавить сушествующую паллету, не бтк            
            self.proc("shiva.AddNewPallet_OldParty", [header_id, count, pallet_id, party_id, is_btk, cell_id, count_all])
            return


        if param == 'get_count_total':
            # GETVALUME - узнать сколько принято штук по данной фактуре
            
            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.proc("shiva.GetInputValume", [header_id, out])
                
            count_input, count_total = res[-1].fetchone()
            self.write({ 'count_input': count_input, 'count_total': count_total})

            return
        
            
        if param == 'get_all_products':

            res = self.execute('''select t.id, t.code, t.name from factura f, tovar t
                               where t.id=f.tovar and f.header= :HEADER order by t.name''', HEADER=header_id)
            
            result = res.fetchall()
            
            if not result:
                raise Exception('Не найдены статусы в справочнике')
            
            
            all_items = []
            for item in result:
                node = {}
                node["id"], node["code"], node["name"] = item
                
                all_items.append(node)
                
            self.write(all_items)
            
            return


class ItemListHandler(BaseHandler):
    '''
    Передача списка товаров клиенту по номеру фактуры
    Список товаров передаётся в виде готового элемента формы <SELECT> </SELECT>
    '''

    urls = r'/mbl/items'

    def post(self):
        inp = self.input(header=False, barcode=False)
        if inp.header:
            # Пришёл номер фактуры - надо отдать список товаров
            try:
                # 1) Вытащим все записи из базы

                self.execute('''select t.id, t.code, t.name from factura f, tovar t
                               where t.id=f.tovar and f.header= :HEADER order by t.name''', HEADER=inp.header)

                rec_list = []
                for rec in self.cursor.fetchall():
                    rec_list.append(rec)

                # 2) Сформируем ответ
                if rec_list:
                    # TODO: Если всего 1 товар найден?
                    resp = "<SELECT ID='ItemsList' class='lists' SIZE=12>"
                    # TODO: Проверить без []
                    resp += "".join(['<OPTION itemid=%s value="%s"> %s </OPTION> ' % (rec[0], rec[1], rec[2]) for rec in rec_list])
                    resp += "</SELECT><BR>"
                    # 3) Отдадим его клиенту
                    self.write(['OK', resp])
                else:
                    # 4) Если ничего не получилось найти - напишем об этом
                    self.write(['WARNING', '<B>нет данных для отображения</B>'])

            except self.application.connect().DatabaseError, err:
                self.write(['ERROR', str(err)])

        if inp.barcode:
            # Пришёл штрихкод - надо отдать код товара и его название
            try:
                # 1) найдём по ШК товар и его ID
                
                self.execute('''select t.id, t.code, t.name from tovar t
                    where sclad.IsNewTovarOrMod(t.id) in (0,1) 
                    and SUBSTR(t.barcode, 0, 12) = :BARCODE ''', BARCODE=inp.barcode)
                rec = self.cursor.fetchone()
                if rec:
                    # 2) сформируем красивый ответ
                    resp = '<BR><P class="hugetext">' + rec[2] + '</P><BR>'
                    # 3) отдадим его клиенту
                    self.write(['OK', rec[0], rec[1], rec[2], resp])
                else:
                    self.write(['WARNING'], 0, 0, 'Штрих-код товара не опознан. Выбирайте из списка')
            except Exception, err:
                self.write(['ERROR', 0, 0, str(err)])
