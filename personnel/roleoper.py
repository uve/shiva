# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import User, Role, Department, RC

#=== Привязка роли к юзеру ====================================================
class RoleDefaultHandler(BaseHandler):
    urls = r'/personnel/roleoper'

    def get(self):
        # кнопки с департаментами РЦ
        deps = RC.get_current(rc=self.session.rc).depart_cls
        bdep = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_2"} for i in deps]

        rols = ','.join('[%s,"%s"]' % (i.id, i.name) for i in Role.select('id<>1'))

        self.write({'def':[{'type':"button", 'text':'Сохранить', 'img':"save24.png", 'imgdis':"save24g.png", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"text", 'text':"  Подразделение:"},
                           {'id':'bdep', 'type':"buttonSelect", 'text':'-', 'items':bdep}],
                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: self.Panels["def"],
                        columns:[
  { type:"ro",   sort:"str", align:"left", width:"*",   label:"Сотрудник" },
  { type:"coro", sort:"str", align:"left", width:"200", label:"Исполняемая роль" }                        
                        ]});
                        var combo = sw_grid.getCombo(1);                                               
                        var cmb = [%s];
                        for(var i in cmb) combo.put(cmb[i][0],cmb[i][1]);
                        
                        window.Cleaner.push(sw_grid);
                        window.ids=0;
                        
                        window.do_tool_1 = function(){
                            var dt="";
                            
                            sw_grid.forEachRow(function(ids){
                                ids2=parseInt(sw_grid.cells(ids, 1).getValue());
                                if(!!ids2){
                                    if(!!dt){dt+='&'}
                                    dt=dt+ids+"="+ids2;                                
                                }
                            });
                            
                            self.NetSend("/personnel/roleoper/data", dt);                            
                            self.LoadGrid(sw_grid, "/personnel/roleoper/data?depart="+window.ids); 
                        }
                        
                        window.do_tool_2 = function(ids2){
                            window.ids=ids2.substr(3);
                            var text = self.Toolbars["def"].getListOptionText("bdep", ids2);
                            self.SetTitle('Основные роли сотрудников отдела: "'+text+'"');                                            
                            self.Toolbars["def"].setItemText("bdep", text);                            
                            self.LoadGrid(sw_grid, "/personnel/roleoper/data?depart="+window.ids);
                        }
                        
                        window.do_tool_2("dep%s");''' % (rols, deps[0].id,)
                    })


#==============================================================================
class RoleDefaultDataHandler(BaseHandler):
    urls = r'/personnel/roleoper/data'

    def get(self):
        
        depart = self.get_argument("depart", None)

        try:
            self.write_XML(Department.get(id=depart).users_cls
                           .as_grid('name', 'role_cls.name', id='id'))
        except:
            self.write_XML('<rows />')


    def post(self):
        try:
            for k, v in self.input().items():
                uid = int(k)
                user = User.get(id=uid)
                user.role = int(v)
                user.save()

                msg = {'TYPE':'W', 'TEXT': 'Роль измененена. Повторите процедуру входа'}
                self.application.sessions.add_message(uid, True, msg)
                self.application.sessions.add_message(uid, False, msg)

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})
