module MovingModule {
	
	export class Moving extends TaskModule.Task{
	
		public class_name = "Moving";
			
		cell_id   : string;
		cell_name : string;
		
		target_id   : string;
		target_name : string;
		
		party_id   : string;
		
	    public start() {
	    	    	
	    	 super.start();
	    	 
	         this.getCellDestination();       
	    }    
		
	
	    public getCellDestination(){
	    	
	    	
	    	this.ajax({
	            type: "POST",
	            url: "/task/getcelldestination",
	            data: { 'task_id': this.task_id},	            
	            success: (resp) => {
	            		            
	            	this.cell_name    = resp["cell_name"]; 
	            	this.cell_id  	  = resp["cell_id"];
	            	
	        	
	            	if (resp["target_id"]){
	        			
			        	  this.target_id   = resp.target_id;
			        	  this.target_name = resp.target_name;		

	        		}			        	
	        		
	     
	            	this.scanCell();
	            	
	            },
	            error:   () => { this.stop(); }
	                     
	        }); 
	    	
	    }
	    
	    
	    public scanCell() {

			this.formCell({			
							text: "Перемещение с адреса: " + this.cell_name,
							expected: this.cell_id,
						    apply: (value) => {
							   	this.cell_id = value;
							   	this.palletConfirm();
						      
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	    
	    
	    
	    public palletConfirm() {
	    	
			var form = new FormModule.Form();
			
			form.FormMenu({
				
				caption: "Подтверждение погрузки паллеты",
				buttons: { 
	
							"Паллета погружена"  : () => { 												
								this.scanParty();								
							},
							
							"Ячейка была пуста"   : () => { 								
						        //SendFail(curr_CellBarcode, 0, 0, 0, ERR_EMPTYCELL);
								this.stop();
							}
				}
			});
			
	    }
	    
	    
	    public scanParty() {

			this.formParty({							
						    apply: (value) => {
							   	this.party_id = value;
							   	this.checkParty();
						      
						    },
						    cancel: () => { 
						    				this.palletConfirm(); 
						    }
						 });
	    }	    
	    
	    
	    
		
	    public checkParty(){
	    	
	    	
	    	this.ajax({
	            type: "POST",
	            url: "/mbl/valid",
	            data: { 'cell_id':  this.cell_id,
	            		'party_id': this.party_id,
	            	},	            
	            success: (resp) => {
	            	
	            	this.scanTarget();	            	
	            },
	            error:   () => { this.scanParty(); }
	                     
	        }); 
	    	
	    }	  
	    
	    
	    
	    
	    public scanTarget() {

	    	if (!this.target_id){
	    		
	    		this.palletMove();
	    		//this.complete("Отвезите паллету в зону отгрузки");	
	    		return;
	    		
	    	}
	    		

    		this.formCell({			
							text: "Перемещение на адрес: " + this.target_name,
							expected: this.target_id,
						    apply: (value) => {
							   	this.target_id = value;
							   	this.targetConfirm();
						      
						    },
						    cancel: () => { 
						    				this.scanParty(); 
						    }
						 });
	    	
	    
	    	
	    	
	    }
	    
	    
	    
	    public targetConfirm() {
	    	
			this.menu({
				
				caption: "Подтверждение погрузки паллеты",
				buttons: { 
	
							"Паллета размещена"  : () => { 												
								this.palletMove();								
							},
							
							"Ячейка была занята"   : () => { 								

								this.nextCell(); // получим новый адрес
							}
				}
			});
			
	    }
	    
	    
	    public nextCell(){
	    	
	    	this.ajax({
	            type: "POST",
	            url: "/mbl/moving/next_cell",
	            data: { 'cell_id':   this.cell_id,	            		
	            		'party_id':  this.party_id,
	            		'target_id': this.target_id,
	            	},	            
	            success: (resp) => {
	            	
	            	this.target_id   = resp.target_id;
	            	this.target_name = resp.target_name;
	            	
	            	this.scanTarget();	            	
	            },
	            error:   () => { this.stop(); }
	                     
	        }); 
	    	
	    }	  
	    
	    
	    
	    public palletMove(){
	    		    	
	    	this.ajax({
	            type: "POST",
	            url: "/mbl/moving/moved",
	            data: { 'cell_id':   this.cell_id,
	            		'target_id': this.target_id,
	            	},	            
	            success: (resp) => {	   
	            	
	            	this.complete("Паллета была успешно размещена");	            	
	            },
	            error:   () => { this.stop(); }
	                     
	        }); 
	    	
	    }	  
	    
	    
	    
	    
	    
	   
	}
}