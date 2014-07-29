var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");

//sw_btk.setAutoSize("b;c", "a;c");

sw_btk.items[0].setText("Список фактур");
sw_btk.items[1].setText("Список товаров");
window.Cleaner.push(sw_btk);
                            
var sw_grid1 = sw_btk.cells("a").attachGrid(1000);

sw_grid1.enableAutoWidth(true);
sw_grid1.setStyle("width: 100% !important;", "");

sw_grid1.columns([
	  { type:"ro", sort:"int",  align:"right", width:"66", id:"5555555",  label:["ID", "#text_filter"] },
	  { type:"ro", sort:"int",  align:"right", width:"45",  label:["Номер", "#text_filter"] },
	  { type:"ro", sort:"date", align:"right", width:"66",  label:["Дата", "#text_filter"] },
	  { type:"ro", sort:"str",  align:"left",  width:"276", label:"Получатель"},
	  { type:"ro", sort:"str",  align:"left",  width:"286", label:"Операция" },
	  { type:"ro", sort:"str",  align:"left",  width:"76",  label:["Статус", "#select_filter"]},
	  { type:"ro", sort:"str",  align:"left",  width:"76",  label:["N отправки"]},
	  { type:"ro", sort:"str",  align:"left",  width:"0"},
	  
	  { type:"ro", sort:"str",  align:"left",  width:"96",  label:["Оклейка", "#select_filter"]},
	  
	  { type:"ro", sort:"str",  align:"left",  width:"10"},
	  { type:"ro", sort:"str",  align:"left",  width:"10"}
]);
                            
sw_grid1.enableMultiselect(true);

                                
window.gts = 1; // ворота
window.ids = 0;


window.Cleaner.push(sw_grid1);
window.do_tool_csv = function(){ self.GridCSV(sw_grid1) }





var pasttypes = [{value: "", text: ""},
	              {% for item in pasttypes %}
					 {value: "{{ item['id'] }}", text: "{{ item['name'] }}"},
				  {% end %}];

var storagetypes = [{value: "", text: ""},
             {% for item in storagetypes %}
				 {value: "{{ item['id'] }}", text: "{{ item['name'] }}"},
			  {% end %}];


var all_sotrud = [{value: "", text: ""},
                    {% for item in all_sotrud %}
       				 {value: "{{ item[0] }}", text: "{{ item[1]}}"},
       			  {% end %}];


var swForm = new dhtmlXForm("swformextinfo", [
	{type:"input",  name:"id",      bind:"id",      label:"id:", 	           labelWidth: 110, disabled:"true" },
    {type:"input",  name:"os_numb", bind:"os_numb", label:"Номер отправки:",   labelWidth: 110, value: ""},
    {type:"select", name:"pallet",  bind:"pallet",  label:"Тип оклейки:", 	   labelWidth: 110, options: pasttypes, disabled:"true" },
    {type:"select", name:"storage", bind:"storage", label:"Тип размещения:",   labelWidth: 110, options: storagetypes},
    {type:"input",  name:"prim",  	bind:"prim", 	label:"Примечание:",	   labelWidth: 110, value: ""},
    {type:"input",  name:"skin",    bind:"skin", 	label:"Кол-во пленки:",    labelWidth: 110, value: "0"},
    {type:"input",  name:"desk",  	bind:"desk", 	label:"№ первой коробки:", labelWidth: 110, value: ""},
    
    {type:"select", name:"sotrud1", bind:"sotrud1", label:"Сборщик 1:",      labelWidth: 110, options: all_sotrud},
    {type:"select", name:"sotrud2", bind:"sotrud2", label:"Сборщик 2:",      labelWidth: 110, options: all_sotrud},
   
    {type:"checkbox", name:"packing", bind:"packing", label: "Пленка на коробки",            labelWidth: 110, checked: false}
]);


var sw_os_numb = swForm.getInput("os_numb");
var sw_prim = swForm.getInput("prim");

window.Cleaner.push(swForm);
            





var sw_grid2 = sw_btk.cells("b").attachGrid();
sw_grid2.columns([
  
      { type:"ro", sort:"int",  align:"right", width:"55", label:"Код" },
      { type:"ro", sort:"str",  align:"left",  width:"*",  label:"Товар" },
      { type:"ro", sort:"int",  align:"right", width:"65", label:"Кол-во" }
      
]);
window.Cleaner.push(sw_grid2);


sw_grid1.attachEvent("onRowSelect", function(id){

        self._messager.clearAll();


        self.LoadGrid(sw_grid2, "/warehouse/assembly/data/tovar?head="+id);

        self.NetSendAsync("/warehouse/assembly/data/info?head="+id, false,function(resp) {                            
                                                   
            if (resp.marsh_cls_name){                              
                self.AddMessage(resp.marsh_cls_name,5);
            }
            if (resp.prim){                              
                self.AddMessage(resp.prim,5);
            }
                                            
            return;
        
        });
        
        
        self.NetSendAsync("/warehouse/sborka/data/messages?head="+id, false,function(resp) {                            
            
        	for (var i=0; i<resp.length; i++) {
        	    // Iterates over numeric indexes from 0 to 5, as everyone expects.
        		
        		self.AddMessage(resp[i].mess,5);
        	}
                                            
            return;
        
        });
                         
});




window.do_tool_test = function(){


	
};



window.do_tool_edit_form = function(ids){
    
	
	ids=sw_grid1.getSelectedRowId();;
    
    swForm.clear();
    swForm.lock();
    
    
    dhtmlxAjax.get("/warehouse/assembly/data/item?" + encodeURI("id="+ ids), function(loader) {
    	
    	
    	var all_results =JSON.parse(loader.xmlDoc.responseText);
    	
		for (var item in all_results) {

    		try{
    			
    			swForm.setItemValue(item, all_results[item]);
    			
    			// console.log( all_results[item] );
    			
    		}
    		catch(e){
    			
    		}
    	}
    	
    
    	
    	swForm.unlock();
    	window.swForm = swForm;

	});
    	
                                
    
    self.ShowPanel("one");

    
                            
   
}



//запись доп. информации
window.do_save_extinfo = function(){

/*
 if (sw_os_numb.value.length < 1 || sw_os_numb.value.length > 32) {
     app.AddMessage('Недопустимая длина номера отправки',2);
     sw_os_numb.focus();
     return 0;
 }
*/  
 // Костыль к DHTMLX, иначе сериализация вручную
 swForm.setItemValue("os_numb", sw_os_numb.value);
 swForm.setItemValue("prim", sw_prim.value);
 
 var dt = swForm.Serialize();
 if(!!swForm.ids){
     dt=dt+"&uid="+swForm.ids;
 }
 //console.log('Serialized: ', dt);
 
 
 self.NetSendAsync("/warehouse/assembly/data/save", dt,function(resp) {
       
	 self.ShowPanel("def");
     
	 
	 window.do_tool_3();
      
  });
     
 
 self.ShowPanel("def");
  
}


 


        // save
window.do_tool_save = function(ids2, check){


    var ids = sw_grid1.getSelectedRowId();    
    if (!ids && ids2){
        ids = ids2;
    }
    
                         
    var pOkNoParty = '&pOkNoParty=1';  //Игноррировать товары без срока годности
    
    /*         
    if (check){
        pOkNoParty = '&pOkNoParty=1';
    }
    */
    
    
    if (!ids){
        self.AddMessage('Фактура не выбрана',3);
        return;
    }
    sw_grid2.editStop();
    
    
    self.NetSendAsync("/warehouse/assembly/data/gts", "ids="+ids+"&gts="+window.gts+pOkNoParty,function(resp) {
    
    window.do_tool_3();                                                         
                             
   });       
                         
}

/************************ SELECT CREATED NEW ROW  ********************/

                     


window.do_clear_filters = function(grid){
    
    try
    {                                   
                                       
        for (var i=0; i < grid.filters.length; i++){                                    
            grid.filters[i][0].value = '';
            //console.log(grid.filters[i][0].value);                                
        }
        
        grid.callEvent("onFilterEnd");
    }
    catch(e){}                                                                   
}                            
                     

window.do_tool_select = function(sw_grid1,ids){

    sw_grid2.clearAll();


    
    self.load(sw_grid1, "/warehouse/assembly/data/head?oper="+window.ids,function() {

        sw_grid1.selectRowById(ids,true,true,true);
                                         
    });
    
};


window.do_tool_consolidation = function(){
    var ids = sw_grid1.getSelectedRowId();
    if (!ids){
        self.AddMessage('Фактуры не выбраны',3);
        return;
    }
    //console.log("selected ids: " + ids);
    
    window.do_clear_filters(sw_grid1);
    /*
    sw_grid2.editStop();
    self.NetSendAsync("/warehouse/assembly/data/consolidation", "ids="+ids,function(resp) {
        window.do_tool_select(sw_grid1,resp.ids);
    });

    */




    dhtmlxAjax.post("/warehouse/assembly/data/consolidation",  "ids="+ids, function(resp){

        var results = JSON.parse(resp.xmlDoc.responseText);


        window.do_tool_select(sw_grid1,results.ids || "");

        if (results.info){
            self.AddMessage(results.info, "info");

        }


    });





}


window.do_tool_deconsolidation = function(){
    var ids = sw_grid1.getSelectedRowId();
    if (!ids){
        self.AddMessage('Фактуры не выбраны',3);
        return;
    }
    //console.log("selected ids: " + ids);
    
    window.do_clear_filters(sw_grid1);

    /*
    sw_grid2.editStop();
    self.NetSendAsync("/warehouse/assembly/data/deconsolidation", "ids="+ids, func = function() {
        
        window.do_tool_3(); 
    });*/



    dhtmlxAjax.post("/warehouse/assembly/data/deconsolidation",  "ids="+ids, function(resp){

        var results = JSON.parse(resp.xmlDoc.responseText);

        window.do_tool_select(sw_grid1,results.ids || "");


        if (results.info){
            self.AddMessage(results.info, "info");

        }



    });


}                         


window.do_tool_rollback = function(){
    var ids = sw_grid1.getSelectedRowId();
    if (!ids){
        self.AddMessage('Фактуры не выбраны',3);
        return;
    }
    
    
    window.do_clear_filters(sw_grid1);
    
    sw_grid2.editStop();
    self.NetSendAsync("/warehouse/assembly/data/rollback", "ids="+ids, func = function() {
        
        
        window.do_tool_3(); 
        });
}           

                            

// ворота
window.do_tool_2 = function(ids){
    window.gts=parseInt(ids.substr(3));
    var text = self.Toolbars["def"].getListOptionText("btngts", ids);                                            
    self.Toolbars["def"].setItemText("btngts", text);
}


// print passport
window.do_tool_4 = function(ids2){
    var ids = sw_grid1.getSelectedRowId();
    if(!ids) self.AddMessage('Выберите фактуру',2)
    else {
        var m=ids2.substr(3);
        var d='';
        //Отгрузочные этикетки
        if(m==2){
            var d=prompt('Диапазон мест разделенные пробелом','').split(' ');
        }
        self.NetSend("/warehouse/printpassport/data/print?head="+ids+"&mode="+m+"&d="+d);
    }                                
}



// Дополнительная информация - переход в режим ввода
window.do_tool_5 = function(){
    var ids = sw_grid1.getSelectedRowId();
    swForm.ids = ids;
    
    //console.log("ids: " + ids);
    
    if(!ids) {
        self.AddMessage('Выберите фактуру',2);
        return;
    }
    // а тут надо совершить проверку поля status
    var s = Number(sw_grid1.cells(ids, 7).getValue());
    if (s >= 4) {
        self.AddMessage('Фактуру с этим статусом нельзя изменить', 2);
        return;
    }

    swForm.setItemValue("os_numb", sw_grid1.cells(ids, 6).getValue());

    var opt = sw_grid1.cells(ids, 9).getValue();
    //console.log(opt);
    if (!!opt) {
        swForm.setItemValue("past_type", opt);
    } else {
        swForm.setItemValue("past_type", 1);
    }
    
    
    var opt2 = sw_grid1.cells(ids, 10).getValue();
    
    //console.log(opt2);
    
    if (!!opt2) {
        swForm.setItemValue("storage_type", opt2);
    } else {
        swForm.setItemValue("storage_type", "");
    }                                
    
    
    self.ShowPanel("one");
}

// Выход из режима ввода доп.информации
window.do_cancel_extinfo = function(){self.ShowPanel("def");}



// фильтр
window.do_tool_3 = function(ids2){     

    if (ids2){
        sessionStorage.setItem("filter_opr_/warehouse/assembly/data/head", ids2);

      }
    else{  
        var opr = sessionStorage.getItem("filter_opr_/warehouse/assembly/data/head");
        ids2 = opr?opr:"opr0";
    }
      
    window.ids=ids2.substr(3);                                                        

    var text = self.Toolbars["def"].getListOptionText("btnopr", ids2);
    
                                                                                
    self.Toolbars["def"].setItemText("btnopr", text);
    

   
    
     sw_grid2.clearAll();
    
    
     self.load(sw_grid1, "/warehouse/assembly/data/head?oper="+window.ids, function(){
    	 
     });
     
     
    }
    
  
        
window.do_tool_3();

