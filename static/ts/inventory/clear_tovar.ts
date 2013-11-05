/// <reference path="inventory.ts" />

module ClearTovarModule {
	
	export class ClearTovar extends InventoryModule.Inventory{
	
		public class_name = "ClearTovar";
	
		product_id    : string;
		count_inbox   : number;
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Списание с производства";

			this.getCode();
	 	}	
	 	
	 	
	 	
	    public getCountInBox(){
		    

			this.menu({
				
				caption: "Выберите режим",
				buttons: { 
	
							"Списать все"  : () => { 												
								
								this.clear_tovar(); 
							},

							"Указать количество"  : () => {
									
								this.get_count();
							},
							
							"Отменить"   : () => { 								

								this.stop();				
							}
			
			
				}
			});
	    	
	    	
	    }
	    
	    
	 	
	 	public get_count() {
	 		 
			var form = new FormModule.Form();
			
			form.FormCount({
				
					text: "Введите количество штук",					
					default_value: this.count_inbox,								
				    apply: (value) => {
				    	
				    	this.count_inbox = value;
				    	this.clear_tovar();
					},
					cancel: () => { 
									
						this.getCountInBox();
									
					}								
			});    		
	
	    }

	 	
	 	public clear_tovar(){

			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/clear_tovar",
	            data: {

	            			product_id   : this.product_id,
	            			count_inbox  : this.count_inbox	            			
	            	  },                    
	            success: () => { this.complete("Товар списан с производства"); },
	            error:   () => { this.stop(); }
	                     
	        }); 
	 		
	 	}
	
	
    
	}
}