module TaskModule {

	declare var main;		
	declare var status;

	export interface TaskInterface {
		
		curr_PalletBarcode: string;
	
	}
	
	
	export class Task extends CoreModule.Core implements TaskInterface{
		
		
	    BCTUSER     = 1; 						// константа - режим ввода ШК пользователя 
	    BCTPALLET   = 2;						// константа - режим ввода ШК паллеты
	    BCTCELL     = 3;						// константа - режим ввода ШК ячейки
	    BCTDELIVERY = 5;						// константа - режим ввода ШК ячейки
	    BCTPARTY    = 7;						// константа - режим ввода ШК партии
	    
	    task_id: string;
		type_id: string;
	    header_id: string;
	    description: string;
		
		curr_PalletBarcode: string;
	
		scanner;
		
	
		constructor() {
			super();
			
			status = false;   // статус - выполняется
	
		}
		
		
		public menu(args) {
			var form = new FormModule.Form();    	
			return form.FormMenu(args);
		}
		
		public formCount(args) {
			var form = new FormModule.Form();    	
			return form.FormCount(args);   				
		}
		
		
		
		public init(){
			main.init();
		}
		
	
	 	public start() {

	 	}


	    public toogle_status(){

            var point = <HTMLElement>document.getElementById("point-status");
            //point.style.display = (point.style.display == "none") ? "block" : "none";
	    }
		
	 	
	 	public task_check() {	 		

            this.toogle_status();

	 		if (status == "false" || status == false ){
	 			return false; 			
	 		}


			this.ajax({
	            type: "POST",
	            url: "/task/check",
	            hidden: true,	                    
	            success: (resp) => {
	            		            	
	    	 		if ((status == "true") || (status == true)){ 			
	    	 			this.application_reload();	    	 			 			
	    	 		}	    	 		
	            	
	            	if (resp && resp["task_id"]){
	            		
	            		var task = new TaskModule.Task();
	            		
	            		task.task_id = resp["task_id"];
	            		task.type_id = resp["type_id"];
	            		task.header_id = resp["header_id"];
	            		task.description = resp["description"];
	            			            		
	            		task.task_new();
	            	}	            		            
	            },
	            error:   () => { }
	                     
	        }); 

	 	}
	 	
	 	
 	
	 	
	    public task_new(){
	    	
	    	status = false;
	    	
	    	this.new_event();
	    	
	    	this.menu({
				
				caption: "Новое задание",
				text:    this.description,
				backgroundColor: 'lightgreen',
				buttons: { 
							"Принять задачу"  : () => { 								
								this.task_apply();
							},
							
							"Отменить"  : () => {	
								this.task_cancel();								
							},
							
				         }

			});
	    }
	 	
	    
	    
	    public task_apply(){
	    	
			this.ajax({
	            type: "POST",
	            url: "/task/apply",
	            data: { 'task_id': this.task_id},	            
	            success: (resp) => {
	            	
	            	
	            	var task:any;
	            	
	            	switch(parseInt(this.type_id))
	            	{
	            		
		    	    	case 1:   /* Сборка */
		                    task = new OrderBatchingModule.OrderBatching();      		                   	
	                   		break;
		    	    	case 11:   /* Сборка Штучного*/
		                    task = new OrderBatchingModule.OrderBatching();      		                   	
	                   		break;	                   		
	                   		
		            	case 3:    /* Размещение */
		            		task = new AllocationModule.Allocation();            	                 	      		                    	                    
		            		break;
                        case 9:    /* Размещение */
		            		task = new AllocationModule.Allocation();
		            		break;
		            		
		            	case 5:   /* Приемка */
		            		task = new AcceptanceModule.Acceptance();
		            		task.message_count = "Введите число коробок на паллете";
		            		break;
		            		
		            	case 6:
		            		task = new MovingModule.Moving();      		 
	                   		break; 
		            	case 7:
		            		task = new MovingModule.Moving();      		 
	                   		break;  	
	                   		
		            	case 10:   /* Приемка сырья */
		            		task = new AcceptanceModule.Acceptance();
		            		task.message_count = "Введите количество упаковок для тары или вес в кг для сырья";
		            		break;	                   
		            		
		    	    	case 12:   /* Сборка Сырья*/
		                    task = new OrderBatchingRawModule.OrderBatchingRaw();      		                   	
	                   		break;	                   		


		    	    	case 13:   /*  Проверка сборки заказа по сырью */
		                    task = new CheckingRawModule.CheckingRaw();
	                   		break;
	            	}

                   	task.task_id   = this.task_id;
                   	task.type_id   = this.type_id;
                   	task.header_id = this.header_id;
                   	task.start();  

	            },
	            error:   () => { 
	            					main.init(); 	 
	            }
	                     
	        }); 
	    	
	    }
	    
	    
	 	
	 	public task_cancel() {	 		
	 		
			this.ajax({
	            type: "POST",
	            url: "/task/cancel",
	            data: { 'task_id': this.task_id},	            
	            success: (resp) => {	            	
	            	main.init();      		            
	            },
	            error:   () => {
	            	main.init();
	            }
	                     
	        }); 

	 	}	 	
	 	
	 	
	    
	    public stop(msg?){
	    
		    this.menu({
				
				caption: "Задание прервано",
				text:    msg,
				buttons: { 
							"Прервать задачу"  : () => { 								
								
								this.abort();

							}
				         }

			});
	    }
	    
		
	    
	    public complete(msg?){
	 	
		    this.menu({
				
				caption: "Задание завершено",
				text:    msg,
				buttons: { 
							"Завершить задачу"  : () => { 								
								
								this.done();

							}
				         }

			});
	    
		
	    }
	    
	    
	    
	    public done(){
	    	

	    	if (this.task_id){	    		
	    	
		    	this.ajax({
		            type: "POST",
		            url: "/task/complete",
		            data: { 'task_id': this.task_id},	            
		            success: () => {	            	
		            	main.init();      		            
		            },
		            error:   () => {
		            	main.init();
		            }
		                     
		        }); 		    	
	    	
	    	} 
	    	else{
	    		main.init();
	    	}
	    	
		    
	    
	    }
	    
	    
	    public abort(){
	    	

	    	if (this.task_id){	    		
	    	
		    	this.ajax({
		            type: "POST",
		            url: "/task/abort",
		            data: { 'task_id': this.task_id},	            
		            success: () => {	            	
		            	main.init();      		            
		            },
		            error:   () => {
		            	main.init();
		            }
		                     
		        }); 		    	
	    	
	    	} 
	    	else{
	    		main.init();
	    	}
	    			  
	    
	    }
	    	
	    	    
	    
	    
	    public formDelivery(settings) {		
	    	
	    	settings.type = this.BCTDELIVERY;
	    	settings.id = "FormBarcodeUser";
	    	
	    	if (!settings.text){
	    		settings.text = "Ввод штрих-кода сборочного";
	    	}
	    	
	    	this.formBarcode(settings);			
	    }
	    
	    
	    
	    
	    public formUser(settings) {		
	    	
	    	settings.type = this.BCTUSER;
	    	settings.id = "FormBarcodeUser";
	    	settings.backgroundColor = "#FF6";
	    	
	    	if (!settings.text){
	    		settings.text = "Ввод штрих-кода пользователя";
	    	}
	    	
	    	this.formBarcode(settings);			
	    }
	    
	    
	    
	    public formCell(settings) {		
	    	
	    	//settings.type = this.BCTCELL;
	    	settings.id = "FormBarcodeCell";
	    	
	    	if (!settings.caption){
	    		settings.caption = "Ввод штрих-кода ячейки";
	    	}
	    	
	    	this.formBarcode(settings);			
	    }
	    
	    
	    public formPallet(settings) {		
	    	
	    	settings.type = this.BCTPALLET;
	    	settings.id = "FormBarcodePallet";
	    	
	    	if (!settings.text){
	    		settings.text = "Ввод штрих-кода паллеты";
	    	}
	    	
	    	this.formBarcode(settings);		
	    }
	    
	    
	    public formParty(settings) {		
	    	
	    	settings.type = this.BCTPARTY;
	    	settings.id = "FormBarcodeParty";
	    	
	    	if (!settings.text){
	    		settings.text = "Ввод штрих-кода партии";
	    	}
	    	
	    	this.formBarcode(settings);			
	    }
	    
	    
	    
	    
	    public formBarcode(settings) {		
	    	
	    	var form = new FormModule.Form();
	 	    	
			
	    	var callback_apply  = settings.apply;
	    	var callback_cancel = settings.cancel;
	    	
	    	
	    	settings.ApplyOnScan = true;
	    		    	
	    	
	    	settings.apply = (barcode) => {
	    		
	    		this.barcode.type = settings.type;
		    	this.barcode.expected = settings.expected;
		    			    	
				if (this.barcode.set(barcode)){

					callback_apply(this.barcode.value);
				}			
				else{
					this.scanner = form.scanner;		
					this.scanner.init();
				}
				
				
	    	}
	    	
	    		    	
	    	settings.cancel = () => { 
						 				if (callback_cancel){
						 					callback_cancel();
						 				}
						 				else{
						 					this.stop();
						 				}
	    	}
	    	
	    	form.FormBarcode(settings);
	    	
	    	/*
			form.FormBarcode({
		
				caption: settings.caption,
				backgroundColor: settings.backgroundColor,
				id:   settings.id,
				text: settings.text,
			    ApplyOnScan: true,
			    apply: (barcode) => {
			    	

			    	this.barcode.type = settings.type;
			    	this.barcode.expected = settings.expected;
			    			    	
					if (this.barcode.set(barcode)){

						settings.apply(this.barcode.value);
					}			
					else{
						this.scanner = form.scanner;		
						this.scanner.init();
					}
										
			    },
			    cancel: () => { 
			    				if (settings.cancel){
			    					settings.cancel();
			    				}
			    				else{
			    					this.stop();
			    				}
			    				
			    				
			    				},  // возврат на начальную форму
			});
			*/
			
			
			
	    }
	    
	    
		
	}

}