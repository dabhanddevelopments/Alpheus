Ext.Loader.setPath("Ext.ux","static/extjs/examples/ux");Ext.require(["Ext.ux.RowExpander"]);Ext.require(["Ext.container.Viewport","Ext.layout.container.Border","Ext.tab.Panel","Ext.tree.*","Ext.data.*","Ext.menu.*","Ext.window.MessageBox","Ext.grid.*",]);function displayInnerGrid(b,d){fields=[];for(i=0;i<b.columns.length;i++){fields[i]=b.columns[i].dataIndex}var e=Ext.create("Ext.data.Store",{fields:fields,data:b.rows,proxy:{type:"memory",reader:{type:"json",root:"objects"}}});var a=Ext.create("Ext.grid.Panel",{store:e,selModel:{selType:"cellmodel"},columns:b.columns,header:false,width:1000,height:150,iconCls:"icon-grid",renderTo:"innergrid"+d,});a.getEl().swallowEvent(["mousedown","mouseup","click","contextmenu","mouseover","mouseout","dblclick","mousemove"])}function lineBarChart(b){b.url="/api/widget/fundperfholdpriceline/";b.qs="?holding__fund="+b.fund+"&holding="+b.holding;var d=$("#data").data("linebar-div");var a=$("#"+d).highcharts();if(typeof a!="undefined"){a.destroy()}$.getJSON(b.url+b.qs,function(e){b.url="/api/widget/fundperfholdvolbar/";$.getJSON(b.url+b.qs,function(h){var f={chart:{renderTo:d,marginTop:5,marginRight:50,},navigator:{enabled:true},scrollbar:{enabled:false,},rangeSelector:{enabled:true,},title:{text:false,},xAxis:[{gridLineWidth:1,type:"datetime",labels:{rotation:-45,align:"right",style:{fontSize:"13px",fontFamily:"Verdana, sans-serif"}},},{}],yAxis:[{height:180,lineWidth:3,offset:0,gridLineWidth:1,title:{text:"Price",margin:5,}},{top:225,lineWidth:3,gridLineWidth:1,offset:0,height:75,title:{text:"Volume",}},],legend:{enabled:true,verticalAlign:"top",y:-10,},series:[{yAxis:0,name:"Price by time",stack:0,data:e,tooltip:{valueDecimals:2},},{name:"Volume by time",yAxis:1,stack:0,data:h,tooltip:{valueDecimals:2},lineWidth:3,marker:{enabled:false},pointWidth:5,type:"column",},]};var g=new Highcharts.Chart(f)})})}function destroyInnerGrid(a){var b=document.getElementById(a.get("id"));var d=b.firstChild;while(d){d.parentNode.removeChild(d);d=d.nextSibling}}function monthlyBar(d,f,a,h){if(typeof a=="undefined"){a="nav"}if(typeof h=="undefined"){h="weight"}var j=$("#data").data("div-fundperfholdperfbar");var e=$("#"+j).highcharts();var b="/api/widget/fundperfholdperfbar/?value_date="+d+"&fund="+f+"&legend=false&fields="+a+"&order_by="+h+"&holding_category__isnull=true";try{e.destroy();$.getJSON(b,function(l){widget={};widget.size_x=5;widget.size_y=3;var k=new Highcharts.Chart({chart:{renderTo:j,type:"column",width:(120*widget.size_x)+(10*widget.size_x)+(10*(widget.size_x-1))-30,height:(120*widget.size_y)+(10*widget.size_y)+(10*(widget.size_y-1))-35,},title:{text:false,},legend:{enabled:false,},xAxis:{type:"category",categories:l.columns,labels:{rotation:-45,align:"right",style:{fontSize:"10px",fontFamily:"Verdana, sans-serif"},enabled:labels,},},series:l.objects,})})}catch(g){}}Ext.onReady(function(){$('<div id="data"></div>').appendTo("body");function f(O){var P=O.page;var M=$("#data").data("page");for(i=0;i<M.length;i++){if(M[i].id==P){el="page"+P;if(M[i].children!==undefined){var N=p();z(N,el);d(M[i]);O.page=M[i].children[0].id}else{var N=n();z(N,el);$("#data").data("grid"+P,"");$('<div id="page'+P+'"></div>').appendTo("#menu")}L(O)}}}function d(N){var M=Ext.getCmp("panel-tab");M.removeAll();for(x=0;x<N.children.length;x++){id=N.children[x].id;$('<div id="page'+id+'" class="gridster"></div>').appendTo("body");$("#data").data("grid"+id,"");M.add({title:N.children[x].title,id:id,contentEl:"page"+id,autoScroll:true,listeners:{activate:function(O){obj={};obj.page=O.id;L(obj)}},})}M.setActiveTab(0)}function z(N,O){var Q=$("#data").data("active-panel");var M=Ext.getCmp("viewport");try{M.remove(Q)}catch(P){}$('<div id="menu" class="gridster"></div>').appendTo("body");try{M.add(N)}catch(P){}M.doLayout();$("#data").data("active-panel",N.id)}function L(N){var M=N.page;console.log("initiating grid");$("#data").data("page_id",M);if($("#data").data("grid"+M)!==undefined&&$("#data").data("grid"+M)!==""){return}N.grid=$("#page"+M).gridster({widget_margins:[10,10],widget_base_dimensions:[120,120],max_size_x:10,max_size_y:10,draggable:{stop:function(O,P){g(JSON.stringify(N.grid.serialize()))}},serialize_params:function(P,O){return{id:O.el[0].id,col:O.col,row:O.row,size_y:O.size_y,size_x:O.size_x,pagewindow:P.context.attributes.pagewindow.value,}}}).data("gridster");N.grid.disable();$("#data").data("grid"+M,N.grid);$.ajax({type:"GET",url:"/api/pagewindow/?page="+M,success:function(O){$("#data").data("grid_data"+M,O);for(i=0;i<O.length;i++){r(O[i],i,N)}}})}function r(P,R,O,Q){if(typeof O.fund=="undefined"){O.fund=$("#data").data("fund")}function W(ab,ac,aa){if(typeof Ext.getCmp("grid"+ab)=="undefined"){fields=[];for(R=0;R<ac.columns.length;R++){fields[R]=ac.columns[R].dataIndex}Ext.create("Ext.data.Store",{storeId:"store"+ab,fields:fields,data:ac,proxy:{type:"memory",reader:{type:"json",root:"rows"}},});return Ext.create("Ext.grid.Panel",{store:Ext.data.StoreManager.lookup("store"+ab),columns:ac.columns,id:"grid"+ab,border:false,flex:aa,})}}function N(ab){var aa=ab.split("-");if(typeof aa[1]=="undefined"){aa[1]=1;aa[0]=ab;ab=ab+"-1"}$.getJSON("/api/widget/fundsubredtable/?fund="+O.fund+"&year="+aa[0]+"&month="+aa[1],function(ac){tab=Ext.getCmp(ab);var ad=W(ab,ac,0);tab.add(ad);$.getJSON("/api/widget/subscriptionredemptionmonth/?fund="+O.fund+"&year="+aa[0]+"&month="+aa[1],function(af){tab=Ext.getCmp(ab);var ae=W("client"+ab,af,1);tab.add(ae)})})}function Y(ab,aa){$.getJSON("/api/widget/fundgrossasset/?fund="+O.fund+"&year="+aa,function(ad){var ac=v(ad,P.window);ab.insert(0,ac);ab.doLayout()})}function S(aa){fund=$("#data").data("fund");var ab=aa.toString().slice(-1);if($.isNumeric(ab)==false){if(aa=="ann_return"){aa="si"}else{if(aa!="si"){aa=aa+"1"}}}if(typeof Ext.getCmp("grid"+aa)=="undefined"){tab=Ext.getCmp(aa);$.getJSON("/api/widget/fundperfmonth/?fund="+fund+"&fields="+aa,function(ag){var af=W(aa,ag);tab.add(af);var ac="inner-tab"+aa;$('<div id="'+ac+'-bar"></div>').appendTo("#"+T);$('<div id="'+ac+'-line"></div>').appendTo("#"+T);widget={};widget.url="";widget.qs="/api/widget/fundperfbenchcompline/?fields="+aa+"&fund="+fund;widget.size_y=3;widget.size_x=6;widget.params={};widget.params.title="";var ad=$("#"+ac+"-bar").highcharts();if(typeof ad=="undefined"){widget.params.type="column";J("",widget,ac+"-bar")}var ae=new Ext.TabPanel({id:"inner-tab-id"+aa,height:600,activeTab:0,items:[{title:"Bar Chart",id:"bar"+aa,contentEl:ac+"-bar",},{title:"Line Graph",id:"line"+aa,contentEl:ac+"-line",}],listeners:{tabchange:function(aj,ai){if(ai.id=="line"+aa){div2=ac+"-line";var ah=$("#"+div2).highcharts();if(typeof ah=="undefined"){widget.params.type="line";J("",widget,div2)}}}}});tab.add(ae)})}}var V=O.page;var M=$("#data").data("grid"+V);var U='<div id="'+V+"_"+P.window.id+'" pagewindow="'+P.id+'" class="layout_block"></div>';M.add_widget(U,P.window.size_x,P.window.size_y,P.col,P.row);var Z="page_"+V+"_"+P.window.id;$('<div id="'+Z+'"></div>').appendTo("body");if(P.window.key=="w15"){$.getJSON("/api/widget/fundsummary/"+O.fund,function(aa){B(P.window.id,V,P.window.name,P.window.size_x,P.window.size_y,P.id,Z);html='<div> <table width="100%" class="html_table"><tr><td>Fund Name</td><td>'+aa.name+"</td></tr><tr><td>Fund Type</td><td>"+aa.fund_type.name+"</td></tr><tr><td>Fund Manager</td><td>"+aa.manager.first_name+aa.manager.last_name+"</td></tr><tr><td> Description</td><td>"+aa.description+"<d></tr><tr><td>Custodian</td><td>"+aa.custodian.name+"</td><td>"+aa.custodian.contact_name+"</td><td>"+aa.custodian.contact_number+"</td><td>Managment Fee</td><td>"+aa.management_fee+"</td><td>Performance Fee</td><td>"+aa.performance_fee+"</td></tr><tr><td>Administrator</td><td>"+aa.administrator.name+"</td><td>"+aa.administrator.contact_name+"</td><td>"+aa.administrator.contact_number+"</td><td>Administrator Fee</td><td>"+aa.administrator.fee+"</td></tr><tr><td>Auditor</td><td>"+aa.auditor.name+"</td><td>"+aa.auditor.contact_name+"</td><td>"+aa.auditor.contact_number+"</td><td>Auditor Fee</td><td>"+aa.auditor.fee+"</td></tr><tr><td>Subscription Terms</td><td>"+aa.subscription_frequency+"</td></tr><tr><td>Redemption Terms</td><td>"+aa.redemption_frequency+"</td></tr><tr><td>Management Fees</td><td>"+aa.management_fee+"</td></tr><tr><td>Performance Fees</td><td>"+aa.performance_fee+"</td></tr><tr><td>Benchmark</td><td>"+aa.benchmark.name+"</td></tr></table> </div>";$(html).appendTo("#"+Z)});return}if(P.window.key=="w18"){B(P.window.id,V,P.window.name,P.window.size_x,P.window.size_y,P.id,Z);parents=[{id:"ann_return",title:"Returns"},{id:"ann_volatility",title:"Volatility"},{id:"sharpe_ratio",title:"Sharpe"},{id:"alpha",title:"Alpha"},{id:"beta",title:"Beta"},{id:"correlation",title:"Correlation"},];children=[{id:"1",title:"1 Year Rolling Annualised"},{id:"3",title:"3 Years Rolling Annualised"},{id:"5",title:"5 Years Rolling Annualised"},];items=[];for(R=0;R<parents.length;R++){childItems=[];if(parents[R].id=="ann_return"){childItems.push({id:"si",title:"Since Inception"})}for(x=0;x<children.length;x++){childItems.push({id:parents[R].id+children[x].id,title:children[x].title,layout:"fit",})}items.push({xtype:"tabpanel",title:parents[R].title,id:"w18-parent-"+parents[R].id,activeTab:0,items:childItems,listeners:{tabchange:function(ab,aa){S(aa.id)}}})}var T="tab-"+P.window.key+"-"+Z;$('<div id="'+T+'"></div>').appendTo("#"+Z);var X=new Ext.TabPanel({renderTo:T,id:"w18-tabs",activeTab:0,items:items,layout:"fit",listeners:{tabchange:function(ab,aa){var ac=aa.id.split("-");S(ac[2])}}});S("si")}else{if(P.window.key=="w23"){this_year=new Date().getFullYear();parents=[];items=[];children=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];for(R=this_year;R>2002;R--){parents.push(R)}for(R=0;R<parents.length;R++){childItems=[];for(x=0;x<children.length;x++){childItems.push({id:parents[R]+"-"+(1+x),title:children[x],layout:{type:"vbox",align:"stretch"}})}items.push({xtype:"tabpanel",title:parents[R],id:"w23-parent-"+parents[R],activeTab:0,items:childItems,listeners:{tabchange:function(ab,aa){N(aa.id)}}})}var T="tab-"+P.window.key+"-"+Z;$('<div id="'+T+'"></div>').appendTo("#"+Z);var X=new Ext.TabPanel({renderTo:T,id:"w23-tabs",activeTab:0,items:items,layout:"fit",listeners:{tabchange:function(ab,aa){var ac=aa.id.split("-");N(ac[2])}}});N(this_year+"-1");return B(P.window.id,V,P.window.name,P.window.size_x,P.window.size_y,P.id,Z)}}if(P.window.key=="w13"){this_year=new Date().getFullYear();parents=[];items=[];for(R=this_year;R>2002;R--){parents.push(R)}for(R=0;R<parents.length;R++){items.push({title:parents[R],id:"w13-year-"+parents[R],})}var T="tab-"+P.window.key+"-"+Z;$('<div id="'+T+'"></div>').appendTo("#"+Z);var X=new Ext.TabPanel({renderTo:T,id:"w13-tabs",activeTab:0,items:items,layout:"fit",listeners:{tabchange:function(ab,aa){var ac=aa.id.split("-");Y(aa,ac[2])}}});tab=Ext.getCmp("w13-year-"+this_year);Y(tab,this_year);return B(P.window.id,V,P.window.name,P.window.size_x,P.window.size_y,P.id,Z)}$.ajax({type:"GET",url:"/api/widgets/?window="+P.window.id,ajaxI:R,success:function(ad){I=this.ajaxI;var ae=P.window.layout+"box";var ab=[];for(x=0;x<ad.length;x++){var ac="page_"+V+"_win_"+P.window.id+"_widget_"+ad[x].id;$('<div id="'+ac+'"></div>').appendTo("#"+Z);var aa=H(O,ad[x],ac);ab[x]={contentEl:ac,height:(120*ad[x].size_y)+(10*ad[x].size_y)+(10*(ad[x].size_y-1)),width:(120*ad[x].size_x)+(10*ad[x].size_x)+(10*(ad[x].size_x-1)),border:false,}}Ext.create("Ext.container.Container",{renderTo:Z,autoFit:true,title:"asdf",header:true,layout:ae,items:ab,});B(P.window.id,V,P.window.name,P.window.size_x,P.window.size_y,P.id,Z)}})}function B(P,R,S,N,M,O,Q){Ext.create("Ext.window.Window",{title:S,height:(120*M)+(10*M)+(10*(M-1))-10,width:(120*N)+(10*N)+(10*(N-1))-10,layout:"auto",floatable:false,draggable:false,closable:false,contentEl:Q,x:0,y:0,renderTo:R+"_"+P,tools:[{type:"close",handler:function(W,V,U,T){Ext.Msg.show({title:"Remove Widget?",msg:"You want to remove the widget from this page?",buttons:Ext.Msg.OKCANCEL,icon:Ext.Msg.CONFIRM,fn:function(Y){if(Y=="ok"){var X=$("#data").data("grid"+R);X.remove_widget($("#"+R+"_"+P));q(O)}}})}}],}).show()}function q(M){$.ajax({type:"DELETE",url:"/api/pagewindow/"+M+"/",success:function(){},error:function(N){},})}function H(P,O,R,N){if(typeof P.fund=="undefined"){P.fund=$("#data").data("fund")}if(typeof N!="undefined"){$.each(N,function(S,T){O.qs=O.qs.replace(S.toUpperCase(),T)})}$.each(O.params,function(S,T){O.qs=O.qs.replace(S.toUpperCase(),T)});if(typeof P.year=="undefined"||typeof P.month=="undefined"){P.year=new Date().getFullYear();P.month=new Date().getMonth()+1}O.div=R;O.url="/api/widget/"+O.key+"/";$.each(P,function(S,T){O.qs=O.qs.replace(S.toUpperCase(),T)});if(O.type=="month_table"){return A(P,O,R)}else{if(O.type=="data_table"){return t(P,O,R)}else{if(O.type=="data_table_sub"){return a(P,O,R)}else{if(O.type=="line_chart"){return J(P,O,R)}else{if(O.type=="chart_doubley"){j(P,O,R)}else{if(O.type=="bar_chart"){var Q=new Date();Q.setDate(1);Q.setHours(-1);var M=P.year+"-"+P.month+"-"+Q.getDate();O.qs=O.qs.replace("DATE",M);return s(P,O,R)}else{if(O.type=="line_bar_chart"){$("#data").data("linebar-div",R);$("#"+R).append("<p>Please select a Holding above</p>")}else{if(O.type=="pie_chart"){return k(P,O,R)}else{if(O.type=="euro_percent_table"){return w(P,O,R)}}}}}}}}}}function J(O,N,P){if(typeof N.params.type=="undefined"){var M="line"}else{var M=N.params.type}$.getJSON(N.url+N.qs,function(R){var Q=new Highcharts.StockChart({chart:{type:M,marginRight:25,size:"100%",renderTo:P,width:(120*N.size_x)+(10*N.size_x)+(10*(N.size_x-1))-10,height:(120*N.size_y)+(10*N.size_y)+(10*(N.size_y-1)),},navigator:{enabled:true,},scrollbar:{enabled:false},rangeSelector:{enabled:false,},title:{enabled:false,},xAxis:{gridLineWidth:1,},yAxis:{title:{text:"Performance"},plotLines:[{value:0,width:1,color:"#808080"}]},tooltip:{},legend:{enabled:true,},series:R,})})}function j(O,N,P){if(typeof N.params.type=="undefined"){var M="line"}else{var M=N.params.type}$.getJSON(N.url+N.qs,function(R){var Q=new Highcharts.StockChart({chart:{type:M,renderTo:P,width:(120*N.size_x)+(10*N.size_x)+(10*(N.size_x-1))-50,height:(120*N.size_y)+(10*N.size_y)+(10*(N.size_y-1))-100,},navigator:{enabled:true,},scrollbar:{enabled:false},rangeSelector:{},title:{text:false},yAxis:[{},{opposite:true}],series:R})})}function s(N,M,O){$.getJSON(M.url+M.qs,function(Q){title=false;if(typeof M.params.title!="undefined"&&M.params.title=="true"){title=M.name}type="column";if(typeof M.params.type!="undefined"){type=M.params.type}yDecimals=true;if(typeof M.params.yDecimals!="undefined"&&M.params.yDecimals==="false"){yDecimals=false}labels=true;if(typeof M.params.labels!="undefined"&&M.params.labels=="false"){labels=false}legend=true;if(typeof M.params.legend!="undefined"&&M.params.legend=="false"){legend=false}scrollbar=false;if(typeof M.params.scrollbar!="undefined"&&M.params.scrollbar=="true"){scrollbar=true}var P=new Highcharts.Chart({chart:{renderTo:O,type:type,width:(120*M.size_x)+(10*M.size_x)+(10*(M.size_x-1))-30,height:(120*M.size_y)+(10*M.size_y)+(10*(M.size_y-1))-35,},title:{text:false},subtitle:{text:false},yAxis:{title:{text:false,},allowDecimals:yDecimals,},legend:{enabled:legend,},series:[{data:Q,color:"white"}],exporting:{enabled:true},xAxis:{type:"category",categories:Q.columns,labels:{rotation:-45,align:"right",style:{fontSize:"10px",fontFamily:"Verdana, sans-serif"},enabled:labels,},},series:Q.objects,});$("#data").data("div-"+M.key,O)})}function A(N,M,O){$.getJSON(M.url+M.qs,function(S){var U=new Date(N.year,N.month-1,1);var W=U.getDay();var R=new Date(N.year,N.month,0);var V=R.getDate();var Q='<table class="month_table"><tr>';if(W<6){for(i=1;i<W;i++){Q+="<td></td>"}}days={};for(i=0;i<S.length;i++){var P=S[i].date.substr(8,2);P=parseInt(P,10);days[P]=S[i].value}for(i=1;i<=V;i++){if(typeof days[i]!="undefined"){var T=days[i]}else{var T=0}date=N.year.toString()+"-"+N.month.toString()+"-"+i;var U=new Date(date);if(U.getDay()==6||U.getDay()==0){if(U.getDay()==0&&i==1){continue}else{if(U.getDay()==6&&i==1){i++;continue}else{Q+="</tr><tr>";i++;continue}}}Q+="<td>"+i+'<a href="#" onclick="monthlyBar(\''+date+"', "+N.fund+');">'+T+"</a></td>"}Q+="</tr></table>";Ext.create("Ext.container.Container",{id:"month-table",width:400,renderTo:O,items:[{id:"month-table-content",xtype:"container",html:Q,}]})})}function l(N,M,O){fields=[];for(i=0;i<M.columns.length;i++){fields[i]=M.columns[i].dataIndex}console.log("HERE");Ext.create("Ext.data.Store",{storeId:N.key,fields:fields,data:M,proxy:{type:"memory",reader:{type:"json",root:"rows"}},});console.log(N.key);console.log(M.columns);console.log(M.rows);return Ext.create("Ext.grid.Panel",{title:N.params.title,store:Ext.data.StoreManager.lookup(N.key),columns:M.columns,height:(120*N.size_y)+(10*N.size_y)+(10*(N.size_y-1))-20,width:(120*N.size_x)+(10*N.size_x)+(10*(N.size_x-1))-20,layout:{type:"vbox",align:"stretch"},listeners:{cellclick:function(U,T,R,P){year=P.data.year;obj.page=$("#data").data("page_id");obj.grid=$("#data").data("grid"+obj.page);extra_params={year:year,};O=$("#data").data("piechart-div");var S="page_"+obj.page+"_win_"+N.window.id;month=R;N.key="fundperfholdperfbar";N.params.value_date__month=month;N.params.value_date__year=year;N.params.holding_category__holding_group="sec";N.params.fund="FUND";N.params.fields="nav";N.type="pie_chart";var Q=$("#"+O).highcharts();Q.destroy();$('<div id="'+widget_id+'"></div>').appendTo("#"+S);H(obj,widget_data[x],widget_id,extra_params)}}})}function w(N,M,O){$.getJSON(M.url+M.qs,function(R){if(typeof Ext.getCmp(O)!="undefined"){S=Ext.getCmp(O);S.destroy()}var S=Ext.create("Ext.tab.Panel",{renderTo:O,id:O,});M.params.title="€";var Q=l(M,R);S.add(Q);S.doLayout();var P=M.qs.replace("fields=nav","fields=weight");M.params.title="% of Fund";$.getJSON(M.url+P,function(U){var T=l(M,U);S.add(T);S.doLayout()})})}function v(Q,P){console.log(Q);var N=$("#data").data("fund");fields=[];c=0;for(i=0;i<Q.columns.length;i++){if(typeof Q.columns[i].columns!="undefined"){for(x=0;x<Q.columns[i].columns.length;x++){fields[c]=Q.columns[i].columns[x].dataIndex;c++}}else{if(typeof Q.columns[i].dataIndex!="undefined"){fields[c]=Q.columns[i].dataIndex;c++}}}fields.push("group");var M=Ext.create("Ext.data.Store",{storeId:"groupStore",fields:fields,groupField:"group",data:Q,proxy:{type:"memory",reader:{type:"json",root:"rows"}}});var O=Ext.create("Ext.grid.feature.Grouping",{groupHeaderTpl:"{name}"});return Ext.create("Ext.grid.Panel",{columnLines:true,store:Ext.data.StoreManager.lookup("groupStore"),columns:Q.columns,features:[O],width:(120*P.size_x)+(10*P.size_x)+(10*(P.size_x-1)),height:(120*P.size_y)+(10*P.size_y)+(10*(P.size_y-1)),})}function t(N,M,O){if(typeof N.fund!="undefined"){$("#data").data("fund",N.fund)}$.getJSON(M.url+M.qs,function(P){c=0;for(i=0;i<P.columns.length;i++){if(typeof P.columns[i].columns!="undefined"){for(x=0;x<P.columns[i].columns.length;x++){fields[c]=P.columns[i].columns[x].dataIndex;c++}}else{if(typeof P.columns[i].dataIndex!="undefined"){fields[c]=P.columns[i].dataIndex;c++}}}Ext.create("Ext.data.Store",{storeId:M.key,fields:fields,data:P.rows,proxy:{type:"memory",reader:{type:"json",root:"rows"}},sortInfo:{direction:"DESC",field:"year"},});return Ext.create("Ext.grid.Panel",{id:O,columnLines:true,store:Ext.data.StoreManager.lookup(M.key),columns:P.columns,width:(120*M.size_x)+(10*M.size_x)+(10*(M.size_x-1)),height:(120*M.size_y)+(10*M.size_y)+(10*(M.size_y-1)),header:false,border:false,enableLocking:true,autoScroll:true,renderTo:O,layout:"fit",listeners:{cellclick:function(T,S,R,Q){year=Q.data.year;N.page=$("#data").data("page_id");N.grid=$("#data").data("grid"+N.page);extra_params={year:year,};month=R;if(M.window.key=="w1"){if(R==0){K("w3",N,extra_params);K("w4",N,extra_params);K("w5",N,extra_params)}else{if(R<13){monthlyBar(year+"-"+month+"-1",N.fund)}}}if(M.window.key=="w6"){if(R==0){M.key="fundperfgrouptable";M.params.value_date__year=year;M.params.holding_category__holding_group="sec";M.params.fund="FUND";M.params.fields="nav";M.type="euro_percent_table";K("w8",N,extra_params);M.params.holding_category__holding_group="sub";K("w9",N,extra_params);M.params.holding_category__holding_group="loc";K("w10",N,extra_params)}else{if(R<13){monthlyBar(year+"-"+month+"-1",N.fund,"performance","weight")}}}}}})})}function K(N,O,M){$.getJSON("/api/widgets/?window__key="+N,function(P){for(x=0;x<P.length;x++){var T="page_"+O.page+"_win_"+P[x].window.id;var Q=T+"_widget_"+P[x].id;if(P[x].type=="data_table"){var R=Ext.getCmp(Q)}else{var R=$("#"+Q).highcharts()}try{R.destroy()}catch(S){}$('<div id="'+Q+'"></div>').appendTo("#"+T);H(O,P[x],Q,M)}})}function a(N,M,O){$.getJSON(M.url+M.qs,function(P){fields=["id"];for(i=0;i<P.columns.length;i++){fields[i]=P.columns[i].dataIndex}var Q=Ext.create("Ext.data.Store",{fields:fields,data:P.rows,proxy:{type:"memory",reader:{type:"json",root:"objects"}}});var R=Ext.create("Ext.grid.Panel",{store:Q,columns:P.columns,selModel:{selType:"cellmodel"},width:(140*M.size_x)+(10*M.size_x)+(10*(M.size_x-1)),height:(140*M.size_y)+(10*M.size_y)+(10*(M.size_y-1)),plugins:[{ptype:"rowexpander",rowBodyTpl:['<div id="innergrid{id}">',"</div>"]}],header:false,border:0,iconCls:"icon-grid",renderTo:O,id:"subtable"+M.key,});R.view.on("expandBody",function(V,T,S,U){var W=T.get("id");if(M.key=="fundperfholdtable"){$.getJSON("/api/widget/fundperfholdtradetable/?holding="+W+"&holding__fund="+N.fund,function(X){displayInnerGrid(X,W);M.holding=T.get("id");M.fund=N.fund;lineBarChart(M)})}else{if(M.key=="fundregister"){$.getJSON("/api/widget/subscriptionredemption/?&fund="+N.fund+"&client="+W,function(X){displayInnerGrid(X,W)})}}if(typeof $("#data").data("last-open-subgrid")!="undefined"){}});R.view.on("collapsebody",function(V,T,S,U){})})}function k(N,M,O){$("#data").data("piechart-div",O);if(M.key=="fundnavpie"){$("#data").data("linebar-div",O);$("#"+O).append("<p>Please click on a month</p>");return}$.getJSON(M.url+M.qs,function(Q){var P=new Highcharts.Chart({chart:{renderTo:O,marginTop:-20,marginLeft:20,marginRight:20,height:(120*2)+(10*2)+(10*(2-1)),width:(120*2)+(10*2)+(10*(2-1)),},title:{text:false},series:[{type:"pie",name:M.name,data:[["Utilities",45],["Financials",26.8]["Mining",26.8],]}]})})}function F(M){setInterval(function(){try{var N=Ext.StoreMgr.lookup(M);N.reload()}catch(O){}},2000)}function o(){var N=new Array();window.oldSetInterval=window.setInterval;window.setInterval=function(P,O){N.push(oldSetInterval(P,O))};for(var M in N){window.clearInterval(M)}}Ext.QuickTips.init();function h(){var M=$("#data").data("page_id");$.ajax({type:"GET",url:"/api/widget/unused/?page="+M,success:function(N){var O=Ext.create("Ext.data.Store",{storeId:"widgets",fields:["name","widget_type"],groupField:"widget_type",autoLoad:true,proxy:{data:N,type:"memory",reader:{type:"json",}},});var Q=Ext.create("Ext.grid.feature.Grouping",{groupHeaderTpl:'{name} ({rows.length} Item{[values.rows.length > 1 ? "s" : ""]})'});var P=Ext.create("Ext.grid.Panel",{iconCls:"icon-grid",frame:true,store:O,header:false,region:"west",width:"60%",bodyBorder:true,hideHeaders:true,features:[Q],columns:[{text:"Widget",flex:1,dataIndex:"name",},{text:"Type",flex:1,dataIndex:"widget_type",hidden:true,}],listeners:{itemclick:function(U,S){$.ajax({type:"GET",url:"/api/widget/info/"+S.data.id,success:function(W){$("#data").data("widget",W);html='<div class="widget_desc"><img src="'+STATIC_URL+"widget-images/"+W.key+'.png"></img><h1>'+W.name+"</h1>"+W.description+"</div>";var X=Ext.getCmp("widget_desc");X.update(html)},dataType:"json",contentType:"application/json",error:function(W){}});try{var T=Ext.getCmp("add_widget_btn");T.enable()}catch(V){}}}});var R=Ext.create("Ext.window.Window",{title:"Layout Window",closable:true,title:"Add Widget",width:"50%",height:"50%",layout:"border",items:[P,{region:"center",autoScroll:true,id:"widget_desc",html:'<div class="widget_preview">&#60;Preview&#62;</div>',}],buttonAlign:"right",buttons:[{scope:this,text:"Cancel",iconCls:"icon-cancel",handler:function(){R.close()}},{scope:this,text:"Add",iconCls:"icon-ok",disabled:true,id:"add_widget_btn",handler:function(){data=$("#data").data("widget");page=$("#data").data("page_id");P={};P.widget=data.resource_uri;P.page="/api/page/"+page+"/";P.row=1;P.col=1;P.size_y=data.size_y;P.size_x=data.size_x;$.ajax({type:"POST",url:"/api/pagewindow/",data:JSON.stringify(P),dataType:"json",contentType:"application/json",success:function(T){var U='<div id="'+page+"_"+data.key+'" pagewindow="'+T.id+'" class="layout_block"></div>';var S=$("#data").data("grid"+page);S.add_widget(U,data.size_x,data.size_y,1,1);H(data,page);B(data.key,page,data.name,data.size_x,data.size_y);R.close()},})}}],}).show()},error:function(N){}})}function g(M){var M=$.parseJSON(M);for(i=0;i<M.length;i++){data={col:M[i].col,row:M[i].row,};$.ajax({type:"PATCH",url:"/api/pagewindow/"+M[i].pagewindow+"/",data:JSON.stringify(data),dataType:"json",contentType:"application/json",error:function(N){},})}}function n(){return Ext.create("Ext.panel.Panel",{region:"center",id:"panel-home",contentEl:"menu",autoDestroy:true,autoScroll:true,defaults:{autoScroll:true},})}function p(){return Ext.create("Ext.tab.Panel",{region:"center",contentEl:"menu",id:"panel-tab",autoDestroy:true,autoScroll:true,layout:"fit"})}var y=new Ext.menu.Menu({items:[{text:"Resize Widget",id:"resize_widget",},{text:"Remove Widget",id:"remove_widget",}],defaults:{listeners:{click:function(N,M){if(N.id=="resize_widget"){}else{if(N.id=="remove_widget"){}}}}},});var E=Ext.create("Ext.menu.Menu",{items:[{text:"Change Theme",menu:{items:[{text:"Default",checked:true,group:"theme",id:"theme_default",checkHandler:D},{text:"BlueBay",checked:false,group:"theme",id:"theme_bluebay",checkHandler:D}]}},{text:"Re-order Panels",id:"enable_drag",},{text:"Lock Panels",id:"disable_drag",hidden:true,},{text:"Log out",id:"log_out",}],defaults:{listeners:{click:function(N,M){page=$("#data").data("page_id");if(N.id=="add_widget"){h()}else{if(N.id=="disable_drag"){$("#data").data("grid"+page).disable();Ext.getCmp("enable_drag").setVisible(true);Ext.getCmp("disable_drag").setVisible(false)}else{if(N.id=="enable_drag"){$("#data").data("grid"+page).enable();Ext.getCmp("disable_drag").setVisible(true);Ext.getCmp("enable_drag").setVisible(false)}else{if(N.id=="log_out"){C()}}}}}}},});function D(N,M){if(N.id==="theme_bluebay"){var O="extjs-themes/bluebay/css/bluebay.css"}else{if(N.id==="theme_default"){var O="extjs/resources/css/ext-all.css"}}Ext.util.CSS.swapStyleSheet("theme",STATIC_URL+O)}function m(M){$.ajax({type:"GET",url:"/api/"+M,success:function(N){$("#data").data(M,N)}})}function b(){$.ajax({type:"GET",url:"/api/menu/",success:function(P){var R=Ext.define("tree",{extend:"Ext.data.Model",fields:[{name:"id",type:"int"},{name:"text",type:"string",mapping:"name"},{name:"page",type:"string"},]});var O=Ext.create("Ext.data.TreeStore",{model:R,proxy:{data:P,type:"memory",reader:{type:"json",}},});var N=Ext.create("Ext.tree.Panel",{id:"main-menu",store:O,rootVisible:false,preventHeader:true,border:false,autoScroll:true,useArrows:true,height:1000,listeners:{itemexpand:{fn:function(S,T){nodeId=S.data.id}},itemclick:{fn:function(T,S,X,U,W,V){if(S.isExpanded()){S.collapse()}else{S.expand()}$("#data").data("fund",S.raw.fund);if(S.raw.page!==null){if(typeof S.raw.page==="object"){S.raw.page=S.raw.page.id}else{var Y=S.raw.page.toString();S.raw.page=Y.replace(/\D/g,"")}}f(S.raw)}}}});var Q=Ext.create("Ext.panel.Panel",{id:"west",region:"west",collapsible:true,title:"Navigation",width:150,items:[N],tools:[{type:"gear",handler:function(V,U,T,S){E.showBy(U,"tr-br?")}}],});var M=Ext.create("Ext.container.Viewport",{layout:"border",id:"viewport",items:[Q,n()]});Ext.EventManager.onWindowResize(M.doLayout,M)}})}Ext.QuickTips.init();var u=new Ext.FormPanel({labelWidth:80,url:"/api/user/login/",frame:true,defaultType:"textfield",monitorValid:true,header:false,style:"padding:10px",headers:{"Content-Type":"application/json"},items:[{fieldLabel:"Username",name:"username",allowBlank:false},{fieldLabel:"Password",name:"password",inputType:"password",allowBlank:false}],buttons:[{text:"Login",formBind:true,handler:function(){u.getForm().submit({method:"POST",headers:{"Content-Type":"application/json","X-HTTP-Method-Override":"POST"},success:function(){e.close();m("fund");m("page");b();page=new Object();page.page=1;L(page)},failure:function(M,N){Ext.Msg.alert("Login failed!","Wrong user name or passsword");u.getForm().reset()}})}}],});var e=new Ext.Window({closeAction:"hide",id:"login-window",title:"Please Login",layout:"fit",width:300,height:150,closable:false,resizable:false,plain:true,border:false,items:[u]});$("#data").data("login-window",e);function C(){$.ajax({type:"GET",url:"/api/user/logout/",success:function(M){var N=$("#data").data("active-panel");Ext.getCmp("west").setVisible(false);Ext.getCmp(N).setVisible(false);$("#data").data("login-window").show()},failure:function(){Ext.Msg.alert("Logout failed!","You could not be logged out.")}})}function G(M){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(M))}$.ajaxSetup({crossDomain:false,beforeSend:function(N,M){if(!G(M.type)){N.setRequestHeader("X-CSRFToken",$.cookie("csrftoken"))}}});$.ajax({type:"GET",url:"/api/loggedin/",success:function(M){m("page");$('<div id="menu" class="gridster"></div>').appendTo("body");b();$('<div id="page1"></div>').appendTo("#menu");$("#data").data("active-panel","panel-home");page=new Object();page.page=1;L(page)},error:function(){$('<div id="menu" class="gridster"></div>').appendTo("body");$('<div id="page1"></div>').appendTo("#menu");$("#data").data("active-panel","panel-home");e.show()}})});