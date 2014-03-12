module OrderBatchingModule {
	
	export class OrderBatching extends TaskModule.Task{
	
		public class_name = "OrderBatching";
		
		OrderPart: string;
	
		pallet_id      : string;
	
		cell_id   	   : string;
		cell_name 	   : string;
		
		target_id      : string;
		target_name    : string;
		
		
		party_id       : string;
		extra_party_id : string;
		
		value		   : string;
		count 	 	   : string;
		count_total    : string;
		
		product_name   : string;
		packlist_id    : string;
		
		scanner;
		
	    public start() {
	    	    	
	    	 super.start();
	    	 
	         this.getPallet();       
	    }    
		
	    
	
		/**
		 *	сканирование ШК паллеты для сборки 
		 */	 
		public getPallet ()  {
			
	
			this.formPallet({					
			    apply: (value) => {
				    	this.pallet_id = value;
				    	this.bind_pallet();
			    },
			    cancel: () => { this.stop(); }
			 });					
			
		}
	
		
		
		public bind_pallet()  {
				     			
			this.ajax({ 	
							type: "POST",
							url: "/mbl/batching/bind_pallet",
							data: { 
										task_id:    this.task_id,			
										pallet_id:  this.pallet_id,
																		 
									},
							success: () => {							
									
									this.printMarks();
							},
							error: () => { this.getPallet(); }
						});
		 
		}
	
			
		
		//-----------------------------------------------------------------------------
		//Отправить к бригадиру
		//-----------------------------------------------------------------------------
	    public printMarks()
		{		    	
	
			this.menu({
		
				caption: "Печать этикеток",
				text: "Пожалуйста, распечатайте партионные наклейки в Шиве, затем нажмите кнопку 'Приступить к сборке'",
				buttons: { 
							"Приступить к сборке"  : () => { this.get_cell(); },
							"Отмена"  : () => { this.stop(); },
				         }
	
			});
	    	
	
		}	
	
	    
	    /**
	     *  вызов shiva.getCellValFromPackList()
	     */
	    public get_cell()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/get_cell",
	            data: {
	                    header_id: this.header_id,
	                    pallet_id: this.pallet_id, 
	                   },
	                    
	            success: (resp) => {
			        	
	            	 		this.value		  = resp.value;         // Сколько нужно взять
	            	 		this.count	      = resp.count;         // Сколько уже собрано
	            	 		this.count_total  = resp.count_total;   // Сколько всего нужно собрать
	            	 		this.product_name = resp.product_name;
	            	 		this.packlist_id  = resp.packlist_id;
		        	  
	            	 		
			        		if (resp["cell_id"]){
			        			
					        	  this.cell_id   = resp.cell_id;
					        	  this.cell_name = resp.cell_name;		
	        		
				        		  this.scan_cell();			        			
			        		}
			        		else if (resp["target_id"]){
			        			
					        	  this.target_id   = resp.target_id;
					        	  this.target_name = resp.target_name;		
	        		
				        		  this.scan_target();
			        		}			        	
			        		else{
			        			 this.complete("Пожалуйста, отвезите паллету в зону сборки и нажмите кнопку [завершить задачу]");			        		  				        		 
			        		}
			        			        	  				               		 
	               	    
	            },
				error: () => {
								this.printMarks(); 
				}
	        }); 
	
		}
	
	    
	    
	    /**
	     *   Ввод ШК ячейки с товаром из которой будет браться товар
	     */
	    public scan_cell() {
	    	
	    	var msg = "Взять коробок: <b>" + this.value + "</b></br>C адреса: " + this.cell_name + "</br>" + this.product_name;
	    	
	    	this.formCell({
		
				caption: "собрано " + this.count + " позиций из " + this.count_total,
				text: msg,
				expected: this.cell_id,
			    apply: (value) => {
			    	
			    		this.cell_id = value;

						this.getCount();								
			    },
			    cancel: () => { 
			    		this.stop();
			    } 
			});
			
	    }
	    
	       
	    
	    
	    /**
	     *   Target Cell
	     *   Ввод ШК ячейки с товаром из которой будет браться товар
	     */
	    public scan_target() {
	    	
	    	this.formBarcode({
		
				caption: "Ввод штрих-кода целевой ячейки",
				text:    "Поместить на адрес: " + this.target_name,
				expected: this.target_id,
			    apply: (value) => {			    	
			    					this.target_id = value;
			    					this.setPalletToDelivery(); 					
			    },
			    cancel: () => { this.get_cell(); }
			});
			
	    }    
	    
	    
	    /**
	     *   Ввод количества погруженных коробок
	     *   
	     */    
	    public getCount() {

	        	
	    	var msg = "Необходимо погрузить " + this.value + " коробок.</br>Введите число погруженных коробок";      	    	    	
	
			this.formCount({
			
					text: msg,					
					apply: (value) => {
				    	
						
				    	this.getConfirm(value);
					},
					cancel: ()=>{ this.scan_cell(); }// переход обратно - на ввод ШК ячейки									
			});    	
			
	
	    }
	    
	    
	    
	    
	    
	    /**
	     *   Подтверждение количества погруженных коробок
	     *   
	     */   
	    public getConfirm(value)
		{
	
			this.menu({
				
				caption: "Подтверждение",
				text:    "С адреса: "+ this.cell_name + "</br>взято коробок:" + value,
				buttons: { 
							"Продолжить"  : () => { 
													 this.value = value;
							   						 this.ok_cell();
							},
							
							"Вернуться"   : () => {	 this.getCount();
							}
				         }
	
			});
				
		}
	    
	    
	    
	    public ok_cell()
		{		    	
	
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/ok_cell",
	            data: { 
		            		pallet_id: 	 this.pallet_id,
			                cell_id:     this.cell_id,
			                count:       this.value, 
			                
			                party_id:        this.party_id,
			                extra_party_id : this.extra_party_id,
			                packlist_id    : this.packlist_id 
			    },	                    
	            success: () => { this.add_again(); },
	            error:   () => { this.get_cell(); }
	                     
	        }); 
	
		}
	    
	
	    /*
	     * Вернуться и взять ещё
	     */
	    public add_again(){   
	    	this.get_cell();
	    }
	
	    
	    
	    
	    public setPalletToDelivery()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/set_pallet",
	            data: {                     
	            	    pallet_id: this.pallet_id, 
	            	    target_id: this.target_id
	                   },	                    
	            success: (resp) => {
	            	
	            	this.complete("Задание окончено, нажмите кнопку [завершить задачу]");
	          	  		
	            },
	            error: () => { this.get_cell(); }
	        });
	
		}    
	   
	}
}