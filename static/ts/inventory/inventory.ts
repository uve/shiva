module InventoryModule {
		
	declare var main;
	declare var CURRENT_RC;
	
	export class Inventory extends TaskModule.Task{
	
		public class_name = "Inventory";
		
		
		caption		 : string;
		
		delivery_id  : string;
		cell_id      : string;
		party_id     : string;
		pallet_id    : string;
		
		product_id   : string;
		product_code : string;
		product_name : string;
		
						
		count		 : number;
		count_inbox  : number;
						
		plus         : number;
		
		all_products = [];
		all_party_status = [];
		
		party_status : string;
		party_number : string;
		
		goden_do: string;
	
			
	 	constructor() {
	 		
	 		super();
	 		
	 		this.caption = "Инвентаризация";
	 		
	 		
	 		this.init();
			
	 		//this.getDateValid();
	 	}
	 	
	 	
	 	public init() {

	 		
			var buttons = { 		
					
					"Проверка ячейки"  : () => {	
												var task = new GetCellInfoModule.GetCellInfo();
					},		
					
					
					"Привязка партии"  : () => {	
													this.plus = 0;
													this.start();    	
												},		
					"Добавление партии" : () => {
													this.plus = 1;
													this.start();		
					},			
					"Очистка ячейки"  : () => {												
													this.emptyCell(); 
					},			
					"Взять из ячейки"  : () => {
													var task = new GetFromCellModule.GetFromCell();
					},	
					"Перемещение ячейки" : () => {				
													var task = new MovingPalletModule.MovingPallet();
					},							
					"Заблокировать ячейку"  : () => {				
													this.blockCell(); 
					},
					"Разблокировать ячейку" : () => {	
													this.unblockCell(); 
					},									
					"Назад"  : () => {
										this.stop();
					}
					
					
		         };
				
			
			
			
			if (CURRENT_RC == 6){
				
				var msk_buttons = {
							
							"Прием ГП с производства"  : () => {
								this.plus = 2;
								this.start(); 						
							},			
							"Добавление ГП с производства" : () => {								
								this.plus = 3;
								this.start();							
							},			
							"Отгрузка клиенту"  : () => {
								var task = new OutputProductModule.OutputProduct(); 
							},				
							"Приемка упаковки"  : () => {
								var task = new InputProductModule.InputProduct(); 
							},		
							"Списание с производства"  : () => { 	
								var task = new ClearTovarModule.ClearTovar(); 					
							}
						};
		
						
				buttons = this.extend(msk_buttons, buttons);
			}
			
			
			
			
			if (CURRENT_RC == 1){
				
				var rc_buttons = {
							
							"Отправка паллеты" : () => {  /* RC */
								
								this.set_pallet_delivery();
							},				

							"Перемещение с штучного" : () => {  /* RC */
								
								this.send_from_item_to_delivery();
							},				

							
						};
		
						
				buttons = this.extend(rc_buttons, buttons);
			}
			
			
			var form = new FormModule.Form();
			form.FormMenu({				
							text: "Выберите режим",				
							buttons: buttons	
			});
			
								
			
	 	}
	 	
	 	
	 	 	
		
		
	    public start() {
	    	    	
	    	 super.start();    	 
	    	 
	    	 
			 this.cell_id      = "";
			 this.party_id     = "";
			 this.pallet_id    = "";
			
			 this.product_id   = "";
			 this.product_code = "";
			 this.product_name = "";
			
			 this.party_number = "";
			
			 this.count_inbox  = 0;
			 this.count  = 0;
		 
			 if (!this.plus){
				 this.plus = 0; // Признак привязки.
			 }
	          
	    	 this.scanCell(); 
	    	 	    	 
	    	 
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
							    	this.checkParty();
						    },
						    cancel: () => { this.scanPallet(); }
						 });
	    }
	    
		
		
		
	    /**
	     * Проверка новая партия или старая
	     * 
	     */
	    public checkParty()
		{		    	
	
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/checkparty",
	            data: {
	            			party_id:  this.party_id
	            	  },                    
	            success: (resp) => { 
	            	
	            				if (resp["is_new"]){
	            					/****
	            					 *  Ввод типа партии, товара, срока годности  и т.д.
	            					 */
	            					
	            					if (!this.product_id){
	            						this.getCode();
	            					}
	            					else{
	            						this.getCountInBox();
	            					}
	            					
	            					
	            				}
	            				else{
	            					this.getCount();
	            				}
	            					
	            					
	            },
	            error:   () => { this.scanParty(); } 
	                     
	        }); 
		}
	
	    
	    
	    
	    public getCode(){
	    	
	    	
	    	var msg = "Введите код товара";      	    	    	
	
			var form = new FormModule.Form();
			
			form.FormCount({
			
					caption: this.caption,
					text: msg,
					
					default_value: parseInt(this.product_code),
					min_value: 1,
								
				    apply: (value) => {
				    		this.getProduct(value);  	
					},
					cancel: () => { this.scanParty(); }								
			});    		
	    	
	    }
		
	    
	    
	    /**
	     * Поиск продукта по базе
	     * 
	     */
	    public getProduct(value : string)
		{		    	
	
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/get_product",
	            data: {
	            			product_code:  value
	            	  },                    
	            success: (resp) => { 
	            					
	            					if (resp.length == 1){
	            						this.product_id   = resp[0]["id"];
	                					this.product_code = resp[0]["code"];
	                					this.product_name = resp[0]["name"];
	                					this.getConfirmProduct();		
	            					}
	            					else{
	            						
	            						this.all_products = resp;
	                					this.showCatalog();
	            					}
	            						
	            },
	            error:   () => { this.getCode(); } 
	                     
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
													this.getCode();												
												  }
				         }
	
			});  		
	
	    }
	    
	    
	    
	    /**
	     * Подтвердить выбранный продукт
	     * 
	     */
	    public getConfirmProduct(){
	    	
	    	
	    	var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Подтверждение продукта",
				text:    this.product_name,
				buttons: { 
							"Потвердить"  : () => { 
	
								this.getCountInBox();
							},
							
							"Вернуться"   : () => { this.getCode(); }
				         }
	
			});
	    	
	
	    }
	    
	    
	    
	    
	    
		 /**
	     *   Ввод количества товара в коробоке
	     *   
	     */    
	    public getCountInBox() {
	 
			var form = new FormModule.Form();
			
			form.FormCount({
			
					caption: this.caption,
					text: "Введите количество товара В КОРОБКЕ (для сырья в упаковке)",					
					default_value: this.count_inbox,								
				    apply: (value) => {
				    	
				    	this.count_inbox = value;
				    	//this.getCount();
				    	
				    	this.getDateValid();
					},
					cancel: () => { 
									
									this.getConfirmProduct();
									
					}								
			});    		
	
	    }
	    
	    
	    public getDateValid(){
	    	
	    	//this.getPartyStatus();

	    	var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Введите срок годности",
				date: true,
				buttons: { 
							"Продолжить"  : () => { 
								
								this.goden_do = form.get_timestamp();
				
								//this.getPartyStatus();
								this.getCount();
							},
							
							"Вернуться"   : () => {
								this.getPartyNumber();
							}
				         }
	
			}); 
	    	
	    }
	
	    
	    
		
		 /**
	     *   Ввод количества коробок
	     *   
	     */    
	    public getCount() {
	    	
	    	//this.count = 5;
	        	
	    	var msg = "Введите количество КОРОБОК или всего кг для сырья";      	    	    	
	
			var form = new FormModule.Form();
			
			form.FormCount({
			
					caption: this.caption,
					text: msg,
									
				    apply: (value) => {
				    	
				    	this.count = value;
				    	this.getPartyNumber();
					},
					cancel: () => { 
						
						if (this.count_inbox){
							this.getCountInBox();
						}
						else{
							this.scanParty(); 
						}
					
					
					}// переход обратно - на ввод ШК ячейки									
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
									
									//this.getDateValid();
									this.getPartyStatus();

							},
							
							"Вернуться"   : () => { this.getCount(); }
				         }
	
			}); 
	    	
	    }
	    
	    

	    
	    
	    
	    
	    public getPartyStatus()
		{	
			
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/all_party_status",                    
	            success: (resp) => { 	            					
	            						this.all_party_status = resp;
	                					this.setPartyStatus();	            					
	            						
	            },
	            error:   () => { 
	            					this.setParty(); 
	            				} 
	                     
	        }); 
		}
	    
	    
	    
	    public setPartyStatus() {
	    	
			var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Выберите статус партии",
				options: this.all_party_status,
				buttons: { 
							"Выбрать"  : () => {
								
									this.party_status = form.value;												
									
									this.setParty();
							},
							
							"Пропустить" : () => { 
												  	this.setParty();												
												  }
				         }
	
			});  		
	
	    }
	    
	    
	    
	    
	    public setParty()
		{		    	
	
			/*
		    	pPallet in integer,
		    	pParty in integer,
		        pTovar in integer,
		        pInBox in integer,
		        pDataDo in date,
		        pNum varchar2,
		        pCell in integer,
		        pVal in float,
		        pPlus in integer,
		        pRet out varchar2
	        */
	        
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/setparty",
	            data: {
	            			cell_id      : this.cell_id,
	            			pallet_id    : this.pallet_id,
	            			party_id     : this.party_id,
	            			product_id   : this.product_id,
	            			party_number : this.party_number,
	            			party_status : this.party_status,
	            			count_inbox  : this.count_inbox,
	            			count   	 : this.count,
	            	        plus    	 : this.plus,
	            	        goden_do   	 : this.goden_do,
	            			
	            	  },                    
	            success: () => { this.chooseType(); },
	            error:   () => { this.getCount(); }
	                     
	        }); 
		}
	    
	    
	    
	    public chooseType(){
	    	
	    	var msg = "Ячейка: " + this.cell_id;
	    	
	    	
			var form = new FormModule.Form();
			
			form.FormMenu({
				
				text: msg,
				buttons: { 
							"Добавить такой же товар"  : () => { 
								
									
								this.count = 0;
								this.count_inbox = 0;
								
								this.plus = 1;	
								this.scanParty();
							},
							"Добавить ДРУГОЙ товар"  : () => { 
								
								this.product_id = "";
								this.product_code = "";
								this.product_name = "";
								
								this.count = 0;
								this.count_inbox = 0;
								
								this.plus = 1;												
								this.scanParty();
							},
							
							"Завершить задачу"   : () => { this.complete(); }
				}
			}); 
	    	
	    }
	    
	    
	
	    
	    /**
	     *   Очистка ячейки
	     */
	    public emptyCell() {
	    	
				this.formCell({					
				    apply: (value) => {
					    	this.cell_id = value;
					    	this.setEmptyCell();
				    },
				    cancel: () => { this.stop(); }
				 });
			
	    }
	    
	    
	    
	    public setEmptyCell()
		{		    	
	
	        
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/empty_cell",
	            data: {
	            			cell_id      : this.cell_id	
	            	  },                    
	            success: () => { this.complete("Ячейка очищена"); },
	            error:   () => { this.emptyCell(); }
	                     
	        }); 
		}
	    
	    
	    
	
	
	    public blockCell() {
	    	
			this.formCell({					
			    apply: (value) => {
				    	this.cell_id = value;
				    	this.setBlockCell();
			    },
			    cancel: () => { this.stop(); }
			 });
			
	    }
	    
	    
	    
	    public setBlockCell()
		{		    	
	
	     
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/block_cell",
	            data: {
	            			cell_id      : this.cell_id	
	            	  },                    
	            success: () => { this.complete("Ячейка заблокирована"); },
	            error:   () => { this.blockCell(); }
	                     
	        }); 
		}
	    
	    
	    
	    public unblockCell() {
	    	
			this.formCell({					
			    apply: (value) => {
				    	this.cell_id = value;
				    	this.setUnblockCell();
			    },
			    cancel: () => { this.stop(); }
			 });
			
	    }
	    
	    
	    public setUnblockCell()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/unblock_cell",
	            data: {
	            			cell_id      : this.cell_id	
	            	  },                    
	            success: () => { this.complete("Ячейка разблокирована"); },
	            error:   () => { this.blockCell(); }
	                     
	        }); 
		}
	    
	    
	    public set_pallet_delivery()
	    {
	    	
	    	this.formCell({		
			    apply: (value) => {
				    	this.cell_id = value;
				    	this.send_to_client();
			    },
			    cancel: () => { this.stop(); }
			 });
	    	
	    }
	    
	    
	    
	    public send_to_client()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/set_pallet_delivery",
	            data: {
	            			cell_id   : this.cell_id	
	            	  },                    
	            success: () => { this.complete("Паллета Отправлена успешно"); },
	            error:   () => { this.stop(); }
	                     
	        }); 
		}
	    
	    
	    
	    
	    public send_from_item_to_delivery()
	    {
	    	
	    	this.formDelivery({		
			    apply: (value) => {
				    	this.delivery_id = value;
				    	this.send_to_delivery();
			    },
			    cancel: () => { this.stop(); }
			 });
	    	
	    }
	    
	    
	    
	    public send_to_delivery()
		{		    	
	
			this.ajax({
	            type: "POST",
	            url: "/mbl/inventory/send_from_item_to_delivery",
	            data: {
	            			delivery_id   : this.delivery_id	
	            	  },                    
	            success: (resp) => { 
	            					var msg = "Взять из ячейки: " + resp.cell_name + "      коробок: " + resp.count;
	            					this.complete(msg);
	            					
	            },
	            error:   () => { this.stop(); }
	                     
	        }); 
		}
	    
	    
	    
	}
}