# coding: utf-8

from core.sw_base import BaseHandler
from barcode.zek_model import depart_uid2barcode, badge, badge_size
from avtuk.avtuk_models import User, RC

#=== Печать бэйджика ==========================================================
class PrintUserHandler(BaseHandler):
    urls = r'/personnel/prnuser'

    def get(self):
        # кнопки с департаментами РЦ
        deps = RC.get_current().depart_cls
        bdep = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_2"} for i in deps]

        self.write({'def':[{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           {'type':"separator"},
                           {'type':"text", 'text':"  Подразделение:"},
                           {'id':'bdep', 'type':"buttonSelect", 'text':'-', 'items':bdep}, ],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                            parent: window.app.Panels["def"],
                            columns:[
  { type:"ro", sort:"str", align:"left", width:"*",   label:"Сотрудник" },
  { type:"ro", sort:"str", align:"left", width:"180", label:"Основная роль" },
  { type:"ro", sort:"str", align:"left", width:"180", label:"Текущая роль" }
                            ]});
                        window.Cleaner.push(sw_grid);
                        window.ids=0;
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }
                        
                        window.do_tool_1 = function(){
                          var idr = sw_grid.getSelectedId();
                          if(!idr) self.AddMessage('Выберите сотрудника!',1);
                          else self.PrintURL(%s,%s,'/personnel/prnuser/data?uid='+idr);
                        }
                        
                        window.do_tool_2 = function(ids2){
                            window.ids=ids2.substr(3);
                            var text = self.Toolbars["def"].getListOptionText("bdep", ids2);
                            self.SetTitle('Печать бэйджика сотрудникам отдела: "'+text+'"');                                            
                            self.Toolbars["def"].setItemText("bdep", text);                            
                            self.LoadGrid(sw_grid, "/personnel/prnuser/data?depart="+window.ids);
                        }
                        
                        window.do_tool_2("dep%s");''' % (badge_size[0], badge_size[1], deps[0].id,)
                     })

#==============================================================================
class PrintUserDataHandler(BaseHandler):
    urls = r'/personnel/prnuser/data'

    def get(self):
        
        uid = self.get_argument("uid", None)

        if uid:
            # генерим картинку для печати
            user = User.get(id=uid)
            if user:
                self.write(badge(depart_uid2barcode(user.depart, user.id), user.name.decode('utf8')))
                self.set_header("Content-Type", "image/svg+xml")

        else:
            # данные для таблицы
 
            depart = self.get_argument("depart", None)

            whr = {'depart':depart} if depart else {}
            whr['visible'] = 1

            self.write_XML(User.select(**whr)
                           .as_grid('name', 'role_cls.name', 'current_role_cls.name', id='id'))
