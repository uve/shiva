# coding: utf-8

from time import strftime, localtime
from core.sw_base import BaseHandler

from avtuk.executor import Executor

#=== Очистка кэша =============================================================
class AdminClearCachHandler(BaseHandler):
    urls = r'/admin/clearcach'

    def get(self):
        self.write({'def':[{'type':"button", 'text':'Удалить', 'img':"process24.png", 'action':'do_tool_1'}],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: self.Panels["def"],
                        columns:[
  { type:"ro", sort:"date", align:"left", width:"120", label:"Окончание" },                        
  { type:"ro", sort:"str",  align:"left", width:"400", label:"SQL" },
  { type:"ro", sort:"str",  align:"left", width:"*",   label:"Таблицы" }    
                        ]});
                        
                        window.Cleaner.push(sw_grid);

                        window.do_tool_1 = function(){
                            var ids = sw_grid.getSelectedRowId();
                            if(!ids) self.AddMessage("Выберите запись в кэше",2)
                            else {
                                var url="/admin/clearcach/data";
                                self.NetSend(url,"id="+ids);
                                self.LoadGrid(sw_grid, url);
                            }                                
                        }
                        
                        self.LoadGrid(sw_grid, "/admin/clearcach/data");
                        '''
                    })


#==============================================================================
class AdminClearCachDataHandler(BaseHandler):
    urls = r'/admin/clearcach/data'

    def get(self):
        self.write_XML('<rows>%s</rows>' % 
                       ''.join('<row id="%s"><cell>%s</cell><cell>%s</cell><cell>%s</cell></row>' % 
                               (k, strftime("%d.%m.%Y %H:%M:%S", localtime(v[1])), v[3], ', '.join(v[2])) for k, v in Executor._obj_cash.items()))

    def post(self):
        try:
            Executor.kill(self.input(id='').id)
            self.write({'info':'OK'})
        except:
            self.write({'warning':'Ошибка записи'})
