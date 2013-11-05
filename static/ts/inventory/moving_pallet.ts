/// <reference path="inventory.ts" />

module MovingPalletModule {
	
	export class MovingPallet extends InventoryModule.Inventory{
	
		public class_name = "MovingPallet";
	
		caption      : string;
		cell_id      : string;
		target_id      : string;	
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Перемещение ячейки";
			
	 		this.cell_id     = "";
			this.target_id     = "";
					
			this.scanCell(); 
	 	}	
		
	
	    
	    public scanCell() {
	  
			this.formCell({			
							text:  "Ввод штрих-кода ИСХОДНОЙ ячейки",
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.destCell();
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	           
	    
	    
	    public destCell() {
	
			this.formCell({		
							text:  "Ввод штрих-кода КОНЕЧНОЙ ячейки",
						    apply: (value) => {
							    	this.target_id = value;
							    	this.setCell();
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	
	    
	    public setCell()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/moving/moved",
	            data: { 'cell_id':   this.cell_id,
	            		'target_id': this.target_id
	            	},	                 
	            success: () => { this.complete("Паллета перемещена"); },
	            error:   () => { this.stop(); }
	                     
	        }); 
		}
	    
  
    
	}
}