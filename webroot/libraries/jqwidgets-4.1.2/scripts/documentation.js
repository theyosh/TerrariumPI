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
        var inputWrapper = $('<div class="search"><div class="wrap"><input id="searchField" type="text" placeholder="I am searching for" value="" autocomplete="off"></div></div>');
        inputWrapper.prependTo(document.body);
        var input = inputWrapper.find('input');
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

        var updateHeightUtility = function () {
            try
            {
                var tables = $('.documentation-table');
                var h = 0;
                $.each(tables, function () {
                    if ($(this).length > 0) {
                        h += $(this).outerHeight();
                    }
                });
                var frameHeight = 250 + h;
                if ($(window.frameElement).length > 0) {
                    $(window.frameElement).height(250 + frameHeight);
                }
                var resize = function () {
                    if ($(window.top.document).find(".doc_menu").length > 0) {
                        var maxHeight = Math.max(frameHeight, 250 + $(window.top.document).find(".doc_menu").height());
                        if ($(window.top).width() < 1330) {
                            maxHeight = frameHeight + 250 + $(window.top.document).find(".doc_menu").height();
                        }

                        $(window.top.document).find(".doc_content").css('min-height',60+ maxHeight + "px");


                        $(window.top.document).find('#tabs-3').css({ height: maxHeight + 'px' });
                        if ($(window.frameElement).length > 0) {
                            $(window.frameElement).height(maxHeight);
                        }
                    }
                }();
            }
            catch (error) {
            }
        }

        var updateHeight = function () {
            try {
                if (document.referrer != "" || window.frameElement) {
                    if (window.top != null && window.top != window.self) {
                        var parentLocation = null;
                        if (window.parent && document.referrer) {
                            parentLocation = document.referrer;
                        }

                        if (parentLocation && parentLocation.indexOf(document.location.host) != -1) {
                            if (window.top.document) {
                                setTimeout(function () {
                                    document.body.style.overflowY = "hidden";
                                    $(window.top.document).find('#tab3').on('click', function (event)
                                    {
                                        updateHeightUtility();
                                    });

                                    if ($(window.top.document).find('#tabs-3').css('display') == "none")
                                        return;

                                    updateHeightUtility();
                                });
                            }
                        }
                    }
                }
            }
            catch (er) {
            }
        }

        $(".documentation-option-type-click").mouseup(function (event) {
            updateHeight();
        });

        updateHeight();

        input.keydown(function (event) {
            if (timer != undefined) clearTimeout(timer);
            var search = function () {
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

                updateHeight();
            }

            timer = setTimeout(function () {
                search();
            }, 500);
            if (event.keyCode == 13) {
                search();
            }

        });
    });
}
catch (error) {
    var er = error;
}