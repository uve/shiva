function doOnLoad() {
	dhtmlx.image_path = '/static/dhtmlx/imgs/';

	// Здесь запоминаются объекты DHTMLX. Перед созданием новых, старые надо почистить.
	// Очистка вызывается автоматом при загрузке нового модуля. Но можно ручками:
	// self.InitContent()
	window.Cleaner = [];
	dhtmlx.skin = "dhx_skyblue";
	window.dhx_globalImgPath="/static/dhtmlx/imgs/";
	
	// само приложение. Доступ или через
	// window.app.foobar()
	// или через self (почти во всех методах есть "var self = this;" )
	// self.foobar()
	app = new ShivaApp(); 
	
	// для древних бравзеров. типа python {}.keys()
	if(!Object.keys) 
		Object.keys = function(o){
			if (o !== Object(o))
				throw new TypeError('Object.keys called on non-object');
			var ret=[],p;
			for(p in o) if(Object.prototype.hasOwnProperty.call(o,p)) ret.push(p);
			return ret;
		}
}

/************************************************************************************************
*                                                                                               *
*************************************************************************************************/
var ShivaApp = function(){
	var self=this;
	this._progres_count = 0; //счетчик показов progress полоски
	
	var HEAD_HEIGHT = 54; //86;//70;//62;//54; // высота хидера (ico 48)
	var LEFT_WIDTH = 205; // ширина левой панели
	var RIGHT_WIDTH = 220;// ширина правой панели
	var TIME_MESSAGE = 2*60*1000; // интервал для запроса сообщений

	// время показа сообщений в правой панели в секундах
	this.TIME_MESSAGE_DEBUG = 50;
	this.TIME_MESSAGE_INFO = 100;
	this.TIME_MESSAGE_WARNING = 300;
	this.TIME_MESSAGE_ERROR = 600;
	
	this.last_url = '/'; // текущий url
	
	this.VSCREENS = ['def','one', 'two']; // имена экранов +['hlp']
		
	this.GW =  new dhtmlXLayoutObject(document.body, "3W");
	this.GW.items[0].setWidth(LEFT_WIDTH);
	this.GW.items[2].setWidth(RIGHT_WIDTH);
		
	//--- Left panel -----------------//
	var Layout0 = this.GW.items[0].attachLayout("2E");
	Layout0.items[0].setHeight(HEAD_HEIGHT);
	Layout0.items[0].hideHeader();
	Layout0.items[0].fixSize(false,true);

	var im = document.createElement("img");
	im.setAttribute('src', "/static/logo.png");
	im.setAttribute('width', Layout0.items[0].getWidth());
	im.setAttribute('height', Layout0.items[0].getHeight());	 	
	im.setAttribute('style', "background-color:#e3efff");
	Layout0.items[0].attachObject(im);
		
	Layout0.items[1].hideHeader();
	this.Accord = Layout0.items[1].attachAccordion();
		
	//--- Center panel -----------------//
	var Layout1 = this.GW.items[1].attachLayout("2E");
	
	this.Title = Layout1.items[0];
	this.Title.setHeight(HEAD_HEIGHT);
	this.Title.setText("");
	this.Title.hideArrow();
	this.Title.fixSize(false,true);
	
	this.Content = Layout1.items[1];
	this.Content.hideHeader();
	
	this.Toolbars = {};
	this.Panels = {}
	
	var n; var scr=this.VSCREENS.concat('hlp');
	for(i in scr){
		n=scr[i];
		this.Toolbars[n] = this.Title.view(n).attachToolbar();
		this.Toolbars[n].setIconsPath("/static/img/");	
		this.Panels[n]=document.createElement("div");
		this.Panels[n].setAttribute('style', "background-color:#eaf2fb;height:100%;pading:0px;width:100%");
		this.Content.view(n).attachObject(this.Panels[n]);
	}
	this._help2toolbars('hlp');
			
	window.ShowPanel_def = function(){ self.ShowPanel('def') }
	window.ShowPanel_one = function(){ self.ShowPanel('one') }
	window.ShowPanel_two = function(){ self.ShowPanel('two') }
	window.ShowPanel_hlp = function(){ self.ShowPanel('hlp') }
	
	

	//--- Right panel -----------------//
	var Layout2 = this.GW.items[2].attachLayout("2E");
	Layout2.items[0].setHeight(HEAD_HEIGHT);
	Layout2.items[0].hideHeader();
	Layout2.items[0].fixSize(false,true);
	
	Layout2.setAutoSize("a", "a");
	
	var d1 = document.createElement("div");
	d1.setAttribute('style', "background-color:#eaf2fb;width:100%;height:100%;position:relative;padding:0;margin:0;");	
	d1.innerHTML = '<div id="user_info" style="color:#0f4161; font:bold 10px verdana; float:left; padding:7px 0 0 4px;">'+
						'<div id="user_name"></div>'+
						'<div id="depart_name"></div>'+
						'<div id="role_name"></div>'+
					'</div>'+
					'<div style="position:absolute; top:5px; right:3px; padding:0;">'+
						'<a style="text-decoration:none; color:#eaf2fb; background-color:#4985b7; padding:2px 4px; font:bold 11px verdana;" href="/logout">Выход</a>'+
					'</div>';
	Layout2.items[0].attachObject(d1);

	
	Layout2.items[1].hideHeader();
	this._messager = Layout2.items[1].attachDataView({
        type:{ hight:60, padding:0, margin:1,
               template:'<div style=\\"background-color:#col#; min-height:60px; overflow: visible;\\">'+
                          '<img style=\\"margin:2px 5px 20px 1px; float:left;\\" src=\\"/static/img/#ic#\\" />'+
                          '<span style=\\"margin:2px 0;\\">#mess#<span>'+
                        '</div>' }
	});

	//this._messager.attachEvent("onItemClick", function(itemId){ setTimeout(function(){ self._messager.remove(itemId) }, 0); })
		
	//--- Auth ---
	this.NetSend("/auth", ' ', function(response){
		if(200==response.xmlDoc.status && response.xmlDoc.responseText){
			this._make_content(response);
		}else{
			this.NetSend("/auth");			
		}
	});
	
	//--- Messages ---
	// запрос сообщений с сервера.
	// 2 раза сделано специально - иногда js глючит и может неинициализироваться
	//setInterval(function(){ self.ServerMessage() }, TIME_MESSAGE);
	//self.ServerMessage();
}

/*************************************************************************************************
* Создает левый аккордион с меню                                                                 *
*************************************************************************************************/
ShivaApp.prototype.MakeMenu = function(){

	this.NetSend("/menu", null, function(response){
		var self=this;
		// del accordion sections
		this.Accord.forEachItem(function(item){
			delete item.data;
			self.Accord.removeItem(item.getId());
		});
	
		// create accordion sections
		var data = eval('('+response.xmlDoc.responseText+')');
		var i,j;
		for (i in data){
			var jsd=data[i][1];
			if(jsd.length){
				var item=this.Accord.addItem(i, data[i][0]);
				// fill accordion sections				
				item.data=item.attachDataView({
					type:{
						template:"<b>#caption#</b><div style=\\\"font-size:9px; color:#0f4161;\\\">#description#</div>",
						height:26, padding:6
					}		
				});
					
				item.data.parse(jsd,'json');				
				item.data.attachEvent("onItemClick", function(itemId){
					self.InitContent();	
                    setCookie("itemId", itemId, { expires: 2592000 }); // месяц - 1*30*24*60*60
					var url = this.get(itemId).url;
					self.last_url = url;
					self.SetTitle(this.get(itemId).caption);
					self.NetSend(url+'?'+new Date().getTime());
				 });
			}
		}
		
		// открываем прошлый модуль
		var itemId = getCookie('itemId');
		if(!!itemId){	
			try{
				this.Accord.forEachItem(function(item){
					for(var i=item.data.first(); i; i=item.data.next(i)){
						if(i==itemId) throw [item, i];
					}
				});
			}catch(e){
				e[0].open();
				e[0].data.show(e[1]);
				e[0].data.select(e[1]);
				e[0].data.callEvent("onItemClick",[e[1]]); 
			}		
		}
	});
}


/*************************************************************************************************
* контент в центральной панели                                                                   *
* panel_name = 'def' или 'one' или 'hlp'                                                         *
*************************************************************************************************/
ShivaApp.prototype._set_content = function(panel_name, content){
	this.Panels[panel_name].innerHTML='<div class="swcnt" style="padding:1px; margin:0; width:100%; height:100%">'+content+'</div>';
}

/*************************************************************************************************
* Главный создатель контента. Получает JSON данные в виде текста. Обычно от self.NetSend         *
*************************************************************************************************/
ShivaApp.prototype._make_content = function(response){
	var self=this;
		
	if(200==response.xmlDoc.status && response.xmlDoc.responseText){
		var resp = eval('('+response.xmlDoc.responseText+')');

		//--- response.precmd ---//
		// js выполняемый в самом начале
		if(resp.precmd) eval(resp.precmd);	
		
		//--- user_info ---//
		// для правого верхнего дива с инфой о пользователе
		if(resp.user_name) document.getElementById('user_name').innerHTML=resp.user_name;
		if(resp.depart_name) document.getElementById('depart_name').innerHTML=resp.depart_name;		
		if(resp.role_name){
			document.getElementById('role_name').innerHTML=resp.role_name;
			this.InitContent();
			this.MakeMenu();
		}

		//--- response. 'def', 'one' ---//
		// Кнопки для тулбара и сырой html
		var v; var iter; var sep; var n;
		for(i=0; i<this.VSCREENS.length; i++){
			n=this.VSCREENS[i];
			v=resp[n];
			
			if(!!v){
				if(typeof v == "string"){
					this._set_content(n,v);
				}else{
					for(j in v){
						vv=v[j];
						if(typeof vv == "string"){
							this._set_content(n,vv);
						}else{
							if(vv.id == 'undefined') vv.id = String(new Date().getTime());
							this.Toolbars[n]._addItem(vv, Object.keys(this.Toolbars[n].objPull).length+1);		
						}
					}				
				}
				
				// добавляем в конец тулбаров кнопку "Help"
				this._help2toolbars(n);
			}
		}

		//--- response.cmd ---//
		// js выполняемый после создания тулбаров и пр.
		if(resp.cmd) eval(resp.cmd);
		
		//--- response.MESSAGES ---//
		// сообщения от сервера для правой панели
		if(resp.debug)   this.AddMessage(resp.debug, 0)
		if(resp.info)    this.AddMessage(resp.info, 1)
		if(resp.warning) this.AddMessage(resp.warning, 2)
		if(resp.error)   this.AddMessage(resp.error, 3)
	}else
	if(404==response.xmlDoc.status){
		this.AddMessage("Страница в разработке", 2)
	}
}

/*************************************************************************************************
* url - url                                                                                      *
* data - передаваемые данные. если Истина - то POST, иначе - GET                                 *
* func - функция обрабатывающая ответ сервера. По умолчанию this._make_content                   *
*************************************************************************************************/
ShivaApp.prototype.NetSend = function(url, data, func){
	if(!func)func=this._make_content;
	
	var self=this;
	
	setTimeout(function(){ 
		self.progressOn();

		var res=new dtmlXMLLoaderObject(true);
		res.async=false;
		res.waitCall=null;		
		res.loadXML(url, !!data, data);
		func.call(self, res);
				
		self.progressOff();
	}, 0);		
}

ShivaApp.prototype.NetSendAsync = function(url, data, func){
	//if(!func)func=this._make_content;
	f=this._make_content;
	var self=this;
	
	setTimeout(function(){ 
		self.progressOn();

		var res=new dtmlXMLLoaderObject(true);
		res.async=false;
		res.waitCall=null;		
		res.loadXML(url, !!data, data);
		
		f.call(self, res);
		
		if(200==res.xmlDoc.status && res.xmlDoc.responseText){
			var resp = eval('('+res.xmlDoc.responseText+')');
				
			if(func)func.call(self, resp);
		}
		
		
		self.progressOff();
	}, 0);		
}
	
/*************************************************************************************************
*  Показывает соответствующую панель (или в терминах DHTMLX view). panel_name = 'def','one','hlp'*
*************************************************************************************************/
ShivaApp.prototype.ShowPanel = function(panel_name){
	if(panel_name == undefined) panel_name='def';
				
	if(!!this.HelpEditor && panel_name != 'hlp'){
		this.HelpEditor.unload();
		this.HelpEditor = null;
	}
			
	this.Title.view(panel_name).setActive();
	this.Content.view(panel_name).setActive();
		
	if(panel_name == 'hlp'){
		this.HelpEditor = new dhtmlXEditor({ parent: this.Panels["hlp"] });
		
		var sep=String(new Date().getTime());          
		this.HelpEditor.tb._addItem({id:sep,type:"button", text:'Сохранить', img:"../../../img/accept24.png" }, 0);
		this.HelpEditor.tb._addItem({id:sep+1,type:"separator"}, 1);
		var self = this;
		this.HelpEditor.tb.attachEvent("onClick",function(id){
			if(id==sep){ self.NetSend("/system/help"+self.last_url, self.HelpEditor.getContent() ) }
		});
		this.HelpEditor.setContentHTML("/system/help"+this.last_url);
	}
}

/*************************************************************************************************
* добавляем в конец тулбаров кнопки "Help"                                                       *
*************************************************************************************************/
ShivaApp.prototype._help2toolbars = function(panel_name){
	var f = (panel_name == 'hlp') ? 'ShowPanel_def' : 'ShowPanel_hlp';	
	var iter=Object.keys(this.Toolbars[panel_name].objPull).length;
	var sep=String(new Date().getTime());
	
	this.Toolbars[panel_name]._addItem({id:sep,type:"separator"}, iter+1);
	this.Toolbars[panel_name].addSpacer(sep);
	this.Toolbars[panel_name]._addItem({id:sep+1,type:"button", text:'Справка', img:"help24.png", action:f}, iter+2);					
}


/************************************************************************************************
* Очистка экрана и памяти                                                                       *
************************************************************************************************/
ShivaApp.prototype.InitContent = function(){
	for(i in window.Cleaner){		
		try{ 
			if(window.Cleaner[i].unload){
				window.Cleaner[i].unload();
			}
			else
			if(window.Cleaner[i].destructor){
				window.Cleaner[i].destructor();
			}
		}catch (e){ }		
			
		window.Cleaner[i]=null;
		delete window.Cleaner[i];			
	}
	window.Cleaner.length=0;
		
	for(i=0; i<this.VSCREENS.length; i++){
		n=this.VSCREENS[i];
		if(n!='hlp'){
			this._set_content(n, '<div style="position:relative; top:50%; left:50%; margin:-60px 0 0 -200px; width:400px; height:200px;">'+
			                        '<img src="/static/logo.png" style="background-color: rgb(234, 242, 251); width: 90%;">'+
			                     '</div>');
			this.Toolbars[n].clearAll();
		}
	}
	
	this.ShowPanel('def');
}


/*************************************************************************************************
* Устанавливает заголовок в центральной панели                                                   *
*************************************************************************************************/	
ShivaApp.prototype.SetTitle = function(title){	
	if(title != undefined) this.Title.setText(title);
}


/*************************************************************************************************
* Выводит сообщения в правую панель.                                                             *
* message - string или Array(strings)                                                            *
* type_message - тип сообщения [0,1,2,3] или ['debug','info','warning','error']                  *
*************************************************************************************************/	
ShivaApp.prototype.AddMessage = function(message, type_message){
	var self=this;
	var ic,t,col;
	switch (type_message) {
		case 0:	case 'debug':   ic='process24.png'; t=this.TIME_MESSAGE_DEBUG;   col='#ebebeb'; break;
		case 1:	case 'info':    ic='info24.png';    t=this.TIME_MESSAGE_INFO;    col='#93c0e7'; break;
		case 2:	case 'warning': ic='warning24.png'; t=this.TIME_MESSAGE_WARNING; col='#ffe5ad'; break;
		case 3:	case 'error':   ic='delete24.png';  t=this.TIME_MESSAGE_ERROR;   col='#ed3a64'; break;
		case 5:	case 'info5':   ic='info24.png';    t=this.TIME_MESSAGE_ERROR;   col='#93c0e7'; break;
		default:                ic='process24.png'; t=this.TIME_MESSAGE_DEBUG;   col='#ebebeb';
	}

	if(typeof message == "string"){
		var idd = this._messager.add({ ic:ic, mess:message, col:col });
		setTimeout(function(){ self._messager.remove(idd) }, 1000*t);
	}else
		for(i in message)
			this.AddMessage(message[i], type_message);
}

	
/*************************************************************************************************
* Печатает пачку урлов.                                                                          *
* Первые 2 аргумента - ширина и высота каждого изображения в мм. Остальные - урлы с картинками   *
* например: self.PrintURL(200,100,'/foo','/bar');                                                *
*************************************************************************************************/
ShivaApp.prototype.PrintURL = function(){
	var arg=[].slice.call(arguments, 0);
	var w=arg[0]; var h=arg[1];
	var urls = arg.slice(2);
	this.Incunable( function(doc){
		for(i in urls)
			doc.write('<img "width="'+(3.75 * w)+'mm" height="'+(3.75 * h)+'mm" src="'+urls[i]+'">');
	});
}

/*************************************************************************************************
* Вывод на принтер. Контент генерируется функцией "generator"                                    *
*************************************************************************************************/
ShivaApp.prototype.Incunable = function(generator){
	if(this.PrintFrame){
		document.body.removeChild(this.PrintFrame);
	}

	this.PrintFrame=document.createElement('IFRAME');
	this.PrintFrame.setAttribute('style', "position:absolute;left:-500px; top:-500px; border:0pt none; padding:0;margin:0; width:0px; height:0px;");	
	document.body.appendChild(this.PrintFrame);
	var doc=this.PrintFrame.contentWindow.document;
	doc.write('<div style="padding:0; margin:0; border: 0pt none;">');
	generator(doc);
	doc.write('</div>');			  
	doc.close();
	
	this.PrintFrame.contentWindow.focus();
	this.PrintFrame.contentWindow.print();
}

/*************************************************************************************************
* Получает сообщения с сервера и показываетс в правой панели                                     *
*************************************************************************************************/
ShivaApp.prototype.ServerMessage = function(){
	var mess = eval("("+dhtmlxAjax.getSync("/system/message?"+new Date().getTime() ).xmlDoc.responseText+")");
	for(var i in mess){
		this.AddMessage(mess[i][0],mess[i][1]); 
	}
}

/*************************************************************************************************
* Загрузка данных из DHTMLX грида в виде CSV                                                     *
*************************************************************************************************/
ShivaApp.prototype.GridCSV = function(grid){
	//grid.csv.cell="\t"; // change CSV delimiter
	grid.setCSVDelimiter(";");
    var csvNew = grid.serializeToCSV(true); 
	if(!csvNew){
		this.AddMessage('Нет данных',1);
		return;
	}
	
	var submitForm = document.createElement("form");
	submitForm.method = "post";
	submitForm.action = "/system/csv";
	submitForm.setAttribute('accept-charset', 'utf-8');
	
	document.body.appendChild(submitForm);
		
	var newElement = document.createElement('INPUT');
 	newElement.type = 'hidden';
 	newElement.setAttribute('name', 'dat');
 	newElement.setAttribute('value', csvNew);	
	submitForm.appendChild(newElement);
	
	var now = new Date;
	
	var fruits = ["Export", now.getUTCFullYear(), now.getUTCMonth()+1, now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes()];
	var filename = fruits.join("-");
	
	
	var newElement = document.createElement('INPUT');
 	newElement.type = 'hidden';
 	newElement.setAttribute('name', 'filename');
 	newElement.setAttribute('value', filename);	
	submitForm.appendChild(newElement);
	
	submitForm.submit();
	submitForm.parentNode.removeChild(submitForm);
	this.AddMessage('Загрузка CSV: '+filename,1);
} 

/*************************************************************************************************
* On/Off прогресс бар при всяких загрузках. Ток чета про моему не фурычит                        *
*************************************************************************************************/
ShivaApp.prototype.progressOn = function(){
	this.GW._progressControlGlobal(true);
	this._progres_count+=1;
}
ShivaApp.prototype.progressOff = function(force){
	this._progres_count-=1;
	if(force)this._progres_count=0;
	if(!this._progres_count)this.GW._progressControlGlobal(false);	
}

/*************************************************************************************************
* Загрузка данных в грид                                                                         *

* *************************************************************************************************/
FilterStorage = function(grid, url){
	var self=this;
	
	//console.log();
	
	
	storage_url = "filters_" + url.split('time')[0] + '_'+grid._cCount + '_';
	
	try
	{
		
	    for (var i=0; i < grid.filters.length; i++){                                                                                                                                              
            grid.filters[i][0].value = sessionStorage.getItem(storage_url + i);                                          
	    }
    }
    catch(e){}    

    try
    {    	    
    	grid.attachEvent("onFilterEnd", function(elements){         
    		//console.log("Event: onFilterEnd");                                                                           
        	for (var i=0; i < grid.filters.length; i++){                                                                        
            	var myVar = sessionStorage.setItem(storage_url + i, grid.filters[i][0].value);                                
        	}    

	    });
	}
	catch(e){}	
		
	
}


ShivaApp.prototype.LoadGrid = function(grid,url){
	var self=this;
	
	
	this.progressOn();
	grid.clearAll();		

	if(url.indexOf('?') == -1){
		url=url+'?time='+new Date().getTime();
	}else{
		url=url+'&time='+new Date().getTime();
	}

	grid.load(url, function(){ 
		
		FilterStorage(grid, url);
		
		var cmd = grid.getUserData('', 'cmd');
		if(!!cmd)eval(cmd);
		var x=['info', 'warning', 'error'];
		for(i in x){
			cmd=grid.getUserData('', x[i]);
			if(!!cmd)
				self.AddMessage(cmd, x[i]);
		}
		
		try{
			grid.filterByAll();
		}		
		catch(e){}
		
	}, "xml");

	this.progressOff();
}


ShivaApp.prototype.serialize = function(obj){
	
	  var str = [];
	  for(var p in obj)
	     str.push(p + "=" + encodeURIComponent(obj[p]));
	  return str.join("&");
}



ShivaApp.prototype.load = function(grid,url, func){
	var self=this;
	
	self.progressOn();
	grid.clearAll();		

	grid.load(url, function(){
		
		self.progressOff();
		if (!func){
			return;
		}
		func.call();    
		
	}, "json");	

}



ShivaApp.prototype.LoadGridAsync = function(grid,url, func){
	var self=this;			
	
	this.progressOn();
	grid.clearAll();
	
	if(url.indexOf('?') == -1){
		url=url+'?time='+new Date().getTime();
	}else{
		url=url+'&time='+new Date().getTime();
	}
	
	

	grid.load(url, function(){ 
		
		FilterStorage(grid, url);
				
						
		var cmd = grid.getUserData('', 'cmd');
		if(!!cmd)eval(cmd);
		var x=['info', 'warning', 'error'];
		for(i in x){
			cmd=grid.getUserData('', x[i]);
			if(!!cmd)
				self.AddMessage(cmd, x[i]);
		}
		
		grid.filterByAll();	
		func.call();
		
	}, "xml");

	

	this.progressOff();
	
	
	
}

/*************************************************************************************************
* Перезагрузка текущей страницы                                                                  *
*************************************************************************************************/
ShivaApp.prototype.Refresh = function(){
	var self=this;
	this.InitContent();
	this.NetSend(self.last_url+'?'+new Date().getTime());
}




/*************************************************************************************************
* Вытаскивает данные из формы                                                                    *
*************************************************************************************************/
dhtmlXForm.prototype.Serialize = function(){
	var formdata = this.getFormData();
	var data=[]; var val;
	for(var i in formdata){
		val=formdata[i];
		if(val != '') data.push(i+"="+encodeURIComponent(val));
	}
	return data.join("&");
}

/*************************************************************************************************
* Русификация календаря                                                                          *
*************************************************************************************************/
dhtmlXCalendarObject.prototype.langData["ru"] = {
    dateformat: "%d.%m.%Y",
    monthesFNames: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    monthesSNames: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
    daysFNames: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
    daysSNames: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    weekstart: 1
}

//Create the XHR object.
function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // XHR for Chrome/Firefox/Opera/Safari.
    xhr.open(method, url, true);
  } else if (typeof XDomainRequest != "undefined") {
    // XDomainRequest for IE.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } else {
    // CORS not supported.
    xhr = null;
  }
  return xhr;
}

function UrlExists(url)
{
	
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    //http.withCredentials = true;
    http.send();
    return http.status!=404;
    
	/*
	var xhr = createCORSRequest('HEAD', url);
	  if (!xhr) {
	    alert('CORS not supported');
	    return;
	  }

	  /*
	  // Response handlers.
	  xhr.onload = function() {
	    var text = xhr.responseText;
	    var title = getTitle(text);
	    alert('Response from CORS request to ' + url + ': ' + title);
	  };

	  xhr.onerror = function() {
	    alert('Woops, there was an error making the request.');
	  };

	  xhr.send();
	  */
	  
}