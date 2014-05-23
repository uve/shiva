

var sw_grid = new dhtmlXGridObject({
    parent: "sw_grid1",
    columns:[
              { type:"ro", align:"left",   width:"0",   label:"Id" },
              { type:"ro", align:"left",   width:"200",  label:"Приоритет" },
              { type:"ro", align:"left",   width:"0",   label:"order" }

    ]});

/*sw_grid.attachHeader("#select_filter,#text_filter,#text_filter,&nbsp;,#cspan");*/

sw_grid.enableDragAndDrop(true);

sw_grid.enableDragOrder(true);
//sw_grid.setDragText(single,plural);

sw_grid.attachEvent("onDrop", function(task_from, task_to){

    var role_id = combo.getSelectedValue();

    dhtmlxAjax.post("/admin/roletask/data", 'role_id=' + role_id + '&task_from=' + task_from + "&task_to=" + task_to,
        function(resp){
         //   alert("Ячейка разблокирована");
    });

});




var combo = new dhtmlXCombo({
    parent:"combo_zone1"

});
combo.readonly(1);

{% for item in all_roles %}
    combo.addOption([
        {value: "{{ item['value'] }}", text: "{{ item['name'] }}"}
    ]);
{% end %}


 combo.attachEvent("onChange", function(){

     var params = {
         role: combo.getSelectedValue()
     };

     self.load(sw_grid, "/admin/roletask/data?" + self.serialize(params), function() {

     });



 });



 combo.selectOption(7);



