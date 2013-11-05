  # coding: utf-8

import logging, time
from core.sw_base import BaseHandler
import settings as config
from avtuk.avtuk_models import User

#=== Статистика по SHIVA и HULK ==============================================#
class SysStatHandler(BaseHandler):
    urls = r'/admin/sys'

    def get(self):
        # данные, которые будут вытаскиваться из Халка

        self.write({'def':[{'type':"button", 'text':'kill Shiva', 'img':"process24.png", 'action':'do_tool_1'},
                           '''
                           <div id="grid_status" style="height:100px; width:600px;"></div>
                           
                           <div id="sw_form_a"></div>                           
                           <div id="tbshiva" style="height:100px; width:100%;"></div>
                           '''],

                    'cmd':'''
                    
                    
                            var sw_grid1 = new dhtmlXGridObject({
                                parent: "grid_status",   
                                xml:"/admin/sys/status",                                                     
                                columns:[
          { type:"ro", sort:"str", align:"left", width:"200",   label:"Версия" },
          { type:"ro", sort:"str", align:"left", width:"*", label:"Время старта" },
          { type:"ro", sort:"str", align:"left", width:"100", label:"Время работы" },
          { type:"ro", sort:"str", align:"left", width:"100", label:"Количество потоков" },
          { type:"ro", sort:"str", align:"left", width:"100",  label:"Размер очереди" }
                                ]});
                            
                            window.Cleaner.push(sw_grid1); 
                              
                                    
                    
                            var sw_grid = new dhtmlXGridObject({
                                parent: "tbshiva",
                                xml:"/admin/sys/data",
                                columns:[
          { type:"ro", sort:"str", align:"left", width:"*",   label:"Сотрудник" },
          { type:"ro", sort:"str", align:"left", width:"180", label:"Основная роль" },
          { type:"ro", sort:"str", align:"left", width:"180", label:"Подразделение" },
          { type:"ro", sort:"str", align:"left", width:"120", label:"Активность" },
          { type:"ro", sort:"str", align:"left", width:"60",  label:"ТСД" },
          { type:"ro", sort:"str", align:"left", width:"90",  label:"IP" }
                                ]});
                                
                            window.do_tool_1 = function(){
                                if("42"==prompt("Ответ на главный вопрос?","")){                
                                  self.NetSend("/admin/sys/data?kill=shiva");
                                }else{
                                  self.AddMessage("Не угадал",2)
                                }
                            }
                                
                            window.Cleaner.push(sw_grid);
                            
                            
                            ''' 
                                           
                   })

        '''
                    % (str(hlk['HULK_VERSION']),
                                                        str(hlk['START_TIME']),
                                                        str(hlk['ELAPSED_TIME']),
                                                        str(hlk['THREADS']),
                                                        str(hlk['QUEUE_SIZE']),
                                                        config.SHIVA_VERSION,)
                    '''   
#=============================================================================#

class SysStatDataHandlerStatus(BaseHandler):
    urls = r'/admin/sys/status'

    def get(self):
        
        hlk = {'HULK_VERSION':'unknown', 'THREADS':'unknown',
               'QUEUE_SIZE':'unknown', 'START_TIME':'unknown',
               'ELAPSED_TIME':'unknown'}
        try:

                    
            self.write_XML('<rows>')
            
            result = ''    
            # items = hlk
    
            # for item in items:
            #    result += '<cell><![CDATA[%s]]></cell>' % str(hlk[item])

            result += '<cell><![CDATA[%s]]></cell>' % hlk['HULK_VERSION']
            result += '<cell><![CDATA[%s]]></cell>' % hlk['START_TIME']
            result += '<cell><![CDATA[%s]]></cell>' % hlk['ELAPSED_TIME']
            result += '<cell><![CDATA[%s]]></cell>' % hlk['THREADS']
            result += '<cell><![CDATA[%s]]></cell>' % hlk['QUEUE_SIZE']
                                                                                                            
            
            self.write_XML('<row id="status">%s</row>' % result)
                           
                                                                                   
            self.write_XML('</rows>')
                    
            print hlk
        except Exception, e:
            logging.error(e)

        
        

class SysStatDataHandler(BaseHandler):
    urls = r'/admin/sys/data'

    def get(self):
        inp = self.input(kill='')

        if inp.kill == 'shiva':
            self.write({'error':'Hulk не отвечает'})

        else:
            self.write_XML('<rows>')

            for k1, v1 in self.application.sessions.data.items():
                u = User.get(id=k1)
                for k2, v2 in v1.items():
                    dt1 = [u.name, u.current_role_cls.name, u.depart_cls.name, time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(v2['kill'] - config.SHIVA_LIFE_SESSION)), k2, v2['data']['ip']]
                    dt2 = ''.join('<cell><![CDATA[%s]]></cell>' % i for i in dt1)

                    self.write_XML('<row id="%s%s">%s</row>' % (k1, k2, dt2))

            self.write_XML('</rows>')
