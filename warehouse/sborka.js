var sw_grid1 = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],                        
                        columns:[
	  { type:"ro", sort:"str",  align:"center",  width:"50", label:"ID"},
	  { type:"ro", sort:"str",  align:"left",    width:"300", label:"Фактура" },
	  { type:"ro", sort:"str",  align:"center",  width:"100", label:"Начало обработки" },
	  { type:"ro", sort:"str",  align:"left",    width:"200", label:"Сотрудник" },
	  ]});
                            
sw_grid1.enableMultiselect(true);

/*

var sw_grid2 = sw_btk.cells("b").attachGrid();
sw_grid2.columns([
  
      { type:"ro", sort:"int",  align:"right", width:"100", label:"Сообщение" },
      { type:"ro", sort:"str",  align:"left",  width:"100",  label:"" },
      { type:"ro", sort:"int",  align:"right", width:"*", label:"" }
      
]);
window.Cleaner.push(sw_grid2);


*/

/*
sw_grid1.attachEvent("onRowSelect", function(id){

        self._messager.clearAll();

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
*/


self.load(sw_grid1, "/warehouse/sborka/data/list?oper="+window.ids);
