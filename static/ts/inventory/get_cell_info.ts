/// <reference path="inventory.ts" />

module GetCellInfoModule {
	
	export class GetCellInfo extends InventoryModule.Inventory{
	
		public class_name = "GetCellInfo";
	
		caption      : string;
		cell_id      : string;
		
		count        : number;
		
		all_cells;
		
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Проверка ячейки";
			
	 		this.cell_id = "";
	 		
	 		this.count = 0;
	 		
					
			this.scanCell(); 
			
	 	}	
		
	
	    
	    public scanCell() {
	    	/*67*/
			this.formCell({					
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.checkCell();
						    },
						    cancel: () => { 
						    		
						    		this.stop(); 
						    }
						 });
	    }
	           
	    
	    
	    public checkCell()
		{		    	
	
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/get_cell_info",
	            data: {
	            			cell_id:  this.cell_id
	            	  },                    
	            success: (resp) => { 
	            	
	            		this.all_cells = resp;
	            		
	            		this.count = resp.length-1;
	            		
	            		this.show_page(0);	
	            					
	            },
	            error:   () => { this.scanCell(); } 
	                     
	        }); 
		}
	
	    
	    
	    
	    public show_page(page : number)
		{		    	
			
			var value = this.all_cells[page];		
			
			var text = value["tname"] +   
					   "</br>Коробок:  "   + value["valume"] + 
					   "</br>В коробке:  " + value["inbox"] +
					   "</br>Ожид. расход (в коробках): " + value["future_exps"] +
					   "</br>Годен до:  "  + value["data"];
			
			
			
			
			var buttons = { 		
					
					"Отменить"   : () => { 								

						this.scanCell(); 			
					}	
					
					
		    };
				
			
			var add_buttons;
			
			
			if (page > 0){
				
				add_buttons = {

							"Назад"  : () => {
									
								this.show_page(page - 1);
								
							}
				};
		
						
				buttons = this.extend(add_buttons, buttons);
			}
			
			
			if (page < this.count){
				
				add_buttons = {

							"Вперед"  : () => {
										
								this.show_page(page + 1);
								
							}
				};
		
						
				buttons = this.extend(add_buttons, buttons);
			}
			
			
			
			
			var caption = value["name"] + "  (" + (page + 1) + "/" + (this.count + 1) + ")";
			
			this.menu({
				
				caption: caption,
				text :   text,
				buttons: buttons
			});
		
		}
	    
	    
    
	}
}