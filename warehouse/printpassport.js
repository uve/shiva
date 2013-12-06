self.Incunable(function(doc){        
	
	var er=[];
	
    {% for item in all_passports %}
    
	    if (UrlExists('{{ RC_IP }}/{{ item.value }}')){
	    	doc.write('<img style="page-break-after: always;" width="{{ width }}" src="{{ RC_IP }}/{{ item.value }}">');
	    }
	    else{
	        er.push('{{ item.name }}');
	    }        
	 
	{% end %}
 
    
    /*console.log(er);*/
             
    
    if(er.length){
        doc.write('<p>Не найдены паспорта качества:</p><table style="border:1 solid #000;">');
        
        var hd=['N','Партия','Код','Товар','Паспорт'];
        doc.write('<tr>');
        for(var i in hd)
            doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+hd[i]+'</td>');
        doc.write('</tr>');
                            
        for(var i in er){
            doc.write('<tr>');
            doc.write('<td style="padding:3px; border-bottom:1 solid #888; border-right:1 solid #000;">'+(1+parseInt(i))+'</td>');
            
            doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+ er[i] +'</td>');
            doc.write('</tr>');
        }                        
        doc.write('</table>');                        
    }               
});