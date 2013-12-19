
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
        
    self.load(sw_grid3, "/personnel/alltsk/data/detail?task_id="+id);
 });


var tabbar = sw_btk.cells("b").attachTabbar();
       
tabbar.addTab("a", "История заданий", 100, 0, 0);
tabbar.addTab("b", "Состав", 100, 100, 0);

tabbar.setTabActive("a");

var sw_grid2 = tabbar.cells("a").attachGrid();
sw_grid2.columns([
  
      { type:"ro", sort:"int",  align:"left", width:"0", label:"ID" },
      { type:"ro", sort:"int",  align:"left", width:"0", label:"Задача" },
      { type:"ro", sort:"str",  align:"left", width:"150", label:"Дата/Время" },
      { type:"ro", sort:"str",  align:"left", width:"300", label:"Описание" },
      { type:"ro", sort:"str",  align:"left", width:"*", label:"Сотрудник" },
      
]);
window.Cleaner.push(sw_grid2);

var sw_grid3 = tabbar.cells("b").attachGrid();
sw_grid3.columns([
  
      { type:"ro", sort:"int",  align:"center", width:"0",   label:"ID" },
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Код" },
      { type:"ro", sort:"str",  align:"left",   width:"*",   label:"Наименование" },
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Адрес" },
      { type:"ro", sort:"str",  align:"center", width:"50",  label:"План" },
      { type:"ro", sort:"str",  align:"center", width:"50",  label:"Факт" },
      { type:"ro", sort:"str",  align:"center", width:"50",  label:"Место" },
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Выполнено" }
      
]);
window.Cleaner.push(sw_grid3);

               
                    
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
                    
                    window.do_tool_1();
                    
                    