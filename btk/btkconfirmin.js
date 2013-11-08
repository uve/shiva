var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");


sw_btk.items[0].setText("Список фактур");
sw_btk.items[1].setText("Список товаров");
window.Cleaner.push(sw_btk);
                            
var sw_grid1 = sw_btk.cells("a").attachGrid();

sw_grid1.columns([
  { type:"ro", sort:"int",  align:"center", width:"80", label:"ID" },  
  { type:"ro", sort:"str",  align:"center", width:"50",  label:"Номер" },
  { type:"ro", sort:"date", align:"center", width:"100", label:"Дата" },          
  { type:"ro", sort:"str",  align:"left",   width:"150", label:"От кого" },
  { type:"ro", sort:"str",  align:"left",   width:"*",   label:"Операция" },  
  { type:"ro", sort:"str",  align:"center", width:"80", label:"Статус" }    
  ]);

    self.load(sw_grid1, "/btk/btkconfirmin/data/head");


    var sw_grid2 = sw_btk.cells("b").attachGrid();
    sw_grid2.columns([
      
          { type:"ro", sort:"int",  align:"center",  width:"55", label:"ID" },
          { type:"ro", sort:"int",  align:"center",  width:"55", label:"Код" },
          { type:"ro", sort:"str",  align:"left",   width:"*",  label:"Товар" },
          { type:"ro", sort:"int",  align:"center", width:"60", label:"Кол-во" },
          { type:"ro", sort:"int",  align:"center", width:"100", label:"Партия" },
          { type:"ro", sort:"int",  align:"center", width:"100", label:"Годен ДО" }
          
    ]);
    window.Cleaner.push(sw_grid2);
                        
                        

    sw_grid1.attachEvent("onRowSelect", function(id){
    	self.Toolbars["def"].disableItem('id_print');
    	    	
        self.load(sw_grid2, "/btk/btkconfirmin/data/list?head="+id);
        
        window.btk_head = id;        
    });
    
    
    sw_grid2.attachEvent("onRowSelect", function(id){
    	self.Toolbars["def"].enableItem('id_print');
    	
    	window.btk_party = id;
    });
    
    
    
    
    self.Toolbars["def"].enableItem('id_print');
    
    
    window.do_print = function(){
    	
    	self.NetSend("/btk/btkconfirmin/data/print?head=" + window.btk_head
                + "&party=" + window.btk_party);
    	
    	/*
    	dhtmlx.confirm({
    		id: 'tttt',
    		title: "Печать",
    		text: "<b>Введите кол-во копий: </b><input type='text' style='text-align: center; width: 20px;' name='party-pages' id='party-pages' value='1'>"//,
    		//callback: do_print_callback
    	});
    	 */
    	
    }
    
    window.do_confirm = function(){
    	
<<<<<<< HEAD
    	self.NetSend("/btk/btkconfirmin/data/confirm?head=" + window.btk_head);
=======
    	self.NetSend("/btk/btkconfirmin/data/confirm?header_id=" + window.btk_head);
>>>>>>> 210fa54e852e44a8f8ddfe37ab681891f2f454b5
    	
        	
    }
    
    
    
                       
                        