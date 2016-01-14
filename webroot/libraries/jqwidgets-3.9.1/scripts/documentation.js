try {
    $(document).ready(function () {
        if (navigator.userAgent.indexOf('MSIE 7.0') >= 0 || navigator.userAgent.indexOf('MSIE 8.0') >= 0)
        {
            $("em").hide();
            $("em").next().hide();
        }
        var url = "../../jqwidgets/styles/jqx.base.css";
        var bootstrapUrl = "../../jqwidgets/styles/jqx.bootstrap.css";

        if (document.createStyleSheet != undefined) {
            document.createStyleSheet(url);
            document.createStyleSheet(bootstrapUrl);
        }
        else {
            var link = $('<link rel="stylesheet" href="' + url + '" media="screen" />');
            $(document).find('head').append(link);           
            var link = $('<link rel="stylesheet" href="' + bootstrapUrl + '" media="screen" />');
            $(document).find('head').append(link);
        }
        var input = $("<input style='padding-left: 2px; margin-top: 10px; outline:none; border-width: 1px; height: 25px; width: 250px;' class='jqx-widget jqx-widget-bootstrap jqx-rc-all jqx-input jqx-input-bootstrap' placeholder='I am searching for'/>");
        input.prependTo(document.body);
        if (navigator.userAgent.indexOf('MSIE 7.0') >= 0 || navigator.userAgent.indexOf('MSIE 8.0') >= 0 || navigator.userAgent.indexOf('MSIE 9.0') >= 0) {
            $("<label>I am searching for</label><br/>").prependTo(document.body);
        }
        var timer = null;
        input.focus(function()
        {
            input.addClass('jqx-fill-state-focus jqx-fill-state-focus-bootstrap');
        });
        input.blur(function () {
            input.removeClass('jqx-fill-state-focus jqx-fill-state-focus-bootstrap');
        });

        input.keydown(function (event) {
            if (timer != undefined) clearTimeout(timer);
            timer = setTimeout(function () {
                var searchString = input.val();
                var items = $(".documentation-option-type-click");
                $.each(items, function () {
                    var item = $(this);
                    var itemText = $.trim(item.text());
                    var match = itemText.toUpperCase().indexOf(searchString.toUpperCase()) != -1;
                    if (!match) {
                        item.parent().hide();
                        item.parent().next().hide();
                    }
                    else {
                        item.parent().show();
                        item.parent().next().show();
                    }
                });

            }, 500);
        });
    });
}
catch (error) {
    var er = error;
}