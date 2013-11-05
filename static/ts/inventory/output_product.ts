/// <reference path="inventory.ts" />

module OutputProductModule {
		
	export class OutputProduct extends InventoryModule.Inventory{
	
		public class_name = "OutputProduct";
	
		caption     : string;
				
		client_id   : string;
		client_name : string;
		
		cell_id     : string;
		count       : number;
		party_id    : string;
		header_id   : string;
		
		all_clients;
		
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Отгрузка клиенту";
	 		this.cell_id   = "";
	 		this.header_id = "";
	
			this.allClients(); 
	 	}	
	 	
	 
	 	
	    public allClients() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/all_clients",
	            data: { },          
	            success: (resp) => {
	            	                this.all_clients = resp;
	            					this.chooseClient(); 
	            },            									
	            error:   () => { this.stop(); }
	                     
	        }); 
	    }
		
	    
	    
	    public chooseClient() {
	    	
			
			var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Выберите клиента",
				options: this.all_clients,
				buttons: { 
							"Продолжить"  : () => {
								
													this.client_id   = form.value;
													this.client_name = form.text;					
	
													this.getConfirmClient();
													
							},
							
							"Вернуться"   : () => { 
													this.stop(); 
							}
				         }
	
			});  		
	
	    }
	    
	    
	    
	    public getConfirmClient(){
	    	
	    	
			this.menu({
				
				caption: "Подтверждение клиента",
				text:    this.client_name,
				buttons: { 
							"Потвердить"  : () => { 
	
								this.startOutput();
							},
							
							"Вернуться"   : () => { this.allClients(); }
				         }
	
			});
	    	
	
	    }
	    
	
	    
	    
	    public startOutput() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/start_output",
	            data: { 
	            		"client_id" : this.client_id 
	            },          
	            success: (resp) => {             					
	            					this.header_id = resp["header_id"];
	            					this.scan_cell(); 
	            },									
	            error:   () => { this.stop(); }
	                     
	        }); 
	    }
	
	
	    
	    public scan_cell() {
	    	
			this.formCell({					
						    apply: (value) => {
							    	this.cell_id = value;
							    	
							    	this.check_party();
						    },
						    cancel: () => { this.chooseType(); }
						 });
	    }
	           
	    
	    
	    
	    public check_party() {
	    	
			this.menu({
				
				caption: "Отгрузка клиенту",
				buttons: { 
							"Подтвердить"    : () => { this.addProduct(); },
							
							"Указать партию" : () => { this.scan_party(); },
							
							"Назад"          : () => { this.scan_cell(); }
				         }
			});
	    }
	           	    
	    
		
	    public scan_party() {
	    	
			this.formParty({					
						    apply: (value) => {
							    	this.party_id = value;														    	
							    	this.get_count();
						    },
						    cancel: () => { this.check_party(); }
						 });
	    }
	    
	    	       
	    
		 /**
	     *   Ввод количества коробок
	     *   
	     */    
	    public get_count() {
	
			var form = new FormModule.Form();
			
			form.FormCount({
			
					text: "Введите количество КОРОБОК",													
				    apply: (value) => {
				    	
				    		this.count = value;
				    		this.addProduct();
					},
					cancel: () => { 	
							this.scan_party();	
					}							
			});    		
			
	    }
	    
	    
	    public addProduct() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/add_product",
	            data: { 
	            		"count"     : this.count,	
	            		"cell_id"   : this.cell_id,
	            		"party_id"  : this.party_id,
	            		"header_id" : this.header_id	            		
	            },          
	            success: () => { this.chooseType(); },									
	            error:   () => { this.chooseType(); }
	                     
	        }); 
	    }
	
	    
	    
	    
	    public chooseType(){
	    	
	    	
			this.menu({
				
				caption: "Отгрузка клиенту",
				buttons: { 
							"Отгрузить ещё" : () => { this.scan_cell(); },
							
							"Приостановить отгрузку" : () => { this.stop(); },
							
							"Завершить"     : () => { this.endOutput();}
				         }
	
			});
	    }
	    
	    
	    
	    public endOutput() {
	    	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/end_output",
	            data: { 
	            		"header_id" : this.header_id 
	            },          
	            success: () => { this.complete("Отгрузка завершена"); },									
	            error:   () => { this.stop(); }
	                     
	        }); 
	    }    
	      
	}
}