# coding: utf-8

from core.sw_base import BaseHandler

from core.common_tools import fetchone
from barcode.zek_model import barcode2depart_sid

from core.utils import Storage
#=============================================================================#
class AuthHandler(BaseHandler):
    urls = r'/auth'

    def get(self):

        self.write({'def':'<div id="sw_form" style="position:relative; top:50%; left:50%; margin:-105px 0 0 -115px;" />',
                    'cmd':'''var swForm = new dhtmlXForm("sw_form", [
                         {type:"label", label:"Введите ваш штрих-код с бэйджика"},
                         {type:"input", id:"barcode", name:"barcode", label:"Штрих-код:", value: "", validate:"^([0-9]{12})?$"},
                         {type:"label", label:"или ваши логин и пароль"}, 
                         {type:"input", id:"login", name:"login", label:"Логин:", value:""},
                         {type:"password", name:"passw", label:"Пароль:", value:""},
            
                         {type:"button", name:"butt", value:"OK", command:"doLogin"}
                        ]);
                        self.SetTitle("Авторизация");
                        swForm.attachEvent("onButtonClick", function(name, cmd){
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
                        
                        window.Cleaner.push(swForm);'''
                    })
        
    def input2(self, **defaults):
        if isinstance(self.request.arguments, dict):
            defaults.update(self.request.arguments)

        return Storage(defaults)

    def post(self):
        
        barcode = self.get_argument("barcode", None)
        
        depart, user_id = None
        
        if barcode:
            depart, user_id = barcode2depart_sid(barcode)
            
        login   = self.get_argument("login", None)
        passw   = self.get_argument("passw", None)
        
                
        res = self.cursor.callproc("shiva_task.GetUser", [login, passw, user_id, depart])
               
        
        user = fetchone(res[-1])
        
        self.write(user)
        
        self.set_cookie('rc',   str(user.rc))
        self.set_cookie('uid',  str(user.id))
        self.set_cookie('role', str(user.role))
        
            
        '''
        
        if user:
            self.session = SessionManager(user.id, user.role, user.rc)
            
            self.set_cookie('uid', str(user.id))
            self.set_cookie('role', str(user.role))
            self.set_cookie('rc', str(user.rc))
        
            self.write({'user_name':user.name, 'depart_name':user.depart_cls.name, 'role_name':user.current_role_cls.name })
        '''

        
#=============================================================================#
class LogoutHandler(BaseHandler):
    urls = r'/logout'

    def get(self):
        # Тока через бравзер
        if self.session:
            self.session.kill()
        self.clear_all_cookies()
        self.redirect("/")

    def post(self):
        # Тока девайсы
        if self.session:
            self.session.kill()
        self.clear_all_cookies()
