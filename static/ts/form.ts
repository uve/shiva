module FormModule {

	export class Form {
		
		id: string;
		parent_id: string;
		scanner;
		
		value: string;
		text: string;
		
		
		DATE_FORMAT: string;
		
		CURRENT_YEAR: number;
		
	    constructor() {
	        this.DATE_FORMAT="dd.mm.yyyy";
	        this.CURRENT_YEAR = 2013;
	    }
		
		
				
			 
	    private getElementsByClassName(className) {
	    	  var found = [];
	    	  var elements = document.getElementsByTagName("*");
	    	  for (var i = 0; i < elements.length; i++) {
	    	    var names = (<HTMLElement>elements[i]).className.split(' ');
	    	    for (var j = 0; j < names.length; j++) {
	    	      if (names[j] == className) found.push(elements[i]);
	    	    }
	    	  }
	    	  return found;
	    	}

	    
		public open(item: string){
	
				
			 var elements = this.getElementsByClassName('win');
			    for( var i=0; i < elements.length; i++ ){
			    	
			    	if ((<HTMLElement>elements[i]).style.display == 'block') {
				    	(<HTMLElement>elements[i]).style.display = 'none';
				    	this.parent_id = (<HTMLElement>elements[i]).getAttribute("id");

				    	/*
				    		console.log("this.parent_id");
				    		console.log(this.parent_id);
				    	*/
			    	}
			    	
			 }
			 document.getElementById(item).style.display = 'block';
			 
			 //console.log('open: ' + this.id);
		 }	
		 
		 
		 public close(){
			 document.getElementById(this.id).style.display = 'none';	
			 
		     //this.open("FrontWindow2");
			 
			 //console.log('close: ' + this.id);
			 
		 }	
	
	
		 /*
		  * Вызов формы ошибки
		  * 
		  */ 
		 public FormError(settings)
		 {
				// MsgText - текст сообщения, содержащий HTML-разметку
			    // btnText - текст на кнопке
			    // func - JS-код, навешиваемый на событие onclick этой кнопки
			 	this.id = "ErrorMessage1";
			
			 	this.open(this.id);

				(<HTMLElement>document.getElementById("ErrorMessageText1")).innerHTML = settings.text;

				(<HTMLElement>document.getElementById("form-1")).className = "win error";
				
				var buttonOK     = <HTMLInputElement>document.getElementById("btnErrorMessage1OK");
				
				buttonOK.onclick = () => {
						 this.close();
						 this.open(this.parent_id);
						 settings.apply();
				};
				
				buttonOK.setAttribute("value", "OK");
				
				buttonOK.focus();
		}
		 
		
		 
		 
		 // вызов универсальной формы ввода штрихкода
		 public FormBarcode(settings)
		 {
			 			 
			 this.id = settings.id;
			 
			 if (!settings.id){
				 this.id = "FormBarcode";	 
			 }
			 
			// alert(form.id);
		     // settings - объект, имеющий свойства:
		 	//     text - текст сообщения, содержащий HTML-разметку
		 	//     expectedType - ожидаемый тип ШК, определяемый самым 1-м символом.
		 	//         1 - пользователь системы
		 	//         2 - паллета
		 	//         3 - ячейка
		 	//         7 - партия
		 	//     ApplyOnScan - Флаг: вызов обработчика apply сразу после сканирования
		 	//     minlength - минимальная длина строки, содержащей ШК (по умолчанию = 1)
		 	//     maxlength - максимальная длина строки, содержащей ШК (по умолчанию = 13)
		 	//     apply - JS-код обработчика, навешиваемый на событие onclick кнопки #1
		 	//     cancel - JS-код обработчика, навешиваемый на событие onclick кнопки #2
	
			
		
		
			
			(<HTMLElement>document.getElementById("EnterBarcode")).style.backgroundColor = "";
			
		
			if (settings.backgroundColor){
				(<HTMLElement>document.getElementById("EnterBarcode")).style.backgroundColor = settings.backgroundColor;
			}
				 
			
			(<HTMLElement>document.getElementById("caption-2")).innerHTML = "";
			(<HTMLElement>document.getElementById("caption-2")).style.display = "none";
			(<HTMLElement>document.getElementById("text-2")).innerHTML = "";
			(<HTMLElement>document.getElementById("text-2")).style.display = "none";
			
			
			if (settings.caption){
				(<HTMLElement>document.getElementById("caption-2")).innerHTML = settings.caption;
				(<HTMLElement>document.getElementById("caption-2")).style.display = "block";
			}
			
			if (settings.text){
				(<HTMLElement>document.getElementById("text-2")).innerHTML = settings.text;
				(<HTMLElement>document.getElementById("text-2")).style.display = "block";
			}
			
						 
			//(<HTMLElement>document.getElementById("EnterBarcodeFormText")).innerHTML = settings.text;			
			
			(<HTMLElement>document.getElementById("EnterBarcodeErrText")).innerHTML = "";						
			
		 	// откроем форму и отобразим поясняющий текст
			this.open("EnterBarcode");
			
			var input = <HTMLInputElement>document.getElementById("InputBarcode");
			input.value = "";
			//input.focus();
			
			
			var buttonOK     = <HTMLInputElement>document.getElementById("btnEnterBarcodeOK");
			var buttonCancel = <HTMLInputElement>document.getElementById("btnEnterBarcodeCancel");
			
			buttonOK.removeAttribute("disabled");
		    buttonCancel.removeAttribute("disabled");
		    
			
			buttonOK.onclick = ()=> {
				
				//buttonOK.focus();
			    		    
				this.scanner.detach();

			    //buttonOK.setAttribute("disabled", "disabled");
			    //buttonCancel.setAttribute("disabled", "disabled");
			    			    			    
		        // разрешён переход на функцию apply сразу по вводу ШК			    
			    if (settings.ApplyOnScan) {						
					 settings.apply(input.value);
				 }
			    

			};
			
			buttonCancel.onclick = ()=>  {
			    
				//buttonOK.setAttribute("disabled", "disabled");
				//buttonCancel.setAttribute("disabled", "disabled");
				this.scanner.detach();					
				settings.cancel();		
								    
			};			
			
			this.scanner = new CoreModule.Scanner(buttonOK.onclick);
		
			 
		 }
		 
		 
		 public get_timestamp(){
			 			 
			 return (this.get_date().getTime() / 1e3).toString();
		 }
		 
		 
		 private get_date(){

			var new_date = new Date();	
						
			var year  = this.get_calendar_value('select-year',  this.CURRENT_YEAR);	
			var month = this.get_calendar_value('select-month', new_date.getMonth() + 1);					
			var date  = this.get_calendar_value('select-date',  new_date.getDate()); 
			 
			var dateObj = new Date(year, month-1, date );

			return dateObj;		
		 }
			
			 
		 
		 
		 private get_calendar_value(id, default_value){
			 
			 
			 
			 var select = <HTMLSelectElement>document.getElementById(id);		
			 
			 if (id != "select-date") // Чтобы не получился бесконечный цикл
			 {
				 select.onchange = () => {
					 
					var new_date = new Date();	
					this.fill_dates("select-date",  1, 31, new_date.getDate());
				 };
			 }
			 else{
			 	 select.onchange = () => {												
					 this.get_date();				 	
				 };	
			 }
			 
			 
			 
			 if (select.options.length > 1){
				 return select.options[select.selectedIndex.toString()].value;		 
			 }
			 
			 return default_value;
		 }
		 
		 
		 

		 
		 private fill_dates(id, min, max, today){

			 var select = <HTMLSelectElement>document.getElementById(id);
			 				
			 while ( select.childNodes.length >= 1 )
			 {
			     select.removeChild(select.firstChild);       
			 }
			 
			 
			 if ((max > 20) && (id == "select-date")){ // Если заполняем числа месяца					
			
				var date = this.get_date();
			
				var year  = this.CURRENT_YEAR;
				var month = date.getMonth()+1;
				 
			    var days=null;
		
			    if(month==4 || month==6 || month==9 || month==11)
			        days=30;
			    else if(month==2)
			    {
			        //Do not forget leap years!!!
			        if(year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)) //Provided by Justin Gregoire
			        {
			            days=29;
			        }
			        else
			        {
			            days=28;
			        }
			    }
			    else 
			        days=31;
			    
			    max = days;
			 }
			 
			 
			 if (today > max){  //Если текущее число например 30,  а выбранном месяце 28 дней
				 today = 1;
			 } 
			 
				 
			 for (var i = min; i <= (max + 3); i++) 
			 {
			     var newOption = <HTMLOptionElement>document.createElement("option");
			     var value = i.toString();
			     
				 if (i == today){
					newOption.selected = true;
				 }
			     
				 if (today < 2000){  // Для месяцев и дат
					 value = ("0" + value).slice(-2);
				 }
				 
				 if (i > max){
					 value = "";
				 }
				 
			     newOption.value=value;
			     newOption.text=value;
			     newOption.innerHTML=value;
			     select.appendChild(newOption);
			 }


		 }
		 
		 
		 
		 // "меню" с кнопками
		 public FormMenu(settings)
		 {
		 	// text - выводимый сверху текст.
		 	// buttons - массив, каждый элемент которого - структура с полями: текст кнопки и функция,
		 	// вызываемая по нажатию
		 	// Также хорошо бы помнить, что много кнопок на экран не вмещается. От силы 5 штук.
		    
			
			this.id = "form-1";
			// откроем форму и отобразим поясняющий текст
			this.open("form-1");
			
			this.value = "";  // !!!!
			
			
			
			(<HTMLElement>document.getElementById("caption-1")).innerHTML = "";
			(<HTMLElement>document.getElementById("caption-1")).style.display = "none";
			(<HTMLElement>document.getElementById("text-1")).innerHTML = "";
			(<HTMLElement>document.getElementById("text-1")).style.display = "none";
			(<HTMLElement>document.getElementById("options-1")).innerHTML = "";
			(<HTMLElement>document.getElementById("options-1")).style.display = "none";
			
			
			
			(<HTMLElement>document.getElementById("select-calendar")).style.display = "none";
			
			
			
			(<HTMLElement>document.getElementById("form-1")).style.backgroundColor = "";
			(<HTMLElement>document.getElementById("form-1")).className = "win ";
			
			
			if (settings.caption){
				(<HTMLElement>document.getElementById("caption-1")).innerHTML = settings.caption;
				(<HTMLElement>document.getElementById("caption-1")).style.display = "block";
			}
			
			if (settings.text){
				(<HTMLElement>document.getElementById("text-1")).innerHTML = settings.text;
				(<HTMLElement>document.getElementById("text-1")).style.display = "block";
			}
			
			if (settings.className){
				(<HTMLElement>document.getElementById("form-1")).className += settings.className;
			}
			
			
			if (settings.backgroundColor){
				(<HTMLElement>document.getElementById("form-1")).style.backgroundColor = settings.backgroundColor;
			}
	
	
			
			if (settings.options){

				
				(<HTMLElement>document.getElementById("options-1")).style.display = "block";
				
				var all_options = <HTMLElement>document.getElementById("options-1");
				
				/*
				var select = (<HTMLSelectElement>document.createElement("select"));
				
				select.className = "select-1";			
								
				select.style.width = '98%';
				select.size = 10;
		
				*/


		        var input_template = "<label><input type='radio' name='chk_group' value='%d' title='%s' />%s</label>";

				var selectArr = new Array();
				selectArr.push ('<div id="select-1" size=10>');
				
				for (var i = 0; i < settings.options.length; i++){ 

					var res = input_template;
					res = res.replace("%d", settings.options[i]["id"]);
					res = res.replace("%s", settings.options[i]["name"]);
					res = res.replace("%s", settings.options[i]["name"]);

				    selectArr.push(res);
				    
				    /*delete settings.options[i];*/
				}
				
				settings.options = null;
				
				selectArr.push ("</div>");

				all_options.innerHTML = selectArr.join("");


				var select = <HTMLElement>document.getElementById("select-1");


				var form = this;

                select.onclick = () => {

                        var radios = document.getElementsByName("chk_group");

                        for (var i = 0; i < radios.length; i++) {

                            var item = <HTMLInputElement> radios[i];
                            if (item.checked) {;

                                form.value = item.value;
                                form.text  = item.title;


                                break;
                            }
                        }


                    };


				(<HTMLElement>document.getElementById("options-1")).style.display = "block";
			
			}
			
			
			if (settings.input){
				
				var all_options = <HTMLElement>document.getElementById("options-1");
				
				(<HTMLElement>document.getElementById("options-1")).style.display = "block";
				
				
				var input = (<HTMLInputElement>document.createElement("input"));
				
				input.className = "input-1";
				
				input.type = "text";
			
				input.style.width = '98%';
				
				input.className = "hugetext centered";
				
				input.value = "";
				
				
				input.onchange = () => { 
					this.value = input.value;
				}
				
				all_options.appendChild(input);
				
				input.focus();
			
			}
			
			
			if (settings.date){
							
				var today = new Date();
				
				var year =  today.getFullYear();
				
				this.fill_dates("select-year",  year - 2, year + 5, year);
				this.fill_dates("select-month", 1, 12, today.getMonth()+1);
				this.fill_dates("select-date",  1, 31, today.getDate());
					 	
				
				
				var select_calendar = <HTMLElement>document.getElementById("select-calendar");
							
				select_calendar.style.display = "block";
	
								
			}
			
			//button.value = item;
			//button.onclick = settings.buttons[item];
			
			
			var all_buttons = <HTMLElement>document.getElementById("buttons-1");
			all_buttons.innerHTML = "";
			
			var buttons_count = 0;
			
			for (var item in settings.buttons) {
						
				var button = (<HTMLInputElement>document.createElement("input"));
				
				button.type = "button";
				button.className = "HugeBtn";
				button.value = item;
				button.onclick = settings.buttons[item];

				all_buttons.appendChild(button);
				buttons_count += 1;
			}
			
			
			all_buttons.className = "";
			
			if (buttons_count <= 2){
				all_buttons.className = "FooterDIV2";				
			}
			
				
			
			
			
			
			

			
		 }
		 
		
		 
		 
		 
		 /**
		  * Форма ввода количества - 5
		  *
		  *
		  * text - выводимый сверху текст.
		  * default_value - значение по умолчанию, возвращаемое в случае отмены ввода
		  * min_value - минимальное допустимое значение величины
		  * max_value - максимальное допустимое значение величины
		  */		 
		 public FormCount(settings)
		 {

			// откроем форму и отобразим поясняющий текст
			this.open("form-5");
			(<HTMLElement>document.getElementById("caption-5")).innerHTML = settings.text;
						
			
			
			var input = <HTMLInputElement>document.getElementById("value-5");
			
			input.value = "";
			
			if (settings.default_value) {
				input.value = settings.default_value;
			}
			
			/*
			 * Разрешить ввод только цифр и точки
			input.onkeyup = ()=>{ 
				input.value = input.value.replace(/[^\d.]/,'');				
			};
			*/
			
			input.focus();
			
			var all_buttons = <HTMLElement>document.getElementById("buttons-5");
			all_buttons.innerHTML = "";			
			

			// Принять
			var button = (<HTMLInputElement>document.createElement("input"));
			button.type = "button";
			button.className = "HugeBtn";
			button.value = "Принять";
			button.onclick = ()=> {			    		    								
									settings.apply(input.value);									
								  };
			all_buttons.appendChild(button);
			
			
			// Отмена
			var button = (<HTMLInputElement>document.createElement("input"));			
			button.type = "button";
			button.className = "HugeBtn";
			button.value = "Отмена";
			button.onclick = ()=> { settings.cancel(); };			
			
			all_buttons.appendChild(button);
			
			
		 }
		

	}
}