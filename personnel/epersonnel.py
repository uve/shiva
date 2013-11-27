# coding: utf-8

from core.sw_base import BaseHandler, md5passw
from avtuk.avtuk_models import Department, Role, User, RC

#=== Управление персоналом ====================================================
class EditUserHandler(BaseHandler):
    urls = r'/personnel/epersonnel'

    def get(self):
        roles = '{value:"0",text:"Не определена"},' + ','.join('{value:"%s",text:"%s"}' % (i.id, i.name) for i in Role.select())
        deps = RC.get_current(rc=self.session.rc).depart_cls
        deps1 = ','.join('{value:"%s",text:"%s"}' % (i.id, i.name) for i in deps)
        deps2 = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_6"} for i in deps]

        self.write({'def':[{'type':"button", 'text':'Новый', 'img':"add24.png", 'imgdis':"add24g.png", 'action':'do_tool_1'},
                           {'type':"button", 'text':'Правка', 'img':"edit24.png", 'imgdis':"edit24g.png", 'action':'do_tool_2'},
                           {'type':"button", 'text':'Удалить', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_tool_3'},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           {'type':"separator"},
                           {'type':"text", 'text':"  Подразделение:"},
                           {'id':"btndep", 'type':"buttonSelect", 'text':'-', 'items':deps2}],

                    'one':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_4'},
                           {'type':"button", 'text':'Отмена', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_tool_5'},
                           '<div id="sw_form" />'],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                            parent: window.app.Panels["def"],
                            columns:[
                { type:"ro", sort:"str", align:"left",   width:"*",   label:"Сотрудник" },
                { type:"ro", sort:"str", align:"left",   width:"180", label:"Основная роль" },
                { type:"ch", sort:"str", align:"center", width:"75",  label:"Активность" }
                            ]});
                        
                        window.Cleaner.push(sw_grid);
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }

                        var swForm = new dhtmlXForm("sw_form", [
                         {type:"input",    name:"ulogin",  bind:"ulogin",  label:"Логин:", value: "", validate:"NotEmpty"},
                         {type:"input",    name:"uname",   bind:"uname",   label:"ФИО:", value: ""},
                         {type:"password", name:"passw",   bind:"passw",   label:"Пароль:", value:"", validate:"NotEmpty"},
                         {type:"select",   name:"urole",   bind:"urole",   label:"Основная роль", options:[''' + roles + ''']},
                         {type:"select",   name:"udepart", bind:"udepart", label:"Подразделение", options:[''' + deps1 + ''']},                         
                        ]);                        
                        window.Cleaner.push(swForm);
                        
                        // Всё это потому, что DHTMLX мутно и нестабильно работает с формами
                        var frm_ulogin = swForm.getInput("ulogin");
                        var frm_uname = swForm.getInput("uname");
                        var frm_passw = swForm.getInput("passw");

                        window.ids=0;
                        
                        //Создать + Правка
                        window.do_tool_12 = function(ids){
                            swForm.ids=ids;
                            if(!!ids){
                                swForm.load("/personnel/epersonnel/data?user="+ids);                                
                            }else{ 
                                swForm.clear();
                                swForm.setItemValue("urole", 0);
                                swForm.setItemValue("passw", "");
                                swForm.setItemValue("udepart", 0);
                            }
                            self.ShowPanel("one");
                        }

                        //Создать
                        window.do_tool_1 = function(){window.do_tool_12(); }

                        //Правка
                        window.do_tool_2 = function(){
                            var ids = sw_grid.getSelectedRowId();
                            
                            if (!ids){ app.AddMessage('Выберите сотрудника',2) }
                            else     { window.do_tool_12(ids) }
                        }
                        sw_grid.attachEvent("onRowDblClicked", do_tool_2);

                        //Удалить
                        window.do_tool_3 = function(){
                            var ids = sw_grid.getSelectedRowId();
                            if (!ids){
                                app.AddMessage('Выберите сотрудника',2);
                            }else{
                                self.NetSend("/personnel/epersonnel/data", 'uid='+ids);
                                self.LoadGrid(sw_grid, "/personnel/epersonnel/data?depart="+window.ids);
                            }
                        }

                        //OK - ввели нового сотрудника
                        window.do_tool_4 = function(){

                            if (frm_passw.value.length < 1 || frm_passw.value.length > 32) {
                                app.AddMessage('Недопустимая длина пароля',2);
                                frm_passw.focus();
                                return 0;
                            }
                            
                            if (frm_ulogin.value.length < 2 || frm_ulogin.value.length > 32) {
                                app.AddMessage('Недопустимая длина логина',2);
                                frm_ulogin.focus();
                                return 0;
                            }

                            // Костыль к DHTMLX, иначе никак
                            swForm.setItemValue("passw", frm_passw.value);
                            
                            var r = /\w/i;
                            
                            swForm.validate();
                            
                            var dt=swForm.Serialize();
                            if(!!swForm.ids){
                                dt=dt+"&uid="+swForm.ids;
                            }
                            self.NetSend("/personnel/epersonnel/data", dt);
                            self.ShowPanel("def");
                            self.LoadGrid(sw_grid, "/personnel/epersonnel/data?depart="+window.ids);                           
                        }

                        //Cancel
                        window.do_tool_5 = function(){ self.ShowPanel("def") }

                        //DEP
                        window.do_tool_6 = function(ids){
                            if(ids.substr(0, 3) == "dep"){
                                var dep = self.Toolbars["def"].getListOptionText("btndep", ids);                                                               
                                self.SetTitle('Управление персоналом:  "'+dep+'"');
                                self.Toolbars["def"].setItemText("btndep", dep);
                                window.ids=ids.substr(3);
                                self.LoadGrid(sw_grid, "/personnel/epersonnel/data?depart="+window.ids);
                            }
                        }
                        
                        window.do_tool_6("dep%s");''' % deps[0].id
                    })


#==============================================================================
class EditUserDataHandler(BaseHandler):
    urls = r'/personnel/epersonnel/data'

    def get(self):

        uid    = self.get_argument("user", None)
        depart = self.get_argument("depart", None)

        if depart:
            self.write_XML(Department.get(id=depart).users_cls
                           .as_grid('name', 'role_cls.name', 'visible', id='id'))
        elif uid:
            dk = {'name':'uname', 'sotrud':'ulogin', 'depart':'udepart', 'role':'urole'}
            self.write_XML(User.get(id=uid).as_xml(*dk.keys(), **dk))

        else:
            self.write_XML('<rows />')


    def post(self):
        inp = self.input(uid=0, uname='', ulogin='', passw='', udepart=0, urole=0)

        try: uid = int(inp.uid)
        except: uid = 0

        try:
            user = User.get(id=uid) if uid else User()

            # DEL
            if not inp.passw and uid:
                user.visible = int(not user.visible)

            # NEW and EDIT
            elif inp.passw:
                user.depart = int(inp.udepart)
                user.name = inp.uname
                user.sotrud = inp.ulogin.upper()
                user.password = md5passw(user.sotrud, str(inp.passw))

                try:
                    rid = int(inp.urole)
                    if user.role <> rid:
                        user.role = rid
                        msg = {'TYPE':'W', 'TEXT': 'Роль измененена. Повторите процедуру входа'}
                        self.application.sessions.add_message(uid, True, msg)
                        self.application.sessions.add_message(uid, False, msg)
                except: pass

            user.save()

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})
