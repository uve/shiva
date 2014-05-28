/// <reference path="orderbatching.ts" />

module OrderBatchingRawModule {
	
	export class OrderBatchingRaw extends OrderBatchingModule.OrderBatching{
	
		public class_name = "OrderBatchingRaw";
		
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
			    		this.get_cell();
			    } 
			});
			
	    }
	    
	       
	    
	
	    
	    
	    /**
	     *   Ввод количества погруженных коробок
	     *   
	     */    
	    public getCount() {

	        	
	    	var msg = "Необходимо погрузить сырья в количесте <b>" + this.value + "</b></br>Введите количество погруженного сырья";      	    	    	
	
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
				text:    "С адреса: "+ this.cell_name + "</br>взято сырья:" + value,
				buttons: { 
							"Продолжить"  : () => { 
												     this.value = value;
							   						 this.scan_party();  ///  отличие от обычной сборки
							},
							
							"Вернуться"   : () => {	 this.getCount();
							}
				         }
	
			});
				
		}
	    
	    
	    
	    public scan_party() {
	    	

	    	this.formParty({

				text: "Введите штрих-код <b>ПАРТИИ</b> сырья",
			    apply: (value) => {
			    	
			    		this.party_id = value;

						this.scan_extra_party();								
			    },
			    cancel: () => { 
			    		/*this.getConfirm();*/
			    	    this.stop();
			    } 
			});
			
	    }
	
	    
	    public scan_extra_party() {
	    	

	    	this.formParty({

				text: "Введите штрих-код <b>ПОДПАРТИИ</b> сырья",
			    apply: (value) => {
			    	
			    		this.extra_party_id = value;

						this.ok_cell();								
			    },
			    cancel: () => { 
			    		this.scan_party();
			    } 
			});
			
	    }
	    
	    
		    
		public add_again(){   
			
			this.menu({
				
				caption: "Подтверждение",
				text:    "Вы можете продолжить сборку сырья, либо взять ещё такое же сырье из этой же ячейки",
				buttons: { 
							"Продолжить"  : () => { 
														this.get_cell();
							},
							
							"Взять ещё"   : () => {	 this.getCount();
							},

                            "Закончить эту паллету"   : () => {	 this.end_pallet_raw();
                            }
				         }
	
			});
			
		}

		public end_pallet_raw(){


			this.ajax({
        	            type: "POST",
        	            url: "/mbl/batching/end_pallet_raw",
        	            data: {
        	            	    pallet_id: this.pallet_id
        	                   },
        	            success: (resp) => {


                              this.target_id   = resp.target_id;
                              this.target_name = resp.target_name;

                              this.scan_target_raw();

        	            },
        	            error: () => { this.add_again(); }
        	        });


		}



        public scan_target_raw() {

            this.formBarcode({

                caption: "Ввод штрих-кода целевой ячейки",
                text:    "Поместить на адрес: " + this.target_name,
                expected: this.target_id,
                apply: (value) => {
                                    this.target_id = value;
                                    this.setPalletToDelivery_raw();
                },
                cancel: () => { this.add_again(); }
            });

        }




	    public setPalletToDelivery_raw()
		{

			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/set_pallet",
	            data: {
	            	    pallet_id: this.pallet_id,
	            	    target_id: this.target_id
	                   },
	            success: (resp) => {

	            	this.getPallet();

	            },
	            error: () => { this.get_cell(); }
	        });

		}



	
	 
	   
	}
}