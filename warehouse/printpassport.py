# coding: utf-8

#import cStringIO, os.path, Image, ImageFilter
from core.sw_base import BaseHandler

#import settings as config
import logging

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

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        columns: [
  { type:"ro", sort:"int",  align:"right", width:"68",  label:["ID", "#text_filter"], },  
  { type:"ro", sort:"int",  align:"right", width:"46",  label:["Номер", "#text_filter"] },
  { type:"ro", sort:"date", align:"right", width:"66",  label:["Дата", "#select_filter"] },
  { type:"ro", sort:"str",  align:"left",  width:"*",   label:"Получатель" },
  { type:"ro", sort:"str",  align:"left",  width:"290", label:["Операция", "#select_filter"] },
  { type:"ro", sort:"str",  align:"left",  width:"100", label:["Статус", "#select_filter"] }
                            ]
                        });
                            
                            sw_grid.enableMultiselect(true);
                                                             
                            window.Cleaner.push(sw_grid);
                            
                            var bar = this.Toolbars["def"];
                            
                            var calendar1 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal1"].obj.firstChild );
                            calendar1.loadUserLanguage("ru");
                            calendar1.setDateFormat("%d.%m.%Y");
                            calendar1.hideTime();
                            calendar1.setDate(new Date());                                                       
                            window.Cleaner.push(calendar1);
                                                        
                            var calendar2 = new dhtmlxCalendarObject( bar.objPull[bar.idPrefix+"cal2"].obj.firstChild );
                            calendar2.loadUserLanguage("ru");
                            calendar2.setDateFormat("%d.%m.%Y");
                            calendar2.hideTime();
                            calendar2.setDate(new Date());
                            window.Cleaner.push(calendar2);
                                                        
                            calendar1.attachEvent("onClick", function (){ window.do_tool_3() });
                            calendar2.attachEvent("onClick", function (){ window.do_tool_3() });                            
                            
                            window.do_tool_csv = function(){ self.GridCSV(sw_grid) }                            
                            window.ids = 0;
                                                                                        
                            // print passport
                            window.do_tool_4 = function(ids2){
                                var ids = sw_grid.getSelectedRowId();
                                if(!ids) self.AddMessage('Выберите фактуру',2)
                                else {
                                    var m=ids2.substr(3);
                                    var d='';
                                    //Отгрузочные этикетки
                                    if(m==2){
                                        var d=prompt('Диапазон мест разделенные пробелом','').split(' ');
                                    }
                                    self.NetSend("/warehouse/printpassport/data/print?head="+ids+"&mode="+m+"&d="+d);
                                }                                
                            }

                            // фильтр
                            window.do_tool_3 = function(ids2){
                                if(!!ids2){
                                    window.ids=ids2.substr(3);
                                    var text = self.Toolbars["def"].getListOptionText("btnopr", ids2);
                                    self.Toolbars["def"].setItemText("btnopr", text);
                                }
                                var d1=calendar1.getDate().valueOf();
                                var d2=calendar2.getDate().valueOf();                                                            
                                self.LoadGrid(sw_grid, "/warehouse/printpassport/data/head?oper="+window.ids+"&d1="+d1+"&d2="+d2);
                            }
                            window.do_tool_3("opr0");'''
                    })



#==============================================================================
class Passport:
    pass

class PrintPassportDataHandler(BaseHandler):
    urls = r'/warehouse/printpassport/data/([^/]+)'

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

                res = self.cursor.execute(sql)
                good = fetchall_by_name(res)

          
                
                all_passports = []
                for item in good:
                    name = item["sertfile"]
                    if not name: continue
                    
                    new_passport = Passport()
                    
                    new_passport.name  = name
                    new_passport.value = urllib.quote(name.decode('utf-8').encode('koi8-r'))                    
                    
                    all_passports.append(new_passport)
                                                    
                
                loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
                
                
                RC_IP = 'http://46.28.129.222'
                if self.request.remote_ip == "46.28.129.222":
                    RC_IP = 'http://192.168.0.1'
                                
                cmd = loader.load("printpassport.js").generate(RC_IP=RC_IP, all_passports=all_passports, width=str(int(3.47 * w)) )            
    
    
                ret = {}
                ret['cmd'] = cmd#.encode('utf8')
                self.write(ret)
                
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
