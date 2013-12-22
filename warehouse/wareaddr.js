var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],       
                        auto_width: true,
                        columns:[
                                  
	  { type:"ch", sort:"str",  align:"left",  width:"20",  label:"Печать" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"ID1" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"status" },
	  
	  { type:"ro", sort:"str",  align:"left",  width:"100", label:["Адрес","#text_filter"] },
	  { type:"ro", sort:"str",  align:"left",  width:"56",  label:["Тип ячейки", "#select_filter"] },
	  { type:"ro", sort:"str",  align:"left",  width:"100", label:["Тип товара", "#select_filter"] },
	  { type:"ro", sort:"str",  align:"right", width:"80",  label:["Код товара","#text_filter"] },
	
	  { type:"ro", sort:"str",  align:"left",  width:"150", label:["Наименование","#text_filter"] },
	  { type:"ro", sort:"int",  align:"right", width:"50",  label:"В коробке" },
	  { type:"ro", sort:"int",  align:"right", width:"40",  label:"Коробок", style: "color: red;" },  
	  { type:"ro", sort:"int",  align:"right", width:"46",  label:"Кол-во" },
	  
	  { type:"ro", sort:"int",  align:"right", width:"46",  label:"Ожид. расход(в коробках)" },
	  
	  
	  { type:"ro", sort:"str",  align:"right", width:"50",  label:["Партия","#text_filter"] },
	  { type:"ro", sort:"date", align:"left",  width:"64",  label:"Годен до" },
	  { type:"ro", sort:"str",  align:"left",  width:"64",  label:["Статус","#text_filter"] }, 
	  { type:"ro", sort:"int",  align:"right", width:"80",  label:"Палета" },  
	  { type:"ro", sort:"date", align:"left",  width:"64",  label:"С даты" },
	  
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"ID2" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test1" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test2" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test3" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test4" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test5" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test6" },
	  { type:"ro", sort:"str",  align:"left",  width:"0",   label:"test7" }
  
    ]});

	sw_grid.enableColumnAutoSize(true);
	
						var col_checked = 1;
						var col_block = 2;
						var col_cell = 3;
					

						
                        window.Cleaner.push(sw_grid);
                        
                        
                        /*
                    	sw_grid.attachEvent("onFilterStart",function(){
                    		
                    		//window.update();
                        })
                        */
                       
                       
                        
                        window.update = function(){ 

                        	params = {}
                        	
                        	self._messager.clearAll()
                        	
                        	var is_filled = false; 

                        	for (var i=0; i<15; i++){
                        		
                        		item = sw_grid.getFilterElement(i);
                        		
                        		if (item && item.value){
                        			params['dhx_filter[' + i + ']'] = item.value;
                        			
                        			is_filled = true;
                        		}                        		
                        		
                        	}
                        	
                        	/*
                        	if (!is_filled){
                        		
                        		app.AddMessage('Фильтры для ячеек не выбраны', 2)
                        		return false;
                        	} 
                        	*/
                        
                            params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");
                        	params["is_all"]   = self.Toolbars["def"].getListOptionSelected("is_all");   
                        	params["is_block"] = self.Toolbars["def"].getListOptionSelected("is_block");
                        	params["godenDo"]  = self.Toolbars["def"].getListOptionSelected("godenDo");
           	
                        	window.sw_grid = sw_grid;
                        	
                        	self.ShowPanel("def");
                            self.load(sw_grid, "/warehouse/wareaddr/data?" + self.serialize(params), function() {
                            	
                            	
                            	window.sw_grid.forEachRow(function(id){

                                 		
                                 	if ( window.sw_grid.cells(id,col_block).getValue() == "-1" ){
                                 		window.sw_grid.setRowTextStyle(id, "background-color: #ffc9da;");
                                 	}

                                      
                                 })

                            });
                        	
                        }
                        
                                                
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }
                        
                        
                        var swForm = new dhtmlXForm("sw_form", [            
		    {type:"input",  labelWidth: 100, width:100, name:"addr",   bind:"addr",   labelAlign: "right", label:"Ячейка:"},
		    {type:"input",  labelWidth: 100, width:100, name:"inbox",  bind:"inbox",  labelAlign: "right", label:"В коробке:"},
		    {type:"input",  labelWidth: 100, width:100, name:"box",    bind:"box",    labelAlign: "right", label:"Коробок:",},
		    {type:"input",  labelWidth: 100, width:100, name:"code",   bind:"code",   labelAlign: "right", label:"Код товара:"},
		    {type:"input",  labelWidth: 100, width:100, name:"num",    bind:"num",    labelAlign: "right", label:"Номер партии:"},						    
		    {type: "combo", labelWidth: 100, width:110, name:"condition_code", bind:"condition_code", labelAlign: "right", label:"Статус партии:", options:[
		                                                                 
		                                                                {value: "", text: ""},
																		{% for item in all_status %}
																			{value: "{{ item[0] }}", text: "{{ item[1] }}"},
																		{% end %}

						                                                    	]}
						   ]);                        

                        
                        
                        window.Cleaner.push(swForm);
                    
                        
                        
                        window.do_tool_edit_form = function(ids){
                            swForm.ids=ids;
                            
                            swForm.clear();
                            swForm.lock();
                            
                            
                            dhtmlxAjax.get("/warehouse/wareaddr/data?psw_id="+ids, function(loader) {
                            	
                            	
                            	var all_results =JSON.parse(loader.xmlDoc.responseText);
                            	
                    			for (var item in all_results) {
     
                            		try{
                            			
                            			swForm.setItemValue(item, all_results[item]);
                            			
                            		}
                            		catch(e){
                            			
                            		}
                            	}
                            	
                            
                            	
                            	swForm.unlock();
                            	window.swForm = swForm;

                        	});
                            	
                                                        
                            
                            self.ShowPanel("one");
                    
                            
                                                    
                           
                        }


                        //Правка
                        window.do_tool_edit = function(){
                            var ids = sw_grid.getSelectedRowId();
                            
                            if (!ids){ app.AddMessage('Выберите ячейку',2) }
                            else     { window.do_tool_edit_form(ids) }
                        }
                        
                        
                      
                        window.do_block = function(){
                            var ids = sw_grid.getSelectedRowId();
                            
                            if (!ids){ 
                        			app.AddMessage('Выберите ячейку',2)
                        			return false;
                        	}
                                                                                    
                         	window.sw_grid.setRowTextStyle(ids, "background-color: #ffc9da;");                         	
                            
                         	var cell_id =  window.sw_grid.cells(ids,col_cell).getValue();
                      
                         	dhtmlxAjax.post("/mbl/inventory/block_cell", 'cell_id=' + cell_id  , function(resp){
                         		alert("Ячейка заблокирована");
                         	});
                        }
                        
                        
                        
                        window.do_unblock = function(){
                            var ids = sw_grid.getSelectedRowId();
                            
                            if (!ids){ 
                        			app.AddMessage('Выберите ячейку',2)
                        			return false;
                        	}
                                                                                    
                         	window.sw_grid.setRowTextStyle(ids, "background-color: #fff;");                         	
                            
                         	var cell_id =  window.sw_grid.cells(ids,col_cell).getValue();
                         	 
                         	
                         	dhtmlxAjax.post("/mbl/inventory/unblock_cell", 'cell_id=' + cell_id  , function(resp){
                         		alert("Ячейка разблокирована");
                         	});
                        }
                        
                        
                        function print_format(format){
    
                        	sw_grid.filterBy(0,0);
                        	
                            var ids = sw_grid.getCheckedRows(0);
                            
                            if (!ids){ 
                        			app.AddMessage('Выберите ячейку',2)
                        			return false;
                        	}
                          
                            var all_ids =  ids.split(",");
                                                      
                                                        
                            var sw_grid_print = new dhtmlXGridObject({                                                  
                                columns:[
                                                                                  	
                                         	{ type:"ro", sort:"str",  align:"center",  width:"100", label:"Ячейка" },                                         	
                                         	{ type:"ro", sort:"str",  align:"left",    width:"100", label:"Код Товара" },
                                         	{ type:"ro", sort:"str",  align:"left",    width:"300", label:"Наименование" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"50",  label:"В коробке" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"50",  label:"Коробок" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"50",  label:"Кол-во" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"100", label:"Партия" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"100", label:"Годен до" },
                                         	{ type:"ro", sort:"str",  align:"center",  width:"100", label:"С даты" },
                                         	
                                         ]
                            });
        
                    
                            var custom_rows = [3, 6, 7, 8, 9, 10, 11, 12, 15 ];
                                                        
                            for (var i = 0; i < all_ids.length; i++) {
                            	row_id = all_ids[i];

                            	var new_row = [];
                            	
                                for (var j = 0; j < custom_rows.length; j++) {
                                	new_row.push( sw_grid.cellById(row_id, custom_rows[j]).getValue() );
                                }
                                	                                                            	
                            	sw_grid_print.addRow(row_id, new_row.join(','));
                            }
                                     
                            
                            if (format == "print"){
                            	sw_grid_print.printView("","<script> window.print(); </script>");
                            }
                            else if (format == "csv"){
                            	
                            	self.GridCSV(sw_grid_print);
                            }
                            
                             
                            sw_grid_print.destructor();
                        }
                        
                        
                        
                        window.do_csv = function(){
                        	print_format("csv");
                        }
                        
                        window.do_print = function(){
                        	print_format("print");
                        }
                        
        
                        
                        
                        window.do_print_party = function(){
                        	
                        	
                        	var row_id = sw_grid.getSelectedId();
                        	var party  = sw_grid.cellById(row_id, 18).getValue();
                        	
                        	self.NetSend("/btk/btkconfirmin/data/print?party=" + party);
                        }
                        
                        
                        window.do_csv_all = function(){
                        	self.GridCSV(sw_grid);
                        }
                        
                        //Cancel
                        window.do_cancel = function(){ self.ShowPanel("def") }
                        
                        
                        window.do_save = function(){ 	
                        	
                        	//swForm.updateValues();
                        	swForm.validate();
                        	
                        	
                            var dt=swForm.Serialize();
                            if(!!swForm.ids){
                                dt=dt+"&uid="+swForm.ids;
                            }
                            
                            
                            self.NetSendAsync("/warehouse/wareaddr/data", dt, function(){
                            	
                            	window.update();
                            	  
                            });
                                                 
                        }
                        
                        
               
                        //window.update();