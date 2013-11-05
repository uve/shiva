/// <reference path="inventory.ts" />

module InputProductModule {
		
	export class InputProduct extends InventoryModule.Inventory{
	
		public class_name = "InputProduct";
	
		caption     : string;

		
		cell_id     : string;
		
		plus        : number;
		count       : number;
		party_id    : string;
		header_id   : string;
		
		all_clients;
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Приемка упаковки";
	 		this.cell_id   = "";
	 		this.header_id = "";
	 		
	 		this.plus = 0;
	
	 		
	 		this.startInput();
	 	}	
	 	
	 
	    
	    
	    public startInput() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/start_input",
	            data: { 

	            },          
	            success: (resp) => {             					
	            					this.header_id = resp["header_id"];
	            					this.start(); 
	            },									
	            error:   () => { this.stop(); }
	                     
	        }); 
	    }
	
	
	    public setParty()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/add_product_to_input",
	            data: {
	            			header_id    : this.header_id,
	            			
	            			cell_id      : this.cell_id,
	            			pallet_id    : this.pallet_id,
	            			party_id     : this.party_id,
	            			product_id   : this.product_id,
	            			party_number : this.party_number,
	            			party_status : this.party_status,
	            			count_inbox  : this.count_inbox,
	            			count   	 : this.count,
	            	        plus    	 : this.plus,
	            	        goden_do   	 : this.goden_do,
	            			
	            	  },                    
	            success: () => { this.chooseType(); },
	            error:   () => { this.getCount(); }
	                     
	        }); 
		}
	    
	    
	    
	    public chooseType(){
	    	
	    	var msg = "Ячейка: " + this.cell_id;
	    	
	    	
			var form = new FormModule.Form();
			
			form.FormMenu({
				
				text: msg,
				buttons: { 
							"Добавить такой же товар"  : () => { 
								
									
								this.count = 0;
								this.count_inbox = 0;
								
								this.plus = 1;	
								this.scanCell();
							},
							"Добавить ДРУГОЙ товар"  : () => { 
								
								this.product_id = "";
								this.product_code = "";
								this.product_name = "";
								
								this.count = 0;
								this.count_inbox = 0;
								
								this.plus = 0;												
								this.scanCell();  // Party ???
							},
							
							"Приостановить приёмку" : () => { this.stop(); },
							
							"Завершить приемку"   : () => { this.endInput(); }
				}
			}); 
	    	
	    }
	    
	    
	  
	    
	    
	    
	    public endInput() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/end_input",
	            data: { 
	            		"header_id" : this.header_id 
	            },          
	            success: () => { this.complete("Приемка завершена"); },									
	            error:   () => { this.stop(); }
	                     
	        }); 
	    }    
	      
	}
}