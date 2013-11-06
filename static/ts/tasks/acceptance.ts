module AcceptanceModule {
	
	export class Acceptance extends TaskModule.Task{
	
		public class_name = "Acceptance";
			
		
		
		is_btk: number;      //Режим приемки: 0 - обычная приемка, 1 - режим БТК
		
		is_party_new: boolean;
		
		cell_id:   string;		
		party_id:  string;
		pallet_id: string;
						
		count:        string;  //Введное количество коробок
		count_all:    string;  //Общее количество штук на паллета, для БТК с неполными коробками
		count_inbox:  string;  //Количество штук в 1 коробке
		
		count_input:  string;  //Количество уже принятых штук терминалом
		count_total:  string;  //Общее количество штук, которые надо принять
		
		caption: string;
						
		message_count: string;
		
		
		all_products: string;
		product_id:   string;
		product_name: string;
		party_number: string;
		goden_do:     string;
		
		
		
	    public start() {
	    	    	
	    	 super.start();
	        	    	
	    	 this.is_btk = 0;	    	 
	    	 this.is_party_new = true;
	    	 
	    	 this.count_input = "0";
	    	 this.count_total = "?";
	    	 
	    	 this.get_type();
	    	
	    	 //this.get_all_products();
	    	 
	    }    

		
	    
	    public get_type(){
		    
	    	
	    	this.caption = "Принято " + this.count_input + " штук из " + this.count_total;
	    	

			this.menu({
				
				caption: this.caption,
				
				buttons: { 
	
							"Принять паллету на склад"  : () => { 												
								
								this.is_btk = 0;
								this.get_count_total(); 								
							},

							"Принять паллету в БТК"  : () => {
								
								this.is_btk = 1;
								this.get_count_total(); 								
								
							},
							
							"Завершить приемку"   : () => { 								

								this.end_header();				
							}
			
			
				}
			});
	    	
	    	
	    }
	    
	    
	    
	    
	    public get_count_total(){
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/get_count_total",     
	 	        data: {   
	 	        		header_id:  this.header_id,	 	        			        		
	 	        },             	 	        
	 	        success: (resp) => {
	 	        					this.count_input = resp.count_input;
	 	        					this.count_total = resp.count_total;
	 	        					
	 	        					
	 	        					this.caption = "Принято " + this.count_input + " штук из " + this.count_total;
	 	        					
	 	        					
		 	   				    	if ( this.is_btk != 1 ){
		 	        					/*
		 	        					 *  Удалять чтобы при приемке в БТК спрашивать ячейку и паллету только один раз
		 	        					 */
		 	        	
		 	        					delete this.cell_id;
		 	        					delete this.pallet_id;
		 					    	}
		 	   				    	
		 	   				    	
		 	   				    	
									if (this.cell_id && this.pallet_id){
										this.scan_party();
									}
									else{
										this.scan_cell();
									}
									
									
	 	        },
	            error:   () => { 
	            					this.stop();
	            } 
	 	    });
	    }
	    
	    
	    
	    

	    

	    
	    

	    
	    
	    public scan_cell() {
	    
			this.formCell({		
							caption: this.caption, 
							text:    "Ввод штрих-кода ячейки приёмки",
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.check_cell();
						    },
						    cancel: () => { 
						    		this.get_type();
						    }
						 });
	    }
	    
	    
	    
    	 //  проверка приёмочной ячейки - можно ли в неё принимать	    
	    public check_cell(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/check_cell",     
	 	        data: {   
	 	        			cell_id:   this.cell_id,
	 	        			header_id: this.header_id
	 	        },             	 	        
	 	        success: () => {
	 	        					this.scan_pallet();
	 	        },
	            error:   () => { this.scan_cell(); } 
	 	    });
	    	
	    }
	    

	    
	    public scan_pallet() {
		    
			this.formPallet({			
						    apply: (value) => {
							    	this.pallet_id = value;
							    	this.check_pallet();
						    },
						    cancel: () => { 
						    		this.scan_cell();
						    }
						 });
	    }
	    
	    
	    
	    public check_pallet(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/check_pallet",     
	 	        data: {   
	 	        		pallet_id:   this.pallet_id,
	 	        		header_id:   this.header_id
	 	        },             	 	        
	 	        success: () => {
	 	        					this.scan_party();
	 	        },
	            error:   () => { 
	            					this.scan_cell(); 
	            } 
	 	    });
	    	
	    }
	    
	    
	    
	    public scan_party() {
		    
			this.formParty({			
						    apply: (value) => {
							    	this.party_id = value;
							    	this.check_party();
						    },
						    cancel: () => { 
						    		this.get_type();
						    }
						 });
	    }
	    
	    
	    
	    
	    public check_party(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/check_party",     
	 	        data: {   
	 	        		party_id:   this.party_id,
	 	        		header_id:  this.header_id
	 	        },             	 	        
	 	        success: (resp) => {
	 	        	
	 	        		if (resp["count_inbox"]){
	 	        				this.count_inbox  = resp["count_inbox"];		
	 	        				this.is_party_new = false;
	 	        				
	 	        				this.get_count();	 	        				
	 	        		}
	 	        		else if (this.is_btk == 1){
	 	        				this.stop("Приёмка новой партии невозможна в режиме БТК");
	 	        		}
	 	        		else {
	 	        				this.get_all_products();
	 	        		}

	 	        		
	 	        },
	            error:   () => { this.scan_party(); } 
	 	    });
	    	
	    }
	    
	    
	    
	    public get_all_products(){
	    	//this.stop("Выбор новой партии не релизован, обратитесь к разработчикам");
	    	
	    	
	    	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/get_all_products",     
	 	        data: {   
	 	        		header_id:  this.header_id
	 	        },             	 	        
	 	        success: (resp) => {
	 	        	
	 	        	this.all_products = resp; 
	 	        	this.showCatalog();
	 	        	
	 	        },
	            error:   () => { this.stop(); } 
	 	    });
	    }

	    
	    
	    public showCatalog() {
	    	
			var form = new FormModule.Form();
			
			form.FormMenu({

				caption: "Выберите продукт",
				options: this.all_products,
				buttons: { 
							"Продолжить"  : () => {
								
									this.product_id   = form.value;
									this.product_name = form.text;					
									
									this.getConfirmProduct();
							},
							
							"Вернуться"   : () => { 
														this.check_party();											
												  }
				         }
	
			});  		
	
	    }
	    
	    
	    /**
	     * Подтвердить выбранный продукт
	     * 
	     */
	    public getConfirmProduct(){
	    	
	    	
	    	this.menu({
				
				caption: "Подтверждение продукта",
				text:    this.product_name,
				buttons: { 
							"Потвердить"  : () => { 
	
								this.getPartyNumber();
							},
							
							"Вернуться"   : () => { this.showCatalog(); }
				         }
	
			});
	    	
	
	    }
	    
	    

	    public getPartyNumber(){
	    	
	    	var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Введите обозначение партии",
				input: true,
				buttons: { 
							"Продолжить"  : () => { 
									
									this.party_number = form.value;									
									
									this.getDateValid();
							},
							
							"Вернуться"   : () => { this.getConfirmProduct(); }
				         }
	
			}); 
	    	
	    }
	    
	    
	    
	    
	    public getDateValid(){
	    	
	    	var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Введите срок годности",
				date: true,
				buttons: { 
							"Продолжить"  : () => { 
								
								this.goden_do = form.get_timestamp();
				
								this.getCountInBox();
							},
							
							"Вернуться"   : () => {
								this.getPartyNumber();
							}
				         }
	
			}); 
	    	
	    }
	    
	    
	    
	    /**
	     *   Ввод количества товара в коробоке
	     *   
	     */    
	    public getCountInBox() {
	 
	    	
	    	/*
	    	 * Если принимаем сырье, то не спрашивать количество в упаковке, а отправлять 1
	    	 */
	    	if (parseInt(this.type_id) == 10){
	    	
	    		this.count_inbox = "1";
	    		this.get_count();
	    		return true;
	    	}
	    	
	    	
			var form = new FormModule.Form();
			
			form.FormCount({
			
			
					text: "Введите количество в упаковке",					
					default_value: this.count_inbox,								
				    apply: (value) => {
				    	
				    	this.count_inbox = value;
				    	this.get_count();
				    	
					},
					cancel: () => { 
									
									this.getDateValid();
									
					}								
			});    		
	
	    }
	    
	    
	    
	    public get_count(){

	    	this.formCount({
			
					text: this.message_count,							
				    apply: (value) => {
				    	
				    	this.count = value;
				   	
				    	
				    	
				    	if (this.is_btk){
				    		// переход на форму ввода общего числа штук
				    		this.get_count_all();
				    	}
				    	else if (this.is_party_new){
				    						    						    		
				    		//this.stop("Ввод количества для новой партии закрыт, обратитесь к разработчикам");
				    		delete this.count_all;
				    		
				    		this.addnewpallet();
				    		
				     	} else {
				     		// Старая партия
				     		// переход на приемку след. паллеты - на форму ввода ШК ячейки
				     		delete this.count_all;
				     		this.addnewpallet_oldparty();
				     	}
				    	 				    					    	
					},
					cancel: () => { 
									
						this.getCountInBox();								
					}								
			});    		
	
	    }
		
	    	    
	    
	    public get_count_all(){
	    	
	    	this.formCount({
				
	    		caption: "Режим БТК",
				text: "Введите общее количество штук",												
			    apply: (value) => {
			    	
			    	this.count_all = value;		    	
		     		this.addnewpallet_oldparty();			    		
				},
				cancel: () => { 
								
					this.get_type();								
				}								
	    	});    		
	    	
	    }
	    
	    
	    
	    public addnewpallet(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/addnewpallet",     
	 	        data: {   
	 	        		header_id:  this.header_id,	 	        		
	 	        		pallet_id:  this.pallet_id,
	 	        		party_id:   this.party_id,
	 	        		cell_id:    this.cell_id,
	 	        		count:      this.count,	 	     
	 	        		is_btk:     this.is_btk,
	 	        		count_inbox: this.count_inbox,
	 	        		
		 	       		product_id:   this.product_id,
		 	       		party_number: this.party_number,
		 	       		goden_do:     this.goden_do,
	 	        },             	 	        
	 	        success: () => {
	 	        					
	 	        					this.get_count_total();
	 	        },
	            error:   () => { 
	            					this.get_count();
	            } 
	 	    });
	    	
	    }
	    
	    
	    
	    public addnewpallet_oldparty(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/addnewpallet_oldparty",     
	 	        data: {   
	 	        		header_id:  this.header_id,	 	        		
	 	        		pallet_id:  this.pallet_id,
	 	        		party_id:   this.party_id,
	 	        		cell_id:    this.cell_id,
	 	        		count:      this.count,	 	     
	 	        		is_btk:     this.is_btk,
	 	        		count_all:  this.count_all,
	 	        },             	 	        
	 	        success: () => {
	 	        					this.get_count_total();
	 	        },
	            error:   () => { 
	            					this.get_count();
	            } 
	 	    });
	    	
	    }
	    
	    

	    

	    
	    
	    
	    public end_header(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/acception/end_header",     
	 	        data: {   
	 	        			header_id:   this.header_id  
	 	        },             	 	        
	 	        success: () => {
	 	        					this.complete("Приемка завершена");
	 	        },
	            error:   () => { this.stop(); } 
	 	    });
	    	
	    }
	   
	}
}