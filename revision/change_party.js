  
var sw_grid1 = new dhtmlXGridObject({
   //parent: "sw_grid1",
   parent: window.app.Panels["def"],
   columns: [
      { type:"ro", sort:"str",  align:"center", width:"80",  label:["Код", "#text_filter"], },  
      { type:"ro", sort:"str",  align:"left"  , width:"100", label:["Номер партии", "#text_filter"] },
      
      { type:"ro", sort:"str",  align:"left", width:"*",   label:["Наименование", "#text_filter"] },
      
  	  { type:"ro", sort:"str",  align:"center", width:"100", label:"Срок годности"},
  
      
        ]
    });




window.Cleaner.push(sw_grid1);


update = function(){ 
	
	params = {};
	//params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");
	
	
	self.load(sw_grid1, "/revision/change_party/data/list?" + self.serialize(params), function() {
    	
		
    });
};

      
update();


window.do_print = function(){
		
		sw_grid1.printView("","<script> window.print(); </script>");      
}