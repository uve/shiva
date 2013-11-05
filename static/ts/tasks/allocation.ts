module AllocationModule {
	
	export class Allocation extends TaskModule.Task{
	
		public class_name = "Allocation";
			
		cell_id   : string;
		pallet_id : string;
		
		
		
	    public start() {
	    	    	
	    	 super.start();
	        
	    	 this.scan_pallet();
	    }    


	    
	    public scan_pallet() {

			this.formPallet({					
						    apply: (value) => {
							    	this.pallet_id = value;
							    	this.scan_cell();
						    },
						    cancel: () => { 
						    				this.stop(); 
						    }
						 });
	    }
	    
	    
	    
	    public scan_cell() {
	    
			this.formCell({					
						    apply: (value) => {
							    	this.cell_id = value;
							    	this.set_place();
						    },
						    cancel: () => { 
						    		this.scan_pallet();
						    }
						 });
	    }
	    
	    

	    public set_place(){
	    
	    	
		 	this.ajax({
	 	        type: "POST",
	 	        url: "/mbl/alloc/set_place",     
	 	        data: {   cell_id:   this.cell_id,
	 	        		  pallet_id: this.pallet_id },             	 	        
	 	        success: () => {
	 	        					this.complete("Паллета была успешно размещена");	 
	 	        },
	            error:   () => { this.stop(); } 
	 	    });
	    	
	    }
	
	    	
		
	   
	}
}