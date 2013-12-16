self.Incunable(function(doc){        
	
	
	var mas=[];
	var er=[];
	
    {% for item in all_passports %}
    
    	try{
    		
    		var url = '{{ RC_IP }}/{{ item.value }}';
    		
    		if (UrlExists(url)){    			
    			mas.push(url);    			
    		}
    		else{
    			er.push('{{ item.name }}');
    		}
    	}
	    catch(e){
	        er.push('{{ item.name }}');
	    }        
	 
	{% end %}
	
	
	
	doc.write('<link rel="stylesheet" type="text/css" href="/static/css/default.css" >');
	
	
	
	doc.write('<div class="block-print">');
	
	
	for(var j in mas){
		//
		
		doc.write('<a><img src="'+ mas[j] +'" /></a>');
		
	}
	
	
	doc.write('</div');
             
    
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