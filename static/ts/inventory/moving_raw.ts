/// <reference path="inventory.ts" />

module MovingRawModule {
	
	export class MovingRaw extends InventoryModule.Inventory{
	
		public class_name = "MovingRaw";
	
		code         : string;
		caption      : string;
		cell_id      : string;
		target_id    : string;	
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Перемещение сырья";
			
	 		this.cell_id     = "";
			this.target_id     = "";
					
			this.scanCell(); 
	 	}	
		
	
	    
	    public scanCell() {
	  
			this.formCell({			
							text:  "Ввод штрих-кода ИСХОДНОЙ ячейки",
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.scanParty();
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	    
	    
	    
	    public scanParty() {
	    	
			this.formParty({					
						    apply: (value) => {
							    	this.party_id = value;
							    	this.getCell();
						    },
						    cancel: () => { this.scanCell(); }
						 });
	    }
	    
	           
	    
	    
	    public getCell()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/moving/GetCellForPartyFromBox",
	            data: { 'party_id':  this.party_id,
	            		'value':     "31"
	            	},	                 
	            success: (resp) => { 
	            					this.code = resp.code;
	            					this.complete("Паллета перемещена"); 
	            },
	            error:   () => { this.stop(); }
	                     
	        }); 
		}
	    
  
    
	}
}