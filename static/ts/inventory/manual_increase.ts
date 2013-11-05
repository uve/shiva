/// <reference path="inventory.ts" />

module ManualIncreaseModule {
	
	export class ManualIncrease extends InventoryModule.Inventory{
	
		public class_name = "ManualIncrease";
	
		caption      : string;
		cell_id      : string;
		
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Ручная подтоварка";			
	 		this.cell_id     = "";							
			this.scanCell(); 
	 	}	
		
	
	    
	    public scanCell() {
	  
			this.formCell({			
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.addCell();
						    },
						    cancel: () => { 
						    				this.completeIncrease(); 
						    }
						 });
	    }
	           
	    
	    public addCell()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/increase/add",
	            data: {
	            			cell_id      : this.cell_id	     
	            	  },                    
	            success: () => { this.nextCell(); },
	            error:   () => { this.completeIncrease(); }
	                     
	        }); 
		}
	    
	    
	    public nextCell()
		{		    		
	    	var form = new FormModule.Form();
	    	
			form.FormMenu({
								
				caption: this.caption,	
				buttons: { 
							"Продолжить"  : () => { this.scanCell(); },							
							"Закончить подтоварку" : () => { this.completeIncrease(); }
				}
	
			});
		
		}
	    
		
		public completeIncrease() {
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/increase/complete",                   
	            success: () => { this.complete("Подтоварка завершена"); },
	            error:   () => { this.stop(); }
	                     
	        }); 
			
		}
			
			
	    
  
    
	}
}