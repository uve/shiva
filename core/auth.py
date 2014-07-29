# coding: utf-8

from core.sw_base import BaseHandler

from core.common_tools import fetchone
from barcode.zek_model import barcode2depart_sid

import cx_Oracle
import os
from core.sw_base import md5passw
from settings import ROOT_DIR

from tornado import template

from core.sessions import SessionManager

#=============================================================================#
class AuthHandler(BaseHandler):
    urls = r'/auth'

    def get(self):
        
        loader = template.Loader(os.path.join(ROOT_DIR, 'core'))
        result = loader.load("auth.js").generate()
       

        self.write({'def':'<div id="sw_form" style="position:relative; top:50%; left:50%; margin:-105px 0 0 -115px;" />',
                    'cmd':result })
        

    def post(self):
        
        
        barcode = self.get_argument("barcode", None)
        login   = self.get_argument("login", None)
        passw   = self.get_argument("passw", None)
        user_id = None
        depart  = None
        
        
        if self.session and self.session.uid:
            user_id = self.session.uid
            
        elif barcode:
            depart, user_id = barcode2depart_sid(barcode)            
        
        elif login and passw:
            #login = str(login).upper()
            #passw = md5passw(login, str(passw))
            login = str(login)
            passw = str(passw)

        else:
            self.write({'error':'Пользователь не найден',
                            'cmd':'self.NetSend("/auth")'})
            return
        
                        
        out = self.cursor.var(cx_Oracle.CURSOR)    
        res = self.proc("shiva.Get_User", [login, passw, user_id, depart, out])               
                        
        user = fetchone(res[-1])
        
        if not user:
            self.write({'error':'Пользователь не найден',
                            'cmd':'self.NetSend("/auth")'})
            return
        

        '''
        if not "role" in user:
        
            sql = "SELECT id, name FROM sw_roles
                  WHERE id = ( SELECT UNIQUE CASE 
                                 WHEN s.role=1 THEN s.role
                                 WHEN h.role IS NOT NULL THEN h.role
                                 WHEN s.role IS NOT NULL THEN s.role  
                                 ELSE NULL
                               END
                               FROM sotrud s
                               LEFT JOIN sw_role_history h ON s.id=h.sotrud AND h.role_end IS NULL
                               WHERE s.id=:id AND ROWNUM<=1 )"
            
            self.execute(sql, id=user["id"])

            user["role"], user["role_name"] = self.cursor.fetchone()
        '''
          
        self.session = SessionManager(user["id"], user["role"])
                
        
        self.session.rc = user["rc"]
        
        
        
        self.set_cookie('uid', str(user["id"]))
        self.set_cookie('role',str(user["role"]))
        self.set_cookie('rc',  str(user["rc"]))

        self.set_cookie('name', str(user["name"]))
        
        #user["user_name"]   = user["name"]        
        #user["role_name"]   = user["role_name"]
        #user["depart_name"] = user[""]
        
        #self.write({'user_name':user.name, 'depart_name':user.depart_cls.name, 'role_name':user.current_role_cls.name })
      
        self.write(user)

        
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
