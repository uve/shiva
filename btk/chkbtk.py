# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Header

from avtuk.executor import Executor

#=== Проверка БТК =============================================================
class BTKChkHandler(BaseHandler):
    urls = r'/btk/chkbtk'

    def get(self):
        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
                 for k, v in enumerate(('-',
                                        'Без розничных продаж и подарков',
                                        'Только розничные продажи',
                                        'Только подарки клиентам'))]
        opers[0]['selected'] = "true"

        self.write({'def':[{'type':"button", 'text':'Принять фактуру', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},

                           {'type':"separator"},
                           {'type':"text", 'text':"  Фильтр:"},
                           {'id':"btnopr", 'type':"buttonSelect", 'text':'-', 'items':opers},

                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],

                    'cmd':'''var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                            sw_btk.items[0].setText("Список фактур");
                            sw_btk.items[1].setText("Список товаров");
                            window.Cleaner.push(sw_btk);

                            var sw_grid1 = sw_btk.cells("a").attachGrid();
                            sw_grid1.columns([
  { type:"ro", sort:"int",  align:"right", width:"68",  label:"ID" },
  { type:"ro", sort:"int",  align:"right", width:"52",  label:"Номер" },
  { type:"ro", sort:"date", align:"right", width:"75",  label:"Дата" },
  { type:"ro", sort:"str",  align:"left",  width:"*",   label:"Поставщик" },
  { type:"ro", sort:"str",  align:"left",  width:"270", label:"Операция" }
                            ]);
                            window.Cleaner.push(sw_grid1);
                            window.do_tool_csv = function(){ self.GridCSV(sw_grid) }

                            var sw_grid2 = sw_btk.cells("b").attachGrid();
                            sw_grid2.columns([
  { type:"ro", sort:"int", align:"right",  width:"55", label:"Партия" },
  { type:"ro", sort:"int", align:"right",  width:"55", label:"Код" },
  { type:"ro", sort:"str", align:"left",   width:"*",  label:"Товар" },
  { type:"ro", sort:"int", align:"right",  width:"60", label:"Кол-во" },
  { type:"dhxCalendar", sort:"date", align:"right", width:"77", label:"Годен до" },
  { type:"ch", sort:"str", align:"center", width:"62", label:"Проверен" }
                            ]);
                            window.Cleaner.push(sw_grid2);

                            sw_grid1.attachEvent("onRowSelect", function(id){
                                    self.LoadGrid(sw_grid2, "/btk/chkbtk/data/tovar?head="+id);
                                }
                            );
                            
                            window.ids = 0;

                            window.do_tool_1 = function(){
                                var ids = sw_grid1.getSelectedRowId();
                                if (!ids){
                                    self.AddMessage('Фактура не выбрана',3);
                                    return;
                                }
                                sw_grid2.editStop();

                                var dat=[];
                                sw_grid2.forEachRow(function(ids2){
                                    if(!!parseInt(sw_grid2.cells(ids2, 4).getValue()))
                                        dat.push(ids2);
                                });

                                self.NetSend("/btk/chkbtk/data/party", "ids="+ids+"&dat="+dat.join());
                                
                                sw_grid2.clearAll();
                                self.LoadGrid(sw_grid1, "/btk/chkbtk/data/head");
                            }
                            
                            window.do_tool_3 = function(ids2){
                                window.ids=ids2.substr(3);
                                
                                var text = self.Toolbars["def"].getListOptionText("btnopr", ids2);                                            
                                self.Toolbars["def"].setItemText("btnopr", text);
                                sw_grid2.clearAll();                            
                                self.LoadGrid(sw_grid1, "/btk/chkbtk/data/head?oper="+window.ids);
                            }
                        
                            window.do_tool_3("opr0");'''
                    })


#==============================================================================
class BTKChkDataHandler(BaseHandler):
    urls = r'/btk/chkbtk/data/([^/]+)'

    def get(self, param):
        if param == 'head':
            try: oper = int(self.input(oper=0).oper)
            except: oper = 0
            self.write_XML(Header.select_BTK(oper, rc=self.session.rc)
                           .as_grid('id', 'num', 'date', 'client_from_cls.name', 'oper_cls.name',
                                    show={'date':lambda val: val.strftime("%d.%m.%Y")}))

        elif param == 'tovar':
            try: head = int(self.input(head=0).head)
            except: head = 0

            sql = '''SELECT pa.party,  t.code, t.name, sum(r.valume) valume, pa.data, 1 sm
                     FROM recordp r, tovar t, party pa, factura f
                     WHERE r.factura=f.id 
                       AND pa.party=r.party
                       AND t.id = pa.tovar 
                       AND f.header=%s
                     GROUP BY pa.party, t.code, t.name, pa.data''' % head
            self.write_XML(Executor.exec_cls(sql)
                           .as_grid('party', 'code', 'name', 'valume', 'data', 'sm',
                                    show={'data':lambda val: val.strftime("%d.%m.%Y")},
                                    id='party'))


    def post(self, param):
        if param == 'party':
            inp = self.input(ids=0, dat='')

            try:
                ids = int(inp.ids)
                for i in [int(i) for i in inp.dat.split(',')]:
                    # Подтверждение партии на БТК
                    # (pHeader in integer, pParty in integer)
                    Executor.exec_sql('BEGIN shiva.OkPartyInput(:d1, :d2); END;', d1=ids, d2=i)

                # подтверждение всей фактуры 
                Executor.exec_sql('BEGIN tsclad.oksdelka(:d1, 0); END;', d1=ids)
                self.write({'info':'Информация сохранена'})
            except:
                self.write({'warning':'Ошибка записи'})
