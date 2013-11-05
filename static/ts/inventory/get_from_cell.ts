/// <reference path="inventory.ts" />

module GetFromCellModule {
	
	export class GetFromCell extends InventoryModule.Inventory{
	
		public class_name = "GetFromCell";
	
		caption      : string;
		cell_id      : string;
		party_id     : string;
		pallet_id    : string;
		target_id    : string;
		
		count		 : number;
	
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Взять из ячейки";
			
	 		this.cell_id      = "";
			this.party_id     = "";
			this.pallet_id    = "";
			
			this.count  = 0;
					
			this.scanCell(); 
			
			//this.set_party();
	 	}	
		
	
	    
	    public scanCell() {
	    	/*67*/
			this.formCell({					
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.scanPallet();
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	           
	    
	    
	    public scanPallet() {
	    	
			this.formPallet({					
						      apply: (value) => {
							    	this.pallet_id = value;
							    	this.scanParty();
						      },
						      cancel: () => { this.scanCell(); }
						   });
	    }
	    
	
	    
	    public scanParty() {
	    	
			this.formParty({					
						    apply: (value) => {
							    	this.party_id = value;
							    	this.getCount();
						    },
						    cancel: () => { this.scanPallet(); }
						 });
	    }
	    
		
		
		 /**
	     *   Ввод количества коробок
	     *   
	     */    
	    public getCount() {
	    	
	        	
	    	var msg = "Введите количество КОРОБОК";      	    	    	
	
			var form = new FormModule.Form();
			
			form.FormCount({
			
					caption: this.caption,
					text: msg,
					
					default_value: this.count,
					min_value: 0,
					max_value: 1000,
								
				    apply: (value) => {
				    	
				    	this.count = value;
				    	this.get_target();
					},
					cancel: () => { 
	
							this.scanParty();
	
					}							
			});    		
			
	    }
	    
	    
	    
	    public get_target(){
	    	
	    	var msg = "Ячейка назначения не выбрана";
	    	
	    	if (this.target_id){
	    		msg = "Ячейка назначения: " + this.target_id;
	    	}
	    	
			this.menu({
				
				text: msg,
				buttons: { 	
					
							"Выбрать ячейку назначения"  : () => {
								
								this.scan_target();
							},
							
							"Изьять из ячейки" : () => {
								
								this.set_party(); 
							},
							
							"Назад" : () => {
								
								this.getCount(); 
							}
				}
			}); 
	    	
	    }
	    
	
   
   
	    
	    
	    public scan_target() {

			this.formCell({					
						    apply: (value) => {
							    	this.target_id = value;
							    	this.set_party();
						    },
						    cancel: () => { 
						    		this.set_party(); 
						    }
						 });
			
	    }
	    
	    
	    
	    public set_party()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/get_from_cell",
	            data: {
	            			cell_id      : this.cell_id,
	            			party_id     : this.party_id,
	            			pallet_id    : this.pallet_id,	            			
	            			target_id    : this.target_id,
	            			count   	 : this.count
	            			
	            	  },                    
	            success: () => { 
	            					this.get_mode(); 
	            },
	            error:   () => { 
	            					this.get_mode(); 
	            }
	                     
	        }); 
		}
	    
	    
	    
	    
	    public get_mode(){
	    	

			this.menu({
				
				caption: "Выберите режим",
				
				buttons: { 						
														
							"Взять ещё с ячейки"  : () => { 
								
								this.party_id = "";						
								this.count = 0;										
								this.scanParty();
							},
							
							"Завершить задачу"   : () => { this.complete(); }
				}
			}); 
	    	
	    }	    
	    
	    
	    
    
	}
}