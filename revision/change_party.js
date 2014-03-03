  
var sw_grid = new dhtmlXGridObject({
   //parent: "sw_grid",
   parent: window.app.Panels["def"],
   columns: [
      { type:"ro", sort:"str",  align:"center", width:"80",  label:["Код", "#text_filter"], },  
      { type:"ro", sort:"str",  align:"left"  , width:"100", label:["Номер партии", "#text_filter"] },
      
      { type:"ro", sort:"str",  align:"left", width:"*",   label:["Наименование", "#text_filter"] },
      
  	  { type:"ro", sort:"str",  align:"center", width:"100", label:"Срок годности"},
  
      
    ]
  });




window.Cleaner.push(sw_grid);




var form = new dhtmlXForm("sw_form", [
                                    
{type:"input",     labelWidth: 100, width:100, name:"type",   bind:"type",  labelAlign: "right", label:"Код товара:"},
{type:"calendar",  labelWidth: 100, width:100, name:"data_full",   bind:"data_full",  labelAlign: "right", label:"Срок годности:",
	serverDateFormat: "%d.%m.%Y", dateFormat: "%d.%m.%Y"},
	
{type:"input",     labelWidth: 100, width:100, name:"num",    bind:"num",   labelAlign: "right", label:"Номер партии:"},

{type:"hidden",     labelWidth: 100, width:100, name:"data",   bind:"data",  labelAlign: "right", label:"Срок годности:"},


 ]);                        





window.do_add = function(){
  	
	
	form.clear();
	
    self.ShowPanel("one"); 
};



window.do_delete = function(){
	var ids = sw_grid.getSelectedRowId();
    
    if (!ids){
    	app.AddMessage('Выберите ячейку',2) 
    }
    else {
    	
    	dhtmlxAjax.post("/revision/change_party/data/delete", "value="+ids, function(){
        	
        	window.update();

        });
    }
    
};

window.do_execute = function(){

	dhtmlxAjax.post("/revision/change_party/data/execute", "value="+ids, function(){
    	
    	window.update();

    });

};

window.do_cancel = function(){ self.ShowPanel("def") };



window.do_save = function(){ 	
	
	//form.updateValues();
	form.validate();

	form.setItemValue("data", form.getCalendar("data_full").getFormatedDate());
	

    var params=form.Serialize();  
	
	dhtmlxAjax.post("/revision/change_party/data/add", params, function(){
    	
    	window.update();
    	
    	self.ShowPanel("def"); 
    	  
    });
                         
}


    


window.update = function(){ 
	
	params = {};
	//params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");
	
	
	self.load(sw_grid, "/revision/change_party/data/list?" + self.serialize(params), function() {
    	
		
    });
};

      
window.update();


window.do_print = function(){
		
		sw_grid.printView("","<script> window.print(); </script>");      
}