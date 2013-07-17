
Ext.Loader.setPath('Ext.ux', 'static/ext-4.2.1/examples/ux');
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

function displayInnerGrid(widget, data, renderId, hideHeaders, height) {

        fields = [];
        for(i=0; i < data.columns.length; i++) {
            fields[i] = data.columns[i].dataIndex;
        }

        if(typeof hideHeaders == 'undefined') {
            hideHeaders: false;
        }
        if(typeof height == 'undefined') {
            height: 100 ;
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
           //console.log(data.rows);
        var innerGrid = Ext.create('Ext.grid.Panel', {
            store: insideGridStore,
            selModel: {
                selType: 'cellmodel'
            },
            columns: data.columns,
            header: false,
            autoFit: true,
            width: 1000,
            height: height,
            iconCls: 'icon-grid',
            hideHeaders: hideHeaders,
            renderTo: 'innergrid-' + widget.id + '-' + renderId,
            /*
            listeners: {
                //cellclick:  function(grid, rowIndex, columnIndex, e) {
                itemclick: function (self, record, item, index, e, eOpts) {

                  //console.log(record);
                  //console.log(item);
                  //console.log(index);
                  //console.log(index);
                    if(widget.window.key == 'w12b') {
                        var win = new Ext.Window({
                            renderTo: Ext.getBody(),
                            html: 'asdf',
                            //items: items,
                            height: 300,
                            width: 400,
                        });
                        //win.show();

                    }
                }
            },
           */
        });
        innerGrid.getEl().swallowEvent([
            'mousedown', 'mouseup', 'click',
            'contextmenu', 'mouseover', 'mouseout',
            'dblclick', 'mousemove'
        ]);

}

function zoomGraph(e, widget) {

    //this is ugly
    var qs = widget.qs.replace('&value_date__month=2,4,6,8,10,12', '');

    var start = new Date(e.min);
    var end = new Date(e.max);

    var start_date = start.getFullYear() + '-' + (start.getMonth() + 1) + '-' + start.getDate();
    var end_date = end.getFullYear() + '-' + (end.getMonth() + 1) + '-' + end.getDate();


    var date = '&value_date__gte=' + start_date + '&value_date__lte=' + end_date;
    //var date = '';

    range = (e.max / 1000 ) - (e.min / 1000);
    range = Math.round( range );

    var filter = '';

    if(range > 300000000) { // more than 9.5 years

        filter = '&value_date__month=2,4,6,8,10,12'; // 1st of month each other month
       //console.log('ALL');

    } else if(range >= 240000000) { // more than 7.5 years

        //var filter = '&value_date__month=2,4,6,8,10,12'; // wed
       //console.log('1Y');

    } else if(range >= 120000000) { // more than 4 years

        //var filter = '&value_date__week_day=3,5'; // tue, thu
       //console.log('6M');

    } else if(range >= 60000000) { // more than 2 years

        //var filter = '&value_date__week_day=2,4,6'; // mon, wed, fri
       //console.log('3M');

    } else {
        var filter = ''; // empty means every month
       //console.log('1M');
    }

    //console.log(range);
    //console.log(date);
    //console.log(start);
    //console.log(end);

    var chart = $('#' + widget.div).highcharts();
    chart.showLoading('Loading data from server...');

    $.getJSON(widget.url + qs + date + filter, function(data22) {
        //console.log(data22[0]);
        //console.log(data22[0].data);
	     chart.series[0].setData(data22[0].data);
		 chart.hideLoading();
	});
}

//@TODO: Merge this with zoomGraph()
function zoomLineBarGraph(e) {

console.log(e);

    holding = $('#data').data('holding');

    var div = $('#data').data('linebar-div');


    var qs = '?holding_category__holding_group__isnull=true&holding=' + holding;

    var start = new Date(e.min);
    var end = new Date(e.max);

    var start_date = start.getFullYear() + '-' + (start.getMonth() + 1) + '-' + start.getDate();
    var end_date = end.getFullYear() + '-' + (end.getMonth() + 1) + '-' + end.getDate();

    var date = '&value_date__gte=' + start_date + '&value_date__lte=' + end_date;


    range = (e.max / 1000 ) - (e.min / 1000);
    range = Math.round( range );

    if(range > 31557600) { // more than 1 year

        var filter = '&value_date__month=2,4,6,8,10,12&value_date__day=1'; // 1st of month each other month
       //console.log('ALL');

    } else if(range >= 31535000) { // more than 6 months

        var filter = '&value_date__week_day=4'; // wed
       //console.log('1Y');

    } else if(range >= 15535000) { // more than 3 months

        var filter = '&value_date__week_day=3,5'; // tue, thu
       //console.log('6M');

    } else if(range >= 7700000) { // more than 1 months

        var filter = '&value_date__week_day=2,4,6'; // mon, wed, fri
       //console.log('3M');

    } else {
        var filter = ''; // empty means every day
       //console.log('1M');
    }

    //console.log(range);
    //console.log(date);
    //console.log(start);
    //console.log(end);

    var chart = $('#' + div).highcharts();
    chart.showLoading('Loading data from server...');

    $.getJSON('/api/widget/fundperfholdpriceline/' + qs + date + filter, function(data) {

	     chart.series[0].setData(data);
		 chart.hideLoading();

        $.getJSON('/api/widget/fundperfholdvolbar/' + qs + date + filter, function(data2) {

	         chart.series[1].setData(data2);
		     chart.hideLoading();

	    });
	});
}


function lineBarChart(widget) {

    widget.url = '/api/widget/fundperfholdpriceline/';
    widget.qs = '?holding_category__holding_group__isnull=true&value_date__month=2,4,6,8,10,12&value_date__day=1&holding__fund=' + widget.fund + '&holding=' + widget.holding;

    $('#data').data('holding', widget.holding);

    var div = $('#data').data('linebar-div');
   //console.log('DIV ' + div);
    var chart = $('#' + div).highcharts();

    if(typeof chart != 'undefined') {
        chart.destroy();
    }

    $.getJSON(widget.url + widget.qs, function(data) {

        widget.url = '/api/widget/fundperfholdvolbar/';

        $.getJSON(widget.url + widget.qs, function(data2) {

            var options = {
                chart: {
                    renderTo: div,
                    marginTop: 5,
                    marginBottom: 50,
                    marginRight: 50,
                    spacingBottom: 50,
                    spacingRight: 50,
                },
                navigator:{
                    enabled:true,
				    adaptToUpdatedData: false,
				    series : {
					    data : data
				    }
			    },
                scrollbar: {
                    enabled:false, //remove ugly scrollbar
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
				    events : {
					    afterSetExtremes : zoomLineBarGraph
				    },
				    minRange: 3600 * 1000 // one hour

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

			    rangeSelector : {
			        enabled: true,
				    buttons: [{
					    type: 'month',
					    count: 1,
					    text: '1m'
				    }, {
					    type: 'month',
					    count: 3,
					    text: '3m'
				    }, {
					    type: 'month',
					    count: 6,
					    text: '6m'
				    }, {
					    type: 'year',
					    count: 1,
					    text: '1y'
				    }, {
					    type: 'all',
					    text: 'All'
				    }],
				    inputEnabled: false, // it supports only days
				    selected : 4 // all
			    },
                series: [
                {
                    yAxis: 0,
                    name: 'Price by time',
                    stack: 0,

                    //data: [1, 12, 32, 43],
                    data: data,
		            tooltip: {
			            valueDecimals: 2
		            },

                },
                {
                    name: 'Volume',
                    yAxis: 1,
                    stack: 0,
                    data: data2,
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
        });
    }

function destroyInnerGrid(record, widget_id) {

    var parent = document.getElementById('innergrid-' + widget_id + '-' + record.get('id'));
    var child = parent.firstChild;

    while (child) {
        child.parentNode.removeChild(child);
        child = child.nextSibling;
    }

}

//call W2 chart on click from monthly calendar view W1

function refreshHoldPerfBar(date, fund, monthly, fields, order_by) {


    if(typeof fields == 'undefined') {
        fields = 'nav';
    }
    if(typeof order_by == 'undefined') {
        order_by = 'weight';
    }
    // gets set when W2 is loaded first time
    var div = $('#data').data('div-fundperfholdperfbar');

    // get the window div so we can set the title, super ugly
    //win_div = div.slice(0, div.indexOf("_widget"));

    var date_title = date
    if(typeof monthly != 'undefined' && monthly == true) {
        date_title = moment(date).format("MMM YYYY")
    }



    //title = title.replace('FUND_NAME', $('#data').data('fund_name'));
    //title = title.replace('DATE', date_title);

    var title = $('#data').data('fund_name') + ' / ' + date_title + ' / Holding Performance Bar Graph';
    //win = Ext.getCmp(win_div);
    //win.setTitle(title);

    var chart = $('#' + div).highcharts();

    var url = '/api/widget/fundperfholdperfbar/?value_date=' + date + '&fund=' + fund + '&legend=false&fields=' + fields + '&order_by=' + order_by + '&holding_category__isnull=true';
    //return monthTable(url, 'fundperfdaily', div);

    // TODO: check if possible to reload the already existing chart's data instead of below
    try {
        chart.destroy();
        $.getJSON(url, function(data) {

                widget = {};
                widget.size_x = 7;
                widget.size_y = 3;
                var chart = new Highcharts.Chart({
                    chart: {
                        renderTo: div,
                        type: 'column',
                        width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 30,
                        height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 35,
                    },
                    title: {
                        text: false,
                    },
                    legend: {
                       enabled: false,
                    },
                    xAxis: {
                        type: 'category',
                        categories: data.columns,
                    labels: {
                        rotation: -45,
                        align: 'right',
                        style: {
                            fontSize: '10px',
                            fontFamily: 'Verdana, sans-serif'
                        },
                        enabled: labels,
                    },
                    },
                    series: data.objects,
                });
        });
    } catch (err) {
        //do nothing
    }
};


Ext.onReady(function() {



    // W18 summary graphs
    function summaryGraphs() {
        graphs = {
            1: [
                {ann_return1: 'Returns one ann'},
                {ann_volatility1: 'Volatility one ann'},
                {alpha1: 'Alpha one ann'},
                {beta1: 'Beta one ann'},
                {sharpe_ratio1: 'Sharpe one ann'},
                {correlation1: 'Correlation one ann'},
            ],
            2: [
                {ann_return3: 'Returns three ann'},
                {ann_volatility3: 'Volatility three ann'},
                {alpha3: 'Alpha three ann'},
                {beta3: 'Beta three ann'},
                {sharpe_ratio3: 'Sharpe three ann'},
                {correlation3: 'Correlation three ann'},
            ],
            3: [
                {ann_return5: 'Returns five ann'},
                {ann_volatility5: 'Volatility five ann'},
                {alpha5: 'Alpha five ann'},
                {beta5: 'Beta five ann'},
                {sharpe_ratio5: 'Sharpe five ann'},
                {correlation5: 'Correlation five ann'},
            ]
        };


        var fund = $('#data').data('fund');

        items = [];
        for(var row in graphs) {

            children = [];

            for(var chart in graphs[row]) {

                key = Object.keys(graphs[row][chart])[0];

                var bar_div = 'summary2-bar-' + key;
                var line_div = 'summary2-line-' + key;

                $('<div id="' + bar_div + '"></div>').appendTo('body');
                $('<div id="' + line_div + '"></div>').appendTo('body');
                //$('<div id="' + innertab_div + '-line"></div>').appendTo('#' + tab_div);

                // widget is global for some reason, so using another name
                win_widget = {}
                win_widget.url = '/api/widget/fundperfmonthmin/';
                win_widget.qs = '?fund=' + fund + '&fields=' + key + '&value_date__month=2,4,6,8,10,12';
                win_widget.size_y = 1.9;
                win_widget.size_x = 3;
                win_widget.div = bar_div;


                win_widget.params = {}
                win_widget.params.type = 'column';
                win_widget.params.legend = 'false';
                win_widget.params.scrollbar = 'false';
                win_widget.params.navigator = 'true';
                win_widget.params.zoom = 'true';
                win_widget.params.rangeSelector = 'true';
                win_widget.params.title = 'false';
                win_widget.params.yAxisTitle = graphs[row][chart][key];
                win_widget.params.date_type = 'month';

                lineChart('', win_widget, bar_div);

                children.push({
                     xtype: 'tabpanel',
                     border: 1,
                     width: (120 * win_widget.size_x) + (10 * win_widget.size_x) + (10 * (win_widget.size_x - 1)) - 20,
                     height: (120 * win_widget.size_y) + (10 * win_widget.size_y) + (10 * (win_widget.size_y - 1)) + 20,
                      items: [
                        {
                            xtype : 'panel',
                            title : 'Bar',
                            contentEl: bar_div,
                            id: bar_div
                        },
                        {
                            xtype : 'panel',
                            title :'Line',
                            contentEl: line_div,
                            id: line_div
                        }
                    ],
                    listeners: {
                        'tabchange': function(tabPanel, tab){
                            win_widget.params.type = 'line';
                            lineChart('', win_widget, tab.id);
                        }
                    }
                })
            }

            parent = {
                xtype: 'container',
                layout: 'hbox',
                items: children,
            }
            items.push(parent)
        }
       //console.log("ROW: " + row);


        Ext.onReady(function(){
            var win = new Ext.Window({
                renderTo: Ext.getBody(),
                items: items,
                listeners: {
                    'close': function(tabPanel, tab){
                        $.each(graphs, function(x, row) {
                            $.each(row, function(key, field) {
                                 key = Object.keys(field)[0];
                                 destroyGrid('summary2-bar-' + key);
                                 destroyGrid('summary2-line-' + key);
                            });
                        });
                    }
                }
            });
            win.toggleMaximize();
            win.show();
        });

    }

    function destroyGrid(div) {
        if(typeof $('#' + div).highcharts() != 'undefined') {
            var widget_obj = $('#' + div).highcharts();
            widget_obj.destroy();
        }
    }

    //$('<div id="main" class="gridster"></div>').appendTo('body');
    $('<div id="data"></div>').appendTo('body');

    function initPage(obj) {

       //console.log('init page');
        var id = obj.page;
       //console.log(id);
       //console.log(obj);
        // All pages used on the site. This is loaded on start.
        // @TODO: Redo this
        var pages = $('#data').data('page');


       //console.log(pages);
       //console.log(obj);

        // No need to reload the page if users clicks on a link
        // to a page they are already on
        //if($('#data').data('active-panel') == id) {
        //    return
        //}
        for(i=0; i<pages.length; i++) {

            if(typeof pages[i].children[0].id != 'undefined') {
                page_id = pages[i].children[0].id;
            } else {
                page_id = pages[i].id;
            }
            if(page_id == id) {

                // Children are tabs
                if(pages[i].children !== undefined) {

                    switchPanel(panelTab());
                    appendTabs(pages[i]);
                    obj.page = page_id;

                } else {

                    switchPanel(panelStandard());
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
                        obj = {};
                        obj.page = tab.id;
                        initGrid(obj);
                    }
                },
            });
        }
        panel.setActiveTab(0);
    }


    function switchPanel(panel) {

        var active = $('#data').data('active-panel');

        // clear the year so other
        $('#data').data('year', false);

        var ws = Ext.getCmp('viewport');

        try {
            ws.remove(active, true);
        } catch(err) {
          //console.log("Failed to remove panel");
           //console.log(err);
        }

        // The 'main' DOM element gets destroyed on remove() with autoDestroy
        // set to true, so we have to re-add it
        $('<div id="menu" class="gridster"></div>').appendTo('body');


        try {
            ws.add(panel);
        } catch(err) {
          //console.log("Failed to add panel");
           //console.log(err);
        }

        ws.doLayout();

        // Save the panel so we know which one to destroy next time
        $('#data').data('active-panel', panel.id);

    }

    function initGrid(obj) {

        var page = obj.page;

console.log('initiating grid');


        $('#data').data('page_id', page);

        // if we have a grid for this page, it means it's already
        // loaded and we do not need to fetch it again
        if($('#data').data('grid' + page) !== undefined && $('#data').data('grid' + page) !== '') {

           //console.log('skipping gridster: grid' + page);
            return;
        }

        obj.grid = $("#page" + page).gridster({
            widget_margins: [10, 10],
            widget_base_dimensions: [120, 120],
            max_size_x: 10,
            max_size_y: 10,
            draggable: {
                stop: function(event, ui){
                    saveWidgetPositions(JSON.stringify(obj.grid.serialize()));
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

        if(typeof obj.fund == 'undefined') {
            obj.fund = $('#data').data('fund');
        }

        // for w18
        function createGrid(tabId, data,flex) {

            if(typeof Ext.getCmp('grid' + tabId) == 'undefined') {

            fields = [];
            for(i=0; i < data.columns.length; i++) {
                fields[i] = data.columns[i].dataIndex;
            }

            Ext.create('Ext.data.Store', {
                storeId: 'store' + tabId,
                fields: fields,
                data: data,
                proxy: {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'rows'
                    }
                },
            });
            return Ext.create('Ext.grid.Panel', {
                store: Ext.data.StoreManager.lookup('store' + tabId),
                columns: data.columns,
                id: 'grid' + tabId,
                border: false,
                flex: flex,
                forceFit: true,
                layout:'fit',
                margin: "0 0 20 0",

                //height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 20,
                //width:  (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 20,
               // renderTo: tabId,
            });
        }
        }

        //for w23
        function appendGridToSubRedTab(tabId) {
           var date = tabId.split("-");
           if (typeof date[1] == 'undefined') {
                date[1] = 1;
                date[0] = tabId;
                tabId = tabId + '-1';
           }
           $.getJSON('/api/widget/fundsubredtable/?fund=' + obj.fund + '&year=' + date[0] + '&month='  + date[1] + '&column_width=80,80', function(data1) {
                tab = Ext.getCmp(tabId);
                var table = createGrid(tabId, data1, 0);
                tab.add(table);
                $.getJSON('/api/widget/subscriptionredemptionmonth/?fund=' + obj.fund + '&year=' + date[0] + '&month='  + date[1] + '&column_width=100,100', function(data2) {
                    tab = Ext.getCmp(tabId);
                    var table = createGrid('client' + tabId, data2, 1);
                    tab.add(table);
                });
           });


        }

        //for w13
        function appendGridToGrossAssetTab(tab, year) {
            $.getJSON('/api/widget/fundgrossasset1/?fund=' + obj.fund + '&year=' + year + '&column_width=160,85', function(assets) {
                var grid = dataGroupTable(assets, data.window);
                tab.insert(0, grid);
                tab.doLayout();
            });
        }

        // for w18
        function appendGridToTab(tabId) {
            fund = $('#data').data('fund');

            // for default child tabs
            var lastCharInString = tabId.toString().slice(-1);
            if($.isNumeric(lastCharInString) == false) {
                if(tabId == 'ann_return') {
                    tabId = 'si'; // ann_return is a special case
                } else if (tabId != 'si') {
                    tabId = tabId + '1';
                }
            }
            if(typeof Ext.getCmp('grid' + tabId) == 'undefined') {

                tab = Ext.getCmp(tabId);
                // get grid data
                $.getJSON('/api/widget/fundperfmonth/?fund=' + fund + '&fields=' + tabId + '&column_width=55,60', function(data) {

                    var table = createGrid(tabId, data);
                    tab.add(table);
                    // div for inner tabs
                    var innertab_div = 'inner-tab' + tabId;
                    $('<div id="' + innertab_div + '-bar"></div>').appendTo('#' + tab_div);
                    $('<div id="' + innertab_div + '-line"></div>').appendTo('#' + tab_div);

                    widget = {}
                    widget.url = '';
                    widget.qs = '/api/widget/fundperfbenchcompline/?fields=' + tabId + '&fund=' + fund;
                    widget.size_y = 3;
                    widget.size_x = 6;
                    widget.params = {}
                    widget.params.title = '';
                    widget.params.date_type = 'month';
                    widget.params.navigator = 'true';
                    widget.params.rangeSelector = 'true';

                    var chart = $('#' +  innertab_div + '-bar').highcharts();

                    if(typeof chart == 'undefined') {
                        widget.params.type = 'line';
                        lineChart('', widget, innertab_div + '-line');
                    }

                    // Bar Chart & Line Graph Tabs
                    var tp2 = new Ext.TabPanel({
                        id: 'inner-tab-id' + tabId,
                        //height: (120 * data.size_y) + (10 * data.size_y) + (10 * (data.size_y - 1)) - 20,
                        //width:  (120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                        height: 600,
                        activeTab: 0,
                        items: [
                        {
                            title: 'Line Graph',
                            id: 'line' + tabId,
                            contentEl: innertab_div + '-line',
                        },
                        {
                            title: 'Bar Chart',
                            id: 'bar' + tabId,
                            contentEl: innertab_div + '-bar',
                        },
                        ],

                        listeners: {
                            'tabchange': function(tabPanel, tab){
                                if(tab.id == 'bar' + tabId) {
                                    div2 = innertab_div + '-bar';

                                    var chart = $('#' + div2).highcharts();
                                   //console.log('got chart');
                                    if(typeof chart == 'undefined') {
                                       //console.log('chart does not exist');

                                        widget.params.type = 'column';
                                        lineChart('', widget, div2);

                                    }
                                }
                            }
                        }
                    });
                    tab.add(tp2);
                });
            }
        }

        var page = obj.page;
        var grid = $('#data').data('grid' + page); // obj.grid;
        var window = '<div id="' + page + '_' + data.window.id + '" pagewindow="' + data.id + '" class="layout_block"></div>';

        grid.add_widget(window, data.window.size_x, data.window.size_y, data.col, data.row);


        // div for window
        var window_id = 'page_' + page + '_' + data.window.id;
        $('<div id="' + window_id + '"></div>').appendTo('body');

        // at TODO:change benchmark to support mtom
        if(data.window.key == 'w15') {
              $.getJSON('/api/widget/fundsummary/' + obj.fund, function(summary) {
             //console.log(summary);
                          widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);
                html = '<div> <table width="100%" class="html_table">' +
                '<tr><td>Fund Name</td><td>'+ summary.name + '</td></tr>' +
                '<tr><td>Fund Type</td><td>'+ summary.fund_type.name + '</td></tr>' +
                '<tr><td>Fund Manager</td><td>'+ summary.manager.first_name + summary.manager.last_name + '</td></tr>' +
                '<tr><td> Description</td><td>'+ summary.description + '<d></tr>' +
                '<tr><td>Custodian</td><td>'+ summary.custodian.name + '</td><td>'+ summary.custodian.contact_name + '</td><td>' + summary.custodian.contact_number + '</td><td>Managment Fee</td><td>'+ summary.management_fee + '</td><td>Performance Fee</td><td>'+ summary.performance_fee + '</td></tr>' +
                '<tr><td>Administrator</td><td>'+ summary.administrator.name + '</td><td>'+ summary.administrator.contact_name + '</td><td>' + summary.administrator.contact_number + '</td><td>Administrator Fee</td><td>'+ summary.administrator.fee + '</td></tr>' +
                '<tr><td>Auditor</td><td>'+ summary.auditor.name + '</td><td>'+ summary.auditor.contact_name + '</td><td>' + summary.auditor.contact_number + '</td><td>Auditor Fee</td><td>'+ summary.auditor.fee + '</td></tr>' +
                '<tr><td>Subscription Terms</td><td>'+ summary.subscription_frequency + '</td></tr>' +
                '<tr><td>Redemption Terms</td><td>'+ summary.redemption_frequency + '</td></tr>' +
                '<tr><td>Management Fees</td><td>'+ summary.management_fee + '</td></tr>' +
                '<tr><td>Performance Fees</td><td>'+ summary.performance_fee + '</td></tr>' +
                '<tr><td>Benchmark</td><td>'+ summary.benchmark.name + '</td></tr>' + '</table> </div>';

                $(html).appendTo('#' + window_id);
            });

            return

        // W18
        } if(data.window.key == 'w18') {

            parents = [
                {id: 'ann_return', title: 'Returns'},
                {id: 'ann_volatility', title: 'Volatility'},
                {id: 'sharpe_ratio', title: 'Sharpe'},
                {id: 'alpha', title: 'Alpha'},
                {id: 'beta', title: 'Beta'},
                {id: 'correlation', title: 'Correlation'},
            ];
            children = [
                {id: '1', title: '1 Year Rolling Annualised'},
                {id: '3', title: '3 Years Rolling Annualised'},
                {id: '5', title: '5 Years Rolling Annualised'},
            ];
            items = [];
            for(i=0; i<parents.length; i++) {

                childItems = [];
                // only Returns have SI
                if(parents[i].id == 'ann_return') {
                    childItems.push({id: 'si', title: 'Since Inception'})
                }

                for(x=0; x<children.length; x++) {

                    childItems.push({
                        id: parents[i].id + children[x].id,
                        title: children[x].title,
                        layout: 'fit',
                    })
                }
                items.push({
                    xtype: 'tabpanel',
                    title: parents[i].title,
                    id: 'w18-parent-' + parents[i].id,
                    activeTab: 0,
                    items: childItems,
                    listeners: {
                        'tabchange': function(tabPanel, tab){
                       //console.log('APPENDING FROM CHILD TAB ' + tab.id);
                            appendGridToTab(tab.id);
                        }
                    }
                });
            }

            // div for tabs
            var tab_div = 'tab-' + data.window.key + '-' + window_id;
            $('<div id="' + tab_div + '"></div>').appendTo('#' + window_id);

            var tp = new Ext.TabPanel({
                renderTo: tab_div,
                id: 'w18-tabs',
                //height: 500,
                //width:  (120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                activeTab: 0,
                items: items,
                layout: 'fit',
                listeners: {
                    'beforetabchange': function(tabPanel, tab){

                        if(tab.id == 'summary-tab') {
                        summaryGraphs();
                        return false;
                        }
                        var id = tab.id.split("-");
                       //console.log('APPENDING FROM PARENT TAB ' + id[2]);
                        appendGridToTab(id[2]);
                    }
                }
            });

            // append grids for default tab
            appendGridToTab('si');

            // The summary tab is a link to a popup window
            tp.add({
                title: 'Summary',
                id: 'summary-tab',
            });

            return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);

        } else if (data.window.key == 'w23') {


            this_year = new Date().getFullYear();

            parents = [];
            items = [];
            children = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            for(i=this_year; i>2002; i--) {
                parents.push(i);
            }
           //console.log(parents);
            for(i=0; i<parents.length; i++) {

                childItems = [];

                for(x=0; x<children.length; x++) {

                    childItems.push({
                        id: parents[i] + '-' + (1 + x),
                        title: children[x],
                        layout:  {type : 'vbox', align : 'stretch' }
                    });
                   //console.log(childItems);
                }
                items.push({
                    xtype: 'tabpanel',
                    title: parents[i],
                    id: 'w23-parent-' + parents[i],
                    activeTab: 0,
                    items: childItems,
                    listeners: {
                        'tabchange': function(tabPanel, tab){
                       //console.log('APPENDING FROM CHILD TAB ' + tab.id);
                        appendGridToSubRedTab(tab.id);
                        }
                    }
                });
            }
           //console.log("whatever");

            // div for tabs
            var tab_div = 'tab-' + data.window.key + '-' + window_id;
            $('<div id="' + tab_div + '"></div>').appendTo('#' + window_id);

            var tp = new Ext.TabPanel({
                renderTo: tab_div,
                id: 'w23-tabs',
                //height: 500,
                //width:  (120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                activeTab: 0,
                items: items,
                layout: 'fit',
                listeners: {
                    'tabchange': function(tabPanel, tab){
                        var id = tab.id.split("-");
                       //console.log('APPENDING FROM PARENT TAB ' + id[2]);
                        appendGridToSubRedTab(id[2]);
                    }
                }
            });
            // set the default tab to January of this year
            appendGridToSubRedTab(this_year + '-1');
            return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);


        } if(data.window.key == 'w13') {

            this_year = new Date().getFullYear();

            parents = [];
            items = [];
            for(i=this_year; i>2002; i--) {
                parents.push(i);
            }
            for(i=0; i<parents.length; i++) {

                items.push({
                    //xtype: 'tabpanel',
                    title: parents[i],
                    id: 'w13-year-' + parents[i],
                });
            }
           //console.log("whatever");

            // div for tabs
            var tab_div = 'tab-' + data.window.key + '-' + window_id;
            $('<div id="' + tab_div + '"></div>').appendTo('#' + window_id);

            var tp = new Ext.TabPanel({
                renderTo: tab_div,
                id: 'w13-tabs',
                //height: 500,
                //width:  (120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                activeTab: 0,
                items: items,
                layout: 'fit',
                listeners: {
                    'tabchange': function(tabPanel, tab){
                        var id = tab.id.split("-");
                        appendGridToGrossAssetTab(tab, id[2]);
                    }
                }
            });

            // set the default tab to January of this year
            tab = Ext.getCmp('w13-year-' + this_year);
            appendGridToGrossAssetTab(tab, this_year);
            return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);

        }

       //console.log(data.window.key)

        // get the widgets for this window
        $.ajax({
            type: "GET",
            url: '/api/widgets/?window=' + data.window.id,
            ajaxI: i,
            success: function(widgets) {

                // now I will be i asynchronously
                I = this.ajaxI;

                // vbox or hbox
                var layout = data.window.layout + 'box';

               //console.log('LAYOUT: ' + layout);
                var items = [];

                for(x=0; x<widgets.length; x++) {

                    // div for widget
                    var widget_id = 'page_' + page + '_win_' + data.window.id + '_widget_' + widgets[x].id;
                    $('<div id="' + widget_id + '"></div>').appendTo('#' + window_id);

                    var panel = createWidget(obj, widgets[x], widget_id);

                    // if it's a datatable we just insert the grid
                    // @TODO: This doesn't actually do anything, it was an attempt to get the scroll bar working on horizontal windows
                    //console.log(widgets[x]);
                    //if(widgets[x].type == "data_table") {

                   //     items[I] = panel;

                   // } else {

                        items[x] = {
                            contentEl: widget_id,
                            height: (120 * widgets[x].size_y) + (10 * widgets[x].size_y) + (10 * (widgets[x].size_y - 1)),
                            width:  (120 * widgets[x].size_x) + (10 * widgets[x].size_x) + (10 * (widgets[x].size_x - 1)),
                            border: false,
                            autoScroll: true,
                        }
                   //}


                }

                Ext.create('Ext.container.Container', {
                    renderTo: window_id,
                    //width:  ((120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20) * 3,
                    autoFit: true,
                    header: true,
                    layout: layout,
                    items: items,
                });

                widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);
            }
        });
    }

    function widgetWindow(key, page, title, size_x, size_y, pagewindow, window) {


        // Sets the fund name to the window title
        if(typeof  $('#data').data('fund_name') != 'undefined') {
            title = title.replace('FUND_NAME', $('#data').data('fund_name'));
            title = title.replace('DATE', moment().format('YYYY')); // for W5, W6 & W7
        }


        Ext.create('Ext.window.Window', {
            title: title,
            // there's gotta be a better way to do this
            height: (120 * size_y) + (10 * size_y) + (10 * (size_y - 1)) - 10,
            width:  (120 * size_x) + (10 * size_x) + (10 * (size_x - 1)) - 10,
            layout: 'auto',
            floatable: false,
            draggable: false,
            closable: false,
            contentEl: window,
            x: 0,
            y: 0,
            renderTo: page + '_' + key,
            id: 'page_' + page + '_win_' + key,
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

        if(typeof obj.fund == 'undefined') {
            obj.fund = $('#data').data('fund');
        }
        obj.id = obj.fund;

        if(typeof obj.holding == 'undefined') {
            obj.holding = 1; //$('#data').data('fund'); // change this later
        }

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

        if(widget.v2 == true) {
            var api = '/api/';
        } else {
            var api = '/api/widget/';
        }
        
        widget.url = api + widget.key + '/';
        
        if(widget.columns != '') {
           widget.qs += '&fields=' + widget.columns; 
        }

        // old way
        $.each(obj, function(key, value) {
             widget.qs = widget.qs.replace(key.toUpperCase(), value);
        });


        if(widget.type == 'data_table') {

            return dataTable(obj, widget, div);

        } else if(widget.type == 'data_table_sub') {

            //return dataTableSub(obj, widget, div);
            return dataTable(obj, widget, div);

        } else if(widget.type == 'data_group_table') {

            return dataGroupTable2(obj, widget, div);

        } else if(widget.type == 'line_chart') {

            return lineChart(obj, widget, div);

        } else if(widget.type == 'chart_doubley') {

            chartDoubleY(obj, widget, div)

        } else if(widget.type == 'bar_chart') {

            // get last day of last month
            var d=new Date();
            d.setDate(1);
            d.setHours(-1);

            var formatted_date = obj.year + '-' + obj.month + '-' + d.getDate();
            widget.qs = widget.qs.replace('DATE', formatted_date);

            return barChart(obj, widget, div);

        } else if(widget.type == 'line_bar_chart') {

            $('#data').data('linebar-div', div);

            $('#' + div).append('<p>Please select a Holding above</p>');

        } else if(widget.type == 'pie_chart') {

            return pieChart(obj, widget, div);

        } else if(widget.type == 'euro_percent_table') {

            return euroPercentTabTable(obj, widget, div);

        }
    }



    function lineChart(obj, widget, div) {

        if(typeof $('#' + div).highcharts() != 'undefined') {
           //console.log('chart already created');
        }

        if(typeof widget.params.type == 'undefined') {
            var type = 'line';
        } else {
            var type = widget.params.type;
        }


        var title = false;
        if(typeof widget.params.title != 'undefined' && widget.params.title == "true") {
            title = widget.name;
        }

        var yDecimals = true;
        if(typeof widget.params.yDecimals != 'undefined' && widget.params.yDecimals === 'false') {
            yDecimals = false;
        }

        var yAxisTitle = 'Performance';
        if(typeof widget.params.yAxisTitle != 'undefined') {
            if(widget.params.yAxisTitle == 'false') {
                yAxisTitle = false;
            } else {
                yAxisTitle = widget.params.yAxisTitle;
            }
        }

        var labels = true;
        if(typeof widget.params.labels != 'undefined' && widget.params.labels == 'false') {
            labels = false;
        }

        var legend = true;
        if(typeof widget.params.legend != 'undefined' && widget.params.legend == 'false') {
            legend = false;
        }

        var scrollbar = false;
        if(typeof widget.params.scrollbar != 'undefined' && widget.params.scrollbar == 'true') {
            scrollbar = true;
        }

        var navigator = false;
        if(typeof widget.params.navigator != 'undefined' && widget.params.navigator == 'true') {
            navigator = true;
        }

        var rangeSelector = true;
        if(typeof widget.params.rangeSelector != 'undefined' && widget.params.rangeSelector == 'false') {
            rangeSelector = false;
        }

        $.getJSON(widget.url + widget.qs, function(data) {

            var options = {
                chart: {
                    type: type,
                    marginRight: 25,
                    //marginBottom: 25,
                    size: '100%',
                    renderTo: div,
                    width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10,
                    height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                },
                navigator:{
                    enabled: navigator,
				    adaptToUpdatedData: false,
				    series: data,
				    height: 20,
                },
                scrollbar: {
                    enabled: scrollbar
                },

                rangeSelector: {
                    enabled: rangeSelector,
                    selected : 4
                },
                title: {
                    text: title,
                //    x: -20 //center
                },
                xAxis: {
                    gridLineWidth: 1,
                },
                yAxis: {
                    title: {
                        text: yAxisTitle,
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
                    enabled: legend,
                    //layout: 'vertical',
                    //align: 'right',
                    //verticalAlign: 'top',
                    //x: -10,
                    //y: 100,
                    //borderWidth: 0
                },
                series: data,
            };

            if(typeof widget.params.date_type != 'undefined' && widget.params.date_type == 'month') {
                options['rangeSelector'] = {
                    enabled: true,
			        buttons: [{
				        type: 'year',
				        count: 1,
				        text: '1y'
			        }, {
				        type: 'year',
				        count: 5,
				        text: '5y'
			        }, {
				        type: 'year',
				        count: 10,
				        text: '10y'
			        }, {
				        type: 'all',
				        text: 'All'
			        }],
			        inputEnabled: false, // no space for it
			        selected : 1
                }
            }
            if(typeof widget.params.zoom != 'undefined' && widget.params.zoom == 'true') {
               //console.log(options.xAxis);
                options['xAxis'] = {
                    events: {
                        afterSetExtremes: function(e){
                           //console.log(e);
                            zoomGraph(e, widget);
                        }
                    },
                    minRange: 3600 * 1000 // one hour
                };
               //console.log(options);
            }
            var chart = new Highcharts.StockChart(options);

        });
    }

   function chartDoubleY(obj, widget, div) {

        if(typeof widget.params.type == 'undefined') {
            var type = 'line';
        } else {
            var type = widget.params.type;
        }

        $.getJSON(widget.url + widget.qs, function(data) {

            var chart = new Highcharts.StockChart({
                chart: {
                    type: type,
                    //marginRight: 25,
                    //marginBottom: 25,
                    //size: '100%',
                    renderTo: div,
                    width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 50,
                    height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 100,
                },
                navigator:{
                    enabled:true,
                },
                scrollbar: {
                    enabled:false
                },
			    rangeSelector : {
				    //selected : 1
				    //enabled: false,
			    },
			    title : {
				    text : false
			    },
                yAxis: [{
			        //title : {
				    //    text : false
			        //},
                },{
                    opposite: true
                }],
			    series: data
            });
        });
    }

    function barChart(obj, widget, div) {

        $.getJSON(widget.url + widget.qs, function(data) {

           //console.log('BAR CHART');
           //console.log(obj);
           //console.log(widget);

            title = false;
            if(typeof widget.params.title != 'undefined' && widget.params.title == "true") {
                title = widget.name;
            }

            type = 'column';
            if(typeof widget.params.type != 'undefined') {
                type = widget.params.type;
            }

            yDecimals = true;
            if(typeof widget.params.yDecimals != 'undefined' && widget.params.yDecimals === 'false') {
                yDecimals = false;
            }


            legend = true;
            if(typeof widget.params.legend != 'undefined' && widget.params.legend == "false") {
                legend = false;
            }

            scrollbar = false;
            if(typeof widget.params.scrollbar != 'undefined' && widget.params.scrollbar == "true") {
                scrollbar = true;
            }
           //console.log(labels);

            var options = {
                chart: {
                    //marginRight: 25,
                    //marginTop: 50,
                    //marginBottom: 50,
                    renderTo: div,
                    type: type,
                    width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 30,
                    height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 35,
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
                    },
                    allowDecimals: yDecimals,
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

                xAxis: {
                    type: 'category',
                    categories: data.columns,
                    //type : "datetime",
                },
                //series: data,
            }

            if(typeof widget.params.labels != 'undefined' && widget.params.labels == 'rotated') {
                labels = {
                    rotation: -45,
                    align: 'right',
                    style: {
                        fontSize: '10px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
                options.xAxis.labels = labels;
            }

            var chart = new Highcharts.Chart(options);



         $('#data').data('div-' + widget.key, div);

        });



    }


    function monthTable(year, month) {

        var fund = $('#data').data('fund');

        $('<div id="calendar"></div>').appendTo('body');

        mo_widget = {}
        mo_widget.url = '/api/widget/fundperfhistcalview/';
        mo_widget.qs = '?fund=' + fund + '&order_by=weight&value_date__year=' + year + '&value_date__month=' + month;

        //console.log(widget.url + widget.qs);
        $.getJSON(mo_widget.url + mo_widget.qs , function(data) {

            // first day in first week of month
            var d = new Date(year, month - 1, 1);
            var first_weekday = d.getDay();

            // last day of the month
            var d2 = new Date(year, month, 0);
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

                date = year.toString() + '-' + month.toString() + '-' + i;

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
                html += '<td>' + i + '<a href="#" onclick="refreshHoldPerfBar(\'' + date + '\', ' + fund + ');">' + val + '</a></td>';
            }

            html += "</tr></table>";




            var win = new Ext.Window({
                renderTo: Ext.getBody(),
                html: html,
                //items: items,
                height: 300,
                width: 400,
                /*
                listeners: {
                    'close': function(tabPanel, tab){
                        $.each(graphs, function(x, row) {
                            $.each(row, function(key, field) {
                                 key = Object.keys(field)[0];
                                 destroyGrid('summary2-bar-' + key);
                                 destroyGrid('summary2-line-' + key);
                            });
                        });
                    }
                }
                */
            });
            win.show();

            return;

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

    function createGrid(widget, data, div) {

        fund = $('#data').data('fund');

        fields = [];
        for(i=0; i < data.columns.length; i++) {
            fields[i] = data.columns[i].dataIndex;
        }

        Ext.create('Ext.data.Store', {
            storeId: widget.key,
            fields: fields,
            data: data,
            proxy: {
                type: 'memory',
                reader: {
                    type: 'json',
                    root: 'rows'
                }
            },
        });

        plugins = [];
        selModel = [];
        if(widget.window.key == 'w10' && $('#data').data('classification') == 'eof') {
            plugins = [{
                ptype: 'rowexpander',
                rowBodyTpl: [
                    '<div id="innergrid-' + widget.id + '-{id}">',
                    '</div>'
                ]
            }];
            selModel = {
                selType: 'cellmodel'
            }
        }

        var euroGrid = Ext.create('Ext.grid.Panel', {
            title: widget.params.title,
            store: Ext.data.StoreManager.lookup(widget.key),
            columns: data.columns,
            height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 20,
            width:  (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 20,
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            plugins: plugins,
            selModel: selModel,
            forceFit: true,
            layout:'fit',

            listeners: {
                cellclick: function(gridView,htmlElement,columnIndex,dataRecord) {

                    year = obj.page = $('#data').data('year');
                    month = columnIndex;

                    if(month != 0) {

                        if(typeof year == 'undefined' || year === false) {
                            year = new Date().getFullYear();
                        }

                        obj.page = $('#data').data('page_id');
                        obj.grid = $('#data').data('grid' + obj.page);
                        extra_params = {
                            year: year,
                        }

                        if(widget.window.key == 'w8') {
                            group = 'sec';
                        } else if(widget.window.key == 'w9') {
                            group = 'sub';
                        } else if(widget.window.key == 'w10') {
                            group = 'loc';
                        }

                        div = $('#data').data('piechart-div-' + widget.window.key);
                        var window_id = 'page_' + obj.page + '_win_' + widget.window.id;


                        widget.key = "fundperfgrouppie";
                        widget.qs = "?fund=" + fund + "&value_date__year=YEAR&value_date__month=" + month + "&holding_category__holding_group=" + group + "&fields=nav&value_date__day=1";
                        widget.params.value_date__year = year;
                        widget.params.holding_category__holding_group = "sec";
                        widget.params.fund = "FUND";
                        widget.params.fields = "nav";
                        widget.type = "pie_chart";
                       //console.log(widget);

                        var widget_obj = $('#' + div).highcharts();
                        widget_obj.destroy();

                        createWidget(obj, widget, div, extra_params);
                    }
               }
            }

        });

        if(widget.window.key == 'w10' && $('#data').data('classification') == 'eof') {

            euroGrid.view.on('expandBody', function (rowNode, record, expandRow, eOpts) {

                if(typeof $('#data').data('year') == 'undefined' || $('#data').data('year') == 'false') {
                    year = new Date().getFullYear();
                } else {
                    year = $('#data').data('year');
                }

                var id = record.get('id');

                $.getJSON('/api/country-breakdown/?fund=' + fund + '&holding_category=' + id + '&value_date__year=' + year + '&date=value_date&name=country__name&value=mtd&fields=value_date,country__name,mtd,si,ytd', function(widget_data) {
                    displayInnerGrid(widget, widget_data, id);
                });

                if(typeof $('#data').data('last-open-subgrid') != 'undefined') {
                    //destroyInnerGrid($('#data').data('last-open-subgrid'));
                }
            });
            euroGrid.view.on('collapsebody', function (rowNode, record, expandRow, eOpts) {
                destroyInnerGrid(record, widget.id);
            });
        }
        return euroGrid;
    }

    function euroPercentTabTable(obj, widget, div) {

        fund = $('#data').data('fund');

        $.getJSON(widget.url + widget.qs, function(data) {
          //console.log('EURO PERCENT');
          //console.log(data);
          //console.log(div);
           var div2 = div + '_' + div
           $('<div id="' + div2 + '"></div>').appendTo("#" + div);

            if(typeof Ext.getCmp(div) != 'undefined') {
                tabPanel = Ext.getCmp(div);
                tabPanel.destroy();
            }
            var tabPanel = Ext.create('Ext.tab.Panel', {
                //height: 200, //(120 * data.size_y) + (10 * data.size_y) + (10 * (data.size_y - 1)) - 20,
                //width:  800, //(120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                //layout: 'fit',
                renderTo: div2,
                id: div2,
            });

            widget.params.title = '€';
            var grid = createGrid(widget, data);
            tabPanel.add(grid);
            tabPanel.doLayout();

            // replace values with percentage
            var qs = widget.qs.replace('fields=nav', 'fields=weight'); // ???
            widget.params.title = '% of Fund';

            $.getJSON(widget.url + qs, function(data2) {
                var grid = createGrid(widget, data2);
                tabPanel.add(grid);
                tabPanel.doLayout();
            });

        });
    }

    function dataGroupTable2(obj, widget, div) {

       $.getJSON(widget.url + widget.qs, function(data) {

            var fund = $('#data').data('fund');

            fields = [];
            c = 0;

            // for nested header columns as well
            for(i=0; i < data.columns.length; i++) {
                if(typeof data.columns[i].columns != 'undefined') {
                    for(x=0; x < data.columns[i].columns.length; x++) {
                        fields[c] = data.columns[i].columns[x].dataIndex;
                        c++;
                    }
                } else {
                    if(typeof data.columns[i].dataIndex != 'undefined') {
                        fields[c] = data.columns[i].dataIndex;
                        c++;
                    }
                }
            }
            fields.push('group');

            var store = Ext.create('Ext.data.Store', {
                storeId: 'groupStore',
                fields: fields,
                groupField: 'group',
                data: data,
                proxy: {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'rows'
                    }
                }
            });

            var groupingFeature = Ext.create('Ext.grid.feature.Grouping',{
                groupHeaderTpl: '{name}',
                collapsible: false,
                depthToIndent: 100,
                enableGroupingMenu: false,

            });

            return Ext.create('Ext.grid.Panel', {
                columnLines: true,
                cls: 'custom-grid-group',
                store: Ext.data.StoreManager.lookup('groupStore'),
                columns: data.columns,
                features: [groupingFeature],
                renderTo: div,
                width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                forceFit: true,
                layout:'fit',

            });
        });
    }


    function dataGroupTable(data, widget) {

       // $.getJSON(widget.url + widget.qs, function(data) {

            var fund = $('#data').data('fund');

            fields = [];
            c = 0;

            // for nested header columns as well
            for(i=0; i < data.columns.length; i++) {
                if(typeof data.columns[i].columns != 'undefined') {
                    for(x=0; x < data.columns[i].columns.length; x++) {
                        fields[c] = data.columns[i].columns[x].dataIndex;
                        c++;
                    }
                } else {
                    if(typeof data.columns[i].dataIndex != 'undefined') {
                        fields[c] = data.columns[i].dataIndex;
                        c++;
                    }
                }
            }
            fields.push('group');

            var store = Ext.create('Ext.data.Store', {
                storeId: 'groupStore',
                fields: fields,
                groupField: 'group',
                data: data,
                proxy: {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'rows'
                    }
                }
            });

            var groupingFeature = Ext.create('Ext.grid.feature.Grouping',{
                groupHeaderTpl: '{name}'
            });

            return Ext.create('Ext.grid.Panel', {
                columnLines: true,
                store: Ext.data.StoreManager.lookup('groupStore'),
                columns: data.columns,
                features: [groupingFeature],
                //renderTo: div,
                width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                forceFit: true,
                layout:'fit',

            });
        //});
    }
    function dataTable(obj, widget, div) {

        var hideHeaders = false;
        if(typeof widget.params.column_header !== 'undefined' && widget.params.column_header == 'false'){
            hideHeaders = true;
        }

        $.getJSON(widget.url + widget.qs, function(data) {

            // for nested header columns as well
            c = 0;
            fields = [];
            for(i=0; i < data.columns.length; i++) {
                if(typeof data.columns[i].columns != 'undefined') {
                    for(x=0; x < data.columns[i].columns.length; x++) {
                        fields[c] = data.columns[i].columns[x].dataIndex;
                        c++;
                    }
                } else {
                    if(typeof data.columns[i].dataIndex != 'undefined') {
                        fields[c] = data.columns[i].dataIndex;
                        c++;
                    }
                }
            }
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

            // for innergrids
            if(widget.type == 'data_table_sub') {
                cls = 'custom-grid-sub';
            } else {
                cls = 'custom-grid';
            }
            var width = (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1));
            var height = (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1));
            plugins = [{
                ptype: 'rowexpander',
                rowBodyTpl: [
                    '<div id="innergrid-' + widget.id + '-{id}">',
                    '</div>'
                ]
            }];
            selModel = {
                selType: 'cellmodel'
            }
            width = width - 23;

            var panel = Ext.create('Ext.grid.Panel', {
                id: div,
                cls: cls,
                columnLines: true,
                hideHeaders: hideHeaders,
                store: Ext.data.StoreManager.lookup(widget.key),
                columns: data.columns,
                width: width,
                height: height,
                header: false,
                border: false,
                //enableLocking: true,
                autoScroll: true,
                renderTo: div,
                plugins: plugins,
                selModel: selModel,
                iconCls: 'icon-grid',
                forceFit: true,
                layout:'fit',
                listeners: {
                    cellclick: function(gridView,htmlElement,columnIndex,dataRecord) {

                        year = dataRecord.data.year;
                       //console.log('CLICKED');
                       //console.log(dataRecord);
                       //console.log(columnIndex);

                        obj.page = $('#data').data('page_id');
                        obj.grid = $('#data').data('grid' + obj.page);
                        extra_params = {
                            year: year,
                        }
                        month = columnIndex;

                        if(widget.window.key == 'w1') {

                            // year view
                            if(columnIndex == 1) {

                                if($('#data').data('classification') == 'sp')  {
                                    refreshWindow('w9c', obj, extra_params);
                                    refreshWindow('w26', obj, extra_params);
                                    refreshWindow('w27', obj, extra_params);
                                    refreshWindow('w28', obj, extra_params);
                                } else if($('#data').data('classification') == 'pe')  {
                                    refreshWindow('w5', obj, extra_params);
                                } else {
                                    refreshWindow('w3', obj, extra_params);
                                    refreshWindow('w4', obj, extra_params);
                                    refreshWindow('w5', obj, extra_params);
                                }

                            // monthly view
                            } else if(columnIndex < 14) {
                                if($('#data').data('classification') == 'pe')  {
                                    refreshWindow('w2', obj, extra_params);
                                } else {
                                    refreshHoldPerfBar(year + '-' + month + '-1', obj.fund, true);
                                }
                            }
                        }
                        else if(widget.window.key == 'w1b') {

                            // year view
                            if(columnIndex == 1) {

                                refreshWindow('w3', obj, extra_params);
                                refreshWindow('w4b', obj, extra_params);
                                refreshWindow('w5b', obj, extra_params);

                            // month view
                            } else if(columnIndex < 14) {
                                refreshHoldPerfBar(year + '-' + month + '-1', obj.fund, true);

                                monthTable(year, month);
                            }
                        }


                        if(widget.window.key == 'w6') {

                            // year view
                            if(columnIndex == 1) {

                                // save this for W8, 9 and 10
                                $('#data').data('year', year);

                                //obj = {};
                                //obj.month = month;
                                //obj.year = year;
                                //obj.fund = fund;
                                //widget.key = "fundperfgrouptable";
                                //widget.params.value_date__year = year;
                                //widget.params.fund = "FUND";
                                //widget.params.fields = "nav";
                                //widget.type = "euro_percent_table";

                                refreshWindow('w8', obj, extra_params);
                                refreshWindow('w9', obj, extra_params);
                                refreshWindow('w10', obj, extra_params);

                            // month view
                            } else if(columnIndex < 13) {
                                refreshHoldPerfBar(year + '-' + month + '-1', obj.fund, true, 'performance', 'weight');
                            }
                        }
                               // var panel = Ext.getCmp("month-table");
                                //panel.remove('month-table-content');

                                /*
                                monthly calendar view disabled for this type of fund
                                $('<div id="asdf"></div>').appendTo('#1');

                                obj = {};
                                obj.month = month;
                                obj.year = year;
                                obj.fund = fund;
                                widget.key = "fundperfhistcalview";
                                widget.params.value_date__year = "YEAR";
                                widget.params.value_date__month = "MONTH";
                                widget.params.fund = "FUND";
                                widget.type = "month_table";
                                createWidget(obj, widget, 'asdf'); //panel.renderTo);
                                */

                    }
                }

            });

            panel.view.on('expandBody', function (rowNode, record, expandRow, eOpts) {

                var id = record.get('id');

                if(widget.key == 'fundperfholdtable') {

                    $.getJSON("/api/widget/fundperfholdtradetable/?holding=" + id + "&holding__fund=" + obj.fund + '&column_width=150,80', function(w11) {

                        displayInnerGrid(widget, w11,id);

                        widget.holding = record.get('id');
                        widget.fund = obj.fund;
                        lineBarChart(widget);
                    });

                } else if(widget.key == 'fundregister') {

                    $.getJSON("/api/widget/subscriptionredemption/?&fund=" + obj.fund + '&client=' + id + '&column_width=100,100', function(w12) {

                        displayInnerGrid(widget, w12, id);
                    });
                }

                if(typeof $('#data').data('year') == 'undefined' || $('#data').data('year') === false) {
                    year = new Date().getFullYear();
                } else {
                    year = $('#data').data('year');
                }

                fund = $('#data').data('fund');

                if(widget.window.key == 'w5b') {
                    $.getJSON('/api/country-breakdown/?fund=' + fund + '&holding_category=' + id + '&value_date__year=' + year + '&date=value_date&name=country__name&value=mtd&fields=id,value_date,country__name,mtd,si,ytd&column_width=80,50', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, true, 50);
                    });
                }
                if(widget.window.key == 'w31') {
                    $.getJSON('/api/holding-history/?holding=' + id + '&holding_category__holding_group__isnull=true&value_date__year=' + year + '&date_type=m&fields=value_date,drawdown,various,distribution,expense,valuation,total_value&total=true&column_width=80,50', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, false, 150);
                    });
                }
                if(widget.window.key == 'w12b') {
                    $.getJSON('/api/holding/?client=' + id + '&distinct=true&total=true&fields=name,currency__name,commit,drawdown,various,residual_commit,distribution,valuation,total_value,proceed,irr', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, false, 150);
                    });
                }





                if(typeof $('#data').data('last-open-subgrid') != 'undefined') {
                    //destroyInnerGrid($('#data').data('last-open-subgrid'));
                }
            });
            panel.view.on('collapsebody', function (rowNode, record, expandRow, eOpts) {
               //console.log(record);
                destroyInnerGrid(record, widget.id);
            });
            return panel;
        });
    }

    function refreshWindow(window_key, obj, extra_params) {
        $.getJSON('/api/widgets/?window__key=' + window_key, function(widget_data) {


            for(x=0; x<widget_data.length; x++) {

                var window_id = 'page_' + obj.page + '_win_' + widget_data[x].window.id;
                var widget_id = window_id + '_widget_' + widget_data[x].id;

                var title = widget_data[x].window.name;

                if(extra_params.year != 'undefined') {
                    date = extra_params.year;
                } else {
                    date = 'Week X'; // fill this in later
                }
                title = title.replace('FUND_NAME', $('#data').data('fund_name'));
                title = title.replace('DATE', date);

                win = Ext.getCmp(window_id);
                win.setTitle(title);

                if(widget_data[x].type == 'data_table') {
                    var widget_obj = Ext.getCmp(widget_id);

                } else {
                    var widget_obj = $('#' + widget_id).highcharts();
                }
                try {
                    widget_obj.destroy();
                } catch(err) {

                }

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
                columnLines: true,
                cls: 'custom-grid',
                //autoWidth: true,
                selModel: {
                    selType: 'cellmodel'
                },
                //autoHeight: true,
                // shouldn't be 120??
                width: (140 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                height: (140 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                plugins: [{
                    ptype: 'rowexpander',
                    rowBodyTpl: [
                        '<div id="innergrid-' + widget.id + '-{id}">',
                        '</div>'
                    ]
                }],
                header: false,
                border: 0,
                iconCls: 'icon-grid',
                renderTo: div,
                id: 'subtable' + widget.key,
            });

            mainGrid.view.on('expandBody', function (rowNode, record, expandRow, eOpts) {

                var id = record.get('id');

                if(widget.key == 'fundperfholdtable') {

                    $.getJSON("/api/widget/fundperfholdtradetable/?holding=" + id + "&holding__fund=" + obj.fund + '&column_width=150,80', function(w11) {

                        displayInnerGrid(widget, w11,id);

                        widget.holding = record.get('id');
                        widget.fund = obj.fund;
                        lineBarChart(widget);
                    });

                } else if(widget.key == 'fundregister') {

                    $.getJSON("/api/widget/subscriptionredemption/?&fund=" + obj.fund + '&client=' + id + '&column_width=100,100', function(w12) {

                        displayInnerGrid(widget, w12, id);
                    });
                }

                if(typeof $('#data').data('year') == 'undefined' || $('#data').data('year') === false) {
                    year = new Date().getFullYear();
                } else {
                    year = $('#data').data('year');
                }

                fund = $('#data').data('fund');

                if(widget.window.key == 'w5b') {
                    $.getJSON('/api/country-breakdown/?fund=' + fund + '&holding_category=' + id + '&value_date__year=' + year + '&date=value_date&name=country__name&value=mtd&fields=id,value_date,country__name,mtd,si,ytd&column_width=80,50', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, true, 50);
                    });
                }
                if(widget.window.key == 'w31') {
                    $.getJSON('/api/holding-history/?holding=' + id + '&holding_category__holding_group__isnull=true&value_date__year=' + year + '&date_type=m&fields=value_date,drawdown,various,distribution,expense,valuation,total_value&total=true&column_width=80,50', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, false, 150);
                    });
                }
                if(widget.window.key == 'w12b') {
                    $.getJSON('/api/holding/?client=' + id + '&distinct=true&total=true&fields=name,currency__name,commit,drawdown,various,residual_commit,distribution,valuation,total_value,proceed,irr', function(widget_data) {
                        displayInnerGrid(widget, widget_data, id, false, 150);
                    });
                }





                if(typeof $('#data').data('last-open-subgrid') != 'undefined') {
                    //destroyInnerGrid($('#data').data('last-open-subgrid'));
                }
            });
            panel.view.on('collapsebody', function (rowNode, record, expandRow, eOpts) {
               //console.log(record);
                destroyInnerGrid(record, widget.id);
            });

        });

    }

    function pieChart(obj, widget, div) {
        $('#data').data('piechart-div-' + widget.window.key, div);

        if(widget.key == "fundnavpie") {
            $('#data').data('linebar-div', div); //re-name

            $('#' + div).append('<p>Please click on a month</p>');
            return
        }


        $.getJSON(widget.url + widget.qs, function(data) {
       //console.log(widget.url + widget.qs);
       //console.log(data);
            var chart = new Highcharts.Chart({
                chart: {
                    renderTo: div,
                    //borderWidth: 1,
                    marginTop: -50,
                    marginLeft: 30,
                    marginRight: 30,
                    //width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                    //height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                    // @TODO: Find out why widget is getting overwritten
                    height: (120 * 2) + (10 * 2) + (10 * (2 - 1)),
                    width:  (120 * 2) + (10 * 2) + (10 * (2 - 1)),
                },
                title: {
                    text: false
                },
                series: [{
                    type: 'pie',
                    name: widget.name,
                    data: data
                }]
            });
        });
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
                    bodyBorder: false,
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

                // ADD WIDGET
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
            layout: 'fit'  //commented this 28th of june 08:03 // outcommented 3rd of july

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

    function setFundName(id) {
         $.ajax({
            type: "GET",
            url: '/api/fund/' + id + '?fields=name,classification__key',
            success: function(data) {
                $('#data').data("fund_name", data.name);
                $('#data').data("classification", data.classification__key);
            }
        });
    }


    function viewPort() {

         //$.ajax({
         //   type: "GET",
         //   url: '/api/menu/',
         //   success: function(data) {

            $.getJSON('/api/menu/', function(data) {
           //console.log('menu data:');
           //console.log(data);
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

                               //console.log('record');
                               //console.log(record);

                                // Expand & collapse node on single click
                                if(record.isExpanded()) {
                                    record.collapse();
                                } else {
                                    record.expand();
                                }

                               //console.log(record.raw);
                               if(typeof record.raw.fund != 'undefined') {
                                    $('#data').data('fund', record.raw.fund);
                                    setFundName(record.raw.fund);
                                }

                                if(record.raw.page !== null) {

                                    if (typeof record.raw.page === 'object') {
                                        record.raw.page = record.raw.page.id;
                                    } else {
                                        var str = record.raw.page.toString();
                                        record.raw.page = str.replace(/\D/g, '');
                                    }
                                }
                              //console.log('INIATING PAGE NUMBER:');
                              //console.log(record.raw);
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
        );
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
