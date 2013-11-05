# coding: utf-8

from core.sw_base import BaseHandler

from barcode.zek_model import barcode2assembly, barcode2depart_sid
import cx_Oracle

#==============================================================================
class ItemAssemblyHandler(BaseHandler):
    urls = r'/itemzone/itemassembly'

    def get(self):
        self.write({'def':['''<table><tr><td><div id="sw_form1" style="padding:10px;"></div></td>
                             <td><div id="sw_form2" style="padding:10px;"></div></td></tr></table>
                           '''],

                    'cmd':'''var sw_boxass1 = new dhtmlXForm("sw_form1",[
                        {type: "label", label: "Штрих-код бэйджика:"},
                        {type:"input", name:"badge"}
                    ]);
   
                    window.Cleaner.push(sw_boxass1);
                    var sw_boxass2 = new dhtmlXForm("sw_form2",[
                        {type: "label", label: "Штрих-код сборочного:"},
                        {type:"input", name:"itemasslist"}
                    ]);
                    window.Cleaner.push(sw_boxass2);

                    var badge_input = sw_boxass1.doWithItem("badge", "getInput");
                    var itemasslist_input = sw_boxass2.doWithItem("itemasslist", "getInput");
                    badge_input.focus();

                    badge_input.onkeypress = function(e){
                        if(e.keyCode==13){
                            itemasslist_input.focus();
                        }  
                    } 
                    itemasslist_input.onkeypress = function(e){
                        if(e.keyCode==13){
                            self.NetSend("/itemzone/itemassembly/data","badge="+badge_input.value+"&itemlistbarcode="+itemasslist_input.value);
                            setTimeout(window.clr_input, 100);
                        }
                    }                             
                    window.clr_input = function(){
                        badge_input.value = '';
                        itemasslist_input.value = '';
                        badge_input.focus();
                    }
                    
                    window.clr_input(); '''
                   })



#==============================================================================
class ItemAssemblyDataHandler(BaseHandler):
    urls = r'/itemzone/itemassembly/data'


    def post(self):
        inp = self.input(itemlistbarcode='', badge='')
        print inp
        _, uid = barcode2depart_sid(inp.badge)
        idd = barcode2assembly(inp.itemlistbarcode)
        ret = self.cursor.var(cx_Oracle.NUMBER)
        self.cursor.execute('begin shiva.SetSotrudToRecordp(:idd, :psotrud, :pout); end;',
                             idd=idd, psotrud=uid, pout=ret)

        r = int(ret.getvalue())
        if r == 0:
            self.write({'info':'Информация сохранена'})
        elif r == -1:
            self.write({'warning':'Неверный штрих-код сотрудника'})
        elif r == -2:
            self.write({'warning':'Сотрудник не в смене'})
        elif r == -3:
            self.write({'warning':'Не соответствие роли сотрудника'})
        elif r == -4:
            self.write({'warning':'К сборочному уже привязан другой сотрудник'})
        elif r == -5:
            self.write({'warning':'Неверный штрих-код сборочного'})
        elif r == -6:
            self.write({'warning':'Сборочный закрыт'})
        else:
            self.write({'warning':'ХБЗ %s' % r})



