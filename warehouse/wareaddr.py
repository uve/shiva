# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import RC


from tornado import template
import cx_Oracle

import os
from settings import ROOT_DIR

from core.common_tools import fetchone, fetchall


#=== Адреса хранения ==========================================================
class WareAddressHandler(BaseHandler):
    urls = r'/warehouse/wareaddr'


    def get(self):


        out = self.cursor.var(cx_Oracle.CURSOR)

        all_tovar_types = self.proc("shiva.GetTovarTypeList", [self.session.rc, out])

        # список типов товара
        tovar_types = [{"id": i[0], "type":"button", "text": i[1]} for i in all_tovar_types[-1].fetchall()]
        
        
        all_storage_types = self.proc("shiva.GetStorageTypeList", [self.session.rc, out])    

        # список типов хранения
        storage_types = [{"id": i[0], "type":"button", "text":i[1]} for i in all_storage_types[-1].fetchall()]                
        
        
        res = self.execute("select id,name from vw_iq_status_cell")
        all_status = res.fetchall()
        
        all_items = [
                            
                           {'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_print'},
                           {'type':"button", 'text':'Печать партии', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_print_party'},

                           {'type':"button", 'text':'Выделенные в CSV', 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_csv', 'title':'Сохранить в CSV'},
                           {'type':"button", 'text':'Все в CSV', 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_csv_all', 'title':'Сохранить все в CSV'},
                 ]
    

        edit_tools = [
                        {'type':"button", 'text':'Правка', 'img':"edit24.png", 'imgdis':"edit24g.png", 'action':'do_tool_edit'},
                        {'type':"separator"},
                        {'type':"button", 'text':"Заблокировать", 'action':'do_block', 'title':'Заблокировать'},
                        {'type':"button", 'text':"Разблокировать", 'action':'do_unblock', 'title':'Разблокировать'},
                        {'type':"separator"},
                      ]
        
        if self.session.role != "26":
            all_items = edit_tools + all_items
            

          
        all_departs = RC.get_current(rc=self.session.rc).depart_cls
        # кнопки с департаментами РЦ  
        departs = [{"id":"%s" % i.id, "type":"button", "text":i.name}
                   for i in all_departs]


                        
        # фильтр ячеек
        is_all = [
                  {"id":"0", "type":"button", "text":"Все"},
                  {"id":"1", "type":"button", "text":"Заполненные"},                  
                  {"id":"2", "type":"button", "text":"Пустые"},
                 ]


        # фильтр ячеек
        is_block = [{"id":"0", "type":"button", "text":"Все"},
                    {"id":"1", "type":"button", "text":"Не заблокированные"},
                    {"id":"2", "type":"button", "text":"Заблокированные"},
                   ]
                    

        # годен до
        godenDo = [{"id":"0",    "type":"button", "text":"Не выбрано"},
                    {"id":"90",  "type":"button", "text":"Истекает не позже 90 дней"},
                    {"id":"180", "type":"button", "text":"Истекает не позже 180 дней"},
                   ]                    
                    
            
        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("wareaddr.js").generate(departs=departs[0], is_all=is_all[0], is_block=is_block[0], all_status=all_status, godenDo=godenDo[0])            
    
        self.write({'def':[
                           
                                                     
                            {'id':'bdep', 'type':"buttonSelect", 'text':'Режимы', 'items': all_items },
                           
                            {'type':"separator"},
                           
                           
                           {'type':"text", 'text':"Подразделение:"},
                           {'id':'departs', 'type':"buttonSelect",  'mode':'select', 'selected': all_departs[0].id,  'items':departs},
                           {'type':"separator"},

                           {'type':"text", 'text':"Ячейки:"},
                           {'id':'is_all', 'type':"buttonSelect",   'mode':'select', 'selected': '1', 'items':is_all},
                           {'type':"separator"},

                           {'type':"text", 'text':"Блокировки:"},
                           {'id':'is_block', 'type':"buttonSelect", 'mode':'select', 'selected': '0', 'items':is_block},
                           {'type':"separator"},
                           
                           
                           {'type':"text", 'text':"Срок Годности:"},
                           {'id':'godenDo', 'type':"buttonSelect", 'mode':'select', 'selected': '0', 'items':godenDo},
                           {'type':"separator"},
                      
                      
                      
                          # {'type':"text", 'text':"Типы товара:"},
                          # {'id':'is_block', 'type':"buttonSelect", 'mode':'select', 'selected': '0', 'items':tovar_types},
                          # {'type':"separator"},                           
                           
                          # {'type':"text", 'text':"Типы хранения:"},
                          # {'id':'is_block', 'type':"buttonSelect", 'mode':'select', 'selected': '0', 'items':storage_types},
                          # {'type':"separator"},
                      
                           
                           
                           {'type':"separator"},
                           {'type':"button", 'img':"restart.png", 'action':'update', 'text':'Обновить'},
             
                           ],

                    'one':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_save'},
                           {'type':"button", 'text':'Отмена', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_cancel'},
                           '<div id="sw_form" />'],
                    
                    'cmd': result      
             })



#==============================================================================
class WareAddressDataHandler(BaseHandler):
    urls = r'/warehouse/wareaddr/data'

    def get(self): 
        
        pDepart      = self.get_argument("departs",  default=None)
        is_All       = self.get_argument("is_all",   default=None)
        is_Block     = self.get_argument("is_block", default=None)
        psw_id       = self.get_argument("psw_id",   default=None)  # # Одна ячейка для редактировани
        
        pCellName    = self.get_argument("dhx_filter[3]",  default="")
        pStorage     = self.get_argument("dhx_filter[4]",  default="")
        pTypeTovar   = self.get_argument("dhx_filter[5]",  default="")
        pCode        = self.get_argument("dhx_filter[6]",  default="")
        pName        = self.get_argument("dhx_filter[7]",  default="")
        pParty       = self.get_argument("dhx_filter[11]", default="")
        pPartyStatus = self.get_argument("dhx_filter[13]", default="")
        
        godenDo      = self.get_argument("godenDo", default=None)
        
        
        out = self.cursor.var(cx_Oracle.CURSOR)
        
        
        res = self.proc("shiva.GetSaldoList", [pDepart, is_All, is_Block, psw_id, pCellName,
                                                          pStorage, pTypeTovar, pCode, pName, pParty, pPartyStatus, godenDo, out])                
     
        all_results = None
             
        if psw_id:                           
            all_results = fetchone(res[-1])        
        else:
            all_results = fetchall(res[-1], count=1)
                    
        self.write(all_results)         



    
    def post(self):
        
        sw_id  = self.get_argument("uid",    default=None)
        addr   = self.get_argument("addr",  default=None)
        inbox  = self.get_argument("inbox", default=None)
        box    = self.get_argument("box",   default=None) 
        code   = self.get_argument("code",  default=None)
        num    = self.get_argument("num",   default=None)
        
        condition_code = self.get_argument("condition_code", default=None)

        
        result = self.proc("shiva.EditPalletPartyCell", [sw_id, addr, box, inbox, code, num, condition_code])
        
        self.write({"status": result})
