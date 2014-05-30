  
var sw_grid1 = new dhtmlXGridObject({
   parent: "sw_grid1",
   columns: [
      { type:"ro", sort:"str",  align:"center", width:"80",  label:["Код", "#text_filter"], },  
      { type:"ro", sort:"str",  align:"left"  , width:"*",   label:["Наименование", "#text_filter"] },
      { type:"ro", sort:"int",  align:"center", width:"100", label:"Товарный остаток"},
      { type:"ro", sort:"int",  align:"center", width:"100", label:"Партионный остаток"},                                                   
      { type:"ro", sort:"int",  align:"center", width:"100", label:"Остаток в ячейках"},
      
        ]
    });



var sw_grid2 = new dhtmlXGridObject({
    parent: "sw_grid2",
    columns: [
        { type:"ro", sort:"str",  align:"center", width:"80",  label:"Адрес" },
        { type:"ro", sort:"str",  align:"left"  , width:"100", label:"Партия" },
        { type:"ro", sort:"int",  align:"center", width:"100", label:"Годен ДО"},
        { type:"ro", sort:"int",  align:"center", width:"100", label:"Количество"},

    ]
});



window.Cleaner.push(sw_grid2);


update = function(){ 
	
	params = {};
	params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");
	
	
	self.load(sw_grid1, "/revision/saldo_gap/data/list?" + self.serialize(params), function() {
    	
		
    });
};

                    
self.Toolbars["def"].attachEvent("onClick", function(id) {
	update();
});
      
update();


window.do_print = function(){
		
		sw_grid1.printView("","<script> window.print(); </script>");      
}


sw_grid1.attachEvent("onRowSelect", function(code){


    params = {"code": code};
    params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");


    self.load(sw_grid2, "/revision/saldo_gap/data/detail?" + self.serialize(params));

});
