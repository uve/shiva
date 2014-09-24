var sw_btk = new dhtmlXLayoutObject(self.Panels["def"], "2E");
                            sw_btk.items[0].setText("Список фактур");
                            sw_btk.items[1].setText("Список товаров");
                            window.Cleaner.push(sw_btk);

                            var sw_grid1 = sw_btk.cells("a").attachGrid();
                            sw_grid1.columns([                            
  { type:"ro", sort:"int",  align:"right", width:"68",  label:["ID", "#text_filter"]  },
  { type:"ro", sort:"int",  align:"right", width:"45",  label:["Номер", "#text_filter"] },
  { type:"ro", sort:"date", align:"right", width:"66",  label:["Дата", "#text_filter"] },
  { type:"ro", sort:"str",  align:"left",  width:"*",   label:"Поставщик" },
  { type:"ro", sort:"str",  align:"left",  width:"290", label:"Операция" },
  { type:"ro", sort:"str",  align:"left",  width:"100", label:["Статус", "#select_filter"] }                            
                            ]);

                            window.Cleaner.push(sw_grid1);
                            window.do_tool_csv = function(){ self.GridCSV(sw_grid1) }                            

                            var sw_grid2 = sw_btk.cells("b").attachGrid();
                            sw_grid2.columns([
  { type:"ro", sort:"int", align:"right", width:"55", label:"Код" },
  { type:"ro", sort:"str", align:"left",  width:"*",  label:"Товар" },
  { type:"ro", sort:"int", align:"right", width:"65", label:"Кол-во" }                      
                            ]);
                            
window.Cleaner.push(sw_grid2);

sw_grid1.attachEvent("onRowSelect", function(id){
        self.LoadGrid(sw_grid2, "/warehouse/acceptance/data/tovar?head="+id);
    }
);

window.gts = 1;
window.ids = 0;

window.do_tool_1 = function(){
    var ids = sw_grid1.getSelectedRowId();
    if (!ids){
        self.AddMessage('Фактура не выбрана',3);
        return;
    }
    sw_grid2.editStop();

    var dat="ids="+ids+"&gts="+window.gts;

    self.NetSend("/warehouse/acceptance/data/gts", dat);
    sw_grid2.clearAll();
    self.LoadGrid(sw_grid1, "/warehouse/acceptance/data/head");
}

window.do_tool_2 = function(ids){
    window.gts=parseInt(ids.substr(3));
    var text = self.Toolbars["def"].getListOptionText("btngts", ids);
    self.Toolbars["def"].setItemText("btngts", text);
}

window.do_tool_3 = function(){

    sw_grid2.clearAll();


    self.load(sw_grid1, "/warehouse/acceptance/data/head",function() {


    });

}
window.do_tool_3();


// print passport
window.do_tool_4 = function(ids2){
    var ids = sw_grid1.getSelectedRowId();
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
};
