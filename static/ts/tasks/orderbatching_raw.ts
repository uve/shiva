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
		

		value_taken    : string;
		value		   : string;
		count 	 	   : string;
		count_total    : string;
		
		product_name   : string;
		packlist_id    : string;
		
		scanner;
		



	    public printMarks()
		{
            this.get_cell();
		}


	    /**
	     *   Ввод ШК ячейки с товаром из которой будет браться товар
	     */
	    public scan_cell() {
	    	
	    	this.party_id = "";
	    	
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

												     this.value_taken = value;


                                                     if ( parseFloat(this.value_taken) == 0 ){

                                                            this.block_cell();
                                                            return;
                                                     }



												     if (this.party_id != ""){
												    	 this.scan_extra_party();
												     }
												     else{
												    	 this.scan_party();  ///  отличие от обычной сборки
												     }
							},
							
							"Вернуться"   : () => {	 this.getCount();  }
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
	    	

	    	this.formExtraParty({

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





        public ok_cell()
		{


			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/ok_cell",
	            data: {
		            		pallet_id: 	 this.pallet_id,
			                cell_id:     this.cell_id,
			                count:       this.value_taken,

			                party_id:        this.party_id,
			                extra_party_id : this.extra_party_id,
			                packlist_id    : this.packlist_id
			    },
	            success: () => {

                                    /* уменьшить количество взятых коробок*/

	                                this.value = (parseFloat(this.value)  - parseFloat(this.value_taken)).toString();
	                                this.add_again();
	            },
	            error:   () => { this.get_cell(); }

	        });

		}



        public add_again(){

                if ( parseFloat(this.value) > 0 ){

                    this.menu_repeat();
                    return;
                }
                else{

                    this.next_pallet();
                    return;
                }

	    
	    }





        public next_pallet() {



            this.menu({

                caption: "Подтверждение",
                buttons: {
                            "Cледующая позиция"  : () => {

                                /* Получить новую ячейку для сборки*/
                                 this.get_cell();
                            },



                            "Закончить эту паллету"   : () => {

                                /* Если на паллете закончилось место, то берем новую паллету */
                                this.end_pallet_raw();
                            }


                         }

            });

        }


		    
		public menu_repeat(){



			this.menu({
				
				caption: "Подтверждение",
				/*text:    "Вы можете продолжить сборку сырья, либо взять ещё такое же сырье из этой же ячейки",*/
				buttons: { 

							"Взять такое же кол-во"  : () => {	
								
								/* Чтобы взять такую же коробку с таким же количеством сырья
								 * и заново не сканировать партии
								 * то перебрасываем сразу на сканировании подпартии
								 */
							    this.scan_extra_party();
							},

							
							"Взять другое кол-во"   : () => {	
								
								/* В случае если мы хотим взять из той же ячейки коробку с другим количеством,
								 * то заново просим ввести количество*/
								this.getCount();
							},
							

                            
				         }
	
			});
			
		}
		
		
		public block_cell(){
			
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/batching/ok_cell",
	            data: { 
		            		pallet_id: 	 this.pallet_id,
			                cell_id:     this.cell_id,
			                count:       "0", 
			                
			                party_id:        this.party_id,
			                extra_party_id : this.extra_party_id,
			                packlist_id    : this.packlist_id 
			    },	                    
	            success: () => { this.get_cell(); },
	            error:   () => { this.get_cell(); }
	                     
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