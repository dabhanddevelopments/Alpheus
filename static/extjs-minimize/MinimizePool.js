/**
 * The author disclaims copyright to this source code. In place of
 * a legal notice, here is a blessing:
 *
 * May you do good and not evil.
 * May you find forgiveness for yourself and forgive others.
 * May you share freely, never taking more than you give.
 */

Ext.define('Ext.ux.plugin.minimize.MinimizePool', {
    singleton: true,
    minimizePanel: null,
    toggleMode: null,
    _windows: new Ext.util.MixedCollection()
});
