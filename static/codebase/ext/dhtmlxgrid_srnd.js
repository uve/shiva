dhtmlXGridObject.prototype.enableSmartRendering=function(b,a,d){arguments.length>2&&(a&& !this.aD[a-1]&&(this.aD[a-1]=0),a=d);this.ahK=ap(b);this.ig=this.ig||20;this.Cr=a||0};dhtmlXGridObject.prototype.enablePreRendering=function(b){this._srnd_pr=parseInt(b||50)};dhtmlXGridObject.prototype.forceFullLoading=function(b,a){for(var d=0;d<this.aD.length;d++)if(!this.aD[d]){var c=b||this.aD.length-d;if(this.callEvent("onDynXLS",[d,c])){var e=this;this.load(this.tR+jv(this.tR)+"posStart="+d+"&count="+c,function(){window.setTimeout(function(){e.forceFullLoading(b,a)},100)},this._data_type)}return}a&&a.call(this)};dhtmlXGridObject.prototype.setAwaitedRowHeight=function(b){this.ig=parseInt(b)};dhtmlXGridObject.prototype._get_view_size=function(){return Math.floor(parseInt(this.aL.offsetHeight)/this.ig)+2};dhtmlXGridObject.prototype._add_filler=function(b,a,d,c){if(!a)return null;var e="__filler__",f=this.uO(e);f.firstChild.style.width="1px";for(var g=1;g<f.childNodes.length;g++)f.childNodes[g].style.display="none";f.firstChild.style.height=a*this.ig+"px";(d=d||this.am[b])&&d.nextSibling?d.parentNode.insertBefore(f,d.nextSibling):cn?this.obj.appendChild(f):this.obj.rows[0].parentNode.appendChild(f);this.callEvent("onAddFiller",[b,a,f,d,c]);return[b,a,f]};dhtmlXGridObject.prototype._update_srnd_view=function(){var b=Math.floor(this.HF.scrollTop/this.ig),a=b+this._get_view_size();if(this.hu){for(var d=this.HF.scrollTop,b=0;d>0;)d-=this.am[b]?this.am[b].offsetHeight:this.ig,b++;a=b+this._get_view_size();b>0&&b--}a+=this._srnd_pr||0;if(a>this.aD.length)a=this.aD.length;for(var c=b;c<a;c++)if(!this.am[c]){var e=this._add_from_buffer(c);if(e== -1){if(this.tR){if(this.Cr&&this.aD[a-1]){var f=this.Cr?this.Cr:a-c,g=Math.max(0,a-this.Cr);this._current_load=[g,a-g]}else this._current_load=[c,this.Cr?this.Cr:a-c];this.callEvent("onDynXLS",this._current_load)&&this.load(this.tR+jv(this.tR)+"posStart="+this._current_load[0]+"&count="+this._current_load[1],this._data_type)}return}else if(this._tgle&&(this._updateLine(this._h2.get[this.aD[c].idd],this.aD[c]),this._updateParentLine(this._h2.get[this.aD[c].idd],this.aD[c])),c&&c==(this.nh?this.aC:this)._r_select)this.eQ(c,this.cell?this.cell._cellIndex:0,!0)}if(this.aC&& !this.nh&&this.hu)this.aC.HF.scrollTop=this.HF.scrollTop};dhtmlXGridObject.prototype._add_from_buffer=function(b){var a=this.render_row(b);if(a== -1)return-1;if(a._attrs.selected||a._attrs.select)this.Th(a,!1,!0),a._attrs.selected=a._attrs.select=null;if(this.Cw){if(this._h2){var d=this._h2.get[a.idd];a.className+=" "+(d.gR%2?this.iI+" "+this.iI:this.hC+" "+this.hC)+"_"+d.gR+(this.bj[d.id].Vn||"")}}else if(this.hC&&b%2==0)a.className=this.hC+(a.className.indexOf("rowselected")!= -1?" rowselected ":" ")+(a.Vn||"");else if(this.iI&&b%2==1)a.className=this.iI+(a.className.indexOf("rowselected")!= -1?" rowselected ":" ")+(a.Vn||"");for(var c=0;c<this._fillers.length;c++){var e=this._fillers[c];if(e&&e[0]<=b&&e[0]+e[1]>b){var f=b-e[0];f==0?(this._insert_before(b,a,e[2]),this._update_fillers(c,-1,1)):f==e[1]-1?(this._insert_after(b,a,e[2]),this._update_fillers(c,-1,0)):(this._fillers.push(this._add_filler(b+1,e[1]-f-1,e[2],1)),this._insert_after(b,a,e[2]),this._update_fillers(c,-e[1]+f,0));break}}};dhtmlXGridObject.prototype._update_fillers=function(b,a,d){var c=this._fillers[b];c[1]+=a;c[0]+=d;c[1]?(c[2].firstChild.style.height=parseFloat(c[2].firstChild.style.height)+a*this.ig+"px",this.callEvent("onUpdateFiller",[c[2]])):(this.callEvent("onRemoveFiller",[c[2]]),c[2].parentNode.removeChild(c[2]),this._fillers.splice(b,1))};dhtmlXGridObject.prototype._insert_before=function(b,a,d){d.parentNode.insertBefore(a,d);this.am[b]=a;this.callEvent("onRowInserted",[a,null,d,"before"])};dhtmlXGridObject.prototype._insert_after=function(b,a,d){d.nextSibling?d.parentNode.insertBefore(a,d.nextSibling):d.parentNode.appendChild(a);this.am[b]=a;this.callEvent("onRowInserted",[a,null,d,"after"])};