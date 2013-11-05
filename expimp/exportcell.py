# coding: utf-8

import datetime
from core.sw_base import BaseHandler
from avtuk.avtuk_models import ExportCell



#=== Все задания ==============================================================
class ExportCellHandler(BaseHandler):
    urls = r'/expimp/exportcell'

    def get(self):
        d1 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d.%m.%Y %H:%d')
        d2 = datetime.datetime.now().strftime('%d.%m.%Y %H:%d')
        
        
        self.write({'def':[{'type':"text", 'text':"Дата с:"},
                           {'id':"cal1", 'type':"buttonInput", 'width':120, 'value':d1},
                           {'type':"text", 'text':" по:"},
                           {'id':"cal2", 'type':"buttonInput", 'width':120, 'value':d2},
                     
                           {'type':"separator"},
                           {'type':"button", 'img':"csv.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           ],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        columns:[
      
                          { type:"ro", sort:"str",  align:"left",  width:"*",   label:["Ячейка","#text_filter"] }      
                        ]
                        });
                        
                        // для очистки памяти !!!
                        window.Cleaner.push(sw_grid);
                        
                        var bar = this.Toolbars["def"];
                        
                        var calendar1 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal1"].obj.firstChild );
                        calendar1.loadUserLanguage("ru");
                        calendar1.setDateFormat('%s');                        
                        //calendar1.hideTime();
                        calendar1.setDate('%s');
                                                                               
                        window.Cleaner.push(calendar1);
                                                        
                        var calendar2 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal2"].obj.firstChild );
                        calendar2.loadUserLanguage("ru");
                        calendar2.setDateFormat('%s');
                        //calendar2.hideTime();
                        calendar2.setDate('%s');
                        window.Cleaner.push(calendar2);
                        
                        calendar1.attachEvent("onClick", function (){ window.do_tool_1() });
                        calendar2.attachEvent("onClick", function (){ window.do_tool_1() });                            
                        
                        
                        
                        // фильтр
                        window.do_tool_1 = function(ids2){
                        
                            window.t = calendar1.getDate();
                        
                            var d1=calendar1.getDate().valueOf();
                            var d2=calendar2.getDate().valueOf();
                            
                            self.LoadGrid(sw_grid, "/expimp/exportcell/data?d1="+d1+"&d2="+d2+"&time="+new Date().getTime());
                        }

                                            
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }
                        
                        window.do_tool_1();''' % ('%d.%m.%Y %H:%i', d1, '%d.%m.%Y %H:%i', d2)
                    })


#==============================================================================
class ExportCellDataHandler(BaseHandler):
    urls = r'/expimp/exportcell/data'

    def get(self):
        try:
            
            d1 = self.get_argument("d1", None)
            d2 = self.get_argument("d2", None)
            
            ds = datetime.datetime.fromtimestamp(int(d1) / 1000).strftime("%Y-%m-%d %H:%M:%S")
            de = datetime.datetime.fromtimestamp(int(d2) / 1000).strftime("%Y-%m-%d %H:%M:%S")

            self.write_XML(ExportCell.select('''begin_date>=TO_TIMESTAMP(:ds, :r1) and begin_date<=TO_TIMESTAMP(:de, :r1)''',
                                                ds=ds, de=de, r1="YYYY-MM-DD HH24:MI:SS")
                           .as_grid('str', 'begin_date',
                                    show={'begin_date':lambda val: val.strftime("%d.%m.%Y %H:%M:%S") },))

        except:
            # заглушка
            self.write_XML('<rows />')

