# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Department
from barcode.zek_model import cell, cell_size
from settings import CURRENT_RC

from avtuk.executor import Executor

#=== Печать ячеек =============================================================
class PrintCellHandler(BaseHandler):
    urls = r'/warehouse/prncell'

    def get(self):
        deps = Department.select('hide is NULL AND rc=:rc', rc=CURRENT_RC)
        
        
        deps2 = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_6"} for i in deps]
        
        

        self.write({'def':[{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"text", 'text':"  Подразделение:"},
                           {'id':"btndep", 'type':"buttonSelect", 'text':'-', 'items':deps2},

                          '''<div style="padding:10px;"><table>
                        <tr><td>Ряд</td><td>Место</td><td>Этаж</td></tr>
                        <tr><td id="zone_line_1"></td><td id="zone_row_1"></td><td id="zone_floor_1"></td></tr>
                        <tr><td id="zone_line_3"></td><td id="zone_row_3"></td><td id="zone_floor_3"></td></tr>
                        <tr><td id="zone_line_5"></td><td id="zone_row_5"></td><td id="zone_floor_5"></td></tr>
                        <tr><td id="zone_line_7"></td><td id="zone_row_7"></td><td id="zone_floor_7"></td></tr>
                        <tr><td><br /></td><td><br /></td><td><br /></td><td><br /></td></tr>
                        <tr><td id="zone_line_2"></td><td id="zone_row_2"></td><td id="zone_floor_2"></td></tr>
                        <tr><td id="zone_line_4"></td><td id="zone_row_4"></td><td id="zone_floor_4"></td></tr>
                        <tr><td id="zone_line_6"></td><td id="zone_row_6"></td><td id="zone_floor_6"></td></tr>
                        <tr><td id="zone_line_8"></td><td id="zone_row_8"></td><td id="zone_floor_8"></td></tr>
                      </table></div>''', ],

                    'cmd':'''window.ids=0;
                        var urls = ["line","row","floor"];
                        for(i in urls){
                            !function(i){
                                self.NetSend("/warehouse/prncell/data?dt="+urls[i], null, function(response){
                                    if(200==response.xmlDoc.status && response.xmlDoc.responseText){
                                        for(j=1;j<9;j++){
                                            var im;
                                            if(i==3)im="image";
                                            var x = new dhtmlXCombo("zone_"+urls[i]+"_"+j, urls[i][0]+j, 150, im);
                                            x.loadXMLString(response.xmlDoc.responseText);
                                            window.Cleaner.push(x);
                                            x.selectOption(0);
                                        }                                
                                    }                            
                                });
                            }(i);                        
                        }
                   

                        
                        window.do_tool_1 = function(){
                            var urs=[%s,%s];
                            for(i=0; i<8; i++)
                                urs.push( "/warehouse/prncell/data?dt=img&depart="+window.ids+"&l="+window.Cleaner[i+0*8].getComboText()+"&r="+window.Cleaner[i+1*8].getComboText()+"&f="+window.Cleaner[i+2*8].getComboText() );
                                
                            self.PrintURL.apply(self, urs);   
                        }

                    
                        //DEP
                        window.do_tool_6 = function(ids){
                            if(ids.substr(0, 3) == "dep"){
                                var dep = self.Toolbars["def"].getListOptionText("btndep", ids);                                                               
                                self.SetTitle('Печать ячеек для:  "'+dep+'"');
                                self.Toolbars["def"].setItemText("btndep", dep);
                                window.ids=ids.substr(3);                                
                            }
                        }
                        
                        window.do_tool_6("dep%s");''' % (cell_size[0], cell_size[1], deps[0].id)
})


#============================================================================#
class PrintCellDataHandler(BaseHandler):
    urls = r'/warehouse/prncell/data'

    def get(self):
        inp = self.input(dt='', l=0, r=0, f=0, depart=0)

        if inp.dt == 'line':
            sql = 'SELECT UNIQUE stelag FROM tovar_place WHERE stelag IS NOT NULL ORDER BY 1'
            self.write_XML(Executor.exec_cls(sql).as_combo('stelag', id='stelag'))

        elif inp.dt == 'row':
            sql = 'SELECT UNIQUE place FROM tovar_place WHERE place IS NOT NULL ORDER BY 1'
            self.write_XML(Executor.exec_cls(sql).as_combo('place', id='place'))

        elif inp.dt == 'floor':
            sql = 'SELECT UNIQUE polka FROM tovar_place WHERE polka IS NOT NULL ORDER BY 1'
            self.write_XML(Executor.exec_cls(sql).as_combo('polka', id='polka'))

        elif inp.dt == 'img':
            try:
                self.write(cell(int(inp.l), int(inp.r), int(inp.f), int(inp.depart)))
                self.set_header("Content-Type", "image/svg+xml")
            except:
                pass
