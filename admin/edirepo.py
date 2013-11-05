# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Report
# #from settings import CURRENT_RC
# #

#==============================================================================
class AdminEdiRepoHandler(BaseHandler):
    urls = r'/admin/edirepo'

    def get(self):
#        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
#                 for k, v in enumerate(('NUMBER', 'VARCHAR2', 'DATE'))]
#        opers[0]['selected'] = "true"
#
#        reps = [{"id":"rep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_4"}
#                 for i in Report.select()]

        self.write({'def':[{'type':"button", 'text':'Новый', 'img':"add24.png", 'imgdis':"add24g.png", 'action':'do_tool_1'},
                           {'type':"button", 'text':'Правка', 'img':"edit24.png", 'imgdis':"edit24g.png", 'action':'do_tool_2'},
                           {'type':"button", 'text':'Удалить', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_tool_3'}],

                    'one':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_4'},
                           {'type':"button", 'text':'Отмена', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_tool_5'},
                           '<div id="sw_form" />'],


#                           {'type':"text", 'text':"  Отчет:"},
#                           {'id':"cal1", 'type':"buttonInput", 'width':100},
#                           {'id':"btnrep", 'type':"buttonSelect", 'text':'-', 'items':reps},
#                           {'type':"separator"},
#                           {'type':"text", 'text':"  Тип:"},
#                           {'id':"btnopr", 'type':"buttonSelect", 'text':'-', 'items':opers},
#                           {'type':"text", 'text':"  Имя:"},
#                           {'id':"btnnam", 'type':"buttonInput", 'width':100},
#                           {'type':"button", 'img':"add24.png", 'title':'Добавить параметр', 'action':'do_tool_5'},
#                           {'type':"button", 'img':"delete24.png", 'title':'Удалить параметр', 'action':'do_tool_6'},
#                           '<textarea id="sw_tsq" style="padding:5px; width:100%;height:100%"></textarea>'

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        columns:[
      { type:"ro", sort:"str", align:"left", width:"100", label:"Название" },
      { type:"ro", sort:"str", align:"left", width:"*",   label:"Описание" },     
      { type:"ro", sort:"str", align:"left", width:"100", label:"Права" }
                        ],
                        xml:"/admin/edirepo/data"});
                        window.Cleaner.push(sw_grid);

                        window.ids=0;

                        //Создать + Правка
                        window.do_tool_12 = function(ids){
                            //console.log('ED',ids);
//                            swForm.ids=ids;
//                            if(!!ids){
//                                swForm.load("/personnel/epersonnel/data?user="+ids);                                
//                            }else{ 
//                                swForm.clear();
//                                swForm.setItemValue("urole", 0); 
//                                swForm.setItemValue("udepart", 0);
//                            }
//                            self.ShowPanel("one");                        
                        }

                        //Создать
                        window.do_tool_1 = function(){ window.do_tool_12() }

                        //Правка
                        window.do_tool_2 = function(){
                            var ids = sw_grid.getSelectedRowId();
                            if (!ids){ app.AddMessage('Выберите отчет',2) }
                            else     { window.do_tool_12(ids) }                        
                        }
                        sw_grid.attachEvent("onRowDblClicked", do_tool_2);

                        //Удалить
                        window.do_tool_3 = function(){
                            var ids = sw_grid.getSelectedRowId();
                            if (!ids){
                                app.AddMessage('Выберите отчет',2);
                            }else{
                                self.NetSend("/admin/edirepo/data", 'delete='+ids);
                                self.LoadGrid(sw_grid, "/admin/edirepo/data");
                            }
                        }

//                        //OK
//                        window.do_tool_4 = function(){
//                            //if (!swForm.validate()){
//                            //    self.AddMessage("Не все поля заполнены",3);
//                            //    return;
//                            //}
                                                     
//                            var dt=swForm.Serialize();                           
//                            if(!!swForm.ids){
//                                dt=dt+"&uid="+swForm.ids;
//                            }
//                            self.NetSend("/personnel/epersonnel/data", dt);                            
//                            self.ShowPanel("def");
//                            self.LoadGrid(sw_grid, "/personnel/epersonnel/data?depart="+window.ids);                           
//                        }

//                        //Cancel
//                        window.do_tool_5 = function(){ self.ShowPanel("def") }

//                        //DEP
//                        window.do_tool_6 = function(ids){
//                            if(ids.substr(0, 3) == "dep"){
//                                var dep = self.Toolbars["def"].getListOptionText("btndep", ids);                                                               
//                                self.SetTitle('Управление персоналом:  "'+dep+'"');
//                                self.Toolbars["def"].setItemText("btndep", dep);
//                                window.ids=ids.substr(3);                                
//                                self.LoadGrid(sw_grid, "/personnel/epersonnel/data?depart="+window.ids);
//                            }
//                        }
                        
//                        window.do_tool_6("dep%s");'''
})



#==============================================================================
class AdminEdiRepoDataHandler(BaseHandler):
    urls = r'/admin/edirepo/data'

    def get(self):
        self.write_XML(Report.select().as_grid('name', 'descript', 'rights',
                                               show={'rights':lambda val: 'Всем' if val is None else 'свой РЦ' if val == 0 else 'свой отдел'}))
#                                               

    def post(self):
        inp = self.input(delete=0)
        print 'INP', inp

        if inp.delete:
            pass

# #        if param == 'gts':
# #            try:
# #                Executor.exec_sql('BEGIN tsclad.oksdelka(:ids, 0); END;', ids=int(self.input(ids=0).ids))
# #                self.write({'info':'Информация сохранена'})
# #            except:
# #                self.write({'warning':'Ошибка записи'})
