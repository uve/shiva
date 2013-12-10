# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Header, Factura


#=== Приемка ==================================================================
class AcceptanceHandler(BaseHandler):
    urls = r'/warehouse/acceptance'

    def get(self):
        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
                 for k, v in enumerate(('-',
                                        'Без розничных продаж и подарков',
                                        'Только розничные продажи',
                                        'Только подарки клиентам'))]
        opers[0]['selected'] = "true"

        gates = [{"id":"gts%s" % i, "type":"button", "text":"%s" % i, "action":"do_tool_2"} for i in range(1, 5)]
        gates[0]['selected'] = "true"
        
        
        prn = [{"id":"prn%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_4"}
                 for k, v in enumerate(('Накладная',))]
                

        self.write({'def':[{'type':"button", 'text':'Принять фактуру', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},

                           {'type':"separator"},
                           {'type':"text", 'text':"  Фильтр:"},
                           {'id':"btnopr", 'type':"buttonSelect", 'text':'-', 'items':opers},

                           {'type':"separator"},
                           {'type':"text", 'text':"  Ворота №:"},
                           {'id':"btngts", 'type':"buttonSelect", 'text':'1', 'items':gates},
                           {'type':"separator"},
                           {'type':"separator"},
                           {'id':"btnprn", 'type':"buttonSelect", 'text':'Печать', 'items':prn},
                           
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],

                    'cmd':'''var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                            sw_btk.items[0].setText("Список фактур");
                            sw_btk.items[1].setText("Список товаров");
                            window.Cleaner.push(sw_btk);

                            var sw_grid1 = sw_btk.cells("a").attachGrid();
                            sw_grid1.columns([                            
  { type:"ro", sort:"int",  align:"right", width:"68",  label:"ID" },
  { type:"ro", sort:"int",  align:"right", width:"46",  label:"Номер" },
  { type:"ro", sort:"date", align:"right", width:"66",  label:"Дата" },
  { type:"ro", sort:"str",  align:"left",  width:"*",   label:"Поставщик" },
  { type:"ro", sort:"str",  align:"left",  width:"290", label:"Операция" },
  { type:"ro", sort:"str",  align:"left",  width:"100", label:"Статус" }                            
                            ]);

                            window.Cleaner.push(sw_grid1);
                            window.do_tool_csv = function(){ self.GridCSV(sw_grid1) }                            

                            var sw_grid2 = sw_btk.cells("b").attachGrid();
                            sw_grid2.columns([
  { type:"ro", sort:"int", align:"right", width:"55", label:"Код" },
  { type:"ro", sort:"str", align:"left",  width:"*",  label:"Товар" },
  { type:"ro", sort:"int", align:"right", width:"65", label:"Кол-во" }                      
                            ]);
                            
                            window.Cleaner.push(sw_grid2);

                            sw_grid1.attachEvent("onRowSelect", function(id){
                                    self.LoadGrid(sw_grid2, "/warehouse/acceptance/data/tovar?head="+id);
                                }
                            );

                            window.gts = 1;
                            window.ids = 0;

                            window.do_tool_1 = function(){
                                var ids = sw_grid1.getSelectedRowId();
                                if (!ids){
                                    self.AddMessage('Фактура не выбрана',3);
                                    return;
                                }
                                sw_grid2.editStop();

                                var dat="ids="+ids+"&gts="+window.gts;
                                
                                self.NetSend("/warehouse/acceptance/data/gts", dat);                               
                                sw_grid2.clearAll();
                                self.LoadGrid(sw_grid1, "/warehouse/acceptance/data/head");                                
                            }
                            
                            window.do_tool_2 = function(ids){
                                window.gts=parseInt(ids.substr(3));
                                var text = self.Toolbars["def"].getListOptionText("btngts", ids);                                            
                                self.Toolbars["def"].setItemText("btngts", text);                            
                            }

                            window.do_tool_3 = function(ids2){
                                window.ids=ids2.substr(3);
                                
                                var text = self.Toolbars["def"].getListOptionText("btnopr", ids2);                                            
                                self.Toolbars["def"].setItemText("btnopr", text);
                                sw_grid2.clearAll();                            
                                self.LoadGrid(sw_grid1, "/warehouse/acceptance/data/head?oper="+window.ids);
                            }
                            window.do_tool_3("opr0");
                            
                            // print passport
                            window.do_tool_4 = function(ids2){
                                var ids = sw_grid1.getSelectedRowId();
                                if(!ids) self.AddMessage('Выберите фактуру',2)
                                else {
                                    var m=ids2.substr(3);
                                    var d='';
                                    //Отгрузочные этикетки
                                    if(m==2){
                                        var d=prompt('Диапазон мест разделенные пробелом','').split(' ');
                                    }
                                    self.NetSend("/warehouse/printpassport/data/print?head="+ids+"&mode="+m+"&d="+d);
                                }                               
                            };
                            
                            '''
                    })



#==============================================================================
class AcceptanceDataHandler(BaseHandler):
    urls = r'/warehouse/acceptance/data/([^/]+)'

    def get(self, param):
        
        
        try:

            if param == 'head':
                oper = self.request.arguments["oper"][0]
                self.write_XML(Header.select_accept(opers=oper, rc=self.session.rc)
                               .as_grid('id', 'num', 'date', 'client_from_cls.name', 'oper_cls.name', 'status_cls.name',
                                        show={'date':lambda val: val.strftime("%d.%m.%Y")}))

            elif param == 'tovar':                
                header = self.request.arguments["head"][0]            
                self.write_XML(Factura.select(header=header)
                               .as_grid('tovar_cls.code', 'tovar_cls.name', 'count'))
        except:
            self.write_XML('<rows />')


    def post(self, param):
        if param == 'gts':

            ids = self.get_argument("ids", default=0)
            gts = self.get_argument("gts", default=1)
               

            try:

                self.cursor.callproc("shiva.NewInput", [ids, gts])
                            
                self.write({'info':'Информация сохранена'})
            except:
                self.write({'warning':'Ошибка записи'})
