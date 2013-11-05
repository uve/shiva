# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Role
from avtuk.executor import Executor

#=== Привязка модулей к роли =================================================#
class RoleModuleHandler(BaseHandler):
    urls = r'/admin/rolemod'

    def get(self):
        brole = [{"id":"role%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_2"}
                 for i in Role.select("id<>1")]

        self.write({'def':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"text", 'text':"  Роль:"},
                           {'id':'brole', 'type':"buttonSelect", 'text':'-', 'items':brole}],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        columns:[
  { type:"ro", sort:"str", align:"left",   width:"200", label:"Секция" },
  { type:"ro", sort:"str", align:"left",   width:"150", label:"Модуль" },
  { type:"ro", sort:"str", align:"left",   width:"*",   label:"Описание" },
  { type:"ch", sort:"int", align:"center", width:"50",  label:"Есть" }
                        ]});
                        sw_grid.attachHeader("#select_filter,#text_filter,#text_filter,&nbsp;,#cspan");

                        window.Cleaner.push(sw_grid);
                        window.role=0;
                        
                        window.do_tool_1 = function(){
                            if(!window.role){
                                self.AddMessage("Выберите роль",2);
                                return;
                            }
                            sw_grid.editStop();                            
                            
                            var mon=[]; var moff=[];
                            
                            sw_grid.forEachRow(function(ids){
                                if(!!parseInt(sw_grid.cells(ids, 3).getValue())){
                                    mon.push(ids);
                                }else{
                                    moff.push(ids);
                                }
                            });
                            
                            self.NetSend("/admin/rolemod/data", "role="+window.role+"&mon="+mon.join()+"&moff="+moff.join());                                
                        }
                        
                        window.do_tool_2 = function(ids2){
                            window.role=ids2.substr(4);
                            var text = self.Toolbars["def"].getListOptionText("brole", ids2);                                            
                            self.Toolbars["def"].setItemText("brole", text);
                            self.LoadGrid(sw_grid, "/admin/rolemod/data?role="+window.role);
                        }'''
                    })



#==============================================================================
class AdminDataHandler(BaseHandler):
    urls = r'/admin/rolemod/data'

    def get(self):
        try:
            sql = '''SELECT m.id, s.caption menu, m.caption, m.description, r.role_id
                     FROM sw_module m
                     LEFT JOIN sw_role_module r ON m.id=r.module_id AND r.ROLE_ID=:role
                     JOIN sw_menu s ON m.sw_menu_id=s.id'''

            self.write_XML(Executor.exec_cls(sql, role=int(self.input().role))
                           .as_grid('menu', 'caption', 'description', 'role_id'))

        except:
            self.write_XML('<rows />')


    def post(self):
        inp = self.input(role=0, mon='', moff='')
        try:
            mon = [int(i) for i in inp.mon.split(',') if i]
            moff = [int(i) for i in inp.moff.split(',') if i]
            Role.get(id=int(self.input().role)).set_modules(mon, moff)

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})
