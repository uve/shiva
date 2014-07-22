# coding: utf-8

#import cStringIO, os.path, Image, ImageFilter
from core.sw_base import BaseHandler

#import settings as config
import logging
import random 

from barcode.zek_model import mm2pix, assembly_bar_label

import urlparse
import datetime

import urllib

from tornado import template

import os
from settings import ROOT_DIR
from tornado.httpclient import HTTPError


from avtuk.avtuk_models import Header, Document, AssemblyList, ListAssembly, Package


from core.common_tools import fetchall_by_name

import cStringIO, os.path, logging, Image, ImageFilter
from avtuk.executor import Executor

from settings import SHIVA_PASSPORT, IMAGES_SERVER_IP, TEMPLATE_DIR


#=== Печать паспортов =========================================================
class PrintPassportHandler(BaseHandler):
    urls = r'/warehouse/printpassport'

    def get(self):
        prn = [{"id":"prn%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_4"}
                 for k, v in enumerate(('Накладная',
                                        'Паспорта качества',
                                        'Отгрузочные этикетки',
                                        'Упаковочный лист',
                                        'Сборочные'))]

        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
                 for k, v in enumerate(('-',
                                        'Без розничных продаж и подарков',
                                        'Только розничные продажи',
                                        'Только подарки клиентам'))]
        opers[0]['selected'] = "true"

        st = datetime.datetime.now().strftime('%d.%m.%Y')

        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("printpassport.js").generate()




        self.write({'def':[{'type':"text", 'text':"Дата с:"},
                           {'id':"cal1", 'type':"buttonInput", 'width':60, 'value':st},
                           {'type':"text", 'text':" по:"},
                           {'id':"cal2", 'type':"buttonInput", 'width':60, 'value':st},

                           {'type':"separator"},
                           {'type':"text", 'text':"  Фильтр:"},
                           {'id':"btnopr", 'type':"buttonSelect", 'text':'', 'items':opers},

                           {'type':"separator"},
                           {'type':"separator"},
                           {'id':"btnprn", 'type':"buttonSelect", 'text':'Печать', 'items':prn},

                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}],

                    'cmd': result
                    })



#==============================================================================
class Passport:
    pass


import httplib


class PrintPassportDataHandler(BaseHandler):
    urls = r'/warehouse/printpassport/data/([^/]+)'

    def is_exists(self, path):

        try:
            conn = httplib.HTTPConnection(IMAGES_SERVER_IP)
            conn.request('HEAD', "/" + path)
            response = conn.getresponse()
            conn.close()
            return response.status == 200

        except:
            return False




    def get(self, param):
        
        
        w, h = 200, 142
        inp = self.input(oper=0, head=0, fname='', mode='', d='', depart=0)

        try:head = int(inp.head)
        except:head = 0

        if param == 'head':
            try: oper = int(inp.oper)
            except: oper = 0

            try: ds = datetime.datetime.fromtimestamp(int(int(inp.d1) / 1000))
            except: ds = datetime.datetime.now()
            ds = ds.date()

            try: de = datetime.datetime.fromtimestamp(int(int(inp.d2) / 1000))
            except: de = datetime.datetime.now()
            de = de.date()

            self.write_XML(Header.select_passport(oper, ds, de, rc=self.session.rc)
                           .as_grid('id', 'num', 'date', 'client_to_cls.name', 'oper_cls.name', 'status_cls.name',
                                    show={'date':lambda val: val.strftime("%d.%m.%Y")}))
            
        elif param == 'print':
            try: mode = int(inp.mode)
            except: raise HTTPError(404)
            
            

            # Накладная
            if mode == 0:                
                
                '''
                out = self.cursor.var(cx_Oracle.CURSOR)                           
                res = self.proc("shiva.header_info", [header_id, out])                  
                results = res[-].fetchone()
                
                результат 
                         id,  
                         num,          -- номер
                         data,          -- дата
                         client_from, -- от кого
                         client_to      -- кому
                 '''
                
        
     
                new_document = Document(self.request.arguments, rc=self.session.rc)                
                return self.write(new_document.as_print())
                                                          

            # Сборочные
            elif mode == 4:
                new_document = AssemblyList(self.request.arguments, rc=self.session.rc)                
                return self.write(new_document.as_print())                 
                # self.write({'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % AssemblyList(head).dump()})
                
            # Упаковочный лист
            elif mode == 3:
                # self.write({'info':'В разработке'})
                new_document = Package(self.request.arguments, rc=self.session.rc)                
                return self.write(new_document.as_print())                      
                
            # Паспорта качества
            elif mode == 10:
                sql = '''SELECT distinct p.num, t.name, v.category,
                                tsclad.getpartysertfile(p.party, :rc) sertfile,
                                SUBSTR(isclad.GetTovarCodeFromModify(t.id), 1, 25) code
                         FROM factura f
                         JOIN tovar t ON f.tovar = t.id
                         LEFT JOIN recordp r on f.id = r.factura
                         JOIN party p on r.party=p.party
                         LEFT JOIN type_tovar v ON t.typet=v.id
                         WHERE f.header = :head AND v.CATEGORY<>5
                         ORDER BY category, name'''

                good = []
                errn = []

          
                                     
                ret = {}
                for i in Executor.exec_cls(sql, rc=self.session.rc, head=head):
                    try:
                        fname = i.sertfile.decode('utf8')
                        if not fname: raise Exception()

                        if fname not in self.application.passport_cash:
                            Image.open(os.path.join(SHIVA_PASSPORT, fname))
                            self.application.passport_cash[fname] = None

                        if fname not in good: good.append(fname)
                    except:
                        errn.append("'%s','%s','%s','%s'" % (i.num, i.code, i.name, '-' if i.sertfile is None else i.sertfile))
                        continue

                if errn: ret['warning'] = ["Не найден паспорт<br/>%s" % i for i in errn]


                goods = u','.join("'%s'" % i for i in good)
                errns = u','.join(u"[%s]" % i.decode('utf8') for i in errn)

                cmd = u'''var fn=[%s]; var er=[%s];
    
                    self.Incunable(function(doc){                
                        for(var i in fn){
                            doc.write('<img width="%s" height="%s" src="/warehouse/printpassport/data/image?mode=1&fname='+fn[i]+'">');
                        }
                        
                        if(!!(fn.length %% 2)){
                            doc.write('<div style="height:600px;"><br/></div>');
                        }                    
                        
                        if(er.length){
                            doc.write('<br/><br/><div>Не найдены паспорта качества:</div><table style="border:1 solid #000;">');
                            
                            var hd=['N','Партия','Код','Товар','Паспорт'];
                            doc.write('<tr>');
                            for(var i in hd)
                                doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+hd[i]+'</td>');
                            doc.write('</tr>');
                                                
                            for(var i in er){
                                doc.write('<tr>');
                                doc.write('<td style="padding:3px; border-bottom:1 solid #888; border-right:1 solid #000;">'+(1+parseInt(i))+'</td>');
                                for(var j in er[i])
                                    doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+er[i][j]+'</td>');
                                doc.write('</tr>');
                            }                        
                            doc.write('</table>');                        
                        }               
                    });''' % (goods, errns, int(3.47 * w), int(3.47 * h))

                ret['cmd'] = cmd.encode('utf8')
                self.write(ret)

                return 
            # Паспорта качества
            elif mode == 1:
                
                sql = '''SELECT distinct p.num, t.name, v.category,
                                tsclad.getpartysertfile(p.party, %s) sertfile,
                                SUBSTR(isclad.GetTovarCodeFromModify(t.id), 1, 25) code
                         FROM factura f
                         JOIN tovar t ON f.tovar = t.id
                         LEFT JOIN recordp r on f.id = r.factura
                         JOIN party p on r.party=p.party
                         LEFT JOIN type_tovar v ON t.typet=v.id
                         WHERE f.header = %s AND v.CATEGORY<>5
                         ORDER BY category, name''' % (self.session.rc, head)

                res = self.execute(sql)
                good = fetchall_by_name(res)

          
                
                all_passports = []
                for item in good:
                    name = item["sertfile"]
                    if not name: continue
                    
                    new_passport = Passport()

                    new_passport.category = item["category"]
                    new_passport.code     = item["code"]
                    new_passport.num      = item["num"]
                    
                    new_passport.name  = name
                    new_passport.value = urllib.quote(name.decode('utf-8').encode('koi8-r'))


                    new_passport.exist = self.is_exists(new_passport.name)

                    all_passports.append(new_passport)

                                                    
                
                loader = template.Loader(TEMPLATE_DIR)

                #all_passports[-1].exist = False    #just for testing..
                

                RC_IP = '192.168.0.1'
                if self.request.remote_ip in ["80.89.129.114", "127.0.0.1", "::1"]:
                    RC_IP = IMAGES_SERVER_IP

                results = loader.load("printpassport.html").generate(remote_ip=self.request.remote_ip, RC_IP=RC_IP, all_passports=all_passports, width=str(int(3.47 * w)), uniq=random.random())

                self.write(results)
                return

                
            # Отгрузочные этикетки
            elif mode == 2:
                
                d = []
                
                try:
                    d = [int(i) for i in inp.d.split(',') if not i is None]
                    d.sort()
                except:
                    pass

                if len(d):
                    # self.write( print_boxass(user=None, m_factura=head, m_start=m_start, m_end=m_end) )
                    
                    self.write({'error':'Печать отключена'})
                    return
                    # self.write({'info':'В разработке'})
                else:
                    self.write({'error':'Неверные параметры'})


        elif param == 'image':
            try: mode = int(inp.mode)
            except: raise HTTPError(404)

            logging.info('Printing image')
            
            
            # Накладная
            if mode == 0:
                self.write({'info':'В разработке'})
                

             # Паспорта качества
            elif mode == 1:

                self.write({'info':'В разработке'})

                '''
                try:
                    imgdata = cStringIO.StringIO()

                    logging.info("Before: %s", inp.fname)
                    fname = os.path.join(SHIVA_PASSPORT, urlparse.unquote(inp.fname).decode('utf8'))
                    im = Image.open(fname).rotate(270).resize(mm2pix((w, h,)), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)


                    im.save(imgdata, format='jpeg')
                    imgdata.seek(0)
                    self.write(imgdata.read())

                    self.set_header("Content-Type", "image/jpeg")
                except Exception, e:
                    logging.error(e)
                    raise HTTPError(404)
                '''

                return                

            # Отгрузочные этикетки
            elif mode == 2:
                self.write({'info':'В разработке'})

            # Упаковочный лист
            elif mode == 3:
                self.write({'info':'В разработке'})

            # Сборочные
            elif mode == 4:
                try:depart = int(inp.depart)
                except:depart = 0

                try:
                    self.write(assembly_bar_label(ListAssembly.get(depart=depart, header=head).id))
                    self.set_header("Content-Type", "image/svg+xml")
                except:
                    raise HTTPError(404)
