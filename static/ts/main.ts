/// <reference path="task.ts" />

module MainModule {
	
	declare var status;
		
	
	export class Main extends TaskModule.Task{
			
	        user_name : string;
	        user_depart : string;
	        user_role : string;
			rc        : string;
	
			constructor(){
				super();
			    
				var task = new TaskModule.Task();
				
			    setInterval(() => {
			    					
			    					task.task_check();
			    				   } , 5000);
			}
		
		 	public init() {
		 		
		 		this.user_name   = "";
		 		this.user_depart = "";
		 		this.user_role   = "";
		 			 		 	    	 	    
		 		this.auth();
		 			 		
		 	}
		 	
		 	
		 	
		 	public auth(value = ""){
		 		
			 	this.ajax({
		 	        type: "POST",
		 	        url: "/auth",     
		 	        data: ({ barcode: value }),             	 	        
		 	        success: (resp) => {
		 	        	
		 	        			if (resp){
		 	        				this.user_name   = resp["name"];
		 	        				this.user_depart = resp["depart"];
		 	        				this.user_role   = resp["role_name"];
		 	        				this.rc          = resp["rc"];
					 	            
			 	        			this.main();
		 	        			}
		 	        			else{
		 	        				this.login();
		 	        			}
		 	        			
		 	        },
		            error:   () => { this.login(); } 
		 	    });
		 	
		 	}
			    
		 	
		 	
		 	public login() {
		 			 			
		 		status = false;
		 		
		 		
		 		this.formUser({					
				      apply: (value) => {
					    	this.auth(value);
				      },
				      cancel: () => { /*reload page*/ }
				   });
		 		
		 	}	 
		 	
		 	
		 	
		 	public logout() {
	
		 		this.ajax({
		 	        type: "POST",
		 	        url: "/logout",
		 	        success: () => { this.init(); },        				 	        
		        	error:   () => { this.init(); } 
		 	        
		 	    });	 		
		 	}	 	
			
		 	
		 	
		 	public main() {

		 		status = true;  /* Пользователь может принимать задания */
		 				 	
				var form = new FormModule.Form();
				
				var caption = this.user_name;
				
				
				var buttons = { 
					
					"Инвентаризация"  : () => {									
						var task = new InventoryModule.Inventory();							
					},

					"Выход"  : () => {									
						this.logout(); 	
					},	
		         }
				
				
				
				if (this.rc == "1"){
					
					var rc_buttons = {
										"Подтоварка"  : () => {									
											var task = new ManualIncreaseModule.ManualIncrease();			
										}
									};
					
					
					buttons = this.extend(rc_buttons, buttons);
				}
				
				
				
				form.FormMenu({
					
					caption: caption,
					text: "Выберите режим",				
					buttons: buttons	
				});
				
						
		 	}	 
		 	
		
	}

}