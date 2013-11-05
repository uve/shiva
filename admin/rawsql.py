# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.executor import Executor

#=== Сырой SQL ================================================================
class RawSQLHandler(BaseHandler):
    urls = r'/admin/rawsql'

    def get(self):        
        self.write({'def':[{'type':"button", 'text':'Execute', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           '<textarea id="sw_tsq" style="padding:5px; width:100%;height:100%"></textarea>'],
                    'cmd':'''var sw_sqla = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                            sw_sqla.items[0].setText("Результат");
                            sw_sqla.items[1].setText("SQL");
                            window.Cleaner.push(sw_sqla);

                            var sw_grid1 = sw_sqla.cells("a").attachGrid();
                            window.Cleaner.push(sw_grid1);
                            window.do_tool_csv = function(){ self.GridCSV(sw_grid1) }                            
                            
                            sw_sqla.cells("b").attachObject("sw_tsq");
                            document.getElementById("sw_tsq").focus();

                            window.do_tool_1 = function(){
                                var dat=document.getElementById('sw_tsq').value;
                                if(!dat)
                                    self.AddMessage('No SQL', 3);
                                else
                                    self.NetSend("/admin/rawsql/data", dat, function(response){
                                        var xml=response.xmlDoc.responseText;
                                        
                                        if(200 != response.xmlDoc.status) self.AddMessage(xml, 3);
                                        else
                                        if(xml) sw_grid1.parse(xml,"xml");
                                    });
                                document.getElementById("sw_tsq").focus();
                            }'''
                    })


#==============================================================================
class RawSQLDATAHandler(BaseHandler):
    urls = r'/admin/rawsql/data'

    def post(self):
        try:
            self.write_XML(Executor.exec_cls(self.request.body, multi=True).as_grid(head=True))
            # self.write(['ERROR', 'Режим заблокирован администратором'])
            # self.write({'error': 'Режим заблокирован администратором' })
            
            pass 
        except Exception, e:
            self.set_status(404)
            self.write(str(e))
