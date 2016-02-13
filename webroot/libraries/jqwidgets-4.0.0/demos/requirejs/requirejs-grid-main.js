require.config({
    paths: {
        "jquery": "../../scripts/jquery-1.11.1.min",
        "jqxcore": "../../jqwidgets/jqxcore",
        "jqxdata": "../../jqwidgets/jqxdata",
        "jqxdata.export": "../../jqwidgets/jqxdata.export",
        "jqxgrid": "../../jqwidgets/jqxgrid",
        "jqxgrid.columnsresize": "../../jqwidgets/jqxgrid.columnsresize",
        "jqxgrid.edit": "../../jqwidgets/jqxgrid.edit",
        "jqxgrid.export": "../../jqwidgets/jqxgrid.export",
        "jqxgrid.selection": "../../jqwidgets/jqxgrid.selection",
        "jqxbuttons": "../../jqwidgets/jqxbuttons",
        "jqxscrollbar": "../../jqwidgets/jqxscrollbar",
        "jqxmenu": "../../jqwidgets/jqxmenu",
         "demos": "../../scripts/demos"
    },
    shim: {
        "demos": {
            export: "$",
            deps: ["jquery"]
        },
        "jqxcore": {
            export: "$",
            deps: ["jquery"]
        },
        "jqxdata": {
            export: "$",
            deps: ["jquery", "jqxcore"]
        },
        "jqxdata.export": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxdata"]
        },
        "jqxgrid": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxdata"]
        },
        "jqxgrid.columnsresize": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        },
        "jqxgrid.edit": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        },
        "jqxgrid.export": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxdata.export", "jqxgrid"]
        },
        "jqxgrid.selection": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        },
        "jqxbuttons": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        },
        "jqxscrollbar": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        },
        "jqxmenu": {
            export: "$",
            deps: ["jquery", "jqxcore", "jqxgrid"]
        }
    }
});
require(["requirejs-grid-app"], function (App) {
    App.initialize();
});