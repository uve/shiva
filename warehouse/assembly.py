# coding: utf-8

import cStringIO, os.path, logging, Image, ImageFilter
from core.sw_base import BaseHandler
from avtuk.avtuk_models import Header, PastingType, StorageType
import settings as config
from barcode.zek_model import mm2pix

import urlparse

from avtuk.executor import Executor

from tornado.httpclient import HTTPError


from tornado import template
import cx_Oracle

from settings import ROOT_DIR


from core.common_tools import fetchone, fetchall

#=== Сборка ==================================================================#
class AssemblyHandler(BaseHandler):
    urls = r'/warehouse/assembly'
    
 

    def get(self):
 

        opers = [{"id":"opr%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_3"}
                 for k, v in enumerate(('-',
                                        'Без розничных продаж и подарков',
                                        'Только розничные продажи',
                                        'Только подарки клиентам'))]
        opers[0]['selected'] = "true"
        
        pasttypes = PastingType.select();
        
        storagetypes = StorageType.select();
        
        
        
        pDepart_type = 3 #pDepart_type – тип департаментов,  в данном случае константа 3 (сборщики)
        
        out = self.cursor.var(cx_Oracle.CURSOR)    
        res = self.cursor.callproc("shiva.GetSotrudList", [self.session.rc, pDepart_type, out])
                
        all_sotrud = res[-1].fetchall()
   
        
        prn = [{"id":"prn%s" % k, "type":"button", "text":"%s" % v, "action":"do_tool_4"}
                 for k, v in enumerate(('Накладная',
                                        'Паспорта качества',
                                        'Отгрузочные этикетки',
                                        'Упаковочный лист',
                                        'Сборочные'))]


        # renderSelect - do not remember last operation in buttonSelect list
 
        loader = template.Loader(os.path.join(ROOT_DIR, 'warehouse'))
        result = loader.load("assembly.js").generate(pasttypes=pasttypes, storagetypes=storagetypes, all_sotrud=all_sotrud)
       
 
 
        self.write({'def':[ 
                              
                           {'id':"btnactions", 'type':"buttonSelect", 'text':'Действия', 'openAll': 'true', 'renderSelect': 'false', 'items':
                            [                             
                             {"id":"act1", 'type':"button", 'text':'Собрать фактуру', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_save'},
                             {"id":"act2", "type":"button", "text":"Консолидировать", "action":"do_tool_consolidation"},
                             
                             {'type':"separator"},
                             {"id":"act4", 'type':"button", 'text':'Доп.информация', 'title':'Ввод дополнительной информации', 'img':"add24.png", 'action':'do_tool_edit_form'},
                             {"id":"act5", 'type':"button", 'text':'Печать паспорта качества', 'title':'Печать паспорта качества', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_4'},
                             
                             {'type':"separator"},
                             {"id":"act3", "type":"button", "text":"Расконсолидировать", "action":"do_tool_deconsolidation"},
                             {'type':"separator"},
                             {"id":"act7", "type":"button", "text":"Откатить фактуру", "action":"do_tool_rollback"}
                            ]},
                           
                           {'type':"separator"},
                           {'type':"text", 'text':"  Фильтр:"},
                           {'id':"btnopr", 'type':"buttonSelect", 'openAll': 'true', 'renderSelect': 'false', 'text':'-', 'items':opers},
                                              
                           {'type':"separator"},
                           {'type':"separator"},
                           {'id':"btnprn", 'type':"buttonSelect", 'text':'Печать', 'items':prn},

                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'},
                           
                           {'type':"separator"},
                           {'type':"button", 'action':'do_tool_test', 'text':'TEST', 'title':'TEST'}],



                    'one':[{'type':"button", 'text':'Сохранить', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_save_extinfo'},
                           {'type':"button", 'text':'Отмена', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_cancel_extinfo'},
                           '<div id="swformextinfo" />'],
                    'two':[{'type':"button", 'text':'Назад', 'img':"delete24.png", 'imgdis':"delete24g.png", 'action':'do_cancel_extinfo'},
                           ],
                    'cmd': result
                    })



#==============================================================================
class AssemblyDataHandler(BaseHandler):
    urls = r'/warehouse/assembly/data/([^/]+)'

    def get(self, param):
        w, h = 200, 142
        
                 
        head  = self.get_argument("head", 0)
        fname = self.get_argument("fname", '')
       
        header_id = self.get_argument("id", default=None)
        
        
        if param == 'item':

            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.cursor.callproc("shiva.GetHeaderAssemblyList", [header_id, None, None, None, out])
                
            all_results = fetchone(res[-1])        
                
            self.write(all_results)
            return        
        
               

        if param == 'head':

            pFilter = self.get_argument("oper", None)
            
            sotrud = self.session.uid
            
            out = self.cursor.var(cx_Oracle.CURSOR)    
            res = self.cursor.callproc("shiva.GetHeaderAssemblyList", [None, self.session.rc, pFilter, sotrud, out])
                
            all_results = fetchall(res[-1], count=0)
                
            self.write(all_results)
            return
                

        elif param == 'info':
         
            self.write(Header.get_item(head, rc=self.session.rc).as_json('prim', 'marsh_cls.name')[0])
            # self.write({'error': 'test' })
        
            
            
        elif param == 'messages':

            sql = "select t.code,t.name,f.valume from factura f left join tovar t on isclad.GetTovarFromModify(f.tovar)=t.id where f.header=:pHeader"

            self.write_XML(Executor.exec_cls(sql, pHeader=head)
                           .as_grid('code', 'name', 'valume'))
                        

        elif param == 'tovar':

            sql = "select t.code,t.name,f.valume from factura f left join tovar t on isclad.GetTovarFromModify(f.tovar)=t.id where f.header=:pHeader"

            self.write_XML(Executor.exec_cls(sql, pHeader=head)
                           .as_grid('code', 'name', 'valume'))


        elif param == 'print':
            
            sql = '''SELECT p.num, t.name, v.category,
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
            for i in Executor.exec_cls(sql, head=head, rc=self.session.rc):
                try:
                    fname = i.sertfile.decode('utf8')
                    if not fname: raise Exception()

                    if fname not in self.application.passport_cash:
                        Image.open(os.path.join(config.SHIVA_PASSPORT, fname))
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
                        doc.write('<img width="%s" height="%s" src="/warehouse/assembly/data/image?fname='+fn[i]+'">');
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


        elif param == 'image':
            try:
                imgdata = cStringIO.StringIO()

                fname = os.path.join(config.SHIVA_PASSPORT, urlparse.unquote(fname).decode('utf8'))
                im = Image.open(fname).rotate(270).resize(mm2pix((w, h,)), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
                im.save(imgdata, format='jpeg')
                imgdata.seek(0)
                self.write(imgdata.read())

                self.set_header("Content-Type", "image/jpeg")
            except Exception, e:
                logging.error(e)
                raise HTTPError(404)



    def post(self, param):
        
        header_id = self.get_argument("ids", default=None)
        pOkNoParty = self.get_argument("pOkNoParty", default=0)
            
        if param == 'gts':                                 
            
            self.cursor.callproc("shiva.AddShedulerHeader", [header_id, pOkNoParty, self.session.uid])            
            #self.write({'info':'Сформированы задания на сборку'})
            
            return
        


        elif param == 'save':

            header_id = self.get_argument("id",    default=None)
            skin    = self.get_argument("skin",    default=None)
            desk    = self.get_argument("desk",    default=None)
            prim    = self.get_argument("prim",    default=None)
            pallet  = self.get_argument("pallet",  default=None)
            os_numb = self.get_argument("os_numb", default=None)            
            storage = self.get_argument("storage", default=None)
            
            packing = self.get_argument("packing", default=0)
            sotrud1 = self.get_argument("sotrud1", default=None)
            sotrud2 = self.get_argument("sotrud2", default=None)
            
            
            out = self.cursor.var(cx_Oracle.STRING)    
            res = self.cursor.callproc("shiva.SetHeaderInfo", [header_id,
                                                               pallet,
                                                               os_numb,
                                                               prim,
                                                               skin,
                                                               storage,
                                                               desk,
                                                               packing,
                                                               sotrud1,
                                                               sotrud2,
                                                               out])
                
            result = str(res)

            self.write({'info':'Информация сохранена'})
   





        elif param == 'consolidation':            


            out = self.cursor.var(cx_Oracle.STRING)    
            res = self.cursor.callproc("tsclad.MakeTotalHeaderNew", [header_id, out])
                
            result = str(res)
            
            self.write({'info':'Консолидация выполнена: фактуры: %s' % result, 'ids': result})



        elif param == 'deconsolidation':            

            result = self.cursor.callproc('tsclad.DelTotalHeaderSclad', [header_id])       
            self.write({'info':'Расконсолидация выполнена успешно'})

                
        elif param == 'rollback':            
            
            result = self.cursor.callproc('shiva.RollbackHeader', [header_id, cx_Oracle.NUMBER])       

            self.write({'info':'Откат фактуры выполнен успешно'})
               



