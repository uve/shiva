# coding: utf-8

import datetime
from core.sw_base import BaseHandler

import cx_Oracle

from avtuk.executor import Executor

#=== Все задания ==============================================================
class AllTaskHandler(BaseHandler):
    urls = r'/personnel/alltsk'

    def get(self):
        st = datetime.datetime.now().strftime('%d.%m.%Y')


        self.write({'def':[{'type':"text", 'text':"Дата с:"},
                           {'id':"cal1", 'type':"buttonInput", 'width':60, 'value':st},
                           {'type':"text", 'text':" по:"},
                           {'id':"cal2", 'type':"buttonInput", 'width':60, 'value':st},

                           {'type':"separator"},
                           {'type':"button", 'img':"restart.png", 'action':'do_tool_task_restart', 'title':'Возобновить задачу'},
                           {'type':"button", 'img':"stop.png", 'action':'do_tool_task_close', 'title':'Завершить задачу'},
                           {'type':"button", 'img':"1.png", 'action':'do_tool_task_priority', 'title':'Установить приоритет'},
                           {'type':"separator"},
                           {'type':"button", 'img':"csv.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           ],

                    'cmd':'''
                    
                    
                        var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                        
                        sw_btk.items[0].setText("Все задания");
                        sw_btk.items[1].setText("История заданий");
                        window.Cleaner.push(sw_btk);
                    
                        var sw_grid1 = sw_btk.cells("a").attachGrid();
                        
                        sw_grid1.columns([
                              { type:"ro", sort:"int",  align:"right", width:"60",  label:["ID","#text_filter"] },
                              { type:"ro", sort:"str",  align:"left",  width:"120", label:["Сотрудник","#select_filter"] },
                              { type:"ro", sort:"str",  align:"left",  width:"200", label:["Задача","#select_filter"] },
                              { type:"ro", sort:"str",  align:"left",  width:"200", label:["Описание","#text_filter"] },
                              { type:"ro", sort:"date", align:"right", width:"105", label:["Постановка","#text_filter"] },
                              { type:"ro", sort:"date", align:"right", width:"105", label:["Попытка","#text_filter"] },      
                              { type:"ro", sort:"date", align:"right", width:"105", label:["Начало","#text_filter"] },
                              { type:"ro", sort:"date", align:"right", width:"105", label:["Окончание","#text_filter"] }      
                                                ]
                                                );

                        sw_grid1.enableAutoWidth(true);
                                               
                        // для очистки памяти !!!
                        window.Cleaner.push(sw_grid1);
                        
                        
                        
                        sw_grid1.attachEvent("onRowSelect", function(id){
                        
                            self.LoadGrid(sw_grid2, "/personnel/alltsk/data/history?task_id="+id);
                            
                         });

                        
                        var sw_grid2 = sw_btk.cells("b").attachGrid();
                        sw_grid2.columns([
                          
                              { type:"ro", sort:"int",  align:"left", width:"100", label:"ID" },
                              { type:"ro", sort:"str",  align:"left", width:"150", label:"Дата/Время" },
                              { type:"ro", sort:"str",  align:"left", width:"300", label:"Описание" },
                              { type:"ro", sort:"str",  align:"left", width:"200", label:"Сотрудник" },
                              
                        ]);
                        window.Cleaner.push(sw_grid2);
                        
                        
                        
                        
                        var bar = this.Toolbars["def"];
                        
                        var calendar1 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal1"].obj.firstChild );
                        calendar1.loadUserLanguage("ru");
                        calendar1.setDateFormat("%d.%m.%Y");
                        calendar1.hideTime();
                        calendar1.setDate(new Date());                                                       
                        window.Cleaner.push(calendar1);
                                                        
                        var calendar2 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal2"].obj.firstChild );
                        calendar2.loadUserLanguage("ru");
                        calendar2.setDateFormat("%d.%m.%Y");
                        calendar2.hideTime();
                        calendar2.setDate(new Date());
                        window.Cleaner.push(calendar2);
                        
                        calendar1.attachEvent("onClick", function (){ window.do_tool_1() });
                        calendar2.attachEvent("onClick", function (){ window.do_tool_1() });                            
                        
                        
                        
                        // фильтр
                        window.do_tool_1 = function(ids2){
                            var d1=calendar1.getDate().valueOf();
                            var d2=calendar2.getDate().valueOf();                                                            

                            
                            self.load(sw_grid1,  "/personnel/alltsk/data/tasks?d1="+d1+"&d2="+d2+"&time="+new Date().getTime(), function() {
      
                            });                            
                        }



                          
                         // возобновить задачу
                            window.do_tool_task_restart = function(){
                            var ids = sw_grid1.getSelectedRowId();
                            if(!ids) self.AddMessage('Выберите задание',2)
                            else{
                                dhtmlxAjax.post("/personnel/alltsk/data/task_restart", encodeURI("task_id=" + ids) , function(resp){                           
                                    window.do_tool_1();
                                });
                            }                  
                        }

                        // прибить задачу
                        window.do_tool_task_close = function(){
                            var ids = sw_grid1.getSelectedRowId();
                            if(!ids) self.AddMessage('Выберите задание',2)
                            else{
                                dhtmlxAjax.post("/personnel/alltsk/data/task_close", encodeURI("task_id=" + ids) , function(resp){
                                    window.do_tool_1();
                                });
                            }                             
                        }
                        
                        
                        window.do_tool_task_priority = function(){
                            var ids = sw_grid1.getSelectedRowId();
                            if(!ids) self.AddMessage('Выберите задание',2)
                            else{
                                dhtmlxAjax.post("/personnel/alltsk/data/task_priority", encodeURI("task_id=" + ids) , function(resp){
                                    window.do_tool_1();
                                });
                            }                             
                        }
                        
                                            
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid1) }
                        
                        window.do_tool_1();'''
                    })


#==============================================================================
class AllTaskDataHandler(BaseHandler):
    urls = r'/personnel/alltsk/data/tasks'

    def get(self, param):
        
        
        if param == "tasks":
            ds = self.get_argument("d1", None)
            if ds:
                ds = datetime.datetime.fromtimestamp(int(ds) / 1000)
                ds = ds.date()
                
            
                
            de = self.get_argument("d2", None)
            if de:
                de = datetime.datetime.fromtimestamp(int(de) / 1000)
                de = de.date()
                
    
            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.proc("shiva_task.GetAllTask", [ds, de, out])
    
            all_results = []
    
            for item in res[-1].fetchall():
                all_results.append({"id": item[0], "data": item })
        
            self.write({"rows": all_results})
            
            
            
            
        if param == "history":
            
            task_id = self.get_argument("task_id", None)

            #sql = "select * from sw_task_history where task_id=:task_id order by datetime desc"
            sql = "select sw.task_id, sw.datetime, sw.description, s.name from sw_task_history sw LEFT JOIN sotrud s ON sw.user_id = s.id WHERE task_id=:task_id order by datetime desc"
            
            self.write_XML(Executor.exec_cls(sql, task_id=task_id).as_grid())



    def post(self, param):
        
        
        user_id = self.session.uid
        task_id = self.get_argument("task_id", None)
        
        
        # user_id - пользователь шивы который остановил задачу
        
        if param == 'task_restart':
            self.proc("shiva_task.UserTaskRestart", [task_id, user_id])   
        
        
        if param == 'task_close':
            self.proc("shiva_task.UserTaskClose",   [task_id, user_id])
        
        
        if param == 'task_priority':
            self.proc("shiva_task.SetTaskPriority",   [task_id])
            
            
        
        self.write({'info':'Информация сохранена',  'cmd':"window.do_tool_1()"})
        
        
        
        