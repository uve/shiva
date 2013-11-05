# coding: utf-8

from core.sw_base import BaseHandler
from barcode.zek_model import barcode2assembly
from avtuk.executor import Executor
import cx_Oracle


#=== Штучная комплектация =====================================================
class ItemzoneItempackageHandler(BaseHandler):
    urls = r'/itemzone/itempackage'


    def get(self):
        inp = self.input(alist=0)
        try: alist = barcode2assembly(int(inp.alist))
        except: alist = 0

        if not alist:
            self.write({'def':['<div id="sw_form" style="padding:10px;"></div>'],
                        'precmd':'self.InitContent();',
                    'cmd':'''var sw_boxass = new dhtmlXForm("sw_form",[
                        {type: "label", label: "Штрих-код сборочного листа:"},
                        {type:"input", name:"badge"}
                    ]);
                    window.Cleaner.push(sw_boxass);

                    var badge_input = sw_boxass.doWithItem("badge", "getInput");
                  
                    badge_input.onkeypress = function(e){
                        var s = badge_input.value;
                        if(e.keyCode==13){
                            self.NetSend("/itemzone/itempackage?alist="+s);
                        }else{
                            if(s.length > 11)
                                setTimeout(window.clr_input, 100);                            
                        }
                     } 
                                        
                     window.clr_input = function(){
                         badge_input.value = '';
                         badge_input.focus();
                     }
                    
                     window.clr_input();'''
                    })

        else:
            ret = self.cursor.var(cx_Oracle.NUMBER)
            self.cursor.execute('begin shiva.SetSotrudToPacklist(:idd, :psotrud, :pout); end;',
                                 idd=alist, psotrud=self.session.uid, pout=ret)

            r = ret.getvalue()
            if r == -1:
                self.write({'warning':'Неверный штрих-код сотрудника'})
            elif r == -2:
                self.write({'warning':'Сотрудник не в смене'})
            elif r == -3:
                self.write({'warning':'Не соответствие роли сотрудника'})
            elif r == -4:
                self.write({'warning':'К упаковочному уже привязан другой сотрудник'})
            elif r == -5:
                self.write({'warning':'Неверный штрих-код сборочного'})
            elif r == -6:
                self.write({'warning':'упаковочный закрыт'})
            elif r == 0:
                self.write({'def':[{'type':"text", 'text':' Товар:'},
                                   {'id':'ibar', 'type':"buttonInput", 'title':'Штрих-код товара'},

                                   {'type':"text", 'text':' Кол-во:'},
                                   {'id':'icnt', 'type':"buttonInput", 'width':50},

                                   {'type':"separator"},
                                   {'type':"separator"},

                                   {'type':"text", 'text':' Вес коробки:'},
                                   {'id':'imas', 'type':"buttonInput", 'width':50},

                                   {'type':"text", 'text':' № коробки:'},
                                   {'id':'inum', 'type':"buttonInput", 'width':40},

                                   {'type':"separator"},
                                   {'type':"button", 'img':"process24.png", 'action':'end_assembly', 'text':'Закончить упаковку'},

                                   '<div id="sw_form" style="padding:10px;"></div>'],
                            'precmd':'self.InitContent();',
                            'cmd':'''var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2U");
                                    sw_btk.items[0].setText("Собрано");
                                    sw_btk.items[1].setText("Осталось собрать");
                                    window.Cleaner.push(sw_btk);
                                    
        
                                    var sw_grid1 = sw_btk.cells("a").attachGrid();
                                    sw_grid1.columns([
          { type:"ro", sort:"int", align:"right", width:"46", label:"Код" },
          { type:"ro", sort:"str", align:"left",  width:"*",  label:"Наименование продукта" },
          { type:"ro", sort:"int", align:"right", width:"48", label:"Кол-во" },
          { type:"ro", sort:"int", align:"right", width:"36", label:"Место" },  
          { type:"ro", sort:"int", align:"right", width:"56", label:"Вес" }                                 
                                    ]);
                                    window.Cleaner.push(sw_grid1);
        
                                    var sw_grid2 = sw_btk.cells("b").attachGrid();
                                    sw_grid2.columns([
          { type:"ro", sort:"int", align:"right", width:"48", label:"Код" },
          { type:"ro", sort:"str", align:"left",  width:"*",  label:"Наименование продукта" },
          { type:"ro", sort:"int", align:"right", width:"48", label:"Кол-во" }
                                    ]);
                                    window.Cleaner.push(sw_grid2);
                                                                    
                                    var bar = this.Toolbars["def"];
                                    
                                    var ibar = bar.objPull[bar.idPrefix+"ibar"].obj.firstChild;
                                    var icnt = bar.objPull[bar.idPrefix+"icnt"].obj.firstChild;
                                    var imas = bar.objPull[bar.idPrefix+"imas"].obj.firstChild;
                                    var inum = bar.objPull[bar.idPrefix+"inum"].obj.firstChild;
                                                                
                                    ibar.onkeypress = function(e){ if(e.keyCode==13) icnt.focus() };                                                        
                                    icnt.onkeypress = function(e){ if(e.keyCode==13){
                                        window.add_assembly_item();
                                        ibar.value="";
                                        icnt.value="";
                                        ibar.focus();                                    
                                    }}                                
                                    imas.onkeypress = function(e){ if(e.keyCode==13) inum.focus() };
                                    inum.onkeypress = function(e){ if(e.keyCode==13){
                                        window.add_assembly_item();
                                        ibar.value="";
                                        icnt.value="";
                                        imas.value="";
                                        inum.value="";
                                        ibar.focus();
                                    }}
                                    
                                    // номер сборочного
                                    window.alist=%s;
                                    
                                    window.add_assembly_item = function(){
                                        self.NetSend("/itemzone/itempackage/data", "alist="+window.alist+"&bar="+ibar.value+"&cnt="+icnt.value+"&mas="+imas.value+"&num="+inum.value);
                                        window.load_assembly_items();
                                    }
                                    
                                    window.del_assembly_item = function(){                               
                                        self.NetSend("/itemzone/itempackage/data", "idd="+sw_grid1.getSelectedRowId());
                                        window.load_assembly_items();
                                    }
                                    
                                    sw_grid1.attachEvent("onRowDblClicked", del_assembly_item);                                
                                    
                                    window.load_assembly_items = function(){
                                        self.LoadGrid(sw_grid1, "/itemzone/itempackage/data?grid=1&alist="+window.alist);
                                        self.LoadGrid(sw_grid2, "/itemzone/itempackage/data?grid=2&alist="+window.alist);
                                    }
                                    
                                    window.end_assembly = function(){ self.Refresh() }
                                    
                                    window.load_assembly_items();
                                    ''' % alist
                            })


            else:
                self.write({'warning':'Чета не так - %s' % r})



#==============================================================================
class ItemzoneItempackageDataHandler(BaseHandler):
    urls = r'/itemzone/itempackage/data'

    def get(self):
        inp = self.input(grid=0, alist=0)

        try:
            alist = int(inp.alist)
            grid = int(inp.grid)

            # left grid
            if grid == 1:
                sql = '''SELECT pl.id,pl.valume,pl.mesto,pl.weight,t.code,t.name 
FROM packlist pl 
JOIN tovar t ON pl.tovar=t.id and pl.sw_header_recordp= :alist'''
                self.write_XML(Executor.exec_cls(sql, alist=alist)
                               .as_grid('code', 'name', 'valume', 'mesto', 'weight', id='id'))



            # right grid
            elif grid == 2:
                sql = '''SELECT * FROM
( SELECT t.id,t.code,t.name,(SUM(ABS(r.valume))-NVL(SUM(p.valume),0)) valume
  FROM sw_header_recordp shr 
  JOIN recordp r  on shr.depart=r.depart 
  JOIN tovar t on t.id=r.tovar
  LEFT JOIN (SELECT tovar,SUM(valume) valume FROM packlist 
             WHERE sw_header_recordp= :alist
             GROUP BY tovar) p ON p.tovar=t.id 
  WHERE shr.id= :alist AND r.factura IN (SELECT id FROM factura WHERE header=shr.header) 
  GROUP BY t.id,t.code,t.name)
WHERE valume<>0'''
                self.write_XML(Executor.exec_cls(sql, alist=alist)
                               .as_grid('code', 'name', 'valume', id='id'))

        except:
            self.write_XML('<rows />')


    def post(self):
        inp = self.input(alist=0, idd=0, bar='', cnt=0, num=0, mas=0)

        try:idd = int(inp.idd)
        except:idd = 0

        try:
            if idd:
                # удаляем из упаковки
                Executor.exec_sql('DELETE FROM packlist WHERE id= :idd', idd=idd)
                self.write({'info':'Информация сохранена'})
            else:
                # добавляем в упаковку
                try:alist = int(inp.alist)
                except:alist = 0
                try:bar = inp.bar
                except:bar = ''
                try:cnt = float(inp.cnt)
                except:cnt = 0.0
                try:num = int(inp.num)
                except:num = 0
                try:mas = float(inp.mas)
                except:mas = 0.0

                ret = self.cursor.var(cx_Oracle.NUMBER)
                self.cursor.execute('begin shiva.AddPackList(:alist, :bar, :cnt, :num, :mas, 0, :ret); end;',
                                     alist=alist, bar=bar, cnt=cnt, num=num, mas=mas, ret=ret)

                r = ret.getvalue()
                if r == -0:
                    self.write({'info':'Информация сохранена'})
                elif r == -1:
                    self.write({'warning':'Товара не существует'})
                elif r == -3:
                    self.write({'warning':'В заказе нет такого продукта'})
                elif r == -4:
                    self.write({'warning':'Количество превышает заказ'})
                else:
                    self.write({'warning':'Чета не так - %s' % r})

        except:
            self.write({'warning':'Ошибка записи'})
