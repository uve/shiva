# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Tovar, TypeTovar, Party
from barcode.zek_model import party2, party_size

#=== Печать зарегестрированных партий ========================================#
class PrintPartRegHandler(BaseHandler):
    urls = r'/warehouse/prnpartreg'

    def get(self):
        self.write({'def':[{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_1'}],
                    'cmd':'''var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                            sw_btk.items[0].setText("Список товаров");
                            sw_btk.items[1].setText("Список партий");

                            window.Cleaner.push(sw_btk);
                            
                            var sw_grid1 = sw_btk.cells("a").attachGrid();
                            sw_grid1.columns([
  { type:"ro", sort:"int", align:"right", width:"50",  label:["Код","#text_filter"] },  
  { type:"ro", sort:"str", align:"left",  width:"260", label:["Тип товара","#select_filter"] },
  { type:"ro", sort:"str", align:"left",  width:"*",   label:["Товар","#text_filter"] }
                            ]);
                                         
                            window.Cleaner.push(sw_grid1);

                            var sw_grid2 = sw_btk.cells("b").attachGrid();
                            sw_grid2.columns([
  { type:"ro", sort:"int",  align:"right", width:"80",  label:["ID","#text_filter"] },                            
  { type:"ro", sort:"int",  align:"right", width:"140", label:["Партия","#text_filter"] },  
  { type:"ro", sort:"date", align:"left",  width:"100", label:["Изготовлен","#text_filter"] },
  { type:"ro", sort:"date", align:"left",  width:"100", label:["Годен до","#text_filter"] },
  { type:"ro", sort:"int",  align:"right", width:"*",   label:"Кол-во" }  
                            ]);                            
                            window.Cleaner.push(sw_grid2);

                            sw_grid1.attachEvent("onRowSelect", function(id){
                                    self.LoadGrid(sw_grid2, "/warehouse/prnpartreg/data?tovar="+id) });
                                                           
                            // print party
                            window.do_tool_1 = function(){
                                var ids = sw_grid2.getSelectedRowId();
                                if(!ids) self.AddMessage('Выберите партию',2)
                                else self.PrintURL(%s,%s,"/warehouse/prnpartreg/data?party="+ids); 
                            }

                            self.LoadGrid(sw_grid1, "/warehouse/prnpartreg/data");''' % party_size
                    })



#=============================================================================#
class PrintPartRegDataHandler(BaseHandler):
    urls = r'/warehouse/prnpartreg/data'

    def get(self):
        inp = self.input(tovar=0, party=0)

        try: tovar = int(inp.tovar)
        except: tovar = 0
        try: part = int(inp.party)
        except: part = 0
        
        

        if tovar:
            
     
            self.write_XML(Party.select(tovar=tovar, order='date DESC')
                           .as_grid('id', 'num', 'd_iss', 'date', 'inbox',
                                  show={'date':lambda val: val.strftime("%d.%m.%Y"),
                                          'd_iss':lambda val: val.strftime("%d.%m.%Y")}))
            

        elif part:
            p = Party.get(id=part)
            self.write(party2(part, p.num, p.tovar_cls.name))
            self.set_header("Content-Type", "image/svg+xml")

        else:
            tt = ','.join(str(i.id) for i in TypeTovar.select_life())

            self.write_XML(Tovar.select('hide=1 AND typet in (%s)' % tt)
                           .as_grid('id', 'typet_cls.name', 'name'))

        return
