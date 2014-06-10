
Ext.Loader.setPath('Ext.ux', staticUrl + 'extjs');
Ext.Loader.setConfig({enabled: true});
Ext.require([
    'Ext.ux.RowExpander',
    'Ext.container.Viewport',
    'Ext.layout.container.Border',
    'Ext.tab.Panel',
    'Ext.tree.*',
    'Ext.data.*',
    'Ext.menu.*',
    'Ext.window.MessageBox',
    'Ext.grid.*',
    'Ext.form.Panel',
    'Ext.form.*',
]);

// Make the first column 2 px wide
Ext.define('Rx.grid.MyRowExpander', function() {
    var spec = {
        extend: 'Ext.ux.RowExpander',
        alias: 'plugin.myrowexpander',

        getHeaderConfig : function() { 
            var me = this;
        
            return {
                width: 2,
                lockable: false,
                sortable: false,
                resizable: false,
                draggable: false,
                hideable: false,
                menuDisabled: true,
                tdCls: Ext.baseCSSPrefix + 'grid-cell-special',
                innerCls: Ext.baseCSSPrefix + 'grid-cell-inner-row-expander',
                renderer: function(value, metadata) {
                    // Only has to span 2 rows if it is not in a lockable grid.
                    if (!me.grid.ownerLockable) {
                        metadata.tdAttr += ' rowspan="2"';
                    }
                    return '<div class="' + Ext.baseCSSPrefix + 'grid-row-expander"></div>';
                },
                processEvent: function(type, view, cell, rowIndex, cellIndex, e, record) {
                    if (type == "mousedown" && e.getTarget('.x-grid-row-expander')) {
                        me.toggleRow(rowIndex, record);
                        return me.selectRowOnExpand;
                    }
                }
            };
        }
    };

    return spec;
});


Ext.define('Ext.form.field.Month', {
    extend:'Ext.form.field.Date',
    alias: 'widget.monthfield',
    requires: ['Ext.picker.Month'],
    alternateClassName: ['Ext.form.MonthField', 'Ext.form.Month'],
    selectMonth: null,
    createPicker: function() {
        var me = this,
            format = Ext.String.format;
        return Ext.create('Ext.picker.Month', {
            pickerField: me,
            ownerCt: me.ownerCt,
            renderTo: document.body,
            floating: true,
            hidden: true,
            focusOnShow: true,
            minDate: me.minValue,
            maxDate: me.maxValue,
            disabledDatesRE: me.disabledDatesRE,
            disabledDatesText: me.disabledDatesText,
            disabledDays: me.disabledDays,
            disabledDaysText: me.disabledDaysText,
            format: me.format,
            showToday: me.showToday,
            startDay: me.startDay,
            minText: format(me.minText, me.formatDate(me.minValue)),
            maxText: format(me.maxText, me.formatDate(me.maxValue)),
            listeners: { 
        select:        { scope: me,   fn: me.onSelect     }, 
        monthdblclick: { scope: me,   fn: me.onOKClick     },    
        yeardblclick:  { scope: me,   fn: me.onOKClick     },
        OkClick:       { scope: me,   fn: me.onOKClick     },    
        CancelClick:   { scope: me,   fn: me.onCancelClick }        
            },
            keyNavConfig: {
                esc: function() {
                    me.collapse();
                }
            }
        });
    },
    onCancelClick: function() {
        var me = this;    
    me.selectMonth = null;
        me.collapse();
    },
    onOKClick: function() {
        var me = this;    
    if( me.selectMonth ) {
               me.setValue(me.selectMonth);
            me.fireEvent('select', me, me.selectMonth);
    }
        me.collapse();
    },
    onSelect: function(m, d) {
        var me = this;    
    me.selectMonth = new Date(( d[0]+1 ) +'/1/'+d[1]);
    }
});  

function investmentNAV(div, type) {

    var id = $('#data').data(type);

    if($('#data').data('date') == 'undefined') {
        var date = new Date();
    } else {
        var date = $('#data').data('date');
    }

    win = Ext.getCmp(div);
    title = 'asdf';

    var holdings = {'ad-hoc': 'Ad-hoc', 'cash': 'Cash', 'loan': 'Loans', 'pe': 'PE Commitments', 'hsbc': 'HSBC', 'cs': 'Credit Suisse'};
    var ajaxReqs = [];
    var grid_data = [];
    var columns = [];
    var i = 0;
    $.each(holdings, function(key, name) {
        if(key == 'hsbc' || key == 'cs') {
            var class_type = 'fund__custodian';
        } else {
            var class_type = 'asset_class';
        }
        ajaxReqs.push($.ajax({
            url: '/api/holding-history/?column_border_y=ytd&column_width=100,180&data_type=year&date=value_date&extra_fields=ytd&holding__' + class_type + '__key=' + key + '&holding__' + type + '=' + id + '&title=holding__name&total=true&value=mtd&value_date__year=' + moment(date).format('YYYY'),
            ajaxI: key,
            success: function(data) {
                x = this.ajaxI;
                $.each(data.rows, function(id, arr) {
                    arr['group'] = holdings[x];
                    //arr['group'] = x;
                    arr['group_order'] = i;
                    i++;
                    grid_data.push(arr);
                });
                columns = data.columns; // it don't matter which one
            }
        }));
    });
    $.when.apply($, ajaxReqs).then(function() {
        // all requests are complete
       //console.log('grid_data');
       //console.log(grid_data);

        columns.push({dataIndex: 'group', collapsible: false});

       //console.log(columns);

        fields = [];
        for(i=0; i < columns.length; i++) {
            fields[i] = {};
            if(i == 0 || columns[i].dataIndex == 'group') {
                fields[i]['type'] = 'string';
            } else {
                fields[i]['type'] = 'float';
            }
            if(typeof columns[i].dataIndex != 'undefined') {
                fields[i]['name'] = columns[i].dataIndex;
            }
        }

        if(typeof columns[1]['summaryType'] != 'undefined') {
            columns[0]['summaryRenderer'] = function(v, params, data){ return 'Total'};
        }

        $.each(grid_data, function(parent, row) {
            $.each(row, function(key, value) {
                // tastypie returns floats as strings, hence this ugly hack
                if(value.toString().indexOf('.') != -1) {
                    grid_data[parent][key] = parseFloat(value.toString());
                }
            });
        });

        var oldPanel = Ext.getCmp('fundperf' + div);
        if(typeof oldPanel != 'undefined') {
            oldPanel.destroy();
        }

        var store = Ext.create('Ext.data.Store', {
            data: grid_data,
            groupField: 'group',
            fields: fields,
            //sortInfo: {field: 'id', direction: 'ASC'},
            //remoteGroup: true,
        });

        var grid = Ext.create('Ext.grid.Panel', {
            height: 950,
            //iconCls: 'icon-grid',
            id: 'fundperf' + div,
            renderTo: div,
            store: store,
            border: false,
            header: false,
            forceFit: true,
            features: [{
               // id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: true,
               // enableGroupingMenu: false
            }],
            columns: columns,
        });
        return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);
    });
}




function displayInnerGrid(widget, data, renderId, hideHeaders, height) {

        //@TODO: Make dynamic
        data.rows[0].year = 'Benchmark';
        data.rows[0].ytd = '';
        fields = [];
        for(i=0; i < data.columns.length; i++) {
            fields[i] = data.columns[i].dataIndex;

            row = data.columns[i].dataIndex;
            data.columns[i]['renderer'] = function(val) {
                if(val == 'Benchmark') {
                    return '<span style="font-size:9; font-weight: normal;">' + val + '</span>';
                };
                if (val > 0) {
                    return '<span style="color: #01017D; font-weight: normal;">' + val + ' %</span>';
                } else if (val < 0) {
                     return '<span style="color: #F73100; font-weight: normal;">' + val + ' %</span>';
                }
                if(val != '') {
                    return '<span style="font-weight: normal;">0 %</span>';
                }
            }

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
            //autoFit: true,
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

function refreshGraph(e, widget) {
    var start = new Date(e.min);
    var end = new Date(e.max);
    
    var start_date = start.getFullYear() + '-' + (start.getMonth() + 1) + '-' + start.getDate();
    var end_date = end.getFullYear() + '-' + (end.getMonth() + 1) + '-' + end.getDate();
    var date = '&value_date__gte=' + start_date + '&value_date__lte=' + end_date;
    console.log('start date', start_date, date);

    var chart = $('#' + widget.div).highcharts();
    chart.showLoading('Loading data from server...');

    $.getJSON(widget.url + widget.qs + date, function(data) {
        console.log('refreshGraph1', widget.url + widget.qs + date);
        //console.log('data', data);
        chart.series[0].setData(data[0].data);
        chart.series[1].setData(data[1].data);
        chart.hideLoading();
    });

    var qs = widget.qs;
    $.getJSON(widget.url + qs + date + '&graph_type=graph', function(data) {
        console.log('refreshGraph2', widget.url + widget.qs + date);
        //console.log('data2', data);
         chart.series[2].setData(data.data);
         chart.hideLoading();
    });



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

    var filter = '&date_type=m';

    if(range > 300000000) { // more than 9.5 years

        filter += '&value_date__month=2,4,6,8,10,12'; // 1st of month each other month
       //console.log('ALL');

    } else if(range >= 240000000) { // more than 7.5 years

        filter += '&value_date__month=2,4,6,8,10,12'; // wed
       //console.log('1Y');

    } else if(range >= 120000000) { // more than 4 years

        filter += '&value_date__week_day=3,5'; // tue, thu
       //console.log('6M');

    } else if(range >= 60000000) { // more than 2 years

        filter += '&value_date__week_day=2,4,6'; // mon, wed, fri
       //console.log('3M');

    } else {
        filter += ''; // empty means every month
       //console.log('1M');
    }

    //console.log(range);
    //console.log(date);
    //console.log(start);
    //console.log(end);

    var chart = $('#' + widget.div).highcharts();
    chart.showLoading('Loading data from server...');

    $.getJSON(widget.url + qs + date + filter, function(data22) {
       //console.log(data22);
        //console.log(data22[0].data);
	     chart.series[0].setData(data22.objects[0].data);
		 chart.hideLoading();
	});
}

//@TODO: Merge this with zoomGraph()
function zoomLineBarGraph(e) {

console.log(e);

    holding = $('#data').data('holding');

    var div = $('#data').data('linebar-div');


    var qs = '?holding=' + holding + '&data_type=graph&y1=price_of_unit&date=value_date&date_type=d';

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

    $.getJSON('/api/holding-history/' + qs + date + filter, function(data) {

       //console.log('DATA');
       //console.log(data);

	     chart.series[0].setData(data.objects[0].data);
		 chart.hideLoading();

		var qs = '?holding=' + holding + '&data_type=graph&y1=no_of_units&date=trade_date';

        $.getJSON('/api/fund/' + qs + date + filter, function(data2) {

	         chart.series[1].setData(data2.objects[0].data);
		     chart.hideLoading();

	    });
	});
}


function lineBarChart(widget) {

    widget.url = '/api/holding-history/';
    widget.qs = '?value_date__month=2,4,6,8,10,12&value_date__day=1&data_type=graph&date=value_date&y1=price_of_unit&date_type=m&holding=' + widget.holding;

    $('#data').data('holding', widget.holding);

    var div = $('#data').data('linebar-div');
   //console.log('DIV ' + div);
    var chart = $('#' + div).highcharts();

    if(typeof chart != 'undefined') {
        chart.destroy();
    }

    $.getJSON(widget.url + widget.qs, function(data) {

        widget.url = '/api/trade/';

        qs = '?data_type=graph&date=trade_date&y1=no_of_units&order_by=trade_date&holding=' + widget.holding;

        $.getJSON(widget.url + qs, function(data2) {


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
				    series : data.objects[0].data,
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
                    data: data.objects[0].data,
		            tooltip: {
			            valueDecimals: 2
		            },
                    marker: {
                       enabled: false
                    }

                },
                {
                    name: 'Volume',
                    yAxis: 1,
                    stack: 0,
                    data: data2.objects[0].data,
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

function refreshHoldPerfBar(widget_key, date, id, monthly, fields, order_by) {

   //console.log('widget_key');
   //console.log(widget_key);
    if(widget_key == 'w45' || widget_key == 'w33') {
        var type = 'client';
        var size_x = 7;
    } else if(widget_key == 'w7') {
        var type = 'fund';
        var size = 7;
    } else {
        var type = 'fund';
        var size_x = 6;
    }

    if(typeof fields == 'undefined') {
        fields = 'mtd';
    }
    if(typeof order_by == 'undefined') {
        order_by = 'weight';
    }
    // gets set when W2 is loaded first time
    var div = $('#data').data('barchart-' + widget_key);


    $('#data').data('date', date);

    var date_title = date;
    if(typeof monthly != 'undefined' && monthly == true) {
        date_title = moment(date).format("MMM YYYY")
    }


    var title = $('#data').data(type + '_name') + ' / ' + date_title + ' / Holding Performance';
    var win_div = div.slice(0, div.indexOf("_widget"));
    win = Ext.getCmp(win_div);
    win.setTitle(title);


    var chart = $('#' + div).highcharts();
    chart.destroy();

    widget = {
        'key': "holding-history",
        'qs': '?value_date=' + date + '&holding__' + type + '=' + id + '&y1=' + fields + '&order_by=' + order_by + '&data_type=graph&date_type=m&title=holding__name',
        'type': "bar_chart",
        'size_x': size_x,
        'size_y': 3,
        'params': {'legend': 'false'},
        'window': {
            'key': widget_key,
        }
    };
    obj = {};
    obj[type] = id;

    return createWidget(obj, widget, div);
};


function holdingTab(id, value) {

    $('#data').data('holding', id);
    $('#data').data('holding_name', value);

    parent_div = 'page111-holdings' + id;

    $('<div id="' + parent_div + '"></div>').appendTo('body');

    var panel = Ext.getCmp('panel-tab');

    tabs = {
        112: 'Performance',
        113: 'Stats',
        114: 'NAV',
        115: 'Summary',
    }
    items = [];
    $.each(tabs, function(key, title) {

        var tab_div = key + '-holdings' + id;

        $('#data').data('grid' + tab_div, '');

        $('<div id="' + tab_div + '" class="gridster"></div>').appendTo('body');
        $('<div id="page' + tab_div + '" class="gridster"></div>').appendTo('body');

        items.push({
            title: title,
            itemId: key,
            contentEl: 'page' + tab_div,
            autoScroll: true,
            listeners: {
                activate: function(tab){
                    obj = {};
                    obj.page = tab_div,
                    initGrid(obj);
                }
            },
        })
    });

    parent_id = 'page111-' + id;
    panel.add({
        xtype : 'tabpanel',
        id: parent_id,
        title: value,
        contentEl: parent_div,
        closable: true,
        autoScroll:true,
        activeTab: 0,
        items: items
    });


    panel.setActiveTab(parent_id);

    //obj = {};
    //obj.page = 112;
    //initGrid(obj);
}

Ext.onReady(function() {

    window.holdingTab = holdingTab;
    window.initGrid = initGrid;
    window.createWidget = createWidget;
    window.investmentNAV = investmentNAV;



    // W18 summary graphs
    function summaryGraphs(type) {
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



        var id = $('#data').data(type);

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
                win_widget2 = {}
                win_widget2.url = '/api/' + type + '-history/';
                win_widget2.qs = '?' + type + '=' + id + '&y1=' + key + '&data_type=graph&date=value_date&value_date__month=2,4,6,8,10,12&order_by=value_date';
                win_widget2.size_y = 1.9;
                win_widget2.size_x = 3;
                win_widget2.div = bar_div;


                win_widget2.params = {}
                win_widget2.params.type = 'column';
                win_widget2.params.legend = 'false';
                win_widget2.params.scrollbar = 'false';
                win_widget2.params.navigator = 'true';
                win_widget2.params.zoom = 'true';
                win_widget2.params.rangeSelector = 'true';
                win_widget2.params.title = 'false';
                win_widget2.params.yAxisTitle = graphs[row][chart][key];
                win_widget2.params.date_type = 'month';

                lineChart('', win_widget2, bar_div);

                children.push({
                     xtype: 'tabpanel',
                     border: 1,
                     width: (120 * win_widget2.size_x) + (10 * win_widget2.size_x) + (10 * (win_widget2.size_x - 1)) - 20,
                     height: (120 * win_widget2.size_y) + (10 * win_widget2.size_y) + (10 * (win_widget2.size_y - 1)) + 20,
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
                            win_widget2.params.type = 'line';
                            lineChart('', win_widget2, tab.id);
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
                
                // is this needed?
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

        // to a page they are already on
        //if($('#data').data('active-panel') == id) {
        //    return
        //}
        for(i=0; i<pages.length; i++) {

            if(typeof pages[i].children != 'undefined') {
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

/*
        if(typeof obj.div == 'undefined') {
            obj.div = 'page' + obj.page
            var 'grid' + page = 'grid' + page;
        } else {
            var 'grid' + page = obj.div;
        }
*/
//console.log('initiating grid');


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

        try {
            var pagewindow = page.split('-')[0];
        } catch(e) {
            var pagewindow = page;
        }
        
        var url = '/api/pagewindow/?page=' + pagewindow;

        $.ajax({
            type: "GET",
            url: url,
            success: function(data) {
            
                $('#data').data('grid_data' + page, data); // doesn't seem to be used anywhere

                console.log('pagewindow', data, url);

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
            obj.fund = $('#data').data('fund_obj');
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
        
        /*
        function appendGridToSubRedTab(tabId) {
           var date = tabId.split("-");
           if (typeof date[1] == 'undefined') {
                date[1] = 1;
                date[0] = tabId;
                tabId = tabId + '-1';
           }
           $.getJSON('/api/clientposition/?fund=' + obj.fund.id + '&year=' + date[0] + '&month='  + date[1] + '&column_width=80,80&widget=w23', function(data1) {
                tab = Ext.getCmp(tabId);
                var table = createGrid(tabId, data1, 0);
                tab.add(table);

                var fields = "&fields=client__name,buy_sell,shares,nav_per_share,nav";

                $.getJSON('/api/clienttransaction/?fund=' + obj.fund.id + '&value_date__year=' + date[0] + '&value_date__month='  + date[1] + '&column_width=100,100' + fields, function(data2) {
                    tab = Ext.getCmp(tabId);
                    var table = createGrid('client' + tabId, data2, 1);
                    tab.add(table);
                });
           });
        }
        */

        //for w13
        function appendGridToGrossAssetTab(tab, year) {
            $.getJSON('/api/fund-grossasset1/?fund=' + obj.fund.id + '&year=' + year + '&column_width=160,85', function(assets) {
                var grid = dataGroupTable(assets, data.window);
                tab.insert(0, grid);
                tab.doLayout();
            });
        }

        // for w18
        function appendGridToTab(tabId) {


            // for default child tabs
            var lastCharInString = tabId.toString().slice(-1);
            if($.isNumeric(lastCharInString) == false) {
                if(tabId == 'ann_return') {
                    tabId = 'si'; // ann_return is a special case
                } else if (tabId != 'si') {
                    tabId = tabId + '1';
                }
            }


            var prefix = '';
            if(data.window.key == 'w18') {
                var type = 'fund';
            } else if(data.window.key == 'w38') {
                var type = 'client';
            } else if(data.window.key == 'w58') {
                var type = 'fund';
                var prefix = 'holding__'
            } else {
                var type = 'holding';
            }

            var type_value = $('#data').data(type);

            if(typeof Ext.getCmp('grid' + tabId) == 'undefined') {

                tab = Ext.getCmp(tabId);
                // get grid data
                $.getJSON('/api/' + type + '-history/?' + prefix + type + '=' + type_value + '&value=' + tabId + '&column_width=55,60&data_type=year&date=value_date&extra_fields=ytd&date_type=m', function(data) {

                    //var table = createGrid(tabId, data);
                    //tab.add(table);
                    // div for inner tabs
                    var innertab_div = 'inner-tab' + tabId;
                    $('<div id="' + innertab_div + '-bar"></div>').appendTo('#' + tab_div);
                    $('<div id="' + innertab_div + '-line"></div>').appendTo('#' + tab_div);
                    $('<div id="' + innertab_div + '-line-table"></div>').appendTo('#' + tab_div);

                    widget = {}
                    widget.url = '';
                    widget.qs = '/api/' + type + '-performance-benchmark/?fields=' + tabId + '&' + type + '=' + type_value;
                    widget.size_y = 5;
                    widget.size_x = 6;
                    widget.params = {
                        'title': '',
                        'date_type': 'month',
                        'navigator': 'true',
                        'rangeSelector': 'true',
                    }

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
                        border: false,
                        height: 750,
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
                        {
                            title: 'Data Table',
                            id: 'line-table' + tabId,
                            contentEl: innertab_div + '-line-table',
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
                                        widget.size_y = 5;
                                        lineChart('', widget, div2);

                                    }
                                }
                                if(tab.id == 'line-table' + tabId) {

                                    var table = createGrid(tabId, data);
                                    tab.add(table);

                                    div2 = innertab_div + '-line-table';

                                    var chart = $('#' + div2).highcharts();

                                    if(typeof chart == 'undefined') {

                                        widget.params.type = 'line';
                                        widget.size_y = 3;

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

        // W15 - Fund Summary
        if(data.window.key == 'w15') {
        
              var fields = 'name,manager__name,description,custodian__name,administrator__name,currency__name,auditor__name,benchpeer__name,asset_class__risk__name,country_risk__name,region_1__name&summary=true';
              $.getJSON('/api/fund/' + obj.fund.id + '/?fields=' + fields, function(summary) {

                    widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id, true);
                    html = '<div> <table class="html_table">' +
                    '<tr><th>Fund Name</th><td>'+ summary.name + '</td><th>Fund Manager</th><td>'+ summary.manager__name + '</td></tr>' +
                    '<tr><th>Benchmark</th><td>' + summary.benchpeer__name + '</td><th>Launch Date</th><td>' + moment(summary.launch_date).format('YYYY-MM-DD') + '</td></tr>' +
                    '<tr><th>Currency</th><td>'+ summary.currency__name + '</td></tr>' +
                    '</table><table class="html_table">' +
                    '<tr><th>Description</th><td>'+ summary.description + '</td></tr>' +
                    '</table><table class="html_table">' +
                    '<tr><td colspan="2"><h3>Fund Classification & Size</h3></td></tr>' +
                    '<tr><th>Starting NAV</th><td>'+ Ext.util.Format.currency(summary.start_nav, '&euro;') + '</td><th>Asset Class Focus</th><td>'+ summary.asset_class__risk__name + '</td></tr>' +
                    '<tr><th>Current NAV</th><td>'+ Ext.util.Format.currency(summary.end_nav, '&euro;') + '</td><th>Country Focus</th><td>'+ summary.country_risk__name + '</td></tr>' +
                    '<tr><th>Net Flows</th><td>'+ Ext.util.Format.currency(summary.net_flow, '&euro;') + '</td><th>Regional Focus</th><td>'+ summary.region_1__name + '</td></tr>' +
                    '</table><table class="html_table">' +
                    '<tr><td colspan="2"><h3>Custody, Admin & Audit Section</h3></td></tr>' +
                    '<tr><th>Custodian</th><td>'+ summary.custodian__name + '</td></tr>' +
                    '<tr><th>Admin</th><td>'+ summary.administrator__name + '</td></tr>' +
                    '<tr><th>Auditor</th><td>'+ summary.auditor__name + '</td></tr>' +
                    '</table><table class="html_table">' +
                    '<tr><td colspan="2"><h3>Fees Section</h3></td></tr>';



                    $.getJSON('/api/fundfee/?summary=true&fund=' + obj.fund.id, function(fee) {

                        for(i=0; i<fee.length; i++) {
                            html += '<tr><th>' + fee[i].name + '</th><td>'+ fee[i].formula + '</td></tr>';
                        }
                   
                        html += '</table><table class="html_table">' +
                        '<tr><td colspan="2"><h3>User Defined Peers Section</h3></td></tr>';
                       
                       $.getJSON('/api/fundpeer/?user=1&fields=benchpeer__name,benchpeer__formula&fund=' + obj.fund.id + '&user=' + $('#data').data('userId'), function(peer) {
                       
                            for(i=0; i<peer.length; i++) {
                                html += '<tr><th>' + peer[i].benchpeer__name + '</th><td>'+ peer[i].benchpeer__formula + '</td></tr>';
                            }
                            html += '</table> </div>';
                            $(html).appendTo('#' + window_id);
                       });
                   });
            });

            return

        } if(data.window.key == 'w47') {

              var fields = 'first_name,last_name,description,custodian__name,custodian__contact_name,user__first_name,user__last_name';
              $.getJSON('/api/client/' + obj.client + '/?fields=' + fields, function(summary) {

             //console.log(summary);
                     widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);
                    html = '<div> <table width="100%" class="html_table">' +
                    '<tr><td>Client Name</td><td>'+ summary.last_name + ', ' + summary.first_name + '</td></tr>' +
                    '<tr><td>Client Manager</td><td>'+ summary.user__first_name + summary.user__last_name + '</td></tr>' +
                    '<tr><td>Description</td><td>'+ summary.description + '<d></tr>' +
                    '<tr><td>Custodian</td><td>'+ summary.custodian__name + '</td><td>'+ summary.custodian__contact_name + '</td></tr>' +

                    $.getJSON('/api/benchmark/?fields=name&client=' + obj.client, function(benchmarks) {

                        for(i=0; i<benchmarks.rows.length; i++) {
                            if(i == 0) {
                                var td = 'Benchmarks';
                            } else {
                                var td = '';
                            }
                            html += '<tr><td>' + td + '</td><td>'+ benchmarks.rows[i].name + '</td></tr>';
                        }


                        html += '</table> </div>';
                        $(html).appendTo('#' + window_id);
                   });
            });

            return

        // W18
        } if(data.window.key == 'w18 disabled' || data.window.key == 'w80'  || data.window.key == 'w38' || data.window.key == 'w58') {

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
                    id: data.window.key + '-parent-' + parents[i].id,
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

            if(data.window.key == 'w80') {
                var type = 'holding';
            } else if(data.window.key == 'w38') {
                var type = 'client';
            } else {
                var type = 'fund';
            }

            var tp = new Ext.TabPanel({
                renderTo: tab_div,
                id: data.window.key + '-tabs',
                //height: 500,
                //width:  (120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                activeTab: 0,
                items: items,
                layout: 'fit',
                listeners: {
                    'beforetabchange': function(tabPanel, tab){

                        if(tab.id == 'summary-tab') {
                            summaryGraphs(type);
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

/*
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


        
        console.log('window_id', window_id);
        
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

*/

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

        // div for window
        var window_id = 'page_' + page + '_' + data.window.id;
        $('<div id="' + window_id + '"></div>').appendTo('body');

        //if(data.window.key == 'w55') {
        //
        //    investmentNAV(window_id, 'fund');
        //    return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);

        //} else 
        if(data.window.key == 'w46') {

            investmentNAV(window_id, 'client');
        } else if(data.window.key == 'w68') { // alpheus funds

            investmentNAV(window_id, 'fund');
        }


        // get the widgets for this window
        $.ajax({
            type: "GET",
            url: '/api/widgets/?window=' + data.window.id + '&disabled=0',
            ajaxI: i,
            success: function(widgets) {
            
            //console.log('widgets', widgets);

                // now I will be i asynchronously
                I = this.ajaxI;

                // vbox or hbox
                var layout = data.window.layout + 'box';

               //console.log('LAYOUT: ' + layout);
                var items = [];

                for(x=0; x<widgets.length; x++) {

                    // div for widget
                    var widget_id = 'page_' + page + '_win_' + data.window.id + '_widget_' + widgets[x].id;
                    $('<div id="' + widget_id + 'top"></div>').appendTo('#' + window_id);
                    $('<div id="' + widget_id + '"></div>').appendTo('#' + window_id);
                    
                    $('#data').data('window_id', window_id);

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

                widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id, obj.scroll);
            }
        });
    }

    function widgetWindow(key, page, title, size_x, size_y, pagewindow, window, scroll) {
    
        if(typeof $('#data').data('date') !== 'undefined') {
            var date = $('#data').data('date');
        } else {
            var date = new Date();
        }
        title = title.replace('YEAR', moment(date).format('YYYY'));
        title = title.replace('MONTH', moment(date).format('MMM'));

        // Sets the fund name to the window title
        if(typeof  $('#data').data('fund_obj') !== 'undefined' && typeof $('#data').data('fund_obj').name !== 'undefined') {
            title = title.replace('FUND_NAME', $('#data').data('fund_obj').name);
        }
        
        if(typeof  $('#data').data('client_name') != 'undefined') {
            title = title.replace('CLIENT_NAME', $('#data').data('client_name'));
        }

        // Sets the holding name to the window title
        if(typeof  $('#data').data('holding_name') != 'undefined') {
            title = title.replace('HOLDING_NAME', $('#data').data('holding_name'));
        }
        

        if(typeof scroll == 'undefined') {
            var scroll = false;
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
            autoScroll: scroll,
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


        if(typeof obj.client == 'undefined') {
            obj.client = $('#data').data('client');
        }

        //if(typeof obj.fund == 'undefined') {
            obj.fund = $('#data').data('fund_obj');
        //}
        
        obj.scroll = false;
        
        if(typeof widget.width == 'undefined') {
            widget.width = (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 30;
        } 
        if(typeof widget.height == 'undefined') {
            widget.height = (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 30;
        }
        
        // is this needed?
        obj.id = obj.fund.id;
        obj.holding__fund = obj.fund.id;

        if(typeof $('#data').data('holding') != 'undefined') {
            obj.holding = $('#data').data('holding');
            widget.holding = obj.holding;
        }


        // new way
        if(typeof extra_params != 'undefined') {
            $.each(extra_params, function(key, value) {
                 widget.qs = widget.qs.replace(key.toUpperCase(), value);
            });
        }
        // is this in use?
        if(typeof widget.params != 'undefined') {
            $.each(widget.params, function(key, value) {
                 widget.qs = widget.qs.replace(key.toUpperCase(), value);
            });
        }


        if(typeof obj.year == 'undefined') {
            obj.year = new Date().getFullYear();
        }
        if(typeof obj.month == 'undefined') {
            obj.month = new Date().getMonth() + 1;
        }
        var date = new Date(obj.year, obj.month - 1);

        if(typeof widget.name != 'undefined') {
            widget.name = widget.name.replace('YEAR', moment(date).format('YYYY'));
            widget.name = widget.name.replace('MONTH', moment(date).format('MMM'));
        }

        widget.div = div; // remove this later

        widget.url = '/api/' + widget.key + '/';


        $.each(obj, function(key, value) {
            // e.g holding__fund=FUND
             try {
                key_val = key.split('__');
                widget.qs = widget.qs.replace(key_val[1].toUpperCase(), value.id);
             } catch(e) {
                 try {
                    widget.qs = widget.qs.replace(key.toUpperCase(), value.id);
                 } catch(e) {
                 }
             }
        });


        if(typeof widget.columns != 'undefined' && widget.columns != '') {
           if(widget.qs.length > 0) {
               widget.qs += '&fields=' + widget.columns;
           } else {
               widget.qs += '?fields=' + widget.columns;
           }
        }
        
        
        console.log('WIDGET KEY', widget.key);
        
        if(widget.key == 'return_histogram') {
        
            return returnHistogram(obj, widget, div);
            
        } else if(widget.key == 'w55') {

            w55(obj, widget, div);                     

        } else if(widget.key == 'w25') {

            w25(obj, div);                     

        } else if(widget.key == 'w12') {
           
            var fields = '&fields=client__name,size,avg_cost_price,market_value';

            $.getJSON("/api/clientposition/?&fund=" + obj.fund.id + '&column_width=100,100&data_type=table' + fields, function(data) {
            
                return dataTable(data, obj, widget, div);
            });            
        
        } else if(widget.key == 'w2') {
        
            return holdingPerformance(obj, widget, div, 'performance');
            
        } else if(jQuery.inArray(widget.key, ['w18', 'w151']) !==-1 ) {
            
            //obj.scroll = true;
            //widget.size_x -= 0.5;
            
            return fundHistoricalStats(obj, widget, div);
        
        } else if(widget.key == 'holding_nav') {
        
            console.log('holding NAV');
        
            return holdingPerformance(obj, widget, div, 'nav');
        
        } else if(widget.type == 'data_table') {

            
            widget.qs += '&fields=estimation';
            console.log('data table url', widget.url + widget.qs);
            $.getJSON(widget.url + widget.qs, function(data) {
                return dataTable(data, obj, widget, div);
            });

        } else if(widget.type == 'data_table_sub') {

            //return dataTableSub(obj, widget, div);
            return dataTable(obj, widget, div);

        } else if(widget.type == 'data_group_table') {

            return dataGroupTable2(obj, widget, div);

        } else if(widget.type == 'line_chart') {

            var url1 = "/api/fundreturnmonthly/?data_type=graph&date=value_date&fund=" + obj.fund.id + "&order_by=value_date&y1=fund_perf&y2=bench_perf&fields=fund__name";
            var url2 = "/api/fundreturnmonthly/?bench_graph=bench_perf&data_type=graph&date=value_date&fund=" + obj.fund.id + "&graph_type=bench&order_by=value_date&y1=fund_perf&y2=bench_perf&fields=fund__name";
        
            //console.log('w16 url1', url1);
            //console.log('w16 url2', url2);
            $.getJSON(url1, function(series) {
                $.getJSON(url2, function(series2) {
                    return lineChart(obj, widget, div, series, series2);
		        });
		    });


        } else if(widget.type == 'w152') {

            var url = "/api/fundreturnmonthly/?widget=w152&fund=" + obj.fund.id;
        
            //console.log('url', url);
            $.getJSON(url, function(series) {
                return lineChart(obj, widget, div, series);
		    });

             

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

            if(widget.window.key == 'w11') {
                $('#' + div).append('<p>Please select a Holding above</p>');

                $('#data').data('linebar-div', div);
            } else {
                lineBarChart(widget);
            }

        } else if(widget.type == 'pie_chart') {

            return pieChart(obj, widget, div);

        } else if(widget.type == 'euro_percent_table') {

            return euroPercentTabTable(obj, widget, div);

        } else if(widget.key == 'w23') {

            return w23(obj, widget, div);

        }
    }
    
    function w25(obj, div) {
    
        $.getJSON("/api/nav-reconciliation/?fund=" + obj.fund.id, function(data) {
                        
            var store = Ext.create('Ext.data.ArrayStore', {
                fields: [
                   {name: 'market_value',   type: 'float'},
                   {name: 'size',           type: 'float'},
                   {name: 'nav',            type: 'float'},
                   {name: 'shares',         type: 'float'},
                ],
                data: data,
            });
            
            var grid = Ext.create('Ext.grid.Panel', {
                store: store,
                columnLines: true,
                columns: [{
                    text: 'Valuation from Clients',
                    columns: [{
                        text: 'Euro NAV',
                        dataIndex: 'market_value',
                        renderer: Ext.util.Format.numberRenderer('0,000.00/i'),
                    }, {
                        text: 'No. of Units',
                        dataIndex: 'size',
                        renderer: Ext.util.Format.numberRenderer('0,000.00/i'),
                    }],
                },{
                    text: '',
                },{
                    text: 'Valuation from Funds',
                    columns: [{
                        text: 'Euro NAV',
                        dataIndex: 'nav',
                        renderer: Ext.util.Format.numberRenderer('0,000.00/i'),
                    }, {
                        text: 'No. of Units',
                        dataIndex: 'shares',
                        renderer: Ext.util.Format.numberRenderer('0,000.00/i'),
                    }],
                }],
                renderTo: div,
            });
        });  
    
    }
    
    
   function w55(obj, widget, div) {
   
        function fetchHtml(year) {
    
           $.get('/admin/fund/performance/?year=' + year, function( html ) {

                $('#w55' + year).empty();
                $(html).appendTo('#w55' + year);
                selectedYear = year;
           });    
        }
        
        years = [];
        items = [];
        selectedYear = new Date().getFullYear();
        for(i=this_year; i>2002; i--) {
            years.push(i);
        }
         
        window_id = $('#data').data('window_id');
        for(i=0; i<parents.length; i++) {
            
            $('<div id="w55' + years[i] + '"></div>').appendTo("#" + window_id);
            
            items.push({
                xtype: 'tabpanel',
                title: years[i],
                id: 'w55-tabs' + years[i],
                autoScroll: true,
                contentEl: 'w55' + years[i],
            });
        }
  
        var tabPanel = new Ext.TabPanel({
            //renderTo: div,
            id: 'w55-tabs',
            activeTab: 0,
            items: items,
            header: false,
            autoFit: true,
            height: widget.height - 10,
            width: widget.width + 5,
            listeners: {
                'tabchange': function(tabPanel, tab){
                    fetchHtml(tab.title);
                }
            }
        });

        var print_methods = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        Ext.create('Ext.container.Container', {
            layout: {
                type: 'vbox'
            },
            header: false,
            renderTo: div,
            height: widget.height + 70,
            width: widget.width + 5,
            header: false,
            items: [tabPanel, {
                xtype: 'container',
                layout: {
                    type: 'hbox'
                },
                padding: 5,
                items: [{
                    xtype: 'combobox',
                    text: 'Print',
                    fieldLabel: 'Print method',
                    store: print_methods,
                    queryMode: 'local',
                    id: 'w55combo',
                    margin: '0 10 0 0',
                    value: 'Year',
                },{                    
                    xtype: 'button',
                    text: 'Print',
                    handler : function() {
                        var date = Ext.getCmp('w55combo').getValue();
                        var url = '/admin/fund/performance/?year=' + selectedYear + '&print=true&date=' + date;
                        window.open(url, 'performance-print','height=' + screen.height + ',width=' + screen.width + ',resizable=no,scrollbars=yes,toolbar=no,menubar=no,location=yes')
                    },
                }],
            }],
        });
        
        fetchHtml(selectedYear);
    }

    
    
    function w23(obj, widget, div) {
    
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
                    flex: true,
                    //forceFit: true,
                    layout:'fit',
                    margin: "0 0 20 0",
                    //height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 20,
                    //width:  (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 20,
                   // renderTo: tabId,
                });
            }
        }
    
   
        function appendGridToSubRedTab(tabId) {
    
               var date = tabId.split("-");
               if (typeof date[1] == 'undefined') {
                    date[1] = 1;
                    date[0] = tabId;
                    tabId = tabId + '-1';
               }
               $.getJSON('/api/sub-red/?fund=' + obj.fund.id + '&year=' + date[0] + '&month='  + date[1] + '&column_width=250,80', function(data1) {
                    tab = Ext.getCmp(tabId);
                    var table = createGrid(tabId, data1, 0);
                    tab.add(table);

                    var fields = "&fields=client__name,buy_sell,shares,nav_per_share,nav";

                    $.getJSON('/api/clienttransaction/?fund=' + obj.fund.id + '&value_date__year=' + date[0] + '&value_date__month='  + date[1] + '&column_width=100,100' + fields, function(data2) {
                        tab = Ext.getCmp(tabId);
                        //console.log('data2', data2, '/api/clienttransaction/?fund=' + obj.fund.id + '&value_date__year=' + date[0] + '&value_date__month='  + date[1] + '&column_width=100,100' + fields);
                        if(data2.length > 0) {
                            var table = createGrid('client' + tabId, data2, 1);
                            tab.add(table);
                        }
                    });
               });    
        }
        
        

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

            for(var p=0; p<children.length; p++) {

                childItems.push({
                    id: parents[i] + '-' + (1 + p),
                    title: children[p],
                    layout:  {type : 'vbox', align : 'stretch' }
                });
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


    
        //var tab_div = 'tab-' + widget.key + '-' + window_id;
        //$('<div id="' + tab_div + '"></div>').appendTo('#' + window_id);


    
         //console.log('window_id', window_id);
  
        var tp = new Ext.TabPanel({
            renderTo: div,
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
        //return widgetWindow(data.window.id, page, data.window.name, data.window.size_x, data.window.size_y, data.id, window_id);

    
    }

    
    function dateSpanPicker(id, div, widget) {
    
        var dateSpan = Ext.create('Ext.form.Panel', {
            header: false,
            border: false,
            width: widget.width,
            bodyPadding: 5,
            items: [
            {
                xtype: 'fieldcontainer',
                layout: 'hbox',
                items: [
                    {
                        xtype: 'datefield',
                        id: id + 'from_date',
                        width: 90,
                        //name: 'from_date',
                        maxValue: new Date(),  // limited to the current date or prior
                        listeners: {
                            select: function(combo, record, index) {
                                url = getReturnHistogramUrl(Ext.getCmp('hist').value);
                                //console.log('new from date', record);
                                from = moment(record).format('YYYY-MM-DD');
                                to = Ext.getCmp(id + 'to_date').getValue();
                                console.log('date from', url);
                                //console.log('old to date', to);
                                to = moment(to).format('YYYY-MM-DD');
                                $.getJSON(url + '&value_date__gte=' + from + '&value_date__lte=' + to, function(new_data) {
                                
                                    var chart = $('#data').data('chart-' + div);
                                    try {
                                       chart.series[0].setData(new_data[0].data);
                                    } catch(err) {
                                        chart.series[0].setData(new_data.data);
                                    }
                                    chart.redraw();
                                });
                            }
                        },                  
                    }, {
                        xtype: 'splitter'
                    }, {
                        xtype: 'datefield',
                        id: id + 'to_date',
                        width: 90,
                        //name: 'to_date',
                        value: new Date(),  // defaults to today
                        maxValue: new Date(),  // limited to the current date or prior
                        listeners: {
                            select: function(combo, record, index) {
                                url = getReturnHistogramUrl(Ext.getCmp('dateTypeHistogram').value);
                                to = moment(record).format('YYYY-MM-DD');
                                from = Ext.getCmp(id + 'from_date').getValue();
                                
                                if(from) {
                                    from = moment(from).format('YYYY-MM-DD');
                                    
                                    $.getJSON(url + '&value_date__gte=' + from + '&value_date__lte=' + to, function(new_data) {
                                    
                                        console.log('date to', url + '&value_date__gte=' + from + '&value_date__lte=' + to);
                                        var chart = $('#data').data('chart-' + div);
                                        try {
                                           chart.series[0].setData(new_data[0].data);
                                        } catch(err) {
                                            chart.series[0].setData(new_data.data);
                                        }
                                        chart.redraw();
                                    });
                                }
                            }
                        }, 
                    }
                ]
             }
             ]
        });
        return dateSpan;
    
    }
    
    
    
    // W2 - Holding Performance Bar & W7 - Holding NAV Bar
    function holdingPerformance(obj, widget, div, perfType) {
    
        if(perfType != 'nav') {
            var title1 = 'Performance';
            var title2 = 'Weighted Performance';
        } else {
            var title1 = 'NAV';
            var title2 = 'Weight';
        }
    
        function getUrl(type) {
        
            if(perfType == 'nav') {
                if(type === 1) {
                    var params = '&y1=marketvaluefundcur&order_by=-weight';
                } else {
                    var params = '&y1=weight&fields=weight&order_by=-weight';
                } 
            } else {   
                if(type === 1) {
                    var params = '&y1=performance&fields=weight&performance=true';
                } else {
                    var params = '&y1=weighted_perf&fields=weight&performance=true';
                }
            }
            var url = '/api/positionmonthly/?title=holding__name&data_type=graph&value_date__year=' + year + '&value_date__month=' + month + '&fund=' + obj.fund.id + params;
            return url;
        }
        
        function updateChart(record, type) {
        
        
            year = moment(record).format('YYYY');
            month = from = moment(record).format('MM');
            
            console.log('update chart w2', getUrl(type));
            $.getJSON(getUrl(type), function(new_data) {

                var options = $('#data').data('chart-options-' + div + '_tab' + type); 
                
                // disabling the fund performance line
                //var url = '/api/fundreturnmonthly/?fund=' + $('#data').data('fund') + '&fields=fund_perf&value_date__year=' + year + '&value_date__month=' + month;
                
               // console.log('dissecting line on bar', url);
                //$.getJSON(url, function(fund) {
                
                    // commented this as for now we are not displaying the fund performance if it's outside the y axis
                   // var fundValues = new Array();
                    //$.each(fund, function( index, value ) {
                   //     fundValues.push(value.fund_perf);
                   // });
                   // var maxVal = Math.max.apply(Math, fundValues); 
                   // var minVal = Math.min.apply(Math, fundValues); 
                    
                    if(widget.key == 'w2' || (widget.key == 'w7' && type !== 1)) {
                        options.yAxis.labels = {
                            formatter: function() {
                                return this.value + '%';
                            }
                        };
                    }
                    options.series = [new_data[0]];
                   // options.yAxis.max = maxVal;
                   // options.yAxis.min = minVal;
                   // options.yAxis.plotLines = [{
                   //     value: fund[0].fund_perf,
                   //     width: 1,
                   //     color: 'black',
                   //     label: {
                   //         text: $('#data').data('fund_name') + ' Performance',
                   //     },
                   //     zIndex: 5,
                  //  }];
                    new Highcharts.Chart(options);
               // });
           });
        }
                
        var year = moment().year();
        var month = moment().month();

        widget.params.labels = 'rotated';
        widget.params.legend = 'false';

        $('<div id="' + div + '_tab1"></div>').appendTo("#" + div);
        $('<div id="' + div + '_tab2"></div>').appendTo("#" + div);
        
        widget.height -= 70; // compensate for date picker
        
        
        widget.qs = '';
        widget.url = getUrl(1);
        console.log('url1', widget.url);
        
        barChart(obj, widget, div + '_tab1');
        
        widget.url = getUrl(2);
        
        console.log('url2', widget.url);
        
        barChart(obj, widget, div + '_tab2');
        
        var data = widget;
        var tabPanel = Ext.create('Ext.tab.Panel', {
            height: widget.height + 70,
            width:  widget.width + 10,
            activeTab: 0,
            border: false,
            items: [
                {
                    title: title1,
                    bodyPadding: 10,
                    //border: false,
                    //id: div + '_tab1',
                    items: [
                        {
                            xtype: 'monthfield',
                            submitFormat: 'Y-m-d',
                            name: 'month',
                            format: 'F, Y',
                            value: new Date(),
                            listeners: {
                                select: function(combo, record, index) {
                                    updateChart(record, 1);
                                }
                            },
                        }, {
                            xtype: 'container',
                            contentEl: div + '_tab1',
                        }
                    ],
                },
                {
                    title: title2,
                    //id: div + '_tab2',
                    bodyPadding: 10,
                    items: [
                        {
                            xtype: 'monthfield',
                            submitFormat: 'Y-m-d',
                            name: 'month',
                            format: 'F, Y',
                            value: new Date(),
                            listeners: {
                                select: function(combo, record, index) {
                                    updateChart(record, 2);
                                }
                            },
                        }, {
                            xtype: 'container',
                            contentEl: div + '_tab2',
                        }
                    ],
                },
            ],
            renderTo: div,
        });
        
        tabPanel.setActiveTab(1);
        tabPanel.setActiveTab(0);
        
    }
    
    function dateFilters(chart, url) {

        var button1m = Ext.create('Ext.Button', {
            text: '1m',
            handler: function() {
                var date = moment().subtract('months', 1).format("YYYY-MM-DD");
                $.getJSON(url + '&value_date__gte=' + date, function(new_data) {
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });
        
        var button3m = Ext.create('Ext.Button', {
            text: '3m',
            handler: function() {
                var date = moment().subtract('months', 3).format("YYYY-MM-DD");
                $.getJSON(url + '&value_date__gte=' + date, function(new_data) {
                    //console.log('3m filter', url + '&value_date__gte=' + date);
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });
        
        var button6m = Ext.create('Ext.Button', {
            text: '6m',
            handler: function() {
                var date = moment().subtract('months', 6).format("YYYY-MM-DD");
                $.getJSON(url + '&value_date__gte=' + date, function(new_data) {
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });            

        var button1y = Ext.create('Ext.Button', {
            text: '1y',
            handler: function() {
                var date = moment().subtract('year', 1).format("YYYY-MM-DD");
                $.getJSON(url + '&value_date__gte=' + date, function(new_data) {
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });
        
        var buttonYtd = Ext.create('Ext.Button', {
            text: 'YTD',
            handler: function() {
                var date = moment().startOf('year').format("YYYY-MM-DD"); 
                $.getJSON(url + '&value_date__gte=' + date, function(new_data) {
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });
        
        var buttonAll = Ext.create('Ext.Button', {
            text: 'All',
            handler: function() {
                $.getJSON(url, function(new_data) {
                    chart.series[0].setData(new_data.data);
                    chart.redraw();
                });
            }
        });


        var buttonContainer = Ext.create('Ext.container.Container', {
            padding: 5,
            items: [button1m, button3m, button6m, button1y, buttonYtd, buttonAll],
        });
        
        return buttonContainer;
    }
    
  
    function dateTypeSelector(id, chart, urlFunc) {

        var dateTypeStore = Ext.create('Ext.data.Store', {
            fields: ['name'],
            data : [
                {"id": "monthly", "name": "Monthly"},
                {"id": "daily", "name": "Daily"},
            ]
        });
        
        var dateTypeSelect = Ext.create('Ext.form.ComboBox', {
            store: dateTypeStore,
            id: id,
            padding: 5, 
            width: 80,
            queryMode: 'local',
            displayField: 'name',
            valueField: 'id',
            listeners: {
                'change': function(field, selectedValue) {
                   dateType = selectedValue;
                    $.getJSON(urlFunc(dateType), function(new_data) {
                        chart.series[0].setData(new_data.data);
                        chart.redraw();
                        //console.log(dateType, new_data);
                        //console.log('date select', getUrl(dateType));
                        Ext.getCmp(id + '_from_date').setValue();
                        Ext.getCmp(id + '_to_date').setValue(new Date());
                    });
                }
            }
        });
               
        // Set default value for drop down
        dateTypeSelect.setValue(dateTypeStore.getAt('0').get('id'));
        
        return dateTypeSelect;
    }

    
    function getReturnHistogramUrl(type) {
        var url = '/api/fundreturn' + type + '/?histogram=true&fields=fund_perf&date_type=monthly&fund=' + obj.fund.id;
        console.log('HISTOGRAM URL', url);
        return url;
    }    
    
    function returnHistogram(obj, widget, div) {
    
        function getUrl(type) {
            console.log('HISTOGRAM URL2', getReturnHistogramUrl(type));
            return getReturnHistogramUrl(type);
        }
        
        $.getJSON(getReturnHistogramUrl('monthly'), function(data) {

            var width = (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10;

            var options = {
	            chart: {
	                renderTo: div,
                    width: width,
                    height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)) - 70,
                    type: 'column',
	            },
	            title: {
	                text: false
	            },
                credits: {
                    enabled: false
                },
                yAxis: {
                    title: {
                        text: false,
                    },
                },
                legend: {
                    enabled: false,
                },
                scrollbar: {
                    enabled: false,
                }, 
                xAxis: {
                    type: 'category',
                    categories: data.columns,
                    labels: {
                        rotation: -45,
                    },
                },
                series: [{
                    data: data.data
                }],
	        };
	        var chart = new Highcharts.Chart(options);
	        
	        $('#data').data('chart-' + div, chart);

            var buttonContainer = dateFilters(chart, getUrl('monthly'));
            var dateSpan = dateSpanPicker('hist_', div, widget);    
            var dateTypeSelect = dateTypeSelector('hist', chart, getUrl);
            
            
            // check if it has daily data, if not we don't display the data type drop down menu            
            $.getJSON("/api/fundreturndaily/?fields=id&fund=" + obj.fund.id, function(data) {
                if(data.length === 0) {
                    items = [buttonContainer, dateSpan];
                } else {
                    items = [buttonContainer, dateTypeSelect, dateSpan];
                }

                var upperContainer = Ext.create('Ext.container.Container', {
                    renderTo: div + 'top',
                    autoFit: true,
                    layout: 'hbox',
                    style: {
                        background: 'white',
                    },
                    items: items,
                });
                
            });    
	    });
    
    }
    
   
    
    function fundHistoricalStats(obj, widget, div) {
        
        function getUrl() {
        
        
            var metricLength = Ext.getCmp(id + 'metric_panel').items.items.length;
            var axis = [];
            var xAxisvals = [];
            
            for(i=0; i<=metricLength - 1; i++) {
                var pos = Ext.getCmp(id + 'position_combo_' + (i + 1));
                var ax = Ext.getCmp(id + 'axis_combo_' + (i + 1));
                axis[i] = {
                   'position': pos.getValue(),
                   'opposite': ax.getValue(),
                }
                
            }
            
            // sort by position
            axis = axis.sort(function(a,b) {
                return a.position - b.position;
            });
            
            widget.yAxis = [];
            ///widget.xAxis = [];
            var top = 0;
            //console.log('axis', axis);
            for(i=0; i<=(axis.length - 1); i++) {
                
                //widget.xAxis[i] = {}; 
                //console.log('LOOPING axis', axis[i]);
                
                // unique positions equal seperate xAxis
                /*
                if(jQuery.inArray(axis[i]['position'], xAxisvals) === -1) {
                    widget.xAxis[i] = {
                        type: 'datetime',
                        //offset: -600,
                        height: 200,
                    };
                    xAxisvals[i] = axis[i]['position'];
                }
                */

                if(axis[i]['position'] == 1) {
                    var top = 50;
                    widget.height = 500;
                }
                else if(axis[i]['position'] == 2) {
                    var top = 500;
                    widget.height = 1000;
                }
                else if(axis[i]['position'] == 3) {
                    var top = 995;
                    widget.height = 1500;
                }
                else if(axis[i]['position'] == 4) {
                    var top = 1400;
                }
                else {
                    top += 900;
                }
                //if(i == 1) {
                //    var top = 500;
                //} else {
                //    var top = 1000;
                //}
                
                widget.yAxis[i] = {
                    height: 400,
                    top: top,
                    minorTickInterval: 'auto',
                };

                if(axis[i]['opposite'] == 'right') {
                    console.log('TRUE');
                    widget.yAxis[i]['opposite'] = true;
                } else {
                    widget.yAxis[i]['opposite'] = false;
                }
                //console.log('debug yAxis3', widget.yAxis);
            }
        
            //widget.xAxis = [{height:;
            
            //console.log('first yAxis', widget.yAxis);
            //console.log('first xAxis', widget.xAxis);
            
            var qVars = new Array('metric', 'yaxis', 'xaxis', 'layer', 'axis', 'plot', 'rfr', 'mar', 'step', 'window', 'sec_under', 'under', 'position');  
            
            // add date_type to qs
            var dateType = Ext.getCmp( id + 'date_type_combo').getValue();
            qs = 'date_type=' + dateType + '&';
            
            // add dates to qs
            var date_from = Ext.getCmp(id + 'from_date').getValue();
            var date_to = Ext.getCmp(id + 'to_date').getValue();
            
            if(date_from !== null) {
                qs += 'value_date__gte=' + moment(date_from).format('YYYY-MM-DD') + '&';
            }
            qs += 'value_date__lte=' + moment(date_to).format('YYYY-MM-DD') + '&';
            
            for(i=0; i<qVars.length; i++) {
            
                qs += '&' + qVars[i] + '=';
            
                for(m=0; m<metricLength; m++) {
                
                    val = Ext.getCmp(id + qVars[i] + '_combo_' + (m + 1)).getValue();
                    qs +=  val + ',';
                }
                qs = qs.slice(0, -1); // remove last comma
            }
            
            return '/api/fundreturn' + dateType + '/?' + qs + '&fund=' + obj.fund.id + '&fields=fund_perf,bench_perf';
        
        }
            
        function updateChart() {
        
            if(widget.key === 'w156') {
            
                chart(obj, widget, div);
            
            } else {
        
                
               if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
               
                    $('<div id="' + div + '_stats_graph"></div>').appendTo("#" + div);
              
                    var graphContainer = Ext.create('Ext.container.Container', {
                        contentEl: div + '_stats_graph',
                        title: 'Graph',
                        width: 945,
                        height: 640,
                    });   
                    
                    var tabPanel = Ext.getCmp(div);
                    
                    
                    if(typeof tabPanel === 'undefined') {       
                  
                        tabPanel = Ext.create('Ext.tab.Panel', {
                            //height: 200, //(120 * data.size_y) + (10 * data.size_y) + (10 * (data.size_y - 1)) - 20,
                            //width:  800, //(120 * data.size_x) + (10 * data.size_x) + (10 * (data.size_x - 1)) - 20,
                            //layout: 'fit',
                            width: 945,
                            renderTo: div,
                            id: div,
                            autoScroll: true,
                        });
                        
                    } else {
                        // remove old panels
                        for(i=0; i<=tabPanel.items.length; i++)
                        {
                            tabPanel.remove(tabPanel.items.getAt(0));
                        }
                        
                    }

                    widget.params.title = 'Table';
                    
                    //console.log('GET URL', getUrl());
                    
                    widget.url = getUrl();
                    widget.params.date_type = Ext.getCmp(id + 'date_type_combo').getValue();
                    
                    
                    
                    var url = widget.url + '&data_type=table&order_by=value_date';

                    console.log('data table url', url);
                    
                    $.getJSON(url, function(data) {
                    
                        
                        chart(obj, widget, div + '_stats_graph');
                        
                        var table = dataTable(data, obj, widget);

                        tabPanel.add(graphContainer);                
                        tabPanel.add(table);
                        tabPanel.doLayout(); 
                        tabPanel.setActiveTab(0);

                        
                    });
                } else if(jQuery.inArray(widget.key, ['w151']) !==-1 ) {
                
                    $('<div id="' + div + '_w151"></div>').appendTo("#" + div);
                
                    var mainContainer = Ext.create('Ext.container.Container', {
                        //contentEl: div + '_metric' + tabId,
                        //contentEl: div + '_w151',
                        autoFit: true,
                        closable: true,
                        padding: '0 5 5 5',
                        autoScroll: true,
                        style: {
                            background: 'white',
                        },
                    }); 
                    
                    widget.xAxis = false;
                    widget.yAxis = false;
                    widget.params.zoom = false;
                    widget.url = getUrl() + '&widget=w151';
                    widget.params.type = 'scatter';
                    var assdf = div + '_w151';
                    chart(obj, widget, div);
                
                }
            }
        }
        
        

    
        
        $('#data').data('chart-' + div, chart);
        
        //var dateSpan = dateSpanPicker('stats_', div, widget); 
        
        
        
        if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
            var id = 'stats_';
        } else if(jQuery.inArray(widget.key, ['w151']) !==-1 ) {
            var id = 'w151_';
        }
        
        var dateSpan = Ext.create('Ext.form.Panel', {
            header: false,
            border: false,
            width: widget.width,
            bodyPadding: 5,
            items: [
            {
                xtype: 'fieldcontainer',
                layout: 'hbox',
                items: [
                    {
                        xtype: 'datefield',
                        id: id + 'from_date',
                        width: 90,
                        //name: 'from_date',
                        maxValue: new Date(),  // limited to the current date or prior
                        listeners: {
                            select: function(combo, record, index) {
                                url = getReturnHistogramUrl(Ext.getCmp('hist').value);
                                //console.log('new from date', record);
                                from = moment(record).format('YYYY-MM-DD');
                                to = Ext.getCmp(id + 'to_date').getValue();
                                console.log('date from', url);
                                //console.log('old to date', to);
                                to = moment(to).format('YYYY-MM-DD');
                                $.getJSON(url + '&value_date__gte=' + from + '&value_date__lte=' + to, function(new_data) {
                                
                                    var chart = $('#data').data('chart-' + div);
                                    try {
                                       chart.series[0].setData(new_data[0].data);
                                    } catch(err) {
                                        chart.series[0].setData(new_data.data);
                                    }
                                    chart.redraw();
                                });
                            }
                        },                  
                    }, {
                        xtype: 'splitter'
                    }, {
                        xtype: 'datefield',
                        id: id + 'to_date',
                        width: 90,
                        //name: 'to_date',
                        value: new Date(),  // defaults to today
                        maxValue: new Date(),  // limited to the current date or prior
                        listeners: {
                            select: function(combo, record, index) {
                                url = getReturnHistogramUrl(Ext.getCmp('dateTypeHistogram').value);
                                to = moment(record).format('YYYY-MM-DD');
                                from = Ext.getCmp(id + 'from_date').getValue();
                                
                                if(from) {
                                    from = moment(from).format('YYYY-MM-DD');
                                    
                                    $.getJSON(url + '&value_date__gte=' + from + '&value_date__lte=' + to, function(new_data) {
                                    
                                        console.log('date to', url + '&value_date__gte=' + from + '&value_date__lte=' + to);
                                        var chart = $('#data').data('chart-' + div);
                                        try {
                                           chart.series[0].setData(new_data[0].data);
                                        } catch(err) {
                                            chart.series[0].setData(new_data.data);
                                        }
                                        chart.redraw();
                                    });
                                }
                            }
                        }, 
                    }
                ]
             }
             ]
        });
        
        var dateSpanTo = dateSpan.items.items[0].items.items[0];
        
        var button1m = Ext.create('Ext.Button', {
            text: '1m',
            handler: function() {
                var date = moment().subtract('months', 1).format("YYYY-MM-DD");
                dateSpanTo.setValue(date);
            }
        });
        
        var button3m = Ext.create('Ext.Button', {
            text: '3m',
            handler: function() {
                var date = moment().subtract('months', 3).format("YYYY-MM-DD");
                dateSpanTo.setValue(date);
            }
        });
        
        var button6m = Ext.create('Ext.Button', {
            text: '6m',
            handler: function() {
                var date = moment().subtract('months', 6).format("YYYY-MM-DD");
                dateSpanTo.setValue(date);
            }
        });            

        var button1y = Ext.create('Ext.Button', {
            text: '1y',
            handler: function() {
                var date = moment().subtract('year', 1).format("YYYY-MM-DD");
                dateSpanTo.setValue(date);
            }
        });
        
        var buttonYtd = Ext.create('Ext.Button', {
            text: 'YTD',
            handler: function() {
                var date = moment().startOf('year').format("YYYY-MM-DD"); 
                dateSpanTo.setValue(date);
            }
        });
        
        var buttonAll = Ext.create('Ext.Button', {
            text: 'All',
            handler: function() {
                var date = moment().subtract('year', 20).format("YYYY-MM-DD");
                dateSpanTo.setValue(date);
            }
        });


        var FilterButtonContainer = Ext.create('Ext.container.Container', {
            padding: 5,
            items: [button1m, button3m, button6m, button1y, buttonYtd, buttonAll],
        });
        

        //var FilterButtonContainer = dateFilters(chart, getUrl('monthly'));
           
        
        var dateType = 'monthly';
            
        var dateTypeStore = Ext.create('Ext.data.Store', {
            fields: ['name'],
            data : [
                {"id": "monthly", "name": "Monthly"},
                {"id": "daily", "name": "Daily"},
            ]
        });
        var dateTypeSelect = Ext.create('Ext.form.ComboBox', {
            store: dateTypeStore,
            id: id + 'date_type_combo',
            padding: 5, 
            width: 80,
            queryMode: 'local',
            displayField: 'name',
            valueField: 'id',
            listeners: {
                'change': function(field, selectedValue) {
                   dateType = selectedValue;
                   
                   /*
                    $.getJSON(urlFunc(dateType), function(new_data) {
                        chart.series[0].setData(new_data.data);
                        chart.redraw();
                        //console.log(dateType, new_data);
                        //console.log('date select', getUrl(dateType));
                        Ext.getCmp(id + '_from_date').setValue();
                        Ext.getCmp(id + '_to_date').setValue(new Date());
                    });
                    */
                }
            }
        }).hide();
        
        // show dateTypeSelect for all except ...
        if(jQuery.inArray(widget.key, ['w155']) ===-1 ) {
            dateTypeSelect.show();
        }
                           
        // Set default value for drop down
        dateTypeSelect.setValue(dateTypeStore.getAt('0').get('id'));
        

        //tabPanel.setActiveTab(0);
        
        var submitButton = Ext.create('Ext.Button', {
            text: 'Add Study',
            handler: function() {
            
                tabId = metricPanel.items.items.length + 1;
                
                var metrics = new Array();
                for(i=0; i<=tabId - 1; i++) {
                    metrics[i] = i + 1;
                }
                
                console.log('ID', id);
                $('<div id="' + div + id + '_metric' + tabId + '"></div>').appendTo("#" + div);
                
                var firstRun = true;
                

                console.log('dateType', dateType);
                
                     
                // Underlying drop down
                ///////////////////////
                if(jQuery.inArray(widget.key, ['w151', 'w155']) !==-1 ) {
                    var multiSelect = true;
                    console.log('multi select true');
                } else {
                    var multiSelect = false;
                    console.log('multi select false');
                }
                var underlyingStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"id": "fund", "name": obj.fund.name},
                        {"id": "benchpeer", "name": obj.fund.benchpeer.name},
                    ],
                    id: id + 'under_store_' + tabId,
                });
                var underlyingSelect = Ext.create('Ext.form.ComboBox', {
                    store: underlyingStore,
                    id: id + 'under_combo_' + tabId,
                    //contentEl: div + '_metric' + tabId,
                    multiSelect: multiSelect,
                    editable: false, 
                    fieldLabel: 'Underlying',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 180,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           //console.log('underlying changing value', selectedValue);
                           
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                });
                underlyingSelect.setValue(underlyingStore.getAt('0').get('id'));
                
                
                
                     
                // Second Underlying drop down
                ///////////////////////
                var secUnderlyingStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"id": "fund", "name": obj.fund.name},
                        {"id": "benchpeer", "name": obj.fund.benchpeer},
                    ],
                    id: id + 'sec_under_store_' + tabId,
                });
                var secUnderlyingSelect = Ext.create('Ext.form.ComboBox', {
                    store: underlyingStore,
                    id: id + 'sec_under_combo_' + tabId,
                    editable: false, 
                    fieldLabel: 'Second Underlying',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 180,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           console.log('sec underlying changing value', selectedValue);
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide(); // hide by default
                
                secUnderlyingSelect.setValue(secUnderlyingStore.getAt('0').get('id'));
                    
                
                // Add the benchmarks assigned to this fund for the underlying drop downs
                $.getJSON("/api/fundpeer/?fields=benchpeer__holding__id,benchpeer__name&fund=" + obj.fund.id +'&user=' + obj.user, function(data) {
                    
                    for(i=0; i < data.length; i++) { 
                         underlyingStore.add({
                            'id': data[i].benchpeer__holding__id, 
                            'name':  data[i].benchpeer__name
                         });
                         secUnderlyingStore.add({
                            'id': data[i].benchpeer__holding__id, 
                            'name':  data[i].benchpeer__name
                         });
                    }

                }); 
                
                // Add the secondary benchmarks assigned to this fund for the underlying drop downs
                if(jQuery.inArray(widget.key, ['w155', 'w156', 'w157']) !==-1 ) {
        
                     underlyingStore.add({
                        'id': obj.fund.sec_bench.id, 
                        'name': obj.fund.sec_bench.name
                     });
                     secUnderlyingStore.add({
                        'id': obj.fund.sec_bench.id, 
                        'name': obj.fund.sec_bench.name
                     });     
                        
                }
                
                // add the flash funds
                if(jQuery.inArray(widget.key, ['w155', 'w156', 'w157']) !==-1 ) {
                    $.getJSON("/api/fund/?fields=name,id&estimate_required=1", function(data) {
                        
                        for(i=0; i < data.length; i++) { 
                             underlyingStore.add({
                                'id': data[i].id, 
                                'name':  data[i].name
                             });
                             secUnderlyingStore.add({
                                'id': data[i].id, 
                                'name':  data[i].name
                             });
                        }

                    }); 
                }
                
                
                
                
                // Window drop down
                //////////////////////
                if(dateType == 'monthly') {
                    var windowStepValues = new Array(1, 3, 6, 9, 12, 24);
                    var windowDefault = 12;
                    var stepDefault = 1;
                } else {        
                    var windowStepValues = new Array(1, 5, 21, 63, 126, 252, 504);
                    var windowDefault = 252;
                    var stepDefault = 21;
                }
                console.log('dateType2', dateType);
                var windowSelect = Ext.create('Ext.form.ComboBox', {
                    store: windowStepValues,
                    id: id + 'window_combo_' + tabId,
                    fieldLabel: 'Window',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 180,
                    queryMode: 'local',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();  // hidden by default
                windowSelect.setValue(windowDefault);
                
                
                
                
                // Step drop down
                //////////////////////
                var stepSelect = Ext.create('Ext.form.ComboBox', {
                    store: windowStepValues,
                    id: id + 'step_combo_' + tabId,
                    fieldLabel: 'Step',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 100,
                    queryMode: 'local',
                    listeners: {
                        'change': function(field, selectedValue) {
                           dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();  // hidden by default
                stepSelect.setValue(stepDefault);
                
                                    
                                       
                var marRfrValues = new Array(0, 1, 2, 3, 4, 5);
                
                // Minimal Acceptable Return drop down (MAR)
                //////////////////////
                var marSelect = Ext.create('Ext.form.ComboBox', {
                    store: marRfrValues,
                    id: id + 'mar_combo_' + tabId,
                    fieldLabel: 'MAR',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 50,
                    queryMode: 'local',
                    listeners: {
                        'change': function(field, selectedValue) {
                           dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();  // hidden by default
                marSelect.setValue(0);
                
                                    
                // Risk Free Rate drop down (RFR)
                //////////////////////
                var rfrSelect = Ext.create('Ext.form.ComboBox', {
                    store: marRfrValues,
                    id: id + 'rfr_combo_' + tabId,
                    fieldLabel: 'RFR',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 50,
                    queryMode: 'local',
                    listeners: {
                        'change': function(field, selectedValue) {
                           dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();  // hidden by default
                rfrSelect.setValue(0);
                
             
             
                
                // What metrics makes the drop down menus Window and Step visible 
                var windowSteps = new Array(
                    "roll_average", "roll_deviation", "roll_cumulative", "roll_skewness", 
                    "roll_kurtosis", "roll_annualised", "roll_volatility",  "roll_sharpe",  
                    "roll_sortino", "roll_downside", "roll_excess", "roll_tracking", "roll_correlation"                    
                );
                
                
                // What metrics makes the Second Underlying drop down visible
                if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
                    var secondUnderlying = new Array(
                        "delta", "roll_excess", 
                        "roll_tracking", "roll_correlation", "roll_alpha",
                        "roll_beta",  "roll_rsq"
                    );
                } else if(jQuery.inArray(widget.key, ['w151', 'w155']) !==-1 ) {
                    var secondUnderlying = [                
                        'delta_cum_returns_final_val', 'tracking_error', 
                        'correlation', 'alpha', 'beta', 'r2',
                    ];
                }
               
               
               
                // What metrics makes the MAR drop down visible
                var mar = new Array("roll_downside");
               
                // What metrics makes the RAR drop down visible
                var rfr = new Array("roll_alpha", "roll_beta", "roll_rsq");
                   
                                                            


                // Metric drop down
                ///////////////////           
                if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
                    var metricData = [
                        {"id": "cumulative", "name": "Cumulative Return"},
                        {"id": "return", "name": "Returns"},
                        {"id": "delta", "name": "Delta Cumulative Return"},
                        {"id": "roll_average", "name": "Rolling Average"},
                        {"id": "roll_deviation", "name": "Rolling Standard Deviation"},
                        {"id": "roll_cumulative", "name": "Rolling Cumulative  Return"},
                        {"id": "roll_skewness", "name": "Rolling Skewness"},
                        {"id": "roll_kurtosis", "name": "Rolling Kurtosis"},
                        {"id": "roll_annualised", "name": "Rolling Annualised Return"},
                        {"id": "roll_volatility", "name": "Rolling Volatility"},
                        {"id": "roll_sharpe", "name": "Rolling Sharpe"},
                        //{"id": "roll_sortino", "name": "Rolling Sortino"},
                        //{"id": "roll_downside", "name": "Rolling Downside Vol"},
                        {"id": "roll_excess", "name": "Rolling Excess Return"},
                        {"id": "roll_tracking", "name": "Rolling Tracking Error"},
                        {"id": "roll_correlation", "name": "Rolling Correlation"},
                        {"id": "roll_alpha", "name": "Rolling Alpha"},
                        {"id": "roll_beta", "name": "Rolling Beta"},
                        //{"id": "roll_rsq", "name": "Rolling RSQ"},
                    ];
                } else {                
                    var metricData = [              
                        {"id": "delta_cum_returns_final_val", "name": "Excess Return"},
                        {"id": "tracking_error", "name": "Tracking Error"},                               
                        {"id": "correlation", "name": "Correlation"},
                        {"id": "alpha", "name": "Alpha"},
                        {"id": "beta", "name": "Beta"},
                        {"id": "r2", "name": "RSQ"},
                        //##### Do not require a second series#####
                        {"id": "mean", "name": "Average"},
                        {"id": "standard_deviation", "name": "Standard Deviation"},
                        {"id": "variance", "name": "Variance"},
                        {"id": "max_drawdown", "name": "Maximum DrawDown"},
                        {"id": "cum_returns_final", "name": "Final Value Cumulative Return"},
                        {"id": "skewness", "name": "Skewness"},
                        {"id": "kurtosis", "name": "Kurtosis"},
                        {"id": "annualised_returns", "name": "Annualised Return"},
                        {"id": "annualised_volatility", "name": "Annualised Volatility"},
                        {"id": "downside_volatility", "name": "Downside Volatility"},
                        {"id": "sortino_ratio", "name": "Sortino Ratio"},
                        {"id": "sharpe_ratio", "name": "Sharpe Ratio"},
                    ]; 
                }
                var metricStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data: metricData,
                    id: id + 'metric_store_' + tabId,
                });
                var metricSelect = Ext.create('Ext.form.ComboBox', {
                    store: metricStore,
                    id: id + 'metric_combo_' + tabId,
                    editable: false, 
                    fieldLabel: 'Metric',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 180,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                        
                            if(jQuery.inArray(widget.key, ['w18', 'w151', 'w155']) !==-1 ) {
                                
                                // show the Second Underlying drop down when certain metrics are selected
                                if(secondUnderlying.indexOf(selectedValue) == -1) {
                                    secUnderlyingSelect.hide();
                                } else {
                                    secUnderlyingSelect.show();
                                }
                            }
                            if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
                            
                                // show the Window drop down when certain metrics are selected
                                if(windowSteps.indexOf(selectedValue) == -1) {
                                    windowSelect.hide();
                                    stepSelect.hide();
                                } else {
                                    windowSelect.show();
                                    stepSelect.show();
                                }
                                
                                // show the MAR drop down when certain metrics are selected
                                if(mar.indexOf(selectedValue) == -1) {
                                    marSelect.hide();
                                } else {
                                    marSelect.show();
                                }
                                
                                // show the RFR drop down when certain metrics are selected
                                if(rfr.indexOf(selectedValue) == -1) {
                                    rfrSelect.hide();
                                } else {
                                    rfrSelect.show();
                                }
                                
                                // Add the open metric tabs to the underlying drop downs
                                if(selectedValue === 'roll_average' || selectedValue == 'roll_deviation') {
                                    for(i=1; i <= tabId; i++) {
                                         store1 = Ext.data.StoreManager.lookup('under_store_' + i);
                                         store2 = Ext.data.StoreManager.lookup('sec_under_store_' + i);
                                         for(x=1; x <= tabId; x++) {
                                             store1.add({
                                                'id': 'metric' + x, 
                                                'name': 'Metric ' + x
                                             });
                                             store2.add({
                                                'id': 'metric' + x, 
                                                'name': 'Metric ' + x
                                             });
                                         }
                                    }
                               }
                           };
                            
                           if(firstRun == false) {
                               updateChart();
                           }

                        }
                    }
                }).hide();
                
                metricSelect.setValue(metricStore.getAt('0').get('id'));
                
                
                // X&Y Axis Drop Down for W151 & W156
                //////////////////////////////
                var xAxisSelect = Ext.create('Ext.form.ComboBox', {
                    store: metricStore,
                    id: id + 'xaxis_combo_' + tabId,
                    fieldLabel: 'X Axis',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 150,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();
                xAxisSelect.setValue(metricStore.getAt('0').get('id'));
                
                var yAxisSelect = Ext.create('Ext.form.ComboBox', {
                    store: metricStore,
                    id: id + 'yaxis_combo_' + tabId,
                    fieldLabel: 'Y Axis',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 150,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                          // dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                }).hide();
                yAxisSelect.setValue(metricStore.getAt('0').get('id'));

                
                
                
                
                
                // Plot Type drop down
                //////////////////////
                var plotStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"id": "line", "name": "Line"},
                        {"id": "column", "name": "Bar"},
                        {"id": "area", "name": "Area"},
                    ],
                    id: id + 'plot_store_' + tabId,
                });
                var plotSelect = Ext.create('Ext.form.ComboBox', {
                    store: plotStore,
                    id: id + 'plot_combo_' + tabId,
                    fieldLabel: 'Plot',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 100,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                });
                plotSelect.setValue(plotStore.getAt('0').get('id'));
                

                
                
                // Axis drop down
                //////////////////////
                var axisStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"id": "left", "name": "Left"},
                        {"id": "right", "name": "Right"},
                    ],
                    id: id + 'axis_store_' + tabId,
                });
                var axisSelect = Ext.create('Ext.form.ComboBox', {
                    store: axisStore,
                    id: id + 'axis_combo_' + tabId,
                    fieldLabel: 'Axis',
                    labelAlign: 'top',
                    padding: '0 5 5 5',
                    width: 100,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        'change': function(field, selectedValue) {
                           //dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                });
                axisSelect.setValue(axisStore.getAt('0').get('id'));
                
                
                
                
                
                
                // Position drop down
                //////////////////////
                var positionValues = new Array(1, 2, 3, 4, 5);
                var positionSelect = Ext.create('Ext.form.ComboBox', {
                    store: positionValues,
                    id: id + 'position_combo_' + tabId,
                    fieldLabel: 'Position',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 100,
                    queryMode: 'local',
                    listeners: {
                        'change': function(field, selectedValue) {
                           if(firstRun == false) {
                               updateChart(div + '_stats_graph' + selectedValue);
                           }
                        }
                    }
                });  
                positionSelect.setValue(1);
                
                
                
                
                
                
                // Layer drop down
                //////////////////////
                var layerStore = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"id": "5", "name": "1"},
                        {"id": "4", "name": "2"},
                        {"id": '3', "name": '3'},
                        {"id": '2', "name": '4'},
                        {"id": '1', "name": '5'},
                    ],
                    id: id + 'layer_store_' + tabId,
                });
                var layerValues = new Array(1, 2, 3, 4, 5);
                var layerSelect = Ext.create('Ext.form.ComboBox', {
                    store: layerStore,
                    id: id + 'layer_combo_' + tabId,
                    fieldLabel: 'Layer',
                    labelAlign: 'top',
                    padding: '0 5 0 5',
                    width: 100,
                    queryMode: 'local',
                    valueField: 'id',
                    displayField: 'name',
                    listeners: {
                        'change': function(field, selectedValue) {
                           dateType = selectedValue;
                           if(firstRun == false) {
                               updateChart();
                           }
                        }
                    }
                });  
                layerSelect.setValue(1);
                
                
                firstRun = false;
                
                
                
                // Show or Hide
                if(jQuery.inArray(widget.key, ['w155']) !==-1 ) {
                    rfrSelect.show();
                    secUnderlyingSelect.show();
                    windowSelect.show();
                    stepSelect.show();
                } else if(jQuery.inArray(widget.key, ['w151', 'w156']) !==-1 ) {
                    xAxisSelect.show();
                    yAxisSelect.show();
                    secUnderlyingSelect.show();
                    marSelect.show();
                    rfrSelect.show();
                } else if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {
                    metricSelect.show();
                }
                
                  

                // Containers
                //////////////
                var upperContainer = Ext.create('Ext.container.Container', {
                    layout:'column',
                    items: [{
                        columnWidth: .75,
                        border: 0,
                        layout: 'hbox',
                        items: [xAxisSelect, metricSelect, windowSelect],
                    },{
                        columnWidth: .25,
                        border: 0,
                        layout: 'hbox',
                        items: [plotSelect, axisSelect],
                    }],
                });    
                
                var lowerContainer = Ext.create('Ext.container.Container', {
                    layout:'column',
                    items: [{
                        columnWidth: .75,
                        border: 0,
                        layout: 'hbox',
                        items: [yAxisSelect, underlyingSelect, secUnderlyingSelect, stepSelect, marSelect, rfrSelect],
                    },{
                        columnWidth: .25,
                        border: 0,
                        layout: 'hbox',
                        items: [positionSelect, layerSelect],
                    }],
                });   
                
                console.log('ID2', id);
                var mainContainer = Ext.create('Ext.container.Container', {
                    contentEl: div + id + '_metric' + tabId,
                    autoFit: true,
                    title: 'Metric ' + tabId,
                    id: id + 'metric_' + tabId,
                    closable: true,
                    padding: '0 5 5 5',
                    autoScroll: true,
                    style: {
                        background: 'white',
                    },
                    items: [upperContainer, lowerContainer],
                    /*
                    listeners: {
                        'close': function(val) {
                            var id = val['id'].replace("metric_","");
                            console.log('CLOSE ID', id);
                            Ext.getCmp('metric_combo_' + id).destroy();
                            updateChart();
                        }
                    }
                    */
                });   
                
                metricPanel.add(mainContainer).show();  
                    
                updateChart();
                
            }
        });
        
        var metricPanel = Ext.create('Ext.tab.Panel', {
            id: id + 'metric_panel',
        });
        
        var SubmitButtonContainer = Ext.create('Ext.container.Container', {
            padding: 5,
            items: [submitButton],
        });
        
        

       // for(i=0; i<windowStepValues.length; i++) {
            //windowStore.add({
            //    'id': windowStepValues[i],
            //    'name': windowStepValues[i]
            //});
       // }
        
        //var asdf = Ext.create('Ext.form.FieldContainer', {
        var upperContainer = Ext.create('Ext.container.Container', {
            renderTo: div + 'top',
            autoFit: true,
            layout: 'hbox',
            style: {
                background: 'white',
            },
            items: [FilterButtonContainer, SubmitButtonContainer, dateTypeSelect, dateSpan],
        });
        //var upperContainer = Ext.create('Ext.container.Container', {
        
        
        // check if it has daily data           
        $.getJSON("/api/fundreturndaily/" + obj.fund.id + "/?fields=id&has_data=true", function(data) {
        
            //if it hasn't, hide the date type drop down menu 
            if(data == 0) {
                dateTypeSelect.hide();
            }
            
        }); 
        
        Ext.create('Ext.container.Container', {
            renderTo: div + 'top',
            items: [metricPanel],
        });
        
        // div for graph & table
        //$('<div id="' + div + '_stats_graph"></div>').appendTo("#" + div);
        //$('<div id="' + div + '_stats_table2"></div>').appendTo("#" + div);
          

        
        /*
        Ext.create('Ext.tab.Panel', {
            renderTo: div,
            items: [{
                title: 'Graph',
                width: 945,
                height: 640,
                autoScroll: true,
                contentEl: div + '_stats_graph',
                border: 1,
            },{
                title: 'Table',
                width: 945,
                height: 640,
                autoScroll: true,
                contentEl: div + '_stats_table',
                border: 1,
            }],
        });
        */
    }
    
    function lineChart(obj, widget, div, series, series2) {
    

        if(typeof series2 !== 'undefined') {
            series[2] = series2;
        }
        
        
        //console.log(series[0].data.length);
        var lastPoint = Array();
        lastPoint[0] = series[0].data[series[0].data.length - 1][1];
        lastPoint[1] = series[1].data[series[1].data.length - 1][1];
        lastPoint[2] = series[2].data[series[2].data.length - 1][1];
        
        if(widget.key === 'w152') {
            lastPoint[3] = series[3].data[series[3].data.length - 1][1];
            lastPoint[4] = series[4].data[series[4].data.length - 1][1];
        }
        //console.log(lastPoint);
        

            
        if(widget.key === 'w152') {
            var yAxis = [{
                    height: 420,
                    lineWidth: 2,
                    labels: {
                        formatter: function() {
                            return this.value + '%';
                        }
                    },
                    //min: 0,
                }, {
                    top: 500,
                    height: 210,
                    lineWidth: 2,
                    labels: {
                        formatter: function() {
                            return this.value + '%';
                        }
                    },
                    //min: 0,
            }];
            /*
                }, {
                    height: 420,
                    opposite:true,
                    linkedTo:0,
                    tickPositions:[lastPoint[0]] ,
                    gridLineWidth:0,
                    offset: 40,
                }, {
                    height: 420,
                    opposite:true,
                    linkedTo:0,
                    tickPositions:[lastPoint[1]] ,
                    gridLineWidth:0
                }, {
                    height: 420,
                    opposite:true,
                    linkedTo:0,
                    tickPositions:[lastPoint[2]] ,
                    gridLineWidth:0
                },{
                    top: 500,    
                    height: 210, 
                    opposite:true,
                    linkedTo:1,
                    tickPositions:[lastPoint[3]],
                    gridLineWidth:0
                },{
                    top: 500,    
                    height: 210, 
                    opposite:true,
                    linkedTo:1,
                    tickPositions:[lastPoint[4]],
                    gridLineWidth:0
            }];
            */
        } else {
        
            var yAxis = [{
                    height: 420,
                    lineWidth: 2,
                    labels: {
                        formatter: function() {
                            return this.value + '%';
                        }
                    },
                    minorTickInterval: 'auto',
                    //min: 0,
                }, {
                    top: 500,
                    height: 210,
                    lineWidth: 2,
                    labels: {
                        x: -20,
                        formatter: function() {
                            return this.value + '%';
                        }
                    },
                    minorTickInterval: 'auto',
                    //min: 0,
            }];
            /*
                }, {
                    height: 420,
                    opposite:true,
                    linkedTo:0,
                    tickPositions:[lastPoint[0]] ,
                    gridLineWidth:0,
                    offset: 40,
                }, {
                    height: 420,
                    opposite:true,
                    linkedTo:0,
                    tickPositions:[lastPoint[1]] ,
                    gridLineWidth:0
                },{
                    top: 500,    
                    height: 210, 
                    opposite:true,
                    linkedTo:1,
                    tickPositions:[lastPoint[2]],
                    gridLineWidth:0
                }];
             */
        }
        
        var options = {
            chart: {
                spacingBottom: -50, // hide the navigator
                renderTo: div,
                width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)) - 10,
                height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
            },
            colors: [
               '#01017D', 
               '#01810E', 
                '#9A5D01',
                'red',
                'brown',
                'LightSkyBlue',
            ],
            navigator:{
                enabled: true,
                adaptToUpdatedData: false,
                height: 0,
                margin: 60,
            }, 
            scrollbar: {
                enabled: false,
            },   
            plotOptions: {
              series: {
                events: {
                  legendItemClick: function(event) {
                      var series = this.yAxis.series,
                          seriesLen = series.length,
                          visible = this.visible ? 1 : -1; 
                          // +1 when visible series, because it will be changed after that callback

                      for(var i = 0; i < seriesLen; i++) {
                        if(!series[i].visible) {
                          visible++;
                        }
                      }
                      if(visible >= 2 && this.index < 2) { // disable fund/bench
                            chart.yAxis[0].update({
                                 height:5
                            });
                            chart.yAxis[1].update({
                                 height: 600,
                                 top: 50,
                            });
                            chart.xAxis[0].update({
                                 offset: -700,
                            });
                            chart.xAxis[1].update({
                                 offset: 0,
                            });
                      } else if(visible >= 1 && this.index >= 2) { // disable delta
                            chart.yAxis[0].update({
                                 height: 600,
                                 top: 50,
                            });
                            chart.yAxis[1].update({
                                 height:5,
                                 top: 50,
                            });
                            chart.xAxis[0].update({
                                 offset: -700,
                            });
                            chart.xAxis[1].update({
                                 offset: 0,
                            });
                      } else {  //  default
                            chart.yAxis[0].update({
                                 height: 420
                            });
                            chart.yAxis[1].update({
                                 height: 210,
                                 top: 500,
                            });
                            chart.xAxis[0].update({
                                 offset: -700,
                            });
                            chart.xAxis[1].update({
                                 offset: -200,
                            });
                      }
                  }
                },
              }
            },
            rangeSelector: {
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
                inputEnabled: true,
                selected : 3
            },
            credits: {
                enabled: false
            },
            title: {
                text: false
            },
            legend: {
                enabled: true,
                y: -75,
            },
            yAxis: yAxis,
            xAxis: [{
                type: 'datetime',
                //events: {
                //    afterSetExtremes: function(e){
                //        refreshGraph(e, widget);
                //    }
                //},
                
                opposite: true,
                offset: -700,
                //offset: -45,
                events:{
                    afterSetExtremes:function(e){
                        console.log(this);
                        var min = this.min,
                            max = this.max,
                            chart = this.chart;
                        
                        chart.xAxis[1].setExtremes(min,max);
                        refreshGraph(e, widget);
                        

                    }
                },
            },{
                type: 'datetime',
                
                offset: -200,
            }],
            
            series: series,
        };
        var chart = new Highcharts.StockChart(options);


    }




    function chart(obj, widget, div) {
    
    
        //var chartDiv = div;
        //div = div + '_stats_graph';

        //console.log('function chart started');
        //if(typeof $('#' + div).highcharts() != 'undefined') {
        //   console.log('chart already created');
        //}

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

        var yAxisTitle = false;
        if(typeof widget.params.yAxisTitle != 'undefined') {
            if(widget.params.yAxisTitle == 'false') {
                yAxisTitle = false;
            } else {
                yAxisTitle = widget.params.yAxisTitle;
            }
        }
        
        if(typeof widget.yAxis !== 'undefined') {
            var yAxis = widget.yAxis;
            for(i=0; i<widget.yAxis.length; i++) {
                yAxis[i]['title'] = {
                    text: yAxisTitle,
                };
            }
        } else {
            var yAxis = {
                title: {
                    text: yAxisTitle,
                },
                minorTickInterval: 'auto',
            };
        }
        
        if(typeof widget.xAxis === 'undefined') {
            var xAxis = {
                type: 'datetime',
                //offset: -200,
                //reversed: true,
            };
        } else {
            var xAxis = widget.xAxis;
        }


        //console.log('widget yAxis', yAxis);
        //console.log('widget xAxis', xAxis);

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
        
        //console.log('HEIGHT', (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)));


        var colors = new Array();
        
        //console.log('yAxis', yAxis);
        //console.log('xAxis', xAxis);
        
        console.log('chart call', 'http://localhost:8000' + widget.url);        
        $.getJSON(widget.url + widget.qs, function(data) {
        
            
        
                
            /**
             * Experimental Highcharts plugin to implement chart.alignThreshold option.
             * Author: Torstein Hønsi
             * Last revision: 2013-12-02
             */ (function (H) {
                var each = H.each;
                H.wrap(H.Chart.prototype, 'adjustTickAmounts', function (proceed) {
                    var ticksBelowThreshold = 0,
                        ticksAboveThreshold = 0;
                    if (this.options.chart.alignThresholds) {
                        each(this.yAxis, function (axis) {
                            var threshold = axis.series[0] && axis.series[0].options.threshold || 0,
                                index = axis.tickPositions && axis.tickPositions.indexOf(threshold);

                            if (index !== undefined && index !== -1) {
                                axis.ticksBelowThreshold = index;
                                axis.ticksAboveThreshold = axis.tickPositions.length - index;
                                ticksBelowThreshold = Math.max(ticksBelowThreshold, index);
                                ticksAboveThreshold = Math.max(ticksAboveThreshold, axis.ticksAboveThreshold);
                            }
                        });

                        each(this.yAxis, function (axis) {

                            var tickPositions = axis.tickPositions;

                            if (tickPositions) {

                                if (axis.ticksAboveThreshold < ticksAboveThreshold) {
                                    while (axis.ticksAboveThreshold < ticksAboveThreshold) {
                                        tickPositions.push(
                                        tickPositions[tickPositions.length - 1] + axis.tickInterval);
                                        axis.ticksAboveThreshold++;
                                    }
                                }

                                if (axis.ticksBelowThreshold < ticksBelowThreshold) {
                                    while (axis.ticksBelowThreshold < ticksBelowThreshold) {
                                        tickPositions.unshift(
                                        tickPositions[0] - axis.tickInterval);
                                        axis.ticksBelowThreshold++;
                                    }

                                }
                                //axis.transA *= (calculatedTickAmount - 1) / (tickAmount - 1);
                                axis.min = tickPositions[0];
                                axis.max = tickPositions[tickPositions.length - 1];
                            }
                        });
                    } else {
                        proceed.call(this);
                    }

                })
            }(Highcharts));

        
            $.each(data, function( index, obj ) {
                colors.push(obj.color);
                
                if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {   
                    yAxis[index]['labels'] = {
                        formatter: function() {
                            return this.value + obj.label;
                        },
                        x: -10,
                    };
                    yAxis[index]['minorTickInterval'] = 'auto';
                 }
                
                
            });
            
            // default colors
            if(colors.length === 0) {
                colors: [
                   'orange',
                ];           
            }


            var options = {
                colors: colors,
                chart: {
                    alignThresholds: true,
                    type: type,
                    marginRight: 25,
                    //marginBottom: 25,
                    spacingBottom: -20,
                    size: '100%',
                    renderTo: div,
                    width: widget.width,
                    height: widget.height,
                },
                credits: {
                    enabled: false
                },
                navigator:{
                    enabled: navigator,
				    adaptToUpdatedData: false,
				    //series: data.objects,
				    height: 20,
                },
                scrollbar: {
                    enabled: scrollbar
                },
                title: {
                    text: title,
                //    x: -20 //center
                },
                //xAxis: {
                //    //gridLineWidth: 1,
                //    type: 'category',
                //    categories: data.objects.columns,
                //},
                //yAxis: yAxis,
                //xAxis: xAxis,
                tooltip: {
                    //valueSuffix: '€'
                },
                legend: {
                    enabled: legend,
                    //layout: 'vertical',
                    //align: 'right',
                    //verticalAlign: 'top',
                    //x: -50,
                    y: -20,
                    //borderWidth: 0
                },
                series: data,
            };
            //console.log('data', data);

            
            if(typeof widget.params.date_type != 'undefined' && widget.params.date_type == 'monthly') {
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
			        inputEnabled: true,
			        selected : 3
                }
            } else if(typeof widget.params.date_type != 'undefined' && widget.params.date_type == 'daily') {
                options['rangeSelector'] = {
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
			        inputEnabled: true,
			        selected : 6
                }
            }
            if(typeof widget.params.zoom != 'undefined' && widget.params.zoom == 'true') {
               //console.log(options.xAxis);
               console.log('ZOOMING');
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
            } else {

            }
            

            if(jQuery.inArray(widget.key, ['w18']) !==-1 ) {            
                console.log('YAXIS');
                options['yAxis'] = yAxis;
            }    
            
            
            if(typeof $('#' + div).highcharts() !== 'undefined') {
                $('#' + div).highcharts().destroy();
                delete $('#' + div);
                //$('<div id="' + div + '"></div>').appendTo("#" + chartDiv);
                console.log('DESTROYING CHART');
            }
            
            if(jQuery.inArray(widget.key, ['w151', 'w156']) !==-1 ) {     
                var chart = new Highcharts.Chart(options);  
            } else {
                var chart = new Highcharts.StockChart(options);
            }
            //var chart = new Highcharts.Chart(options); // cannot be used with rangeSelector options
            //console.log('CREATING NEW CHART');
           
        });
    }
 

    function monthTable(year, month) {

        var fund = $('#data').data('fund');

        
        var title = 'FUND_NAME / MONTH YEAR / Historical Performance';
        title = title.replace('FUND_NAME', $('#data').data('fund_obj').name);
        title = title.replace('YEAR', moment(new Date(year)).format("YYYY"))
        title = title.replace('MONTH', moment(new Date(year, month - 1)).format("MMMM"))


        $('<div id="calendar"></div>').appendTo('body');
        mo_widget = {}
        mo_widget.url = '/api/fundreturndaily/';
        mo_widget.qs = '?fund=' + fund + '&fields=value_date,fund_mtd&order_by=value_date&value_date__year=' + year + '&value_date__month=' + month;

        $.getJSON(mo_widget.url + mo_widget.qs , function(data) {

            // first day in first week of month
            var d = new Date(year, month - 1, 1);
            var first_weekday = d.getDay();
            var first_date = year.toString() + '-' + month.toString() + '-' + 1;
            var first_week_of_month = moment(first_date).format("w");
            console.log(first_date, first_week_of_month);

            // last day of the month
            var d2 = new Date(year, month, 0);
            var last_day_of_month = d2.getDate();

            var html = '<table class="month_table"><tr>';
            //html += '<th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><tr><th>' + first_week_of_month + '</th>';
            html += '<th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><tr>';

            // empty cells for months that do not start on a monday
            if(first_weekday < 6) {
                for(i=1; i<first_weekday; i++) {
                    html += "<td></td>";
                }
            }

            // converting the data object
            days = {};
            for(i=0; i < data.length; i++) {
                var day = data[i].value_date.substr(8,2);
                day = parseInt(day, 10);
                days[day] = data[i].fund_mtd;
            }
            
            var week_count = 0;

            for(i=1; i<=last_day_of_month; i++) {

                if(typeof days[i] != 'undefined') {
                    var val = days[i];
                } else {
                    var val = 0;
                }

                date = year.toString() + '-' + month.toString() + '-' + i;
                //day = moment(date).format("Do");

                week = parseInt(moment(date).format("w")) + 1;

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
                        if(i != last_day_of_month && week_count < 4){
                            //html += '<th>' + week + '</th>';
                            week_count++;
                        }
                        continue;
                    }

                }
                if(val < 0) {
                    style = ' style="color: #F73100;"';
                } else {
                    style = ' style="color: #01017D;"';
                }
                html += '<td><div><span class="month_table_day">' + i + '</span><span class="month_table_val"><a href="#"' + style + ' onclick="refreshHoldPerfBar(\'w2\', \'' + date + '\', ' + fund + ');">' + val + ' <span style="font-weight: normal;">%</span></a></div></span></td>';
            }

            html += "</tr></table>";

            var win2 = Ext.getCmp('open_win');
            if (win2) {
                win2.close();
            }

            var win = new Ext.Window({
                id: 'open_win',
                renderTo: Ext.getBody(),
                html: html,
                title: title,
                //items: items,
                height: 340,
                //width: 475,
                width: 400,
            });

            win.show();

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
        if(typeof widget.window !== 'undefined' && widget.window.key == 'w10' && $('#data').data('classification') == 'eof') {
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

console.log('WIDGET', widget);

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
                        obj.year = year;
                        obj.month = month

                        if(widget.window.key == 'w8' || widget.window.key == 'w66') {
                            var group = 'sec';
                            var group_name = 'Sector';
                        } else if(widget.window.key == 'w9') {
                            var group = 'sub';
                            var group_name = 'Sub-Sector';
                        } else if(widget.window.key == 'w9b') {
                            var group = 'ass';
                            var group_name = 'Asset Class';
                        } else if(widget.window.key == 'w9c') {
                            var group = 'inv';
                            var group_name = 'Investment Type'
                        } else if(widget.window.key == 'w8b') {
                            var group = 'hol';
                            var group_name = 'Holding';

                        } else if(widget.window.key == 'w10' || widget.window.key == 'w67') {
                            var group = 'loc';
                            var group_name = 'Location';
                        }

                        div = $('#data').data('piechart-div-' + widget.window.key);
                        var window_id = 'page_' + obj.page + '_win_' + widget.window.id;

                        var value_date = "&value_date__year=YEAR&value_date__month=" + month + "&value_date__day=1";

                        widget.key = "holding-breakdown";
                        widget.qs = "?fund=" + fund + "&category__group=" + group + "&y1=base_nav&data_type=graph&date=value_date&title=category__name" + value_date;
                        widget.name = 'NAV by ' + group_name + ' MONTH YEAR';
                        widget.params.value_date__year = year;
                        widget.params.holding_category__holding_group = "sec";
                        widget.params.fund = "FUND";
                        widget.params.fields = "base_nav";
                        widget.type = "pie_chart";
                       //console.log(widget);

                        var widget_obj = $('#' + div).highcharts();
                        widget_obj.destroy();

                        createWidget(obj, widget, div, extra_params);
                    }
               }
            }

        });

        if(typeof widget.window !== 'undefined' && widget.window.key == 'w10' && $('#data').data('classification') == 'eof') {

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
            var qs = widget.qs.replace('value=euro_nav', 'value=weight'); // ???
            widget.params.title = '% of Fund';

            $.getJSON(widget.url + qs, function(data2) {
                var grid = createGrid(widget, data2);
                tabPanel.add(grid);
                tabPanel.doLayout();
            });
            tabPanel.setActiveTab(0);

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
    
    
    
    

    function barChart(obj, widget, div) {

        $.getJSON(widget.url + widget.qs, function(data) {
        
            console.log('bar chart data', data.data)
        
            var title = false;
            if(typeof widget.params.title != 'undefined' && widget.params.title == "true") {
                title = widget.name;
            }

            var type = 'column';
            if(typeof widget.params.type != 'undefined') {
                type = widget.params.type;
            }

            var yDecimals = true;
            if(typeof widget.params.yDecimals != 'undefined' && widget.params.yDecimals === 'false') {
                yDecimals = false;
            }

            var legend = true;
            if(typeof widget.params.legend != 'undefined' && widget.params.legend == "false") {
                legend = false;
            }

            var scrollbar = false;
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
                    width: widget.width,
                    height: widget.height,
                },
                title: {
                    text: false
                },
                subtitle: {
                    text: false
                },
                credits: {
                    enabled: false
                },
                yAxis: {
                    title: {
                        text: false,//'Holding Performance XXXX-XX-XX'
                    },
                    minorTickInterval: 'auto',
                    allowDecimals: yDecimals,
                },
                legend: {
                    enabled: legend,
                },

                exporting: {
                    enabled: true
                },

                xAxis: {
                    type: 'category',
                    categories: data.columns,
                    //type : "datetime",
                },
                series: data,
            }

            if(typeof widget.params.labels != 'undefined' && widget.params.labels == 'rotated') {
                labels = {
                    rotation: 90,
                    align: 'left',
                    style: {
                        fontSize: '8px',
                        fontFamily: 'Verdana, sans-serif'
                    },
                    formatter: function() {
                        if(this.value.length > 20) {
                            return this.value.substr(0, 20) + '...';
                        } else {
                            return this.value;
                        }
                    }
                }
                options.xAxis.labels = labels;
            }

           //console.log(widget.window.key);
            // vertical fund performance line over bar graph
            
            if(widget.window.key == 'w2') { 
            
                var year = moment().year();
                year = 2013;  // @TODO: get rid of this later
                var month = moment().month();
                var url = '/api/fundreturnmonthly/?fund=' + $('#data').data('fund_obj').id + '&fields=fund_perf&value_date__year=' + year + '&value_date__month=' + month;
                
                //$.getJSON(url, function(fund) {
                //    options.yAxis.plotLines = [{
                //        value: fund[0].fund_perf,
                //        width: 1,
                //        color: 'black',
                //        label: {
                //            text: $('#data').data('fund_obj').name + ' Performance',
                //        },
                //        zIndex: 5,
                //    }];
                    var chart = new Highcharts.Chart(options);
                    
                    $('#data').data('chart-' + div, chart);
                    $('#data').data('chart-options-' + div, options);
              // });
            } else {
                var chart = new Highcharts.Chart(options);
            }

            // save div for later
            $('#data').data('barchart-' + widget.window.key, div);
            
            // save data
            $('#data').data('chart-' + div, chart);
            
            // save options
            $('#data').data('chart-options-' + div, options);
            
            return chart;

        });



    }
  
    


    function dataTable(data, obj, widget, div) {

        var hideHeaders = false;
        var title = false;
        
        if(typeof widget.params !== 'undefined') {
        
            if(typeof widget.params.column_header !== 'undefined' && widget.params.column_header == 'false'){
                hideHeaders = true;
            }
            
            if(typeof widget.params.title !== 'undefined'){
                title = widget.params.title;
            }  
            
        }

        
        var renderTo = false;
        if(typeof div !== 'undefined'){
            renderTo = div;
        }
        
        if(typeof widget.width === 'undefined') {
            var width = (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1));
        } else {
            var width = widget.width;
        }
        
        if(typeof widget.height === 'undefined') {
            var height = (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1));
        } else {
            var height = widget.height;
        }
    

        // for nested header columns as well
        //console.log('data.columns', data.columns);
        fields = [];
        console.log('data table widget key', widget.key);
        for(i=0; i < data.columns.length; i++) {
            if(typeof data.columns[i].columns != 'undefined') {
            
               // console.log('UNDEFINED');
                
                for(x=0; x < data.columns[i].columns.length; x++) {
                    arr = {};
                    row = data.columns[i].columns[x].dataIndex;


                    if($.isNumeric(row)) {
                        arr['type'] = 'float';
                    } else {
                        arr['type'] = 'string';
                    }
                    arr['type'] = 'string';
                    arr['name'] = row
                    fields.push(arr);
                }
            } else {
                row = data.columns[i].dataIndex;
                
                if(row != 'year' && row != 'date' && row != 'client__name') {
                    
                    data.columns[i]['renderer'] = function(val) {
                    
                        format_val = val.replace('e', '');
                        
                        if(widget.window.key == 'w6') {
                            number = Ext.util.Format.currency(format_val, '&euro;');
                            if(val.search('e') !== -1) {
                                number = number + 'e';
                            }
                        } else {
                            number = val;
                        }
                        
                        if (format_val == "-1000") {
                            return '<span style="color:black;">-';
                        } else if (format_val > 0) {
                            renderer = '<span style="color: #01017D;">' + number;
                        } else if (format_val < 0) {
                            renderer = '<span style="color:#F73100;">' + number;
                        } else if (format_val == 0) {
                            return '<span style="color:black;">0.00';
                        }
                        
                        if(val != '') {
                            //renderer = ' <span style="font-weight: normal;">';
                        }
                        
                        if(widget.window.key == 'w6') {
                            return renderer +  ' </span>';
                        } else {
                            //console.log('ASDF', data.columns);
                            return renderer +  ' %</span>';
                        }
                        /*
                        if(row == 'ytd') {
                                color = 'white;';
                            } else {
                                color = '#1803A1;';
                            }
                            return '<span style="color: ' + color + '">' + val + ' <span style="font-weight: normal;">%</span></span>';
                        } else if (val < 0) {
                            return '<span style="color:red;">' + val + ' <span style="font-weight: normal;">%</span></span>';
                        }
                        return '0.00 <span style="font-weight: normal;">%</span>';
                        */
                    };
                }
                if(typeof row != 'undefined') {
                
                   // console.log('UNDEFINED2');
                    
                    arr = {};
                    if($.isNumeric(row)) {
                        arr['type'] = 'float';
                    } else {
                        arr['type'] = 'string';
                    }
                    arr['type'] = 'string';
                    arr['name'] = row
                    fields.push(arr);
                }
            }
        }

        console.log('data.columns', data.columns);
        if(typeof data.columns[1]['summaryType'] != 'undefined') {
            data.columns[0]['summaryRenderer'] = function(v, params, data){ return 'Total'};
        }

        $.each(data.rows, function(parent, row) {

            if($.isArray(row)) {
                $.each(row, function(key, value) {

                    // tastypie returns floats as strings, hence this ugly hack
                    if(value.toString().indexOf('.') != -1) {
                        //data.rows[parent][key] = parseFloat(value.toString());
                    }
                });
            } else {

                // tastypie returns floats as strings, hence this ugly hack
                if(row.toString().indexOf('.') != -1) {
                    //data.rows[parent] = parseFloat(row.toString());
                }
            }
        });
        
        if(widget.key === 'w18') {
            var sortProperty = 'date';
        } else if(widget.key === 'w12') {
            var sortProperty = 'client__name';
        } else {
            var sortProperty = 'id';
        }
        
        
        console.log('FIELDS', fields, data);

        var tableStore = Ext.create('Ext.data.Store', {
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
            sorters: [ {
                property: sortProperty,
                direction: 'ASC'
            } ],
        });
        
        if(widget.window.key == 'w12') {
    
            tableStore.filter([
                {filterFn: function(item) { return item.get("size") > 0; }}
            ]);
            Ext.create('Ext.form.Panel', {
                bodyPadding: 5,
                flex: 1,
                border: 0,
                height: 30,
                items: [{
                    xtype: 'fieldcontainer',
                    fieldLabel: 'Show Historic',
                    defaultType: 'checkboxfield',
                    items: [{
                        name: 'size',
                        inputValue: '0',
                        id: 'size_checkbox',
                        handler: function (field, value) { 
                            if(!value) {
                                tableStore.filter([
                                    {filterFn: function(item) { return item.get("size") > 0; }}
                                ]);
                            } else {
                                tableStore.clearFilter();
                            }
                        }
                    }]
                }],
                renderTo: div + 'top',
            });        
        
        }

        // for innergrids
        if(widget.type == 'data_table_sub') {
            cls = 'custom-grid-sub';
        } else {
            cls = 'custom-grid';
        }

        plugins = [{
            ptype: 'myrowexpander',
            rowBodyTpl: [
                '<div id="innergrid-' + widget.id + '-{id}">',
                '</div>'
            ]
        }];
        //selModel = {
        //    selType: 'cellmodel'
        //}

        // link to holding pages from table
        if(widget.window.key == 'w11') {

            for(i=0; i<data.columns.length; i++) {

                if(data.columns[i].dataIndex == 'name') {
                    data.columns[i].renderer = function (value, metaData, record, row, col, store, gridView) {
                        return '<a href="javascript:holdingTab(' + record.internalId + ',  \'' + value + '\');">' + value + '</a>';
                    };
                }

            }
        }

        var isClicked = new Array();
        
        var panel = Ext.create('Ext.grid.Panel', {
            title: title,
            id: div,
            cls: cls,
            columnLines: true,
            hideHeaders: hideHeaders,
            store: Ext.data.StoreManager.lookup(widget.key),
            columns: data.columns,
            width: width,
            height: height - 10,
            header: false,
            border: false,
            //enableLocking: true,
            autoScroll: true,
            //overflowY: 'scroll', // always show scrollbar
            renderTo: renderTo,
            plugins: plugins,
            //selModel: selModel, // selModel causing empty row at end of grid
            iconCls: 'icon-grid',
            forceFit: true,
            layout:'fit',
            //features: [{
            //    ftype: 'summary'
            //}],

            listeners: {
                cellclick: function(gridView,htmlElement,columnIndex,dataRecord) {

                    var id = dataRecord.data.id;
                    var year = dataRecord.data.year + '';

                    var month = columnIndex - 1;
                 
                    // first column
                    if(columnIndex == 1) {
                        if(widget.window.key == 'w1' || widget.window.key == 'w1b') {
                        
                            if(year.substr(0, 5) !== 'bench') {

                                $.getJSON("api/fundreturnmonthly/?align=center&data_type=year&date=value_date&extra_fields=bench_ytd&fund=" + obj.fund.id + "&fields=estimation&value=bench_perf&value_date__year=" + year, function(w1) {
                                    
                                    tableStore.load();
                                    
                                    if(jQuery.inArray(id, isClicked) !== -1) {
                                    
                                        isClicked.splice(isClicked.indexOf(id), 1);
                                        for(i=0; i<data.rows.length; i++) {
                                            if(data.rows[i]['id'] === (id + 1)) {
                                                data.rows.splice(i, 1);
                                            }
                                        }
                                    } else {
                                        w1.rows[0]['id'] = id + 1;
                                        w1.rows[0]['year'] = 'Bench';
                                        w1.rows[0]['ytd'] = w1.rows[0]['bench_ytd'];
                                        console.log('w1', w1.rows[0]);
                                        data.rows.push(w1.rows[0]);
                                        isClicked.push(id);
                                    }
                                    tableStore.loadData(data.rows);
                                    tableStore.sync();
                                });
                            }
                        }
                    } else {
                        if(widget.window.key == 'w1b' && columnIndex > 0 && columnIndex < 14) {
                            monthTable(year, month);
                        }
                    }
                            

                    obj.page = $('#data').data('page_id');
                    obj.grid = $('#data').data('grid' + obj.page);
                    extra_params = {
                        year: year,
                    }
                    obj.year = year // for refreshable pie chart name
                    obj.month = 1;
                    month = columnIndex - 1;

                }
            }

        });


        panel.view.on('expandBody', function (rowNode, record, expandRow, eOpts) {

            var id = record.get('id');




            if(widget.window.key == 'w11') {

                var fields = 'trade_date,settlement_date,no_of_units,trade_price_euro,fx_euro,trade_price_base,base_nav';
                //var fields = 'trade_date,settlement_date,buy_sell,no_of_units,trade_price_base_base,fx_to_euro,trade_price_base,base_nav';
                $.getJSON("/api/trade/?holding=" + id + '&column_width=150,80&fields=' + fields, function(w11) {

                    displayInnerGrid(widget, w11,id);

                    widget.holding = record.get('id');
                    widget.fund = obj.fund.id;
                    lineBarChart(widget);
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
                $.getJSON('/api/holding-history/?holding=' + id + '&value_date__year=' + year + '&date_type=m&fields=value_date,drawdown,various,distribution,expense,valuation,total_value&total=true&column_width=80,50', function(widget_data) {
                    displayInnerGrid(widget, widget_data, id, false, 150);
                });
            }
            if(widget.window.key == 'w12') {
                var fields = '&shares,nav_per_share,nav,buy_sell,value_date';
                $.getJSON('/api/clienttransaction/?fund=' + fund + '&client=' + id + '&data_type=table' + fields, function(widget_data) {
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
        //Ext.getCmp('some_id').hide();
        return panel;
    
    }

    function refreshWindow(window_key, obj, extra_params) {


        $.getJSON('/api/widgets/?window__key=' + window_key, function(widget_data) {


            for(x=0; x<widget_data.length; x++) {

                var window_id = 'page_' + obj.page + '_win_' + widget_data[x].window.id;
                var widget_id = window_id + '_widget_' + widget_data[x].id;



                var title = widget_data[x].window.name;

                year = extra_params.year;
                week = 1; // fill this dynamic later

                title = title.replace('FUND_NAME', $('#data').data('fund_obj').name);
                title = title.replace('YEAR', year);
                title = title.replace('WEEK', week);

                win = Ext.getCmp(window_id);

                if(typeof win != 'undefined') {
                    win.setTitle(title);
                    //return;
                } else {
                   //console.log(window_id);
                }

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



    function refreshWindow(window_key, obj, extra_params) {


        $.getJSON('/api/widgets/?window__key=' + window_key, function(widget_data) {


            for(x=0; x<widget_data.length; x++) {

                var window_id = 'page_' + obj.page + '_win_' + widget_data[x].window.id;
                var widget_id = window_id + '_widget_' + widget_data[x].id;



                var title = widget_data[x].window.name;

                year = extra_params.year;
                week = 1; // fill this dynamic later

                title = title.replace('FUND_NAME', $('#data').data('fund_obj').name);
                title = title.replace('YEAR', year);
                title = title.replace('WEEK', week);

                win = Ext.getCmp(window_id);

                if(typeof win != 'undefined') {
                    win.setTitle(title);
                    //return;
                } else {
                   //console.log(window_id);
                }

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
                },
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


               //console.log('outcommented');

                /*

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


                */


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
                    type: 'pie',
                    marginTop: 0,
                    marginLeft: 30,
                    marginRight: 30,
                    //width: (120 * widget.size_x) + (10 * widget.size_x) + (10 * (widget.size_x - 1)),
                    //height: (120 * widget.size_y) + (10 * widget.size_y) + (10 * (widget.size_y - 1)),
                    // @TODO: Find out why widget is getting overwritten
                    height: (120 * 2) + (10 * 2) + (10 * (2 - 1)),
                    width:  (120 * 2) + (10 * 2) + (10 * (2 - 1)),
                },
                title: {
                    text: widget.name,
                },
                series: data.objects
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

                                    widgetWindow('', data.key, page, data.name, data.size_x, data.size_y);

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

    function setFund(id) {
         $.ajax({
            type: "GET",
            url: '/api/fund/' + id + '?fields=name,benchpeer__name,benchpeer__id,sec_bench__name,sec_bench__id',//,benchpeer__name',//,classification__id',
            success: function(data) {
            
                var fund = {
                    id: data.id,
                    name: data.name,
                    benchpeer: {
                        id: data.benchpeer__id,
                        name: data.benchpeer__name,
                    },
                    sec_bench: {
                        id: data.sec_bench__id,
                        name: data.sec_bench__name,
                    },
                };
                console.log('SETTING FUND');
                $('#data').data("fund_obj", fund);
            }
        });
    }

    function setClientName(id) {
         $.ajax({
            type: "GET",
            url: '/api/client/' + id + '?fields=first_name,last_name',
            success: function(data) {
                $('#data').data("client_name", data.last_name + ', ' + data.first_name);
            }
        });
    }

    function popup(section, page, width, height) {
        if(typeof width == 'undefined') {
            width = 900;
        }
        if(typeof height == 'undefined') {
            height = 700;
        }        
        window.open("/admin/" + section + "/" + page + "/", "", "fullscreen=no,toolbar=no,status=no,menubar=no,scrollbars=yes,resizable=yes,directories=yes,location=no,width="+width+",height="+height+",left=400,top=100");
    }

    function viewPort() {

         //$.ajax({
         //   type: "GET",
         //   url: '/api/menu/',
         //   success: function(data) {

            $.getJSON('/api/menu/', function(data) {

                /*
                $.getJSON('/api/client/?fields=first_name,last_name&order_by=last_name', function(clients) {

                   //console.log(clients);
                    client_list = [
                        {
                            "expanded": false,
                            "children": [],
                            //"fund": 0,
                            "id": 'client_cat1',
                            "name": "Clients A - E",
                            //"page": 0
                        },
                        {
                            "expanded": false,
                            "children": [],
                            //"fund": 0,
                            "id": 'client_cat2',
                            "name": "Clients F - L",
                            //"page": 0
                        },
                        {
                            "expanded": false,
                            "children": [],
                            //"fund": 0,
                            "id": 'client_cat3',
                            "name": "Clients M - R",
                            //"page": 0
                        },
                        {
                            "expanded": false,
                            "children": [],
                            //"fund": 0,
                            "id": 'client_cat4',
                            "name": "Clients S - U",
                            //"page": 0
                        },
                        {
                            "expanded": false,
                            "children": [],
                            //"fund": 0,
                            "id": 'client_cat5',
                            "name": "Clients V - Z",
                            //"page": 0
                        }
                    ]
                    $.each(clients.rows, function(key, client) {
                        //if(client.last_name.charCodeAt(0)
                        //console.log(client);
                        var ascii = client.last_name.toLowerCase().charCodeAt(0);

                        var child = {
                            "expanded": false,
                            "client": client.id,
                            "id": ('client' + client.id).valueOf(),
                            "leaf": true,
                            "name": client.last_name + ", " + client.first_name,
                            "page": 10
                        }

                        if(ascii < 102) { // a-e
                            var index = 0;
                        } else if(ascii < 109) { // f-l
                            var index = 1;
                        } else if(ascii < 115) { // m-r
                            var index = 2;
                        } else if(ascii < 122) { // s-u
                            var index = 3;
                        } else { // v-z
                            var index = 4;
                        }

                        client_list[index].children.push(child);
                    });

                    $.each(data, function(key, menu) {
                        if(menu.id == 21) { // clients
                            data[key].children = client_list;
                        }
                    });

                   */

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

                                }
                            },
                            dblclick: function() {
                                return false;
                            },
                            itemclick: {
                                fn: function(view, record, item, index, event, opts) {
                                
                                    var asdf = record;

                                   console.log('ITEM CLICKED');
                                   //console.log(record);

                                    // Expand & collapse node on single click
                                    if(record.isExpanded()) {
                                        record.collapse();
                                    } else {
                                        record.expand();
                                    }

                                    //console.log('record.raw', record.raw);
                                    if(typeof record.raw.fund !== 'undefined' && record.raw.fund !== null && record.raw.fund !== 0) {
                                        $('#data').data('fund', record.raw.fund);
                                        
                                        // for some reason record.raw.fund gets overwritten with obj.fund
                                        // this really ugly hack solves it
                                        if(typeof record.raw.fund === 'object') {
                                            var fundId = record.raw.id;
                                        } else {
                                            var fundId = record.raw.fund;
                                        }
                                        setFund(fundId);
                                    }
                                    
                                    if(typeof record.raw.benchpeer != 'undefined') {
                                        $('#data').data("benchpeer", record.raw.benchpeer);
                                    }
                                    
                                    //console.log(record.raw);
                                    if(typeof record.raw.client != 'undefined') {
                                        $('#data').data('client', record.raw.client);
                                        setClientName(record.raw.client);
                                    }

                                    if(record.raw.page !== null) {

                                        if (typeof record.raw.page === 'number') {
                                            record.raw.page = record.raw.page;
                                        } else if (typeof record.raw.page === 'object') {
                                            record.raw.page = record.raw.page.id;
                                        } else {
                                            try {
                                                var str = record.raw.page.toString();
                                            } catch(e) {
                                                var str = record.raw.page;
                                            }
                                            record.raw.page = str.replace(/\D/g, '');

                                        }
                                    }

                                    page_id = record.raw.id;

                                    if(page_id == 222) {
                                        popup('v2', 'fund', 1300, 800);
                                    } else if(page_id == 97) {
                                        popup('client', 'subscriptionredemption');
                                    } else if(page_id == 98) {
                                        popup('v2', 'custodian');
                                    } else if(page_id == 99) {
                                        popup('v2', 'auditor');
                                    } else if(page_id == 100) {
                                        popup('v2', 'administrator');
                                    } else if(page_id == 101) {
                                        popup('fund', 'classification');
                                    } else if(page_id == 219) {
                                        popup('fund', 'returnestimate', 1000, 800);
                                    } else if(page_id == 220) {
                                        popup('v2', 'fundstyle');
                                    } else if(page_id == 221) {
                                        popup('v2', 'alpheusgroup');
                                    } else if(page_id == 102) {
                                        popup('app', 'fundperformanceestimate');
                                    } else if(page_id == 103) {
                                        popup('holding', 'holding');
                                    } else if(page_id == 112) {
                                        popup('holding', 'fund');
                                    } else if(page_id == 105) {
                                        popup('holding', 'fundequity');
                                    } else if(page_id == 106) {
                                        popup('holding', 'fundoption');
                                    } else if(page_id == 107) {
                                        popup('holding', 'fundfixedincome');
                                    } else if(page_id == 108) {
                                        popup('holding', 'fundsidepocket');
                                    } else if(page_id == 109) {
                                        popup('holding', 'fundprivateequity');
                                    } else if(page_id == 114) {
                                        popup('holding', 'clientfund');
                                    } else if(page_id == 115) {
                                        popup('holding', 'clientequity');
                                    } else if(page_id == 116) {
                                        popup('holding', 'clientoption');
                                    } else if(page_id == 117) {
                                        popup('holding', 'clientfixedincome');
                                    } else if(page_id == 118) {
                                        popup('holding', 'clientsidepocket');
                                    } else if(page_id == 119) {
                                        popup('holding', 'clientprivateequity');

                                    } else if(page_id == 110) {
                                        popup('holding', 'category');
                                    } else if(page_id == 111) {
                                        popup('app', 'holdingperformanceestimate');
                                    } else if(page_id == 122) {
                                        popup('trade', 'fund');
                                    } else if(page_id == 123) {
                                        popup('trade', 'fundequity');
                                    } else if(page_id == 124) {
                                        popup('trade', 'fundoption');
                                    } else if(page_id == 125) {
                                        popup('trade', 'fundfixedincome');
                                    } else if(page_id == 126) {
                                        popup('trade', 'fundsidepocket');
                                    } else if(page_id == 127) {
                                        popup('trade', 'fundprivateequity');
                                    } else if(page_id == 128) {
                                        popup('trade', 'clientfund');
                                    } else if(page_id == 129) {
                                        popup('trade', 'clientequity');
                                    } else if(page_id == 130) {
                                        popup('trade', 'clientoption');
                                    } else if(page_id == 131) {
                                        popup('trade', 'clientfixedincome');
                                    } else if(page_id == 132) {
                                        popup('trade', 'clientsidepocket');
                                    } else if(page_id == 133) {
                                        popup('trade', 'clientprivateequity');
                                    } else if(page_id == 134) {
                                        popup('app', 'counterparty');
                                    } else if(page_id == 135) {
                                        popup('app', 'counterpartytrader');
                                    } else if(page_id == 136) {
                                        popup('app', 'benchmark');
                                    } else if(page_id == 137) {
                                        popup('app', 'benchmarkperformance');
                                    } else if(page_id == 138) {
                                        popup('app', 'peer');
                                    } else if(page_id == 139) {
                                        popup('app', 'peerperformance');
                                    } else if(page_id == 140) {
                                        popup('client', 'client');
                                    } else if(page_id == 141) {
                                        popup('v2', 'country');
                                    } else if(page_id == 142) {
                                        popup('v2', 'currency');
                                    } else if(page_id == 143) {
                                        popup('fund', 'fxhedge');
                                    } else if(page_id == 144) {
                                        popup('fund', 'deposit');
                                    } else if(page_id == 145) {
                                        popup('auth', 'user');
                                    } else if(page_id == 147) {
                                        popup('auth', 'group');
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
                        //draggable: true,
                        title: 'Navigation',
                        width: 150,
                        border: 0,
                        split: true, // draggable
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

            //});
        });
    }


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
















Ext.require(["Ext.util.Cookies", "Ext.Ajax"], function(){
    // Add csrf token to every ajax request
    var token = Ext.util.Cookies.get('csrftoken');
    if(!token){
        Ext.Error.raise("Missing csrftoken cookie");
    } else {
        Ext.Ajax.defaultHeaders = Ext.apply(Ext.Ajax.defaultHeaders || {}, {
            'X-CSRFToken': token
        });
    }
});





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

        //win.show();
        var formPanel = Ext.create('Ext.form.Panel', {
            frame: true,
            title: 'Login',
            width: 340,
            bodyPadding: 5,
            renderTo: Ext.getBody(),
            items: [{
                xtype: 'textfield',
                name: 'username',
                fieldLabel: 'Username',
            },{
                xtype: 'textfield',
                inputType: 'password',
                name: 'password',
                fieldLabel: 'Password',
            }],

            // Reset and Submit buttons
            buttons: [{
                text: 'Submit',
                handler: function() {
                    var form = formPanel.getForm();
                    form.submit({
                        url: '/api/user/login/',
                        success: function(form, action) {
                        
                            $('#data').data('userId', action.result.user_id);
                            
                            formPanel.hide();

                            setGlobal('fund');
                            setGlobal('page');

                            viewPort();

                            page = new Object();
                            page.page = 1;
                            initGrid(page);
                        },
                        failure: function(form, action) {
                            Ext.Msg.alert('Login failed!', 'Wrong user name or passsword');
                            form.reset();
                        }
                    });
                }
            }],
        });

        formPanel.center();
        formPanel.show();




    }
});



});
