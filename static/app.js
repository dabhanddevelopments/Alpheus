
Ext.Loader.setPath('Ext.ux', 'static/ext-4.2.0/examples/ux');
Ext.require([
    'Ext.ux.RowExpander'
]);

Ext.require([
    'Ext.container.Viewport',
    'Ext.layout.container.Border',
    'Ext.tab.Panel',
    'Ext.tree.*',
    'Ext.data.*',
    'Ext.menu.*',
    'Ext.window.MessageBox',
    'Ext.grid.*',
]);

function displayInnerGrid(renderId) {

    $.getJSON("/api/widget/tradetable/?identifier=" + renderId, function(data) {
    
        console.log('render id: ' + renderId.toString());
    
        fields = [];
        for(i=0; i < data.columns.length; i++) {
            fields[i] = data.columns[i].dataIndex;
        }
        
        var insideGridStore = Ext.create('Ext.data.Store', {
            //storeId: "inner_" + widget.key,
            fields: fields,
            data: data.rows,
            proxy: {
                type: 'memory',
                reader: {
                    type: 'json',
                    root: 'objects'
                }
            }
        });
        
        var innerGrid = Ext.create('Ext.grid.Panel', {
            store: insideGridStore,
            selModel: {
                selType: 'cellmodel'
            },
            columns: data.columns,
            header: false,
            width: 500,
            height: 150,
            iconCls: 'icon-grid',
            renderTo: renderId,
        });
        innerGrid.getEl().swallowEvent([
            'mousedown', 'mouseup', 'click',
            'contextmenu', 'mouseover', 'mouseout',
            'dblclick', 'mousemove'
        ]);

    });
}


function lineBarChart(obj, widget) {

    var div = $('#data').data('linebar-div');
    var chart = $('#' + div).highcharts();
    chart.destroy();

   $.getJSON(widget.url + widget.qs, function(data) {
     
        var options = {     
            chart: {
                renderTo: div,
                marginTop: 5,
            },
            navigator:{
                enabled:true
            },
            scrollbar: {
                enabled:false, //remove ugly scrollbar
            },

            rangeSelector: {
                enabled: true,
	            //selected: 1
            },  
            title: {
                text: false,
            },
            xAxis: [{
                gridLineWidth: 1,
                type : "datetime",
                labels: {
                    rotation: -45,
                    align: 'right',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                },

            },{ }],
            yAxis: [
            {
                height: 180,
                lineWidth: 3,
                offset: 0,
                gridLineWidth: 1,
                title: {
                    text: 'Price',
                    margin: 5,
                }
            },
            {
                top: 225,
                lineWidth: 3,
                //min: 0,
                //max: 5,
                gridLineWidth: 1,
                offset: 0,
                height: 75,
                title: {
                    text: 'Volume',
                }
            },
            ],
            
            legend: {
                enabled: true,
                //layout: 'vertical',
                //align: 'right',
                verticalAlign: 'top',
                y: -10,
                //y: 100,
                //borderWidth: 0
            },
            series: [
            {
                yAxis: 0,
                name: 'Price by time',
                stack: 0,

                //data: [1, 12, 32, 43],       
                data: data.line,
		        tooltip: {
			        valueDecimals: 2
		        }, 
		                  
            },
            {
                name: 'Volume by time',
                yAxis: 1,
                stack: 0,
                data: data.bar,
		        tooltip: {
			        valueDecimals: 2
		        },  
                lineWidth: 3,
                marker: {
                    enabled: false
                },
                pointWidth: 5,
                type: 'column',
                
            },
            ]
        };

        var chart = new Highcharts.Chart(options);

        });
    }

function destroyInnerGrid(record) {

    var parent = document.getElementById(record.get('id'));
    var child = parent.firstChild;

    while (child) {
        child.parentNode.removeChild(child);
        child = child.nextSibling;
    }

}

//call chart on click
// TODO: rewrite when you figure out how to get the id of the cell clicked
function monthlyBar(date, fund) {

    var div = $('#data').data('div-holdperfbargraph');
    console.log(div);
    var chart = $('#' + div).highcharts();
    
    var url = '/api/widget/holdperfbargraph/?date=' + date + '&fund=' + fund + '&order_by=weight';
    //return monthTable(url, 'fundperfdaily', div);

console.log('CALLEd');
console.log(url);
    try {
        chart.destroy();
        $.getJSON(url, function(data) {

                var chart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        type: 'column',
                        //width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10,
                        //height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 30,
                    },  
                    //title: {
                    //    text: '',
                    //},
                    labels: {
                        rotation: -45,
                        align: 'right',
                        style: {
                            fontSize: '10px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    },
                    xAxis: {
                        type: 'category',
                        categories: data.columns,
                    },
                    series: data.objects,
                });
        });
    } catch (err) {
        //do nothing
    }
};    
    

Ext.onReady(function() {



    //$('<div id="main" class="gridster"></div>').appendTo('body');
    $('<div id="data"></div>').appendTo('body');

    function initPage(obj) {
    
        var id = obj.page;
        console.log(id);
        console.log(obj);
        // All pages used on the site. This is loaded on start.
        // @TODO: Redo this
        var pages = $('#data').data('page');

        // No need to reload the page if users clicks on a link 
        // to a page they are already on
        //if($('#data').data('active-panel') == id) {
        //    return
        //}
        for(i=0; i<pages.length; i++) {

            if(pages[i].id == id) {
            //    var page = pages[i];
    

                el = 'page' + id;

                // Children are tabs
                if(pages[i].children !== undefined) {

                    var panel = panelTab();

                    switchPanel(panel, el);
                    appendTabs(pages[i]);
                    
                    obj.page = pages[i].children[0].id;
                    //console.log('child tabs');
                    //console.log(obj);
                    //console.log(pages[i].children);
                    

                } else {

                    var panel = panelStandard();
                    switchPanel(panel, el);

                    $('#data').data('grid' + id, '');
                    $('<div id="page' + id + '"></div>').appendTo('#menu');
                }
                
                initGrid(obj);
                    
                // stops all widgets to auto reload/refresh
                //clearAllIntervals();
            }
        }
    }


    // dynamically adds the tabs to the tab panel from the supplied pages
    function appendTabs(tabs) {

        var panel = Ext.getCmp('panel-tab');

        panel.removeAll();
        //$('<div id="page' + tabs.id + '" class="gridster"></div>').appendTo('body');
        //$('#data').data('grid' + tabs.id, ''); // ???

//console.log('adding div page' + tabs.id);
        // The root is the first tab
        /*
        panel.add({
            id: tabs.id,
            title: tabs.title,
            contentEl: 'page' + tabs.id,
            autoScroll:true,
            listeners: {
                activate: function(tab){
                    initGrid(tab.id);
                }
            },
        });
        */ 

        for(x=0; x<tabs.children.length; x++) {

            id = tabs.children[x].id;

            $('<div id="page' + id + '" class="gridster"></div>').appendTo('body');
            $('#data').data('grid' + id, '');

            panel.add({
                title: tabs.children[x].title,
                id: id,
                contentEl: 'page' + id,
                autoScroll:true,
                listeners: {
                    activate: function(tab){
                        initGrid(tab.id);
                    }
                },
            }); 
        }
        panel.setActiveTab(0);
    }
        

    function switchPanel(panel, el) {

        var active = $('#data').data('active-panel'); 

        var ws = Ext.getCmp('viewport');

        try {
            ws.remove(active);
        } catch(err) {
            console.log("Failed to remove panel");
            console.log(err);
        }

        // The 'main' DOM element gets destroyed on remove() with autoDestroy
        // set to true, so we have to re-add it
        $('<div id="menu" class="gridster"></div>').appendTo('body');


        try {
            ws.add(panel);
        } catch(err) {
            console.log("Failed to add panel");
            console.log(err);
        }
  
        ws.doLayout();  

        // Save the panel so we know which one to destroy next time
        $('#data').data('active-panel', panel.id);

    }

    function initGrid(obj) {
        
        var page = obj.page;
        
//console.log('initiating grid');


        $('#data').data('page_id', page);
    
        // if we have a grid for this page, it means it's already 
        // loaded and we do not need to fetch it again
        if($('#data').data('grid' + page) !== undefined && $('#data').data('grid' + page) !== '') {

            console.log('skipping gridster: grid' + page);
            return;
        }

        obj.grid = $("#page" + page).gridster({
            widget_margins: [10, 10],
            widget_base_dimensions: [140, 140],
            max_size_x: 10,
            max_size_y: 10,
            draggable: {
                stop: function(event, ui){ 
                    saveWidgetPositions(JSON.stringify(grid.serialize()));
                    //console.log('widget stopped');
                }
            },
            serialize_params: function($w, wgd) { 
                return { 
                    id: wgd.el[0].id, 
                    col: wgd.col, 
                    row: wgd.row,
                    size_y: wgd.size_y,
                    size_x: wgd.size_x,
                    pagewindow: $w.context.attributes.pagewindow.value,
                } 
            }
        }).data('gridster');

        obj.grid.disable();

        $('#data').data('grid' + page, obj.grid);

        $.ajax({
            type: "GET",
            url: '/api/pagewindow/?page=' + page,
            success: function(data) {

                $('#data').data('grid_data' + page, data);
                
                
                // get the window id from pagewindow by filtering by page id (of current page)
                // delete window div/dom
                // create function below
                // call that function with the 
                

                for(i=0; i<data.length; i++) {
                
                    createWindows(data[i], i, obj);

                }       
            }
        });
    }
    

    function createWindows(data, i, obj, extra_params) {
    
        var page = obj.page;
        var grid = $('#data').data('grid' + page); // obj.grid;
        var window = '<div id="' + page + '_' + data.window.id + '" pagewindow="' + data.id + '" class="layout_block"></div>';
        
console.log('DAATA win');
console.log($('#3_5'));
        grid.add_widget(window, data.size_x, data.size_y, data.col, data.row);
        
        
        // get the widgets for this window
        $.ajax({
            type: "GET",
            url: '/api/widgets/?window=' + data.window.id,
            ajaxI: i,
            success: function(widgets) {
            
                // now I will be i asynchronously
                I = this.ajaxI;
            
                // div for window
                var window_id = 'page_' + page + '_' + data.window.id;
                $('<div id="' + window_id + '"></div>').appendTo('body'); 
                console.log('window id: ' + window_id);

                // vbox or hbox
                var layout = data.window.layout + 'box'; 

                var items = [];
                
                for(x=0; x<widgets.length; x++) {
                
                    // div for widget
                    var widget_id = 'page_' + page + '_win_' + data.window.id + '_widget_' + widgets[x].id;
                    $('<div id="' + widget_id + '"></div>').appendTo('#' + window_id);
                    
                    items[I] = {
                        renderTo: widget_id,        
                        height: (140 * data.size_y) + (10 * data.size_y) + (10 * (data.size_y - 1)) - 20,
                        width:  (140 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                        border: false,   
                    }
                    
                    createWidget(obj, widgets[x], widget_id);
                }
                
                Ext.create('Ext.container.Container', {
                    renderTo: window_id,
                    layout: layout,
                    items: items
                });
                
                widgetWindow(data.window.id, page, data.window.name, data.size_x, data .size_y, data.id, window_id);
            }
        });
    } 

    function widgetWindow(key, page, title, size_x, size_y, pagewindow, window) {
    
        Ext.create('Ext.window.Window', {
            title: title,
            // there's gotta be a better way to do this
            height: (140 * size_y) + (10 * size_y) + (10 * (size_y - 1)) - 10,
            width:  (140 * size_x) + (10 * size_x) + (10 * (size_x - 1)) - 10,
            layout: 'auto',
            floatable: false,
            draggable: false,
            closable: false, 
            contentEl: window,
            x: 0,
            y: 0,
            renderTo: page + '_' + key,
            tools: [{
               type: 'close',
               handler: function(e, toolEl, panel, tc) {
                    Ext.Msg.show({
                         title:'Remove Widget?',
                         msg: 'You want to remove the widget from this page?',
                         buttons: Ext.Msg.OKCANCEL,
                         icon: Ext.Msg.CONFIRM,
                         fn:function (buttonId) {
                             //console.log('buttonId:' + buttonId);
                             if (buttonId == "ok") {

                                var grid = $('#data').data('grid' + page);

                                grid.remove_widget($('#' + page + '_' + key));

                                removePageWindow(pagewindow);
                            }
                         }
                    });
               }
            }],
        }).show();
    }

    function removePageWindow(id) {
         $.ajax({
            type: "DELETE",
            url: "/api/pagewindow/" + id + '/',
            success: function() {
                //console.log('removed widget');
            },
            error: function(err) {
                //console.log('problem removing widget');
                //console.log(err);
            },
        });          
    }

    function createWidget(obj, widget, div, extra_params) {
    
    
        // new way
        if(typeof extra_params != 'undefined') {
            $.each(extra_params, function(key, value) {
                 widget.qs = widget.qs.replace(key.toUpperCase(), value);
            });
        }
        $.each(widget.params, function(key, value) {
             //console.log(key.toString() + value.toString());
             widget.qs = widget.qs.replace(key.toUpperCase(), value);
        });
        
        if(typeof obj.year == 'undefined' || typeof obj.month == 'undefined') {
            obj.year = new Date().getFullYear();
            obj.month = new Date().getMonth() + 1;
        }
        
        widget.div = div; // remove this later
        widget.url = '/api/widget/' + widget.key + '/';

        // old way
        $.each(obj, function(key, value) {
             widget.qs = widget.qs.replace(key.toUpperCase(), value);
        });

        
        if(widget.type == 'month_table') {
        
            return monthTable(obj, widget, div);
            
        } else if(widget.type == 'data_table') {
        
            return dataTable(obj, widget, div);
            
        } else if(widget.type == 'data_table_sub') {
        
            return dataTableSub(obj, widget, div);
            
        } else if(widget.type == 'line_chart') {
        
            return lineChart(obj, widget, div);
        
        } else if(widget.type == 'bar_chart') {
        
            // get last day of last month
            var d=new Date(); 
            d.setDate(1); 
            d.setHours(-1);
            
            var formatted_date = obj.year + '-' + obj.month + '-' + d.getDate();
            widget.qs = widget.qs.replace('DATE', formatted_date);
            
            return barChart(obj, widget, div);
            
        } else if(widget.type == 'line_bar_chart') {
            return LineBarChart(obj, widget, div);
       
       }
        try {
            $.getJSON(url, function(data) {
                switch(widget.type) {
                  case 'graph':      graph(widget, data, div); break;
                  case 'pie_chart':  pieChart(widget, data, div); break;
                }

                // enables ajax auto reload/refresh for this widget
                //enableReload(widget.id);
            })
        } catch (err) {
            //console.log(err);
        }
    }

    function graph(widget, data, div) {

//console.log('creating graph');
        try {
            $.jqplot(div, data, 
                { 
                  axes:{yaxis:{min:-10, max:240}}, 
                  series:[{color:'#5FAB78'}]
            });
        } catch (err) {
            //console.log(err);
        }
    }
    
    function lineChart(obj, widget, div) {
    
        $.getJSON(widget.url + widget.qs, function(data) {
            
            var chart = new Highcharts.StockChart({
                chart: {
                    type: 'line',
                    marginRight: 25,
                    //marginBottom: 25,
                    size: '100%',
                    renderTo: div,
                    width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10,
                    height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                },
                navigator:{
                    enabled:true,
                },
                scrollbar: {
                    enabled:false
                },

                rangeSelector: {
                    enabled: false,
	                //selected: 1
                },                  
                title: {
                    enabled: false,
                //    text: widget.name,
                //    x: -20 //center
                },
                xAxis: {
                    gridLineWidth: 1,
                },
                yAxis: {
                    title: {
                        text: 'Performance'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    //valueSuffix: '€'
                },
                legend: {
                    enabled: true,
                    //layout: 'vertical',
                    //align: 'right',
                    //verticalAlign: 'top',
                    //x: -10,
                    //y: 100,
                    //borderWidth: 0
                },
                series: data,
            });
        });
    }

    function barChart(obj, widget, div) {
    
        $.getJSON(widget.url + widget.qs, function(data) {
        
        
            title = false;
            if(typeof widget.params.title != 'undefined' && widget.params.title == "true") {
                title = widget.name;
            }
            
        
            legend = true;
            if(typeof widget.params.legend != 'undefined' && widget.params.legend == "false") {
                legend = false;
            }
        
            scrollbar = false;
            if(typeof widget.params.scrollbar != 'undefined' && widget.params.scrollbar == "true") {
                scrollbar = true;
            }
    
            var chart = new Highcharts.Chart({
                chart: {
                    //marginRight: 25,
                    //marginTop: 50,
                    //marginBottom: 50,
                    renderTo: div,
                    type: 'column',
                    width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10,
                    height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 30,
                }, 
                title: {
                    text: false
                },
                subtitle: {
                    text: false
                },

                yAxis: {
                    title: {
                        text: false,//'Holding Performance XXXX-XX-XX'
                    }
                },
                legend: {
                    enabled: legend,
                },
                series: [{
                    //name: name,
                    data: data,
                    color: 'white'
                }],
                exporting: {
                    enabled: true
                },
                labels: {
                    rotation: -45,
                    align: 'right',
                    style: {
                        fontSize: '10px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                },
                xAxis: {
                    type: 'category',
                    categories: data.columns,
                    //type : "datetime",
                },
                series: data.objects,            
            })
        

                    
         $('#data').data('div-' + widget.key, div);
            
        });
        


    }
    

    function LineBarChart(obj, widget, div) {
    
        $('#data').data('linebar-div', div);

        $.getJSON(widget.url + widget.qs, function(data) {
        
       var options = {     
            chart: {
                renderTo: div,
                marginTop: 5,
            },
            navigator:{
                enabled:true
            },
            scrollbar: {
                enabled:false, //remove ugly scrollbar
            },

            rangeSelector: {
                enabled: true,
	            //selected: 1
            },  
            title: {
                text: false,
            },
            xAxis: [{
                gridLineWidth: 1,
                type : "datetime",
                labels: {
                    rotation: -45,
                    align: 'right',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                },

            },{ }],
            yAxis: [
            {
                height: 180,
                lineWidth: 3,
                offset: 0,
                gridLineWidth: 1,
                title: {
                    text: 'Price',
                    margin: 5,
                }
            },
            {
                top: 225,
                lineWidth: 3,
                //min: 0,
                //max: 5,
                gridLineWidth: 1,
                offset: 0,
                height: 75,
                title: {
                    text: 'Volume',
                }
            },
            ],
            
            legend: {
                enabled: true,
                //layout: 'vertical',
                //align: 'right',
                verticalAlign: 'top',
                y: -10,
                //y: 100,
                //borderWidth: 0
            },
            series: [
            {
                yAxis: 0,
                name: 'Price by time',
                stack: 0,

                //data: [1, 12, 32, 43],       
                data: data.line,
		        tooltip: {
			        valueDecimals: 2
		        }, 
		                  
            },
            {
                name: 'Volume by time',
                yAxis: 1,
                stack: 0,
                data: data.bar,
		        tooltip: {
			        valueDecimals: 2
		        },  
                lineWidth: 3,
                marker: {
                    enabled: false
                },
                pointWidth: 5,
                type: 'column',
                
            },
            ]
        };

        var chart = new Highcharts.Chart(options);
        
        });        
    }
        
            
    

    function monthTable(obj, widget, div) {
    
        
        //console.log(widget.url + widget.qs);
        $.getJSON(widget.url + widget.qs , function(data) {
        
            // first day in first week of month
            var d = new Date(obj.year, obj.month - 1, 1);
            var first_weekday = d.getDay();
            
            // last day of the month
            var d2 = new Date(obj.year, obj.month, 0);
            var last_day_of_month = d2.getDate();

            var html = '<table class="month_table"><tr>';
            
            // empty cells for months that do not start on a monday
            if(first_weekday < 6) {
                for(i=1; i<first_weekday; i++) {
                    html += "<td></td>";
                }
            }
            
            // converting the data object
            days = {};
            for(i=0; i < data.length; i++) {
                var day = data[i].date.substr(8,2);
                day = parseInt(day, 10);
                days[day] = data[i].value;
            }
            
            for(i=1; i<=last_day_of_month; i++) {
            
                if(typeof days[i] != 'undefined') {
                    var val = days[i];
                } else {
                    var val = 0;
                }
                
                date = obj.year.toString() + '-' + obj.month.toString() + '-' + i;

                // exclude weekends
                var d = new Date(date);
                if(d.getDay() == 6 || d.getDay() == 0) {
                
                    // first day of month is a sunday
                    if(d.getDay() == 0 && i == 1) {
                        continue;
                    // first day of month is a saturday
                    } else if(d.getDay() == 6 && i == 1) {
                        i++;
                        continue;
                    // is normal weekend. break row 
                    } else {
                        html += "</tr><tr>";
                        i++;
                        continue;   
                    }
                
                }
                html += '<td>' + i + '<a href="#" onclick="monthlyBar(\'' + date + '\', ' + obj.fund + ');">' + val + '</a></td>';
            }
            
            html += "</tr></table>";
        
            Ext.create('Ext.container.Container', {
                id: 'month-table',
                width: 400,
                renderTo: div,
                items: [{
                    id: 'month-table-content',
                    xtype: 'container',
                    html: html,
                }]
            });
        });
    }

    function dataTable(obj, widget, div) {
    
        // TODO: get rid of this later
        if(typeof obj.fund != 'undefined') {
            $('#data').data('fund', obj.fund);
        }
    
        $.getJSON(widget.url + widget.qs, function(data) {
        
            var fund = $('#data').data('fund');
            
            fields = [];
            for(i=0; i < data.columns.length; i++) {
                fields[i] = data.columns[i].dataIndex;
            }
            //console.log(fields);
 
            Ext.create('Ext.data.Store', {
                storeId: widget.key,
                fields: fields,
                data: data.rows,
                proxy: {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'rows'
                    }
                },
                sortInfo: {
                    direction: "DESC",
                    field: "year"
                },
            });

            Ext.create('Ext.grid.Panel', {
                id: div,
                store: Ext.data.StoreManager.lookup(widget.key),
                columns: data.columns,
                width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                header: false,
                border: false,
                enableLocking: true,
                autoScroll: true,
                renderTo: div,
                forceFit: true,
                listeners: {
                    cellclick: function(gridView,htmlElement,columnIndex,dataRecord) {
                    
                        year = dataRecord.data.year;
                        
                        obj.page = $('#data').data('page_id');
                        obj.grid = $('#data').data('grid' + obj.page);
                        extra_params = {
                            year: year,
                        }
                        
                        refreshWindow('w3', obj, extra_params);
                        refreshWindow('w4', obj, extra_params);
                        refreshWindow('w5', obj, extra_params);
                        
                        // year view
                        if(columnIndex == 0) {
                            
                        // month view
                        } else if(columnIndex < 13) {
                            month = columnIndex;
                            
                            
                            
                            var panel = Ext.getCmp("month-table");
                            panel.remove('month-table-content');
                            
                            obj = {};
                            obj.month = month;
                            obj.year = year;
                            obj.fund = fund;
                            widget.key = "fundperfmonthtable";
                            widget.params.date__year = "YEAR";
                            widget.params.date__month = "MONTH";
                            widget.params.fund = "FUND";
                            widget.type = "month_table";
                            createWidget(obj, widget, panel.renderTo);
                        }
                    }
                }
            });
        });
    }
    
    function refreshWindow(window_key, obj, extra_params) {
        $.getJSON('/api/widgets/?window__key=' + window_key, function(widget_data) {
            
            for(x=0; x<widget_data.length; x++) {
            
                var window_id = 'page_' + obj.page + '_win_' + widget_data[x].window.id;
                var widget_id = window_id + '_widget_' + widget_data[x].id;
                
                if(widget_data[x].type == 'data_table') {
                    var widget_obj = Ext.getCmp(widget_id);
                    
                } else {
                    var widget_obj = $('#' + widget_id).highcharts();
                }
                widget_obj.destroy();
                
                $('<div id="' + widget_id + '"></div>').appendTo('#' + window_id);
                
                createWidget(obj, widget_data[x], widget_id, extra_params);
            }
            
        });
    }
    
    function dataTableSub(obj, widget, div) {
    
        $.getJSON(widget.url + widget.qs, function(data) {
        
            fields = ['id'];
            for(i=0; i < data.columns.length; i++) {
                fields[i] = data.columns[i].dataIndex;
            }
         
            var mainStore = Ext.create('Ext.data.Store', {
                //storeId: widget.key,
                fields: fields,
                data: data.rows,
                proxy: {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'objects'
                    }
                }
            });
            
            
            var mainGrid = Ext.create('Ext.grid.Panel', {
                store: mainStore,
                columns: data.columns,
                //autoWidth: true,
                selModel: {
                    selType: 'cellmodel'
                },
                //autoHeight: true,
                width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                plugins: [{
                    ptype: 'rowexpander',
                    rowBodyTpl: [
                        '<div id="{id}">',
                        '</div>'
                    ]
                }],
                header: false,
                border: 0,
                iconCls: 'icon-grid',
                renderTo: div
            });

            mainGrid.view.on('expandBody', function (rowNode, record, expandRow, eOpts) {
                var id = record.get('id');
                displayInnerGrid(record.get('id'));
                
                widget.url = '/api/widget/holdlinegraph/';
                widget.qs = '?identifier=' + record.get('id') + '&fund=' + obj.fund;
                widget.div = div;
                
                lineBarChart('', widget);
                
                if(typeof $('#data').data('last-open-subgrid') != 'undefined') {
                    //destroyInnerGrid($('#data').data('last-open-subgrid'));
                }
1            });
            mainGrid.view.on('collapsebody', function (rowNode, record, expandRow, eOpts) {
                destroyInnerGrid(record);
            }); 
            
        });
    
    }

    function pieChart(widget, data, div) {


        var chart = new Highcharts.Chart({
            chart: {
                renderTo: div,
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Browser market shares at a specific website, 2010'
            },
            tooltip: {
        	    pointFormat: '{series.name}: <b>{point.percentage}%</b>',
            	percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    size: 200,
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Browser share',
                data: [
                    ['Firefox',   45.0],
                    ['IE',       26.8],
                    {
                        name: 'Chrome',
                        y: 12.8,
                        sliced: true,
                        selected: true
                    },
                    ['Safari',    8.5],
                    ['Opera',     6.2],
                    ['Others',   0.7]
                ]
            }]
        });

//console.log('creating pie chart');
//console.log(data);
/*
        var plot1 = jQuery.jqplot(div, data, 
        { 
            seriesDefaults: {
                renderer: jQuery.jqplot.PieRenderer, 
                rendererOptions: {
                    showDataLabels: true
                }
            }, 
            legend: { show:true, location: 'e' }
        });
*/
    }


    function enableReload(storeId) { 

////console.log(storeId);
            setInterval(function() {

            try {
                var store = Ext.StoreMgr.lookup(storeId);
                store.reload();
            } catch(err) {
                ////console.log(err);
            }
        }, 2000);
    }

    function clearAllIntervals() {
        var intervals = new Array();
        window.oldSetInterval = window.setInterval;
        window.setInterval = function(func, interval) {
            intervals.push(oldSetInterval(func, interval));
        }
        for (var interval in intervals) {
           window.clearInterval(interval);
        }
    }

/*
    var overviewStore = Ext.create('Ext.data.Store', {
        storeId:'overview_table',
        fields:['name', 'aum', 'mtd', 'ytd', 'one_day_var', 'total_cash', 'usd_hedge', 'checks', 'unsettled', ],
        autoLoad: {start: 0, limit: 50 },
        //autoLoad: false,
        pageSize: 50, // items per page
        proxy: {
            type: 'ajax',
            url: 'api/funds/?format=json',
            reader: {
                type: 'json',
                root: 'rows',
                totalProperty: 'total',
                id: 'id',
            }
        },
    });

    var overviewGrid = Ext.create('Ext.grid.Panel', {
        title: 'Overview Table',
        store: overviewStore,
        columns: [
            { text: 'id', dataIndex: 'id', locked: true, width: 30 },
            { text: 'Fund Name',  dataIndex: 'name', locked: true, width: 150},
            { text: '€ AUM', dataIndex: 'aum' },
            { text: 'Checks', dataIndex: 'checks' },
            { text: '% MTD', dataIndex: 'mtd' },
            { text: '% YTD', dataIndex: 'ytd' },
            { text: '1 Day Var', dataIndex: 'one_day_var' },
            { text: 'Cash Held <br>in Fund', dataIndex: 'total_cash' },
            { text: "USD Positions <br>Current FX Hedge", dataIndex: 'usd_hedge' },
            { text: 'Unsettled', dataIndex: 'unsettled' },
        ],
        height: "100%",
        width: "100%",
        header: false,
        border: true,
        enableLocking: true,
        autoScroll: true,
        //renderTo: 'center1',
        viewConfig: {
            loadMask: false 
        },
        dockedItems: [{
            xtype: 'pagingtoolbar',
            store: overviewStore,   // same store GridPanel is using
            dock: 'bottom',
            displayInfo: true
        }],
        listeners: {
            activate: function(tab) {
                clearAllIntervals();
                enableReload('overview_table');
            }
        }
    });


    // So the window dimensions stay 100% when the window is resized
    Ext.EventManager.onWindowResize(overviewGrid.doLayout, overviewGrid); 
*/

    Ext.QuickTips.init();


    // NOTE: This is an example showing simple state management. During development,
    // it is generally best to disable state management as dynamically-generated ids
    // can change across page loads, leading to unpredictable results.  The developer
    // should ensure that stable state ids are set for stateful components in real apps.
    //Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));


    function addWidget() {

        var page_id = $('#data').data('page_id');

        $.ajax({
            type: "GET",
            url: "/api/widget/unused/?page=" + page_id,
            success: function(unused) {


                var widget_data = Ext.create('Ext.data.Store', {
                    storeId: 'widgets',
                    fields:['name', 'widget_type'],
                    //sorters: ['cuisine','name'],
                    groupField: 'widget_type',
                    autoLoad: true,
                    proxy: {
                        data: unused,
                        type: 'memory',
                        reader: {
                            type: 'json',
                        }
                    },
                });

                var groupingFeature = Ext.create('Ext.grid.feature.Grouping',{
                    groupHeaderTpl: '{name} ({rows.length} Item{[values.rows.length > 1 ? "s" : ""]})'
                });

        //console.log('creating add widget window');
        //console.log(page_id);

                var grid = Ext.create('Ext.grid.Panel', {
                    iconCls: 'icon-grid',
                    frame: true,
                    store: widget_data,
                    header: false,
                    region: 'west',
                    width: "60%",
                    bodyBorder: true,
                    //border: "0, 0, 0, 95%",
                    hideHeaders: true,
                    features: [groupingFeature],
                    columns: [{
                        text: "Widget",
                        flex: 1,
                        dataIndex: "name",
                    },{
                        text: "Type",
                        flex: 1,
                        dataIndex: "widget_type",
                        hidden: true,
                    }],
                    listeners: {
                        itemclick:function( grid, record) {

        //console.log('fetching widget info');
        //console.log(record.data.id);
                            $.ajax({
                                type: "GET",
                                url: "/api/widget/info/" + record.data.id,
                                success: function(data) {
                                    //console.log('success');
        //console.log('logging data');
        //console.log(data);
                                    $('#data').data('widget', data);

                                    html = '<div class="widget_desc"><img src="' + STATIC_URL + 'widget-images/' + data.key + '.png"></img><h1>' + data.name + '</h1>' + data.description + '</div>'
                                    var preview = Ext.getCmp('widget_desc');
                                    preview.update(html);
                                },
                                dataType: "json",
                                contentType: "application/json",
                                error: function(data) {
                                    //console.log('err');
                                }
                                });
                            try {
                                var btn = Ext.getCmp('add_widget_btn');
                                btn.enable();
                            } catch(err) { 
                                //console.log("'add_widget_btn' could not be enabled");
                            }
                        }
                    }
                });


                var win = Ext.create('Ext.window.Window', {
                    title: 'Layout Window',
                    closable: true,
                    //animateTarget: this,
                    title: 'Add Widget',
                    width: "50%",
                    height: "50%",
                    layout: 'border',
                    items: [grid, {
                        region: 'center',
                        //frame: true,
                        autoScroll: true,
                        id: 'widget_desc',
                        html: '<div class="widget_preview">&#60;Preview&#62;</div>',
                    }],
	                buttonAlign:'right',
	                buttons:[{
                        scope: this,
                        text: 'Cancel',
                        iconCls: 'icon-cancel',
		                handler:function() {
                            win.close();
                        }
	                }, {
		                scope:this,
		                text:'Add',
		                iconCls:'icon-ok',
		                disabled:true,
                        id: 'add_widget_btn',
		                handler:function() {

                            data = $('#data').data('widget');
                            page = $('#data').data('page_id');

                            grid = {};
                            grid.widget = data.resource_uri;
                            grid.page = "/api/page/" + page + "/";
                            grid.row = 1;
                            grid.col = 1;     
                            grid.size_y = data.size_y;
                            grid.size_x = data.size_x;

                            $.ajax({
                                type: "POST",
                                url: "/api/pagewindow/",
                                data: JSON.stringify(grid),
                                dataType: "json",
                                contentType: "application/json",
                                success: function(pagewindow) {
//console.log('adding widget');

                                    var div = '<div id="' + page + '_' + data.key + '" pagewindow="' + pagewindow.id + '" class="layout_block"></div>';
                                    var grid = $('#data').data('grid' + page);

                                    grid.add_widget(div, data.size_x, data.size_y, 1, 1);

                                    createWidget(data, page);

                                    widgetWindow(data.key, page, data.name, data.size_x, data.size_y);

        //console.log('finished, closing add widget window');

                                    win.close();

                                },
                            });
		                }
                    }],
                }).show();
                // So the window dimensions stay 100% when the window is resized
                //Ext.EventManager.onWindowResize(overviewGrid.doLayout, win); 

            }, 
            error: function(data) {
                  //console.log('error');      
            }
        });

    }



    function saveWidgetPositions(grid) {

        var grid = $.parseJSON(grid);

        for(i=0; i<grid.length; i++) {

            data = {
                col: grid[i].col,
                row: grid[i].row,
            }
    
            $.ajax({
                type: "PATCH",
                url: "/api/pagewindow/" + grid[i].pagewindow + '/',
                data: JSON.stringify(data),
                dataType: "json",
                contentType: "application/json",
                error: function(err) {
                    //console.log('problem saving widget position');
                    //console.log(err);
                },
            });  
        }
    }

    function panelStandard() {
        return Ext.create('Ext.panel.Panel', {
            region: 'center', 
            id: 'panel-home', 
            contentEl: 'menu', 
            autoDestroy: true,
            autoScroll: true,
            defaults: {autoScroll: true}, // enables scrolling temporary 
        });
    }

    function panelTab() {
////console.log('creating tab panel with el: ' + el);
        return Ext.create('Ext.tab.Panel', {
            region: 'center',
            contentEl: 'menu', 
            id: 'panel-tab', 
            autoDestroy: true,
            autoScroll: true,
            //style: 'overflow: auto',
            layout: 'fit'
            
        });
    }





    // not used ATM
    var widget_menu = new Ext.menu.Menu({
        items: [{
	        text: 'Resize Widget',
            id: 'resize_widget',
        },{
	        text: 'Remove Widget',
            id: 'remove_widget',
        }],
        defaults: {
            listeners: {
                click: function(tab, eOpts) {
                    if(tab.id  == "resize_widget") {
                    } else if(tab.id  == "remove_widget") {


                    } 
                }
            }
        },
    });


    var config_menu = Ext.create('Ext.menu.Menu', {
        items: [
        //{
	    //    text: 'Add Widget',
        //    id: 'add_widget',
        //},
        //{
	    //    text: 'Settings',
        //    id: 'settings',
        //},
        {
            text: 'Change Theme',
            menu: {      
                items: [
                    {
                        text: 'Default',
                        checked: true,
                        group: 'theme',
                        id: 'theme_default',
                        checkHandler: onItemCheck
                    }, {
                        text: 'BlueBay',
                        checked: false,
                        group: 'theme',
                        id: 'theme_bluebay',
                        checkHandler: onItemCheck
                    }
                ]
          }
        },{
	        text: 'Re-order Panels',
            id: 'enable_drag',
        },{
	        text: 'Lock Panels',
            id: 'disable_drag',
            hidden: true,
        },{
	        text: 'Log out',
            id: 'log_out',
        }],
        defaults: {
            listeners: {
                click: function(item, eOpts) {

                     page = $('#data').data('page_id');

                    if(item.id  == "add_widget") {
                        addWidget();
                    } else if(item.id  == "disable_drag") {

                        $('#data').data('grid' + page).disable();
                        Ext.getCmp('enable_drag').setVisible(true);
                        Ext.getCmp('disable_drag').setVisible(false);

                    } else if(item.id  == "enable_drag") {

                        $('#data').data('grid' + page).enable();
                        Ext.getCmp('disable_drag').setVisible(true);
                        Ext.getCmp('enable_drag').setVisible(false);

                    } else if(item.id == "log_out") {

                        logout();

                    } 
                }
            }
        },
    });

    function onItemCheck(item, checked) {

        //@TODO: Move this to a config file or something
        if(item.id === "theme_bluebay") {

            var theme = "extjs-themes/bluebay/css/bluebay.css";

        } else if(item.id === "theme_default") {

            var theme = "extjs/resources/css/ext-all.css";
        }

        Ext.util.CSS.swapStyleSheet("theme", STATIC_URL + theme);

    }

    // fetching data needed on load
    function setGlobal(var_name) {
         $.ajax({
            type: "GET",
            url: '/api/' + var_name,
            success: function(data) {
                $('#data').data(var_name, data);
            }
        });
    }

    
    function viewPort() {

         $.ajax({
            type: "GET",
            url: '/api/menu/',
            success: function(data) {

//console.log('menu loaded');
                var tree_model = Ext.define('tree', {
                    extend: 'Ext.data.Model',
                    fields: [
                        {name: 'id',    type: 'int'},
                        {name: 'text',  type: 'string', mapping: 'name'},
                        {name: 'page',  type: 'string'},
                    ]
                });

                var store = Ext.create('Ext.data.TreeStore', {
                    model: tree_model,
                    proxy: {
                        data : data,
                        type: 'memory',
                        reader: {
                            type: 'json',
                        }
                    },
                });
                
                var tree = Ext.create('Ext.tree.Panel', {
                    id: 'main-menu',
                    store: store,
                    rootVisible: false,
                    preventHeader: true,
                    border: false,
                    autoScroll: true,
                    useArrows: true,
                    height: 1000,
                    listeners: {
                        itemexpand: {
                            fn: function(record, opts) {
                            
                                nodeId = record.data.id;
                                
                                //console.log(nodeId);

                            }
                        },
                        itemclick: {
                            fn: function(view, record, item, index, event, opts) {

                                // Expand & collapse node on single click
                                if(record.isExpanded()) {
                                    record.collapse();
                                } else {
                                    record.expand();
                                }
                                
                                console.log(record.raw.page);
                                
                                
                                if(record.raw.page !== null) {
                                
                                    if (typeof record.raw.page === 'object') {
                                        record.raw.page = record.raw.page.id;
                                    } else {
                                        var str = record.raw.page.toString();
                                        record.raw.page = str.replace(/\D/g, '');
                                    }
                                }
                                
                                initPage(record.raw);

                            }
                        }
                    }
                });


                var panel_west = Ext.create('Ext.panel.Panel', {
                    id: 'west',
                    region: 'west',
                    collapsible: true,
                    title: 'Navigation',
                    width: 150,
                    items: [tree],
                    tools: [{
                       type: 'gear',
                       handler: function(e, toolEl, panel, tc){
                         config_menu.showBy(toolEl, 'tr-br?');
                       }
                    }],
                });

                var viewport = Ext.create('Ext.container.Viewport', {
                    layout: 'border',
                    id: 'viewport', 
                    items: [panel_west, panelStandard()]
                });
                Ext.EventManager.onWindowResize(viewport.doLayout, viewport);

             }
        });
    }


 
    
     Ext.QuickTips.init();
 
    var login = new Ext.FormPanel({ 
        labelWidth: 80,
        url: '/api/user/login/', 
        frame: true, 
        defaultType: 'textfield',
        monitorValid: true,
        header: false,
        style: 'padding:10px',
        headers: { 'Content-Type': 'application/json' },
        items:[
            { 
                fieldLabel:'Username', 
                name:'username', 
                allowBlank:false 
            },{ 
                fieldLabel:'Password', 
                name:'password', 
                inputType:'password', 
                allowBlank:false 
        }],
 
        buttons:[{ 
            text:'Login',
            formBind: true,	 
            handler:function() { 
                login.getForm().submit({ 
                    method:'POST', 
                    //waitTitle:'Connecting', 
                    //waitMsg:'Sending data...',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-HTTP-Method-Override': 'POST'
                    },
                    success:function() { 

                        //location.reload();
                        win.close();

                        setGlobal('fund');
                        setGlobal('page');

                    	viewPort();
                    	
                    	page = new Object();
                    	page.page = 1;
                        initGrid(page);
                    },
                    failure:function(form, action){ 
                        Ext.Msg.alert('Login failed!', 'Wrong user name or passsword'); 
                        login.getForm().reset(); 
                    } 
                }); 
            }
        }],
    });

    var win = new Ext.Window({
        closeAction: 'hide',
        id: 'login-window',
        title: 'Please Login', 
        layout:'fit',
        width:300,
        height:150,
        closable: false,
        resizable: false,
        plain: true,
        border: false,
        items: [login]
    });
    $('#data').data('login-window', win);
    

    function logout() {
        $.ajax({
            type: "GET",
            url: '/api/user/logout/',
            success: function(data) {
                var active = $('#data').data('active-panel');
                Ext.getCmp('west').setVisible(false);
                Ext.getCmp(active).setVisible(false);
                $('#data').data('login-window').show();
            },
            failure: function() {
                Ext.Msg.alert('Logout failed!', 'You could not be logged out.');
                //@TODO: Log this 
            }
        });
    }


// sending a csrftoken with every ajax request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});



// create a DOM for all pages on load, including children
// 1. set root: #main1
// 2. set tab panel: #tab_panel1
// 3. set child root #main2


// Is the user logged in?
$.ajax({
    type: "GET",
    url: '/api/loggedin/',
    success: function(data) {
    //$('<div id="main1" class="gridster"></div>').appendTo('body');


        //setGlobal('client'); not implemented yet
        //setGlobal('fund');
        setGlobal('page');

        $('<div id="menu" class="gridster"></div>').appendTo('body');
        viewPort();

        $('<div id="page1"></div>').appendTo('#menu');
        $('#data').data('active-panel', 'panel-home'); 
    	page = new Object();
    	page.page = 1;
        initGrid(page);


    },
    error: function() {

        $('<div id="menu" class="gridster"></div>').appendTo('body');
        $('<div id="page1"></div>').appendTo('#menu');
        $('#data').data('active-panel', 'panel-home'); 

        win.show();
    }
});


    
});
