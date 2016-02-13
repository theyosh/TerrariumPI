define(["jQuery", "demos", "jqxcore", "jqxbuttons", "jqxtree", "jqxpanel", "jqxscrollbar"], function () {
    var initialize = function () {
        $(document).ready(function () {
            $('#jqxTree').jqxTree({ height: '300px', width: '300px' });
            $('#jqxTree').css("visibility", "visible");
        });
    };
    return {
        initialize: initialize
    };
});