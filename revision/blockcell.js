var sw_block = new dhtmlXLayoutObject(self.Panels["def"], "2E");                      
                        
sw_block.items[0].setText("Заблокированные ячейки");
sw_block.items[1].setText("История паллеты");
window.Cleaner.push(sw_block);
                            
var sw_grid1 = sw_block.cells("a").attachGrid();

sw_grid1.columns([
                  { type:"ro", sort:"str",  align:"center", width:"30",  label:"ID" },
                  { type:"ro", sort:"str",  align:"center", width:"60",  label:["Адрес", "#text_filter"] },
                  { type:"ro", sort:"date", align:"center", width:"90",  label:["Дата", "#text_filter"] },
                  { type:"ro", sort:"str",  align:"left",   width:"*",   label:["Тип", "#select_filter"] },
                  { type:"ro", sort:"str",  align:"center", width:"150", label:["Сотрудник", "#select_filter"] },   
                  { type:"ro", sort:"int",  align:"center", width:"60",  label:["Палета", "#text_filter"] },  
                  { type:"ro", sort:"int",  align:"center", width:"40",  label:"Кол-во" },  
                  { type:"ro", sort:"int",  align:"center", width:"52",  label:"Партия" }
  ]);

    self.load(sw_grid1, "/revision/blockcell/data/list");

    window.Cleaner.push(sw_grid1);

    var sw_grid2 = sw_block.cells("b").attachGrid();
    sw_grid2.columns([
      
          { type:"ro", sort:"int",  align:"center", width:"55",  label:"ID" },
          { type:"ro", sort:"int",  align:"center", width:"55",  label:"Код" },
          { type:"ro", sort:"str",  align:"left",   width:"*",   label:"Товар" },
          { type:"ro", sort:"int",  align:"center", width:"60",  label:"Кол-во" },
          { type:"ro", sort:"int",  align:"center", width:"100", label:"Партия" },
          { type:"ro", sort:"int",  align:"center", width:"100", label:"Годен ДО" }
          
    ]);
    window.Cleaner.push(sw_grid2);
                        
                        
    
    sw_grid1.attachEvent("onRowSelect", function(id){
    	
    	var row_id  = sw_grid1.getSelectedId();
    	var cell_id = sw_grid1.cellById(row_id, 1).getValue();
    	
        self.load(sw_grid2, "/revision/blockcell/data/history?cell_id=" + cell_id);    
    });
    

    
    
    
    
    
                       
                        