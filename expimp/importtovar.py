# coding: utf-8

from core.sw_base import BaseHandler


#=== Все задания ==============================================================
class ImportTovarHandler(BaseHandler):
    urls = r'/expimp/importtovar'

    def get(self):


        
        self.write({'def':['<div id="sw_form" style="padding:10px;"></div><div id="sw_form_create" style="padding:10px;"></div>'],

                    'cmd':'''var formData = [{
                                                type: "fieldset",
                                                label: "Импорт товаров из 1C",
                                                list: [{
                                                    autoStart: true,
                                                    type: "upload",
                                                    name: "myFiles",
                                                    inputWidth: 330,
                                                    url: "/expimp/importtovar",                                                
                                                    swfPath: "/static/codebase/ext/uploader.swf",
                                                    
                                                }]
                                            },
                                                                                        
                                            {
                                                type: "fieldset",
                                                label: "Создать новую номенклатуру",
                                                list: [
                                                    {type:"input",    name:"code",      bind:"code",    label:"Код в 1С:"},
                                                    {type:"input",    name:"name",      bind:"name",    label:"Наименование:"},
                                                    {type:"input",    name:"articul",   bind:"articul", label:"Артикул в 1С"},
                                                    {type: "button",  name:"save", offsetTop:10,  value:"Создать"}
                                                ]
                                            }
                                
                                
                                            ];
                             myForm = new dhtmlXForm("sw_form", formData);
                             
                             
                             myForm.attachEvent("onButtonClick", function(id){                             
                                   if (id=='save'){                                        
                                        myForm.send("/expimp/create_tovar","post",function(){
                                            alert("Номенклатура создана");
                                            
                                            myForm.reset();
                                            myForm.clear();
                                        });
                                    }
                            });
                                                     
                             
    
                        
                        '''
                    })


    def post(self):
        

        f1 = self.request.files['file'][0]        
        
        mas = f1["body"].splitlines()
        
        
        for item in mas:
            
            try:
                item = item.decode('cp1251').encode('utf8')[:80]
                self.cursor.execute('''begin 
                                    shiva.ImportTovar(str => :pStr);
                               end;''', pStr=item);
            except Exception as e:
                print e
                pass

            
        # self.write({'warning':'Ошибка записи'})
