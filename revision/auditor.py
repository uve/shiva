#!/usr/bin/env python
# -*- coding: utf8 -*- 

from core.sw_base import BaseHandler

import settings as config

import json
# from barbam_models import AssemblyList

import os
from settings import ROOT_DIR


from tornado import template
from settings import TEMPLATE_DIR
import cx_Oracle


import time

from core.common_tools import fetchall, fetchone, fetchall_by_name

from avtuk.avtuk_models import RC
#===  =========================================================
class AuditorHandler(BaseHandler):
    urls = r'/revision/auditor'

    def get(self):
                                 

        self.cursor.execute("select id, name from tehno.type_tovar where hide=1 order by name")     
        all_types = self.cursor.fetchall()                                        
  
                        
        loader = template.Loader(os.path.join(ROOT_DIR, 'revision'))
        result = loader.load("auditor.js").generate(all_types=all_types)
       
        all_departs = RC.get_current().depart_cls
        # кнопки с департаментами РЦ
        
        departs = [{"id":"%s" % i.id, "type":"button", "text":i.name} for i in all_departs]       
       
        self.write({'def':[
                           
                           {'type':"text", 'text':"Подразделение:"},
                           {'id':'departs', 'type':"buttonSelect",  'mode':'select', 'selected': all_departs[0].id,  'items':departs},
                           {'type':"separator"},
                           
                           {'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_print'},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_revision', 'text':'Отправить задание на терминал'},
                           '''<table style='width:100%'>
                                <tr>
                                    <td style="width:200px;"><select style="width:100%;" id="combo_zone2" name="alfa1"></select></td>
                                    <td style="width:400px;"><select style="width:100%;" id="combo_zone1" name="alfa1"></select></td>                                    
                                </tr>
                                <tr>
                                    <td colspan="2"><span>Список ячеек с продуктом:</span></td>
                                    <td style="padding-left: 10px;"><span>Товарные остатки:</span>  <b id="tovarsaldo"></b>  </td> 
                                </tr>
                                <tr><td colspan="2"><div id='sw_grid1' style="width:100%; height:250px;"></div></td></tr>
                                <tr><td colspan="2"><span>История ячейки:</span></td></tr>
                                <tr><td colspan="2"><div id='sw_grid2' style="width:100%; height:300px;"></div></td></tr>
                                
                              </table>                             
                           '''],

                    'cmd': result
         
            })


#==============================================================================
class AuditorDataHandler(BaseHandler):
    urls = r'/revision/auditor/data/([^/]+)'


    def get(self, param):

        cell_id = self.get_argument("cell_id", None)
         
        depart = self.get_argument("depart", None)
            
        typet = self.get_argument("typet",  "0")  
        tovar = self.get_argument("tovar", "0")
        mode  = self.get_argument("mode",  "0")

        out = self.cursor.var(cx_Oracle.CURSOR) 
        
        if param == 'tovars':
                
            self.cursor.execute("select id, code, name from tovar where hide=1 and typet=%s order by name" % typet)     
            results = self.cursor.fetchall()
            
            self.write(results)
            
            return       

        if param == 'head':
                        
            if mode == '0':   
 
                res = self.cursor.callproc("shiva.GetRevisionSaldoCell", [depart, tovar, out])  
                
                all_results = fetchall(res[-1])
                
                self.write(all_results)  
                return
            

            
            if mode == '1':
                
                epoch_time = int(time.time())
    
                data = cx_Oracle.DateFromTicks(epoch_time)
                obor = "+"
                
                #data_s = data_e = "26.08.2013"
                
                result = self.cursor.callfunc('sclad.GetSaldoTovar', cx_Oracle.NUMBER, parameters=[tovar, depart, data, obor])
                                                               
                isp = json.dumps(int(result))
                                
                self.write(isp)
                
                return  


            #Список остатков по партиям. Временно отключен!
            if mode == '2':   
            
                sql = '''select p.party, p.num, to_char(p.data,'DD.MM.YYYY') data, p.inbox, tsclad.GetPartyOst(p.party,%s) saldo from party p  
                        where p.tovar=%s and tsclad.GetPartyOst(p.party,%s)>0''' % (depart, tovar, depart)                  

                self.cursor.execute(sql)     
                results = fetchall(self.cursor)                                        
                
                self.write(results)
                
                
                return

        #Список остатков по партиям. Временно отключен!
        elif param == 'cell_history':
                
            res = self.cursor.callproc("shiva.getpallethistory", [cell_id, out])  
            
            all_results = fetchall(res[-1])
            
            self.write(all_results)  
            return
            
            
            
            return
            
        ###### ПЕЧАТЬ ######     
            
        elif param == 'print':
            
            
            sql = "select id, code, name from tovar where id=%s"  % tovar

            self.cursor.execute(sql)        
            result = fetchone(self.cursor)
                
                           
            try: tovar_name = result["name"]
            except: tovar_name = ""   
            
            try: tovar_code = result["code"]
            except: tovar_code = ""                         
                                                    
            sql = '''Select tp.name, p.num, p.inbox, pp.tovar_place, 
                        shiva.GetSaldoCell(tp.id,Null) saldo,  to_char(p.data,'DD.MM.YYYY') data
                        from palet_place pp, sw_palete_party spp, party p, tovar_place tp
                        where  pp.tovar_place=tp.id and tp.depart in (3,16) and tp.status=1 and 
                        pp.end_date is Null and pp.palete=spp.palete and spp.party_id=p.party and 
                        p.tovar=%s
                        order by tp.name''' % tovar
    
            self.cursor.execute(sql)        
            result_mode1 = fetchall_by_name(self.cursor)
            #result_mode1 = Executor.exec_cls(sql, pTovar=tovar, multi=True)            
            
            total1 = sum(item["saldo"] for item in result_mode1)

    
            sql = '''select p.party, p.num, p.inbox, 
                         tsclad.GetPartyOst(p.party,3)+tsclad.GetPartyOst(p.party,16) saldo,
                         to_char(p.data,'DD.MM.YYYY') data
                         from party p 
                         where p.tovar=%s and 
                         tsclad.GetPartyOst(p.party,3)+tsclad.GetPartyOst(p.party,16)>0''' % tovar
    
            #result_mode2 = Executor.exec_cls(sql, pTovar=tovar, multi=True)
            result_mode2 = self.cursor.fetchall()
            
            total2 = sum(item["saldo"] for item in result_mode2)   
    
    
            result = self.cursor.callfunc('isclad.GetTovarSaldoSclad', returnType=cx_Oracle.NUMBER, parameters=[tovar, 1])                                               
            total3 = json.dumps(int(result))   
            
            
            loader = template.Loader(TEMPLATE_DIR)        
            output = loader.load("auditor.html").generate(data1=result_mode1, total1=total1,
                                                          data2=result_mode2, total2=total2,
                                                          tovar_name=tovar_name, tovar_code=tovar_code,
                                                          total3=total3)
        
        
           
        
            output = output.replace('\n', '').replace('\r', '')
            
            self.write({'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output})       


        elif param == 'maketaskrevision':
            
            pRevision = cx_Oracle.NUMBER

            result = self.cursor.callfunc('shiva.MakeTaskRevision', returnType=[tovar, self.session.rc], parameters=[pRevision])                        

            
            self.write({'info':'Задание на ревизию сформировано'})
                       
            return
            # pTovar - tovar.id
            # pSclad -     в начальных установках shiva где-то есть номер РЦ , для ЦС он 1
            # pRevision - варианты возвратного параметр пока неопределены            
