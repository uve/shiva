var fn=[%s]; var er=[%s];

    self.Incunable(function(doc){                
        for(var i in fn){
        	
        	
            doc.write('<img width="%s" height="%s" src="/warehouse/printpassport/data/image?mode=1&fname='+fn[i]+'">');
        }
        
        if(!!(fn.length %% 2)){
            doc.write('<div style="height:600px;"><br/></div>');
        }                    
        
        if(er.length){
            doc.write('<br/><br/><div>Не найдены паспорта качества:</div><table style="border:1 solid #000;">');
            
            var hd=['N','Партия','Код','Товар','Паспорт'];
            doc.write('<tr>');
            for(var i in hd)
                doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+hd[i]+'</td>');
            doc.write('</tr>');
                                
            for(var i in er){
                doc.write('<tr>');
                doc.write('<td style="padding:3px; border-bottom:1 solid #888; border-right:1 solid #000;">'+(1+parseInt(i))+'</td>');
                for(var j in er[i])
                    doc.write('<td style="border-bottom:1 solid #888; border-right:1 solid #000;">'+er[i][j]+'</td>');
                doc.write('</tr>');
            }                        
            doc.write('</table>');                        
        }               
});''' % (goods, errns, int(3.47 * w), int(3.47 * h))
