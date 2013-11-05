# coding: utf-8

from core.sw_base import BaseHandler

#==============================================================================
class BTKBlockHandler(BaseHandler):
    urls = r'/btk/blockl'

    def get(self):
        self.write({'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],                        
                        columns:[
  { type:"ro", sort:"int",  align:"right", width:"62",  label:"Код товара" },  
  { type:"ro", sort:"str",  align:"left",  width:"*",   label:"Товар" },
  { type:"ro", sort:"str",  align:"left",  width:"70",  label:"Партия" },          
  { type:"ro", sort:"date", align:"left",  width:"68",  label:"Годен до" },
  { type:"ro", sort:"int",  align:"right", width:"56",  label:"Кол-во" },  
  { type:"ro", sort:"str",  align:"right", width:"54",  label:"Адрес" },
  { type:"ro", sort:"int",  align:"right", width:"60",  label:"Палета" },
  { type:"ro", sort:"date", align:"left",  width:"111", label:"С даты" },
  { type:"ro", sort:"str",  align:"left",  width:"111", label:"Статус" }    
                        ],                        
                        
                        xml:"/btk/blockl/data"
                        });
                        window.Cleaner.push(sw_grid);
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }''',

                    'warning':'Страница в разработке'
                    })


#==============================================================================
class BTKBlockDataHandler(BaseHandler):
    urls = r'/btk/blockl/data'

    def get(self):
        self.write_XML('<rows></rows>')

#        self.write_XML(Department.get(self.application.connect, id=depart).users_cls
#                       .as_grid('name', 'role_cls.name', 'current_role_cls.name', id='id'))
