# coding: utf-8

from core.sw_base import BaseHandler, md5passw
from avtuk.avtuk_models import User


#=== Смена пароля ============================================================#
class ChangePasswHandler(BaseHandler):
    urls = r'/admin/chpassw'

    def get(self):
        self.write({'def':[{'type':"button", 'text':'Сменить', 'img':"id_card24.png", 'imgdis':'id_card24g.png', 'action':'do_tool_1'},
                           '<div id="sw_form"></div>' ],
                    'cmd':'''var sw_chpassw = new dhtmlXForm("sw_form",[
                        {type: "label", label: "Старый пароль:"},
                        {type:"password", name:"pass1"},
                        {type: "label", label: "Новый пароль:"},
                        {type:"password", name:"pass2"} 
                      ]);
                      window.Cleaner.push(sw_chpassw);
                                            
                      window.do_tool_1 = function(){
                          self.NetSend("/admin/chpassw", sw_chpassw.Serialize() );
                          sw_chpassw.setItemValue('pass1','');
                          sw_chpassw.setItemValue('pass2','');                          
                      }'''})


    def post(self):
        try:
            inp = self.input(pass1='', pass2='')
            user = User.get(id=self.session.uid)
            s = user.sotrud.upper()
            if user.password == md5passw(s, inp.pass1):
                user.password = md5passw(s, inp.pass2)
                user.save()
            else:
                raise Exception()

            self.write({'info':'Пароль изменен'})
        except:
            self.write({'error':'Ошибка смены пароля!'})
