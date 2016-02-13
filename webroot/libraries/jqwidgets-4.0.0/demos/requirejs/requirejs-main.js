require.config({
    paths: {
        "jQuery": "../../scripts/jquery-1.11.1.min",
        "jqxcore": "../../jqwidgets/jqxcore",
        "jqxbuttons": "../../jqwidgets/jqxbuttons",
        "jqxpanel": "../../jqwidgets/jqxpanel",
        "jqxscrollbar": "../../jqwidgets/jqxscrollbar",
        "jqxtree": "../../jqwidgets/jqxtree",
        "demos": "../../scripts/demos"
    },
    shim: {
        "demos": {
            export: "$",
            deps: ["jQuery"]
        },
        "jqxcore": {
            export: "$",
            deps: ['jQuery']
        },
        "jqxbuttons": {
            export: "$",
            deps: ['jQuery', "jqxcore"]
        },
        "jqxpanel": {
            export: "$",
            deps: ['jQuery', "jqxcore"]
        },
        "jqxscrollbar": {
            export: "$",
            deps: ['jQuery', "jqxcore"]
        },
        "jqxtree": {
            export: "$",
            deps: ['jQuery', "jqxcore"]
        }
    }
});
require(["requirejs-app"], function (App) {
    App.initialize();
});