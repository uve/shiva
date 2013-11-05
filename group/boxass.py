#!/usr/bin/env python
# -*- coding: utf-8 --

from core.sw_base import BaseHandler
from avtuk.avtuk_models import User, Factura, NotInPeriodException, NotUserException

from barcode.zek_model import box_label_size, box_label
import cx_Oracle

from avtuk.executor import Executor

#==============================================================================
          
                
                
class BoxAssembleHandler(BaseHandler):
    urls = r'/group/boxass'
    

    def get(self):
        self.write({'def':['<div id="sw_form" style="padding:10px;"></div>'],

                    'cmd':'''var sw_boxass = new dhtmlXForm("sw_form",[
                        {type: "label", label: "Штрих-код бэйджика:"},
                        {type:"input", name:"badge"}
                    ]);
                    window.Cleaner.push(sw_boxass);
                   
                    var badge_input = sw_boxass.doWithItem("badge", "getInput");
                    
                    badge_input.onkeypress = function(e){
                        var s = badge_input.value;
                        
                        console.log(s);
                        
                        if(s.length > 10){
                            if(s.length < 12){
                                self.NetSend("/group/boxass", "badge="+s+String.fromCharCode(e.charCode));
                            }
                            setTimeout(window.clr_input, 100);                            
                        }
                    } 
                                        
                    window.clr_input = function(){
                        badge_input.value = '';
                        badge_input.focus();
                    }
                    
                    window.clr_input();'''
                    })

    def post(self):
        try:
            user = User.get_auth(self.input(badge='').badge)
            if not user:
                raise NotUserException()

        except NotUserException:
            self.write({'error':'Пользователь не найден',
                        'cmd':'window.clr_input();'})
            return

        except NotInPeriodException:
            self.write({'error':'Пользователь не в смене',
                        'cmd':'window.clr_input();'})
            return

        except:
            self.write({'error':'Проблемы с сервером (boxass)',
                        'cmd':'window.clr_input();'})
            return


        # Сборщик покоробочной зоны 
        if user.role == 9:            
            self.write(self.print_boxass(user))

        # Сборщик поштучной зоны
        elif user.role == 22:
            pass

        # Комплетовщик поштучной зоны
        elif user.role == 23:
            pass

        else:
            self.write({'error':'Не санкционированный доступ!!!!',
                        'cmd':'window.clr_input();'})



    def print_boxass(self, user=None, m_factura=None, m_start=None, m_end=None):
        # TODO: Аленина функция проверки необходимости печати
        
        
        isp = 1
        
        m_name = ""
        
        if user:
               
            
            result = self.cursor.callfunc('shiva.GetNeedLabel', returnType=cx_Oracle.NUMBER, parameters=[user.id])                                               
            isp = int(result)
            
        
            sql = '''SELECT MIN(m_start) f, MAX(m_end) l, factura
                     FROM packlist 
                     WHERE sotrud=(SELECT sotrud FROM sotrud WHERE id = :sid)
                       AND dend IS NULL
                    GROUP BY factura'''
        
     
            x = Executor.exec_cls(sql, multi=False, sid=user.id)
            
            try:
                m_start = x.f
                m_end = x.l
                m_factura = x.factura 
                m_name = user.name
            except:
                pass
    
        
        if m_factura and isp == 1:
            return {'info':m_name,
                        'precmd':'self.InitContent();',
                        'def':['<div id="sw_mess" style="padding:10px;">Фактура: %s, места: %s..%s</div>' % (m_factura, m_start, m_end)],
                        'cmd':'''var urs=[%s,%s];
                            for(i=%s; i<=%s; i++)
                                urs.push("/group/boxass/data?factura=%s&position="+i +"&time="+new Date().getTime() );
                            self.PrintURL.apply(self, urs);   
                                                
                            setTimeout(function(){ self.Refresh() }, 3000);
                        ''' % (box_label_size[0], box_label_size[1], m_start, m_end, m_factura)}
                
    
    
        elif isp == 0:
            return {'info':m_name,
                        'precmd':'self.InitContent();',
                        'def':['<div id="sw_mess" style="padding:10px;"> Тип  оклейки  не покоробочный, печати отгрузочных этикеток не требуется</div>'],
                        'cmd':'setTimeout(function(){ self.Refresh() }, 2000);'}
                        
        else:
            return {'info':m_name,
                        'precmd':'self.InitContent();',
                        'def':['<div id="sw_mess" style="padding:10px;">Печать не нужна</div>'],
                        'cmd':'setTimeout(function(){ self.Refresh() }, 2000);'}
        
        
#==============================================================================
class BoxAssembleDataHandler(BaseHandler):
    urls = r'/group/boxass/data'

    def get(self):
        inp = self.input(factura=0, position=0)

        factura = Factura.get(header=int(inp.factura))
        # print 'FF', factura
        
       
        z = box_label(u"%s\\%s" % (factura.header_cls.num, factura.header),
                       factura.header_cls.client_to_cls.sender,
                       factura.header_cls.client_from_cls.bank_cls.phone,
                       factura.header_cls.client_to_cls.bank_cls.adress,
                       factura.header_cls.client_to_cls.name,
                       factura.header_cls.client_to_cls.bank_cls.phone,
                      inp.position, factura.header_cls.os_numb or 0)
        
        
        self.write(z)
        self.set_header("Content-Type", "image/svg+xml")
