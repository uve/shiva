var swForm = new dhtmlXForm("sw_form", [
                         {type:"label", label:"Введите ваш штрих-код с бэйджика"},
                         {type:"input", id:"barcode", name:"barcode", label:"Штрих-код:", value: "", validate:"^([0-9]{12})?$"},
                         {type:"label", label:"или ваши логин и пароль"}, 
                         {type:"input", id:"login", name:"login", label:"Логин:", value:""},
                         {type:"password", name:"passw", label:"Пароль:", value:""},
            
                         {type:"button", name:"butt", value:"OK", command:"doLogin"}
                        ]);


    self.SetTitle("Авторизация");
    swForm.attachEvent("onButtonClick", function(name, cmd){
    	self._messager.clearAll();
        self.NetSend("/auth", swForm.Serialize() );
    });
                           
    var frm_barcode = swForm.getInput("barcode");
    var frm_login = swForm.getInput("login");
    var frm_passw = swForm.getInput("passw");
                                                                          
    frm_barcode.onkeypress = function(e){
    	
        if(e.keyCode==13){
        	frm_login.focus();
            frm_barcode.focus();
            self.NetSend("/auth", swForm.Serialize() )
        }
    }
                        
    frm_login.onkeypress = function(e){
    
    	if(e.keyCode==13) frm_passw.focus();
    }
 
    frm_passw.onkeypress = function(e){
    	
        if(e.keyCode==13){
            frm_login.focus();
            frm_passw.focus();
            self.NetSend("/auth", swForm.Serialize() );
        }
    } 
    
    window.Cleaner.push(swForm);