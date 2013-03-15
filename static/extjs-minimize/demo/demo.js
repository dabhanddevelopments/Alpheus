Ext.onReady(function(){
    vp = Ext.create('Ext.container.Viewport', {
        layout: 'border',
        renderTo: Ext.getBody(),
        items: [
            {
                xtype: 'panel',
                region: 'center',
                items: [
                    {
                        xtype: 'button',
                        text: 'criar',
                        handler: function(){
                            w = Ext.create('Ext.window.Window', {
                                minimizable: true,
                                height: 100,
                                width: 100,
                                title: 'Window',
                                minimizedTitle: 'Mini',
                                plugins: ['Minimize']
                            });
                            w.show();
                        }
                    }
                ]
            },
            {
                xtype: 'minimizebar',
                itemId: 'mp',
                region: 'south',
                toggleMode: 'hide'
            }
        ]
    });
    
    console.log('fim');
});
