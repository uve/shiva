var sw_grid = new dhtmlXGridObject({
	
       parent: window.app.Panels["def"],
       columns:[{
         label:"Номера партий",
         type:"ro",
         sort:"int"
       }]                        
     });
     window.Cleaner.push(sw_grid);


     function print_party(party){
         sw_grid.clearAll();
         sw_grid.csv.row = ",";
         
         
         var url = "/warehouse/prnpart/data/";

         dhtmlxAjax.post(url + party, "", function(response) {
         	
         	
         	var data =JSON.parse(response.xmlDoc.responseText);
         	
         	sw_grid.parse(data.join(), "csv");
            
            var rand = Math.random()*Math.random();
            
            var urs = [{{ size[0] }}, {{ size[0] }}];
           
            for(i in data){

                urs.push( "/warehouse/print_barcode/?code="+data[i] + "&random=" + rand);


            }
            self.PrintURL.apply(self, urs);

     	});
  	 
     }
 
 
     window.do_tool_print_party = function(){     
    	 print_party("party");
     }
     
     window.do_tool_print_extra_party = function(){     
    	 print_party("extra_party");
     }
                       