define(["jquery", "demos", "jqxcore", "jqxdata", "jqxdata.export", "jqxgrid", "jqxgrid.columnsresize", "jqxgrid.edit", "jqxgrid.export", "jqxgrid.selection", "jqxbuttons", "jqxscrollbar", "jqxmenu"], function () {
    var initialize = function () {
        $(document).ready(function () {
            // renderer for grid cells.
            var numberrenderer = function (row, column, value) {
                return '<div style="text-align: center; margin-top: 5px;">' + (1 + value) + '</div>';
            }
            // create Grid datafields and columns arrays.
            var datafields = [];
            var columns = [];
            for (var i = 0; i < 26; i++) {
                var text = String.fromCharCode(65 + i);
                if (i == 0) {
                    var cssclass = 'jqx-widget-header';
                    columns[columns.length] = { pinned: true, exportable: false, text: "", columntype: 'number', cellclassname: cssclass, cellsrenderer: numberrenderer };
                }
                datafields[datafields.length] = { name: text };
                columns[columns.length] = { text: text, datafield: text, width: 60, align: 'center' };
            }
            var source =
            {
                unboundmode: true,
                totalrecords: 100,
                datafields: datafields,
                updaterow: function (rowid, rowdata) {
                    // synchronize with the server - send update command   
                }
            };
            var dataAdapter = new $.jqx.dataAdapter(source);
            // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {
                width: 670,
                source: dataAdapter,
                editable: true,
                columnsresize: true,
                selectionmode: 'multiplecellsadvanced',
                columns: columns
            });
            $("#excelExport").jqxButton();
            $("#excelExport").click(function () {
                $("#jqxgrid").jqxGrid('exportdata', 'xls', 'jqxGrid', false);
            });
        });
        $("#jqxWidget").css('visibility', 'visible');
    };
    return {
        initialize: initialize
    };
});