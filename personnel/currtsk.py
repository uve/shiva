# coding: utf-8

from core.sw_base import BaseHandler

#=== Текущие задания =========================================================
class CurrentTaskHandler(BaseHandler):
    urls = r'/personnel/currtsk'

    def get(self):
        self.write({'def':[{'type':"button", 'img':"restart.png", 'action':'do_tool_task_restart', 'title':'Возобновить задачу'},
                           {'type':"button", 'img':"stop.png", 'action':'do_tool_task_close', 'title':'Завершить задачу'},
                           {'type':"button", 'img':"1.png", 'action':'do_tool_task_priority', 'title':'Установить приоритет'},
                           {'type':"separator"},
                           {'type':"button", 'img':"csv.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],
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
                        
                            self.load(sw_grid2, "/personnel/alltsk/data/history?task_id="+id);
                            
                         });

                        
                        var sw_grid2 = sw_btk.cells("b").attachGrid();
                        sw_grid2.columns([
                          
                              { type:"ro", sort:"int",  align:"left", width:"100", label:"ID" },
                              { type:"ro", sort:"str",  align:"left", width:"150", label:"Дата/Время" },
                              { type:"ro", sort:"str",  align:"left", width:"300", label:"Описание" },
                              { type:"ro", sort:"str",  align:"left", width:"200", label:"Сотрудник" },
                              
                        ]);
                        window.Cleaner.push(sw_grid2);
                        
                   
                   
                   
                        // фильтр
                        window.do_tool_1 = function(ids2){

                           self.load(sw_grid1,  "/personnel/alltsk/data/tasks", function() {
      
                            });
                        }
                        
                        window.Cleaner.push(sw_grid1);
                        
                        
                        
                        
                        
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
                        
                        
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid1) };
                        window.do_tool_1();
                        '''
                    })

