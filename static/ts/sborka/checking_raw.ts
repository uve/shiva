/// <reference path="../inventory/inventory.ts" />

module CheckingRawModule {
		
	export class CheckingRaw extends InventoryModule.Inventory{
	
		public class_name = "CheckingRaw";
	
		caption     : string;

		party_id    : string;
		header_id   : string;

		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption   = "Проверка сборки заказа по сырью";
	 		this.party_id  = "";

	 	}	
	 	


	    public scanParty() {
	    	
			this.formParty({
						    text: "Ввод экстра-партии",
						    apply: (value) => {
							    	this.party_id = value;
							    	this.ScanExtraParty_Raw();
						    },
						    cancel: () => { this.scanPallet(); }
						 });
	    }
	    



	     public ScanExtraParty_Raw()
         {

            this.ajax({
                type: "POST",
                url: "/sborka/scan_extra_party_raw",
                data: {
                            party_id     : this.party_id,
                            header_id    : this.header_id
                      },
                success: (resp) => {

                        if (parseInt(resp.count) == 0){

                            this.IsRawHeaderReady();
                        }
                        else{
                            this.scanParty();
                        }
                },
                error: () => {

                           this.scanParty();
                }

            });
         }

	    
	    public IsRawHeaderReady()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/sborka/is_raw_header_ready",
	            data: {
	            			header_id    : this.header_id
                },
	            success: (resp) => {
	            			this.complete("Заказ проверен");
	            },
                error: () => {

                            this.scanParty();
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