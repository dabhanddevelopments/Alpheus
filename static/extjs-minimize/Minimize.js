/**
 * The author disclaims copyright to this source code. In place of
 * a legal notice, here is a blessing:
 *
 * May you do good and not evil.
 * May you find forgiveness for yourself and forgive others.
 * May you share freely, never taking more than you give.
 */

Ext.define('Ext.ux.plugin.minimize.Minimize', {
    extend: 'Ext.AbstractPlugin',
    alias: 'plugin.Minimize',
    requires: ['Ext.ux.plugin.minimize.MinimizePool'],
    
    init: function(window){
        //TODO verificar se é window
        window.minimizable = true;
        window.minimized = false;

        Ext.ux.plugin.minimize.MinimizePool._windows.add(window);
        
        if(Ext.ux.plugin.minimize.MinimizePool.toggleMode == 'toggle'){
            var title = window.minimizedTitle || window.title,
                minimizePanel = Ext.ux.plugin.minimize.MinimizePool.minimizePanel;

            var buttonConfig = {
                window: window,
                text: title,
                enableToggle: true,
                pressed: true,
                toggleHandler: this.toggleHandler
            };
            
            button = this.addMinimizedButton(buttonConfig);

            window.on('minimize', this.toggleMinimizeHandler, this, {button: button});
            window.on('beforeclose', this.closeWindow, this, {button: button});
            window.on('titlechange', this.changeTitle, this, {button: button});
        }
        else if(Ext.ux.plugin.minimize.MinimizePool.toggleMode == 'hide'){
            window.on('minimize', this.hideMinimizeHandler, this);
            window.on('beforeclose', this.closeWindow, this);
        }
    },

    changeTitle: function(window, newTitle, oldTitle, opts){
        if(!window.minimizedTitle){
            var button = opts.button;
            button.setText(newTitle);
        }
    },
    
    addMinimizedButton: function(config){
        var minimizePanel = Ext.ux.plugin.minimize.MinimizePool.minimizePanel,
            pos = minimizePanel.items.length - 2;

        for(var attrname in Ext.ux.plugin.minimize.MinimizePool.buttonConfig){
            config[attrname] = Ext.ux.plugin.minimize.MinimizePool.buttonConfig[attrname]; 
        }

        var button = Ext.create('Ext.button.Button', config);
        minimizePanel.insert(pos, button);

        return button;
    },
    
    hideMinimizeHandler: function(window){
        var title = window.minimizedTitle || window.title;

        var buttonConfig = {
            window: window,
            text: title,
            handler: this.showHandler
        };

        this.addMinimizedButton(buttonConfig);
        window.minimized = true;
        window.hide();
    },
    
    closeWindow: function(window, opts){
        var button = opts.button;
        if(button){
            button.destroy();
        }
        Ext.ux.plugin.minimize.MinimizePool._windows.removeAtKey(window.id);
    },
    
    toggleMinimizeHandler: function(window, opts){
        var button = opts.button;
        button.toggle(false);
    },
    
    showHandler: function(){
        this.window.minimized = false;
        this.window.show();
        this.destroy();
    },
    
    toggleHandler: function(button, state){
        //TODO animation
        this.window.minimized = !state;
        if(state){
            this.window.show();
        } else {
            this.window.hide();
        }
    }
});
