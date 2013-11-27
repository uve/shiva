# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Department, RC

#=== Список юзеров ============================================================
class PersonnelHandler(BaseHandler):
    urls = r'/personnel/personnel'

    def get(self):
        # кнопки с департаментами РЦ
        deps = RC.get_current(rc=self.session.rc).depart_cls
        bdep = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_2"} for i in deps]

        self.write({'def':[{'type':"text", 'text':"  Подразделение:"},
                           {'id':'bdep', 'type':"buttonSelect", 'text':'-', 'items':bdep},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                            parent: window.app.Panels["def"],
                            columns:[
  { type:"ro", sort:"str", align:"left", width:"*",   label:"Сотрудник" },
  { type:"ro", sort:"str", align:"left", width:"180", label:"Основная роль" },
  { type:"ro", sort:"str", align:"left", width:"180", label:"Текущая роль" }
                            ]});

                        window.Cleaner.push(sw_grid);
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }
                        window.ids=0;
                        
                        window.do_tool_2 = function(ids2){
                            window.ids=ids2.substr(3);
                            var text = self.Toolbars["def"].getListOptionText("bdep", ids2);
                            self.SetTitle('Список сотрудников отдела: "'+text+'"');                                            
                            self.Toolbars["def"].setItemText("bdep", text);                            
                            self.LoadGrid(sw_grid, "/personnel/personnel/data?depart="+window.ids);
                        }
                        window.do_tool_2("dep%s");''' % deps[0].id
                    })


#==============================================================================
class PersonnelDataHandler(BaseHandler):
    urls = r'/personnel/personnel/data'

    def get(self):
        try: depart = int(self.input().depart)
        except: depart = 0

        self.write_XML(Department.get(id=depart).users_cls
                       .as_grid('name', 'role_cls.name', 'current_role_cls.name', id='id'))
