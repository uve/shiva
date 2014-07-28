var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");

sw_btk.items[0].setText("Список фактур");
sw_btk.items[1].setText("Список товаров");
window.Cleaner.push(sw_btk);
                            
var sw_grid1 = sw_btk.cells("a").attachGrid();

sw_grid1.columns([
  { type:"ro", sort:"int",  align:"center", width:"80", label:["ID","#text_filter"] },  
  { type:"ro", sort:"str",  align:"center", width:"50",  label:["Номер","#text_filter"] },
  { type:"ro", sort:"date", align:"center", width:"100", label:"Дата" },          
  { type:"ro", sort:"str",  align:"left",   width:"150", label:"От кого" },
  { type:"ro", sort:"str",  align:"left",   width:"*",   label:"Операция" },  
  { type:"ro", sort:"str",  align:"center", width:"80", label:"Статус" }    
  ]);


	function update(){ 
	
		self.load(sw_grid1, "/btk/btkconfirmin/data/head");
	}
	
	update();
	
	
    var sw_grid2 = sw_btk.cells("b").attachGrid();
    sw_grid2.columns([
      
          { type:"ro", sort:"int",  align:"center",  width:"55", label:["ID","#text_filter"] },
          { type:"ro", sort:"int",  align:"center",  width:"55", label:["Код","#text_filter"] },
          { type:"ro", sort:"str",  align:"left",   width:"*",  label:"Товар" },
          { type:"ro", sort:"int",  align:"center", width:"60", label:"Кол-во" },
          { type:"ro", sort:"int",  align:"center", width:"100", label:["Партия","#text_filter"] },
          { type:"ro", sort:"int",  align:"center", width:"100", label:"Годен ДО" },
          { type:"ro", sort:"int",  align:"center", width:"0", label:"cid" },
          { type:"ro", sort:"int",  align:"center", width:"0", label:"cid" },
          {
				label:"Статус партии",
				width:100,
				type:"co",
				options:{
					{% for item in all_status %} 
				    	"{{ item['id'] }}":"{{ item['name'] }}",
				    {% end %}
				}
			}
          
    ]);
    window.Cleaner.push(sw_grid2);
                        
                        
    
    var col_status = 6;
    var col_status_name = 8;
    var status = {
			 "100":"#BFFFCC", //кондиция
			 "101":"#ffc9da", //брак
			 "102":"#FFD191", //аллергены
			 "103":"#FFF8A6" //карантин		
	}
	

    sw_grid1.attachEvent("onRowSelect", function(id){
    	self.Toolbars["def"].disableItem('id_print');
    	    	
    	window.btk_head = id;
    	
    	
    	
    	    	

        self.load(sw_grid2, "/btk/btkconfirmin/data/list?head="+id, 
        
				        function() {
				        	
				        	
				        	sw_grid2.forEachRow(function(id){
				
				        		var value = sw_grid2.cells(id,col_status).getValue();        		
				        		sw_grid2.cells(id,col_status_name).setValue(value);
				        		
				        		if (status[value]){
				        			sw_grid2.setRowTextStyle(id, "background-color: " + status[value]);	
				        		}
				        		
				                 
				             })

        });
    
    
        
           
    });
    
    
    sw_grid2.attachEvent("onRowSelect", function(id){
    	self.Toolbars["def"].enableItem('id_print');
    	
    	window.btk_party = id;
    });
    

    sw_grid2.attachEvent("onEditCell",function(stage, id,index,value){
        //called each time when cell changed
    	if(stage==2){ 

    		if (status[value]){
    			sw_grid2.setRowTextStyle(id, "background-color: " + status[value]);	
    		}
    		
        	self.NetSend("/btk/btkconfirmin/data/change_status?head=" + window.btk_head
                    + "&party=" + window.btk_party+ "&status=" + value);
    	} 
        return true; 
    })

    
    
    
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


        dhtmlxAjax.post("/btk/btkconfirmin/data/confirm", "head=" + window.btk_head, function(resp){

            var results = JSON.parse(resp.xmlDoc.responseText);

            if (results.error){
                self.AddMessage(results.error, "error");
            }
            else{
                update();
            }

    	});



    }
    
    
    
                       
                        