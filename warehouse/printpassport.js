var sw_grid = new dhtmlXGridObject({
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

    if(!ids) {
        self.AddMessage('Выберите фактуру',2)
        return false;
    }

    var mode = ids2.substr(3);



    //Отгрузочные этикетки
    if(mode == '2'){
        var d=prompt('Диапазон мест разделенные пробелом','').split(' ');
    }

    var d='';


    var url= "/warehouse/printpassport/data/print?head=" + ids + "&mode=" + mode + "&d=" + d;

    if (mode == '1'){

        window.open(url);
    }
    else
    {
        self.NetSend(url);
    }



    return true;

    /*
     else {
     var m=ids2.substr(3);
     var d='';
     //Отгрузочные этикетки
     if(m==2){
     var d=prompt('Диапазон мест разделенные пробелом','').split(' ');
     }

     if (m == 1){

     var url= "/warehouse/printpassport/data/print?head="+ids+"&mode="+m+"&d="+d;

     window.open(url,'_blank');
     window.open(url);
     }
     else
     {
     self.NetSend("/warehouse/printpassport/data/print?head="+ids+"&mode="+m+"&d="+d);
     }


     }

     */

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


window.do_tool_3("opr0");