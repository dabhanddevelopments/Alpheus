
Ext.require([
    'Ext.tree.*',
    'Ext.data.*',
    'Ext.menu.*',
    'Ext.window.MessageBox'
]);


Ext.onReady(function() {


    //$('<div id="main" class="gridster"></div>').appendTo('body');
    $('<div id="data"></div>').appendTo('body');

    function initPage(id) {

        // All pages used on the site. This is loaded on start.
        var pages = $('#data').data('page');

        // No need to reload the page if users clicks on a link 
        // to a page they are already on
        //if($('#data').data('active-panel') == id) {
        //    return
        //}

        for(i=0; i<pages.length; i++) {

            if(pages[i].id == id) {
    
                el = 'main' + id;

                // If a page has children, it means it's the first
                // tab in a collection of tabs
                if(pages[i].children !== undefined) {

                    var panel = panelTab('tab_panel' + id);

                    switchPanel(panel, el);
                    appendTabs(pages[i]);

                } else {

                    var panel = panelStandard(el);
                    switchPanel(panel, el);

                }
                    
                // stops all widgets to auto reload/refresh
                //clearAllIntervals();

                initGrid(id);
            }
        }
    }


    // dynamically adds the tabs to the tab panel from the supplied pages
    function appendTabs(tabs) {

        var panel = Ext.getCmp('panel-tab');

        panel.removeAll();

        //$('<div id="main' + tabs.id + '" class="gridster"></div>').appendTo('#main');

        // The root is the first tab
        panel.add({
            id: tabs.id,
            title: tabs.title,
            contentEl: 'main' + tabs.id,
            listeners: {
                activate: function(tab){
                    initGrid(tab.id);
                }
            },
        }); 

        for(x=0; x<tabs.children.length; x++) {

            id = tabs.children[x].id;

            //$('<div id="main' + id + '" class="gridster"></div>').appendTo('#main');

            panel.add({
                title: tabs.children[x].title,
                id: id,
                contentEl: 'main' + id,
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

        if(active === undefined) {
            active = 'panel-home';
            //$('<div id="' + el + '"></div>').appendTo('body');
        }

        //var ws = Ext.getCmp(active);
        //ws.setVisible(false);
        //ws.doLayout();  

        //var ws = Ext.getCmp(el);
        //ws.setVisible(true);
        //ws.doLayout();  


        var ws = Ext.getCmp(active);

        try {
            //console.log('removing: ' + active);
            ws.remove(active);
        } catch(err) {
            //console.log("Failed to remove panel");
            //console.log(err);
        }

        //$('#' + el).remove();

        // The 'main' DOM element gets destroyed on remove() with autoDestroy
        // set to true, so we have to re-add it
        ////console.log('CREATING dOM: ' + el);
        //    $('<div id="' + el + '"></div>').appendTo('body');


        try {
            ws.add(panel);
            //console.log('panel added');
        } catch(err) {
            //console.log("Failed to add panel");
            //console.log(err);
        }
  
        ws.doLayout();  

        // Save the panel so we know which one to destroy next time
        $('#data').data('active-panel', panel.id);

    }

    function initGrid(page) {
        
//console.log('initiating grid');
//console.log(page);

        $.ajax({
            type: "GET",
            url: '/api/pagewidget/?page=' + page,
            success: function(data) {

                // if we have a grid for this page, it means it's already 
                // loaded and we do not need to fetch it again
                if($('#data').data('grid' + page) !== undefined) {
////console.log('skipping gridster');
                    return;
                }


                var grid = $("#main" + page).gridster({
                    widget_margins: [10, 10],
                    widget_base_dimensions: [140, 140],
                    max_size_x: 10,
                    max_size_y: 10,
                    draggable: {
                        stop: function(event, ui){ 
                            $.cookie("grid-data", JSON.stringify(grid.serialize()));
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
                            //id: $($w).attr('data-id'),
                        } 
                    }
                }).data('gridster');

//console.log('initiated gridster');
                grid.disable();

                $('#data').data('grid' + page, grid);
                $('#data').data('grid_data' + page, data);
                $('#data').data('page_id', page);

    //console.log('starting loop');
                for(i=0; i<data.length; i++) {

                    var row = data[i];
    //console.log('CREATING ');
                    var widget = '<div id="' + row.widget.key + '" class="layout_block"></div>';

                    grid.add_widget(widget, row.size_x, row.size_y, row.col, row.row);

                    createWidget(row.widget, page);

                    widgetWindow(row.widget.key, row.widget.name, row.size_x, row.size_y, row.id);
                }       
//console.log('finishing loop');
            }

        });
    }

    function widgetWindow(key, title, size_x, size_y, grid_id) {

//console.log('creating widget window');
        Ext.create('Ext.window.Window', {
            title: title,
            // there's gotta be a better way to do this
            height: (140 * size_y) + (10 * size_y) + (10 * (size_y - 1)) - 10,
            width:  (140 * size_x) + (10 * size_x) + (10 * (size_x - 1)) - 10,
            layout: 'auto',
            floatable: false,
            draggable: false,
            closable: false, 
            contentEl: "widget" + key,
            x: 0,
            y: 0,
            renderTo: key,
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
                                var grid = $('#data').data('grid')
                                grid.remove_widget( $('#widget' + key) );
                                removeWidget(grid_id);
                            }
                         }
                    });
               }
            }],
        }).show();
    }

    function removeWidget(id) {
         $.ajax({
            type: "DELETE",
            url: "/api/pagewidget/" + id + '/',
            success: function() {
                //console.log('removed widget');
            },
            error: function(err) {
                //console.log('problem removing widget');
                //console.log(err);
            },
        });          
    }

    function createWidget(widget) {

//console.log('creating widget');
//console.log(widget);

        $('<div id="widget' + widget.key + '"></div>').appendTo('body');

        try {
            $.getJSON('/api/widget/' + widget.key + '/', function(data) {
                switch(widget.type) {
                  case 'data_table': dataTable(widget, data); break;
                  case 'graph':      graph(widget, data); break;
                  case 'pie_chart':  pieChart(widget, data); break;
                  case 'bar_chart':  barChart(widget, data); break;
                }

                // enables ajax auto reload/refresh for this widget
                //enableReload(widget.id);
            })
        } catch (err) {
            //console.log(err);
        }
    }

    function graph(widget, data) {

////console.log('creating graph');
        try {
            $.jqplot("widget" + widget.key, data, 
                { 
                  axes:{yaxis:{min:-10, max:240}}, 
                  series:[{color:'#5FAB78'}]
            });
        } catch (err) {
            //console.log(err);
        }
    }

    function barChart(widget, data) {

////console.log('creating bar chart');
        try {
            var plot1 = $.jqplot("widget" + widget.key, data, {
                
                series:[{renderer:$.jqplot.BarRenderer}],
                axesDefaults: {
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
                    tickOptions: {
                      angle: -30,
                      fontSize: '10pt'
                    }
                },
                axes: {
                  xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                  }
                }
            });
        } catch (err) {
            //console.log(err);
        }


    }

    function dataTable(widget, data) {

////console.log('creating datatable');
////console.log(data);
        try {

            var table = Ext.create('Ext.data.Store', {
                fields:['name', 'email', 'phone'],
                autoLoad: true,
                proxy: {
                    type: 'ajax',
                    url: '/api/widget/' + widget.key + '/',
                    reader: {
                        type: 'json',
                        root: 'items',
                    }
                },
            });

            Ext.create('Ext.grid.Panel', {
                store: table,
                columns: [
                    { text: 'Name',  dataIndex: 'name' },
                    { text: 'Email', dataIndex: 'email', flex: 1 },
                    { text: 'Phone', dataIndex: 'phone' }
                ],
                height: 290,
                width: 450,
                header: false,
                border: false,
                enableLocking: true,
                autoScroll: true,
                renderTo: "widget" + widget.key,

            });

        } catch (err) {
            //console.log(err);
        }

    }

    function pieChart(widget, data) {

////console.log('creating pie chart');
////console.log(data);

        var plot1 = jQuery.jqplot('widget' + widget.key, data, 
        { 
            seriesDefaults: {
                renderer: jQuery.jqplot.PieRenderer, 
                rendererOptions: {
                    showDataLabels: true
                }
            }, 
            legend: { show:true, location: 'e' }
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

                                    html = '<div class="widget_desc"><img src="{{ STATIC_URL }}widget-images/' + data.key + '.png"></img><h1>' + data.name + '</h1>' + data.desc + '</div>'
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

                            var div = '<div id="' + data.key + '" class="layout_block"></div>';
                            var grid = $('#data').data('grid' + page);

                            grid.add_widget(div, data.size_x, data.size_y, 1, 1);

                            addGrid(data);

                            createWidget(data);

                            widgetWindow(data.key, data.name, data.size_x, data.size_y);

                            win.close();
		                }
                    }],
                }).show();
                // So the window dimensions stay 100% when the window is resized
                Ext.EventManager.onWindowResize(overviewGrid.doLayout, win); 

            }, 
            error: function(data) {
                  //console.log('error');      
            }
        });

    }

    function addGrid(widget) {

        page = $('#data').data('page_id');

        grid = {};
        grid.widget = widget.resource_uri;
        grid.page = "/api/page/" + page + "/";
        grid.row = 1;
        grid.col = 1;     
        grid.size_y = widget.size_y;
        grid.size_x = widget.size_x;

//console.log('adding grid');
//console.log(grid);

        $.ajax({
            type: "POST",
            //headers: {'X-HTTP-Method-Override': 'POST'},
            url: "/api/pagewidget/",
            data: JSON.stringify(grid),
            success: function() {
                //console.log('success');
            },
            error: function(err) {
                //console.log('error');
                //console.log(err);
            },
            dataType: "json",
            contentType: "application/json",
            //processData: false
        });
    }





    function panelStandard(el) {
////console.log('creating standard panel with el: ' + el);
        return Ext.create('Ext.panel.Panel', {
            stateId: 'asdf',
            region: 'center', 
            id: 'panel-home', 
            contentEl: el, 
            //autoDestroy: true,
            autoScroll: true,
        });
    }

    function panelTab(el) {
////console.log('creating tab panel with el: ' + el);
        return Ext.create('Ext.tab.Panel', {
            region: 'center',
            contentEl: el, 
            id: 'panel-tab', 
            //autoDestroy: true,
            autoScroll: true,
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
        items: [{
	        text: 'Add Widget',
            id: 'add_widget',
        },{
	        text: 'Settings',
            id: 'settings',
        }, {
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

        Ext.util.CSS.swapStyleSheet("theme", "static/" + theme);

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
                    store: store,
                    rootVisible: false,
                    preventHeader: true,
                    border: false,
                    autoScroll: true,
                    useArrows: true,
                    height: 1000,
                    listeners: {
                        itemclick: {
                            fn: function(view, record, item, index, event) {


                                // Expand & collapse node on single click
                                if(record.isExpanded()) {
                                    record.collapse();
                                } else {
                                    record.expand();
                                }

                                if(record.raw.page !== null) {
                                    //initPage(record.raw.page.replace(/\D/g, ''));
                                }

                                nodeId = record.data.id;
                                checked = record.data.checked;
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

                Ext.create('Ext.container.Viewport', {
                    layout: 'border',
                    id: 'viewport', 
                    items: [panel_west, panelStandard('main1')]
                });

                //$('#data').data('active-panel', 'panel-home');
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
                    },
                    success:function() { 
                        win.close();
                    	viewPort();
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

// only called once on load
function initDOM() {

    $.ajax({
        type: "GET",
        url: '/api/page/',
        success: function(page) {

            $('#data').data('page', page);

            for(i=0; i<page.length; i++) {

                //@TODO: change this to native to make it faster

                // page elements
                $('<div id="main' + page[i].id + '" class="gridster"></div>').appendTo('body');
////console.log('creating: main' + page[i].id);

                // the children are tab pages
                if(page[i].children !== undefined) {
                 
                    // the tab panel element
                    $('<div id="tab_panel' + page[i].id + '"></div>').appendTo('body');
////console.log('creating: tab_panel' + page[i].id);

                    for(x=0; x<page[i].children.length; x++) {

                        // element for this tab
                        $('<div id="main' + page[i].children[x].id + '" class="gridster"></div>').appendTo('#tab_panel' + page[i].id);
////console.log('creating tab: main' + page[i].children[x].id);

                    }
                }
            }
        }
    });
}

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
        setGlobal('fund');
        //setGlobal('page');
        initDOM();

        viewPort();

        //$('<div id="main1" class="gridster"></div>').appendTo('body');
        initGrid(1);

    },
    error: function() {
        win.show();
    }
});


    
});
