# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Header, Factura

import os
from tornado import template
import cx_Oracle

from settings import ROOT_DIR

from core.common_tools import fetchone, fetchall


#=== Приемка ==================================================================
class AcceptanceHandler(BaseHandler):
    urls = r'/warehouse/acceptance'

    def get(self):

        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("acceptance.js").generate()

        '''
        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
                 for k, v in enumerate(('-',
                                        'Без розничных продаж и подарков',
                                        'Только розничные продажи',
                                        'Только подарки клиентам'))]
        opers[0]['selected'] = "true"

        gates = [{"id":"gts%s" % i, "type":"button", "text":"%s" % i, "action":"do_tool_2"} for i in range(1, 5)]
        gates[0]['selected'] = "true"
        '''

        prn = [{"id":"prn%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_4"}
               for k, v in enumerate(('Накладная',))]

        self.write({'def':[{'type':"button", 'text':'Принять фактуру', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},

                           {'id':"btnprn", 'type':"buttonSelect", 'text':'Печать', 'items':prn},
                           
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],

                    'cmd' : result
                    })



#==============================================================================
class AcceptanceDataHandler(BaseHandler):
    urls = r'/warehouse/acceptance/data/([^/]+)'

    def get(self, param):

        if param == 'head':


            out = self.cursor.var(cx_Oracle.CURSOR)

            res = self.proc("shiva.GetHeaderIncomeList", [out])

            all_results = fetchall(res[-1], count=0)

            self.write(all_results)
            return

            #oper = self.request.arguments["oper"][0]
            #self.write_XML(Header.select_accept(opers=oper, rc=self.session.rc)
            #               .as_grid('id', 'num', 'date', 'client_from_cls.name', 'oper_cls.name', 'status_cls.name',
            #                        show={'date':lambda val: val.strftime("%d.%m.%Y")}))

        elif param == 'tovar':
            header = self.request.arguments["head"][0]
            self.write_XML(Factura.select(header=header)
                           .as_grid('tovar_cls.code', 'tovar_cls.name', 'count'))



    def post(self, param):
        

        if param == 'gts':

            ids = self.get_argument("ids", default=0)
            gts = self.get_argument("gts", default=1)
               

            try:

                self.proc("shiva.NewInput", [ids, gts])
                            
                self.write({'info':'Информация сохранена'})
            except:
                self.write({'warning':'Ошибка записи'})
