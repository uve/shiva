/// <reference path="../inventory/inventory.ts" />

module PodtovarkaShtukaModule {
		
	export class PodtovarkaShtuka extends InventoryModule.Inventory{
	
		public class_name = "PodtovarkaShtuka";
	
		caption     : string;
				

		cell_id     : string;		
		party_id    : string;
		pallet_id   : string;
		header_id   : string;
		
		count       : number;
		
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption   = "Подтоварка штучной сборки";
	 		this.cell_id   = "";
	 		this.party_id  = "";
	 		this.pallet_id = "";
	 		this.header_id = "";
	 		this.count     = 0;
	
			this.get_header(); 
	 	}	
	 	
	 
	 	
	    public get_header() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/sborka/new_sborka_for_shtuka",
	            data: { },          
	            success: (resp) => {
	            	
	            		this.header_id = resp.header_id;
	            		
	            		this.scanCell();
	            }
	                     
	        }); 
	    }
	    
	    
	    
	    public scanCell() {
	    	
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
				    	this.add_box();
					},
					cancel: () => { 
	
							this.scanParty();
	
					}							
			});    		
			
	    }
	    
	    
	    
	    public add_box()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/sborka/add_factura_for_shtuka",
	            data: {
	            			cell_id      : this.cell_id,
	            			party_id     : this.party_id,
	            			pallet_id    : this.pallet_id,	            			
	            			header_id    : this.header_id,
	            			count   	 : this.count
	            			
	            	  },                    
	            success: () => { 
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
							
							"Завершить подтоварку"   : () => { 
								
								
								this.end_factura();
								
							}
				}
			}); 
	    	
	    }	   
	    
	    
	    public end_factura()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/sborka/end_factura_for_shtuka",
	            data: {            			
	            			header_id    : this.header_id,	            			
	            	  },                    
	            success: () => { 
	            			
	            			this.complete(); 
	            }
	                     
	        }); 
		}
	    
	    
	      
	}
}