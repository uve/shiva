# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Pallet
from barcode.zek_model import pallet, pallet_size, pallet2barcode, barcode2pallet

#=== Печать палет ============================================================#
class PrintPalletHandler(BaseHandler):
    urls = r'/warehouse/prnpalet'

    def get(self):
        self.write({'def':[{'type':"button", 'text':'Печать', 'img':"print.gif", 'imgdis':"print_dis.gif", 'action':'do_tool_1'}],
               'cmd':'''var sw_grid = new dhtmlXGridObject({
                            parent: window.app.Panels["def"],
                            columns:[{
                                label:"Номера палет",
                                type:"ro",
                                sort:"int"
                            }]                        
                        });
                        window.Cleaner.push(sw_grid);
                        
                        window.do_tool_1 = function(){
                          sw_grid.clearAll();
                          sw_grid.csv.row = ",";
                          
                          self.NetSend("/warehouse/prnpalet/data", " ", function(response){
                              if(200==response.xmlDoc.status && response.xmlDoc.responseText){
                                 var data = eval('('+response.xmlDoc.responseText+')');
                                 sw_grid.parse(data.join(), "csv");
                                 var urs=[%s,%s];
                                 for(i in data){
                                     urs.push( "/warehouse/prnpalet/data?ids="+data[i] );
                                 }
                                 self.PrintURL.apply(self, urs);
                              }
                          });                          
                        }''' % pallet_size
                    })



#=============================================================================#
class PrintPalletDataHandler(BaseHandler):
    urls = r'/warehouse/prnpalet/data'

    def get(self):
        self.write(pallet(barcode2pallet(self.input(ids='').ids)))
        self.set_header("Content-Type", "image/svg+xml")


    def post(self):
        ids = []
        for _ in range(10):
            x = Pallet()
            x.save()
            ids.append(pallet2barcode(x.id))

        self.write(ids)
