  
var MAXCONST = MAXCONST;


var sw_grid1 = new dhtmlXGridObject({
   parent: "sw_grid1",
   columns: [
      { type:"ro", sort:"str",  align:"center", width:"100",  label:["Адрес ячейки", "#text_filter"], },  
      { type:"ro", sort:"str",  align:"center", width:"100",  label:["Номер Партии", "#text_filter"] },
      { type:"ro", sort:"int",  align:"center", width:"100",  label:["Штук в коробке", "#text_filter"] },
      { type:"ro", sort:"int",  align:"center", width:"100",  label:["Штук", "#select_filter"] },
      { type:"ro", sort:"date", align:"center", width:"100",  label:["Годен до", "#select_filter"] },
      
        ]
    });
                     

window.sw_grid1 = sw_grid1;                                                   
window.Cleaner.push(sw_grid1);

var sw_grid2 = new dhtmlXGridObject({
    parent: "sw_grid2",
    columns: [
              
      { type:"ro", sort:"str",  align:"center", width:"0",   label:"Id", },        
      { type:"ro", sort:"date", align:"center", width:"100", label:"Дата", },  
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Номер фактуры" },
      { type:"ro", sort:"int",  align:"center", width:"100", label:"В коробке"},
      { type:"ro", sort:"int",  align:"center", width:"100", label:"Коробок"},                          
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Фактура" },
      { type:"ro", sort:"str",  align:"center", width:"100", label:"Сотрудник" },
      { type:"ro", sort:"int",  align:"center", width:"100",  label:"Тип" }
      
        ]
    });
               
window.Cleaner.push(sw_grid2);




window.do_tool_print = function(){
    var m_product = z.getSelectedValue();
    self.NetSend("/revision/auditor/data/print?mode=1&tovar=" + m_product);
}

window.do_tool_revision = function(){
    var m_product = z.getSelectedValue();
    self.NetSend("/revision/auditor/data/maketaskrevision?tovar=" + m_product);
}





function sumColumn(sw_grid, ind) {
    var out = 0;
    for (var i = 0; i < sw_grid.getRowsNum(); i++) {
        out += parseFloat(sw_grid.cells2(i, ind).getValue());
    }
    return out;
}


function grid_update(sw_grid) {

    row_id = MAXCONST;   //Const

    sw_grid.deleteRow(row_id);

    res = sumColumn(sw_grid, 3);

    sw_grid.addRow(row_id,["","", "Всего:", res]);
    sw_grid.setRowTextBold(row_id);

    sw_grid.lockRow(row_id, 'true');

}


sw_grid1.attachEvent("onAfterSorting", function(index,type,direction){
    grid_update(sw_grid1);
});

/*
 sw_grid2.attachEvent("onAfterSorting", function(index,type,direction){
 grid_update(sw_grid2);
 });
 */



sw_grid1.attachEvent("onRowSelect", function(id){

    if (id == MAXCONST){
        return false;
    }
    self.load(sw_grid2, "/revision/auditor/data/cell_history?cell_id=" + id);

});





/***********  COMBO ***********/


var z= new dhtmlXCombo("combo_zone1");
z.setOptionHeight(300);

z.attachEvent("onKeyPressed",function(){

    z.clearAll();

    text = z.getComboText();

    if (text.length < 4)
        return false;


    dhtmlxAjax.get("/revision/auditor/data/products?mask="+text, function(xml){

        z.loadXMLString(xml.xmlDoc.responseText);
    })


});









      
                    
z.attachEvent("onChange",function(){

      var m_product = z.getSelectedValue();
      if (!m_product){
    	  return false;
      }

      console.log(m_product);
      
      var depart  = self.Toolbars["def"].getListOptionSelected("departs");
      
      self.load(sw_grid1, "/revision/auditor/data/head?mode=0&tovar=" + m_product + "&depart="+depart,function() {                                    
            grid_update(sw_grid1);  
      });
      

            
            
    dhtmlxAjax.get("/revision/auditor/data/head?mode=1&tovar=" + m_product + "&depart="+depart,function(loader){

         var tovarsaldo = document.getElementById("tovarsaldo");
         tovarsaldo.innerHTML = loader.xmlDoc.responseText;
         
    });

          
});            
