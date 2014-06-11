  
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
        { type:"ro", sort:"str",  align:"center", width:"100", label:"Партия" },
        { type:"ro", sort:"str",  align:"center", width:"100", label:"Годен ДО"},
        { type:"ro", sort:"str",  align:"center", width:"100", label:"Количество"},

    ]
});



window.Cleaner.push(sw_grid2);


update = function(){ 
	
	params = {};
	params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");
	
	
	self.load(sw_grid1, "/revision/saldo_gap/data/list?" + self.serialize(params), function() {
    	
		
    });
};



window.change_depart = function(){

    update();

}

update();



sw_grid1.attachEvent("onRowSelect", function(code){


    params = {"code": code};
    params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");


    self.load(sw_grid2, "/revision/saldo_gap/data/detail?" + self.serialize(params));

});



window.do_print = function(){

    sw_grid1.printView("","<script> window.print(); </script>");
}



window.do_csv = function(){

    var params = {};

    params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");


    if (params["departs"] != '3' && params["departs"] != '31'){
        return false;
    }

    var new_grid = new dhtmlXGridObject({
        /*parent: "sw_grid1",*/
        columns: [
            { type:"ro", sort:"str",  align:"center", width:"80",  label:"Код" },
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Наименование" },
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Товарный остаток"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Адрес"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Остаток в ячейке"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Всего на адресах"}

        ]
    });


    self.load(new_grid, "/revision/saldo_gap/data/csv?" + self.serialize(params), function() {

        self.GridCSV(new_grid);
    });


}




window.do_csv_full = function(){

    var params = {};

    params["departs"]  = self.Toolbars["def"].getListOptionSelected("departs");


    if (params["departs"] != '3' && params["departs"] != '31'){
        return false;
    }

    var new_grid = new dhtmlXGridObject({
        /*parent: "sw_grid1",*/
        columns: [
            { type:"ro", sort:"str",  align:"center", width:"80",  label:"Код" },
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Наименование" },
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Товарный остаток"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Адрес"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Остаток в ячейке"},
            { type:"ro", sort:"str",  align:"center", width:"100", label:"Всего на адресах"}

        ]
    });


    self.load(new_grid, "/revision/saldo_gap/data/csv_full?" + self.serialize(params), function() {

        self.GridCSV(new_grid);
    });


}