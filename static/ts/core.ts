module CoreModule {

	declare var DatalogicScanner1;
	declare var Device;
	declare var TORNADO_HASH;
	declare var IS_RELOAD;
	
	
	export class Error {
		
		message: string;
		
	    constructor(message: string, id?: string, callback?) {
	    	
	    	this.message = message;
	    	
	    	var form = new FormModule.Form();
				
	    	form.FormMenu({
				
				caption: "Ошибка",
				text:    this.message,
				className: "error",
				buttons: { 
							"OK"  : () => { 
								
								form.close();
								if (form.parent_id && !callback && (form.id != form.parent_id)) { form.open(form.parent_id); }											
								if (callback) { callback(); }	
							}
				         }

			});

	    	if (id){
	            (<HTMLElement>document.getElementById(id)).innerText = this.message;
	    	}
			
	    }   		
	    
	}	
	
	
	
	export class Info {
		
		message: string;
		
	    constructor(message: string, id?: string, callback?) {
	    	
	    	this.message = message;
	    		
	       	var form = new FormModule.Form();
			
	    	form.FormMenu({
				
				caption: "Сообщение",
				text:    this.message,
				className: "info",
				buttons: { 
							"OK"  : () => { 
								
								form.close();
								if (form.parent_id && !callback && (form.id != form.parent_id)) { form.open(form.parent_id); }											
								if (callback) { callback(); }						
							}
				         }

			});
		    	

	    	
	    	if (id){
	            (<HTMLElement>document.getElementById(id)).innerText = this.message;
	    	}
			
	    }   		
	    
	}	

	
	
	
	export class Scanner {
		
		DefaultBarcodeType: string;
		
		
		barcode: Barcode;
		
		scanhandler_object;
		callback;
		
			
	    constructor(callback) {

	    	this.callback = callback;

	    	DatalogicScanner1.style.visibility = "hidden";
	    	DatalogicScanner1.style.width = 1;
	    	DatalogicScanner1.style.height = 1;
	       
	    	this.DefaultBarcodeType = "EAN 13";
	    	
	    	this.scanhandler_object = () => ( this.ScanHandler() );
	    
	        this.init();
	    }
	    
	    
	    public init(){
	     	
	    	
	        try{
	        	DatalogicScanner1.bScanEnabled = true;
	    		DatalogicScanner1.attachEvent("LabelScanned", this.scanhandler_object);

	    	}
	    	catch(e){
	    		//new Error("DatalogicScanner1 not found 1");
	    	}
	    	
	    }
	    
	    public detach()
	    {	    	

	        try{
	        	DatalogicScanner1.bScanEnabled = false;
	    		DatalogicScanner1.detachEvent("LabelScanned", this.scanhandler_object);
	    	}
	    	catch(e){
	    		//new Error("DatalogicScanner1 not found 2");
	    	}
	    	
	    }
	    
	    
	    
	    public ScanHandler()
	    {	    	

        	var input = <HTMLInputElement>document.getElementById("InputBarcode");
        	
        	//alert(input.toString());
        	input.value = DatalogicScanner1.sLabelText;	       	
        	
        	this.detach();
        	
        	this.callback.call(this);        	
        	
	    }
	}
	
	export class Barcode {
		id:       string;
		value:    string;
		type:  	  number;
		expected: string;
	
	    BCTUSER     = 1; 						// константа - режим ввода ШК пользователя 
	    BCTPALLET   = 2;						// константа - режим ввода ШК паллеты
	    BCTCELL     = 3;						// константа - режим ввода ШК ячейки
	    BCTDELIVERY = 5;						// константа - режим ввода ШК ячейки
	    BCTPARTY    = 7;						// константа - режим ввода ШК партии
		
	    
	    constructor() {

	    }    
	    
	    set(value: string) {

	    	try{
	    		
	    		this.isValidBarcodeType(value, this.type);
	    		this.isEqualExpected(value, this.type, this.expected);
	    			    	
		    	this.value = this.BarcodeToID(value);  //Если нужно вырезать ID	
	    		return true;
	    	}
	    	catch(err){
	    		var error = new Error(err, "EnterBarcodeErrText");
	    		return false;
	    	}

	    	
	    }    
	    
	    
	    private BarcodeToID(barcode)
	    {
	    	if (!barcode) return "";

	    	/* Для этих типов не извлекать id-шник */
	    	if ((this.type == this.BCTUSER) || (this.type == this.BCTCELL) || (!this.type)) {		    			    		
	    		return barcode;
	    	}

	    	var n = barcode.length;
	        var ID = (n >= 11) ? Number(barcode.substring(1, 12)) : barcode;
	        return ID.toString();
	    }
	    
	    
	    // проверка ШК на внутренний тип
	    private isValidBarcodeType(barcode: string, expectedType: number)
	    {
	    	
	    	if (barcode.length < 4){
	    		throw "неправильная длина штрихкода (минимум 4)";
	    	}
	    	
	    	if (!expectedType){
	    		//new Error("No expected Type");
	    		return true;
	    	}
	    	var n = Number(barcode.toString().substring(0, 1));
	    	
	    	if (n != expectedType){
	    		switch (expectedType) {
	    			case this.BCTUSER:     throw "ожидается ШК пользователя";
			            break;
	     			case this.BCTPALLET:   throw "ожидается ШК паллеты";
			            break;
	     			case this.BCTCELL:     throw "ожидается ШК ячейки";
			            break;
			        case this.BCTDELIVERY: throw "ожидается ШК сборочного";
			            break;
	     			case this.BCTPARTY:    throw "ожидается ШК партии";
			            break;
			        default:               throw "Неизвестная ошибка ШК";
	    		}
	    		//NewInnerText("EnterBarcodeErrText", errtext);
				//return false;
	  		} else {
				return true;
			} 
	    }
	    
	    
	    
	    // проверка ШК на ожинаемое значение
	    private isEqualExpected(barcode: string, expectedType: number, expected: string)
	    {

	    	if (!expectedType){
	    		//new Error("No expected Type");
	    		return true;
	    	}
	    	
	    	if (!expected){	    		
	    		return true;
	    	}
	    	
	    	if (barcode.toString().substring(0,10) != expected.toString().substring(0,10)){
	    		switch (expectedType) {
	    			case this.BCTUSER:     throw "Введён неправильный штрих-код пользователя";
			            break;
	     			case this.BCTPALLET:   throw "Введён неправильный штрих-код паллеты";
			            break;
	     			case this.BCTCELL:     throw "Введён неправильный штрих-код ячейки";
			            break;
			        case this.BCTDELIVERY: throw "Введён неправильный штрих-код сборочного";
			            break;
	     			case this.BCTPARTY:    throw "Введён неправильный штрих-код партии";
			            break;
			        default:               throw "Неизвестная ошибка ШК";
	    		}
	    		//NewInnerText("EnterBarcodeErrText", errtext);
				//return false;
	  		} else {
				return true;
			} 
	    }	    

	}
	
	export interface CoreInterface {
		class_name: string;
		barcode: Barcode;
	}
	
	
	export class Core implements CoreInterface{
		
		class_name: string;
		barcode: Barcode;


		SERVER_TIMEOUT: number;


		timeout_callback;
	
	
	    constructor() {
	    	
	    	this.barcode = new Barcode();

	    	this.SERVER_TIMEOUT = 1000;

	    	this.timeout_callback = null;
	                  
	    }    
	   	   
	    
	    public write(message: string) {
	
			try{				
				console.log(message);
			}
			catch(e){
				//alert(message);
			}
		}    

	    
	    
	    public info(message: string) {
	    	
			try{				
				console.log( message, this);
			}
			catch(e){
				//alert(message);
			}
		}    
	    
	    /*
	     * Кодирование данных (простого ассоциативного массива вида
	     * { name : value, ...} в  URL-escaped строку (кодировка UTF-8)
		*/
		private urlEncodeData(data) {
			var query = [];
			if (data instanceof  Object) {
				for (var k in data) {
					query.push(encodeURIComponent(k) + "=" +
							encodeURIComponent(data[k]));
				} 
				return query.join('&');
			} 
			else {
				return encodeURIComponent(data);
			}
		}
	    
		
		private createRequestObject() {

			  if (typeof XMLHttpRequest != 'undefined') {
			       return new XMLHttpRequest();
			  }


			  var progIDs = [ 'Msxml2.XMLHTTP.6.0',
			                  'Msxml2.XMLHTTP.5.0',
			                  'Msxml2.XMLHTTP.4.0',
			                  'Msxml2.XMLHTTP.3.0',
			                  'Msxml2.XMLHTTP',

			                  'Microsoft.XMLHTTP' ]; // MSXML5.0, MSXML4.0 and Msxml2.DOMDocument all have issues - be careful when using.  Details below.

              for (var i = 0; i < progIDs.length; i++) {
                  try {

                      var xmlhttp = new ActiveXObject(progIDs[i]);

                      return xmlhttp;
                  }
                  catch (e) {
                  }
              }

        }


		
		public start_loading(){

			var form = new FormModule.Form();
	    	form.open("loading");
	    	
	    	window.scrollTo(0,0);
		}
		
		public stop_loading(){
	    	var preloader_id = "loading";
	    	document.getElementById(preloader_id).style.display = 'none';

		}
		

		public new_event(){
			
			try{
				Device.BlinkGreenLed(50,20,true,true);
			}catch(e){}
		    // отобразим текст задания и проиграем звук

	    	
	    	document.getElementById("sound_element").innerHTML= 
	    		"<embed src='/static/beam.wav' hidden=true autostart=true loop=false>";
		}
		
		
		/**
		 * Аналог асинхронного вызова из jQuery.ajax
		 */
	    public ajax(settings) {

	    	if (!settings.hidden){
	    		this.start_loading();
	    	}
	    	
	    	var xmlhttp = this.createRequestObject();


    		xmlhttp.onreadystatechange = () => {


            var readyState  = 9;
            var status = 9;


           try {

                readyState = xmlhttp.readyState;
                status = xmlhttp.status;

           } catch(e) {
           }



            /*
            var point = document.getElementById("point-status");
             point.innerHTML =  point.innerHTML + readyState + '.' + status + '</br>';
             */

    		  if (readyState != 4) return;

    		  clearTimeout(this.timeout_callback) // очистить таймаут при наступлении readyState 4

    		  if ( TORNADO_HASH != xmlhttp.getResponseHeader("tornado_hash") ){
    			  IS_RELOAD = true;
    		  }
    		  
    		  
    		  
	  	    	if (!settings.hidden){
	  	    		this.stop_loading();
		    	}
    		  

    		  if (xmlhttp.status == 200) {
    		      // Все ок
    			  		  
    			  if (xmlhttp.responseText) {
    			  
	    			  var result = eval( '(' + xmlhttp.responseText + ')' );
	    			  
	    			  if (result.error) {
	    			    
	    			      if (!settings.hidden){
	    			    	  var error = new Error(result.error, "", () => { settings.error(); });
	    			      }
	        			  return;
	    			  }
	    			  
	    			  if (result.info) {
	    				  
	    				  if (!settings.hidden){
	    					  var info = new Info(result.info, "", () => { settings.success(result); });
	    				  }
	        			  return;
	
	    			  }	    			  
    			  }
    			  
    			  settings.success(result);    		     
    		  } else {

    			  if (settings.hidden){
    				  return false;
    			  }

    			  var msg = (xmlhttp.statusText != 'Unknown') ?  xmlhttp.statusText : "Нет связи с сервером, проверьте интернет-соединение";


    			  var error = new Error(msg, "", () => {
    				  	settings.error(); 
    			  });

    		  }
    		}



    		xmlhttp.open(settings.type, settings.url, true);


	    	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	    	//xmlhttp.setRequestHeader("Content-length", settings.data.length);
	    	//xmlhttp.setRequestHeader("Connection", "close");




    		for (var item in settings.data){

        		if (typeof settings.data[item] === "undefined"){ 
        			delete settings.data[item];
        		}
    		} 




            xmlhttp.send(this.urlEncodeData(settings.data));


            /*
    		this.timeout_callback = setTimeout( () => {

                   xmlhttp.abort();
                   xmlhttp.abort();

    		 }, this.SERVER_TIMEOUT);

    		 */

		}    
	    
	    
		public application_reload(){

	 		if (IS_RELOAD == "true" || IS_RELOAD == true){ 			

	 			location.reload(true);
	 		 			
	 		}	    
			
		}
		
		
		public extend(destination, source) {
		    for (var property in source) {
		        if (source.hasOwnProperty(property)) {
		            destination[property] = source[property];
		        }
		    }
		    return destination;
		}

	

	}
}