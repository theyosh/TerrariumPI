function prepareSimulator(id, structure) {
    var touchDevice = $.jqx.mobile.isTouchDevice();
    var hasFullScreenParam = window.location.toString().indexOf('fullscreen') >= 0;
    if (!touchDevice) {
        var theme = "mobile";
        var device = "mobile";
        var hasParam = window.location.toString().indexOf('?');
        if (hasParam != -1) {
            var start = window.location.toString().indexOf('(');
            var end = window.location.toString().indexOf(')');
            var device = window.location.toString().substring(start + 1, end);
            if (device === "") device = "mobile";
            var className = "device-" + device;

            if (device !== "android" && device !== "blackberry" && device !== "win8" && device !== "mobile") {
                device = "mobile";
                var className = "device-" + device;
            }

            if (device == "android") theme = "android";
            if (device == "blackberry") theme = "blackberry";
            if (device == "win8") theme = "windowsphone";
        }
    }

    if (touchDevice || hasFullScreenParam) {
        $("#container").removeClass();
        $("#container").addClass('mobile-container');
        if (id === "window" && !hasFullScreenParam) {
            $("#container").css('min-height', 700);
        }

        var toolbar = $('<div id="demoToolbar" style="border-bottom: 1px solid #555; z-index: 9999999999; position: absolute; top:0; width: 100%; height: 40px;"><div id="demoToolbarButton" style="float: left; margin: 5px; margin-left: 10px; padding: 3px 10px;"><div style="float: left;"></div><span style="float: left;">Back</span><div style="clear:both;"></div></div></div>');
        if (!hasFullScreenParam) {
            $("#container").prepend(toolbar);
        }
        else {
            $("#container").css('padding-top', '0px');
            $("#container").css('padding-bottom', '0px');
            if (theme == "windowsphone") {
                $(document.body).css('background', "#000");
                $(document.body).css('color', "#fff");
            }
            else if (theme == "android") {
                $(document.body).css('background', "#000");
                $(document.body).css('color', "#fff");
            }
            else if (theme === "mobile") {
                $(document.body).css('background', "fff");
                $(document.body).css('color', "#000");
            }
        }

        var html = $("#container").parent().html();
        $("#demoContainer").remove();
        $(document.body).html(html);
        var match = null;
        var version = "";
        var userAgent = navigator.userAgent;
        var os = "Other";
        var osTypes = {
            ios: { name: 'iOS', regex: new RegExp('(?:' + 'i(?:Pad|Phone|Pod)(?:.*)CPU(?: iPhone)? OS ' + ')([^\\s;]+)') },
            android: { name: 'Android', regex: new RegExp('(?:' + '(Android |HTC_|Silk/)' + ')([^\\s;]+)') },
            webos: { name: 'webOS', regex: new RegExp('(?:' + '(?:webOS|hpwOS)\/' + ')([^\\s;]+)') },
            blackberry: { name: 'BlackBerry', regex: new RegExp('(?:' + 'BlackBerry(?:.*)Version\/' + ')([^\\s;]+)') },
            bb10: { name: 'BlackBerry', regex: new RegExp('(?:' + 'BB10(?:.*))([^\\s;]+)') },
            rimTablet: { name: 'RIMTablet', regex: new RegExp('(?:' + 'RIM Tablet OS ' + ')([^\\s;]+)') },
            chrome: { name: 'Chrome OS', regex: new RegExp('CrOS') },
            mac: { name: 'MacOS', regex: new RegExp('mac') },
            win: { name: 'Windows', regex: new RegExp('win') },
            linux: { name: 'Linux', regex: new RegExp('linux') },
            bada: { name: 'Bada', regex: new RegExp('(?:' + 'Bada\/' + ')([^\\s;]+)') },
            other: { name: 'Other' }
        }

        $.each(osTypes, function (index, value) {
            match = userAgent.match(this.regex) || userAgent.toLowerCase().match(this.regex);

            if (match) {
                if (!this.name.match(/Windows|Linux|MaxOS/)) {
                    if (match[1] && (match[1] == "HTC_" || match[1] == "Silk/")) {
                        version = "2.3";
                    } else {
                        version = match[match.length - 1];
                    }
                }

                os = { name: this.name, version: version, platform: navigator.platform };
                return false;
            }
        });
        if (!hasFullScreenParam) {
            var theme = "windowsphone";
            if (os.name === "Android" || os.name === "Bada" || os.name === "Chrome OS" || os.name === "webOS") {
                theme = "android";
            }
            if (os.name === "iOS" || os.name === "MacOS") {
                theme = "mobile";
            }
            if (os.name === "Windows") {
                theme = "windowsphone";
            }
            if (os.name === "BlackBerry" || os.name === "RIMTablet") {
                theme = "blackberry";
            }


            $("#demoToolbar").addClass('jqx-widget-header jqx-widget-header-' + theme);
            $("#demoToolbar").addClass('jqx-listmenu-header jqx-listmenu-header-' + theme);
            $("#demoToolbar").css('padding', '0px');
            $("#demoToolbar").css('padding-top', '5px');

            if (theme == "windowsphone") {
                $("#demoToolbar").css('background', "#2A2A2B");
                $("#demoToolbar").css('border-bottom-color', "#000");
                $(document.body).css('background', "#000");
                $(document.body).css('color', "#fff");
            }
            else if (theme == "android") {
                $("#demoToolbar").css('background', "#000");
                $("#demoToolbar").css('border-bottom-color', "#333");
                $(document.body).css('background', "#000");
                $(document.body).css('color', "#fff");
            }
            else if (theme === "mobile") {
                $("#demoToolbar").css('background', "#f8f8f8");
                $("#demoToolbar").css('border-bottom-color', "#b2b2b2");
                $(document.body).css('background', "fff");
                $(document.body).css('color', "#000");
            }

            $("#demoToolbarButton").jqxButton({ theme: theme });
            $("#demoToolbarButton").css('border-radius', '10px');
            $("#demoToolbarButton").find('div:first').addClass('jqx-listmenu-backbutton-arrow' + ' jqx-listmenu-backbutton-arrow-' + theme);

            $("#demoToolbarButton").click(function () {
                window.open('../index.htm', '_self');
            });
        }
        $(document.body).css('visibility', 'visible');
        return theme;
    }
    if (hasParam != -1) {
        switch (id) {
            case "grid":
            case "scheduler":
            case "kanban":
            case "layout":
            case "dockinglayout":
            case "gauge":
            case "chart":
            case "menu":
            case "treemap":
            case "tabs":
            case "editor":
            case "panel":
            case "window":
            case "photoGallery":
            case "splitter":
            case "popover":
            case "draw":
            case "ribbon":
            case "rangeSelector":
                className += "-tablet";
                break;
        }
        if ($("#demoContainer").length > 0) {
            $("#demoContainer")[0].className = className;
            $("#container")[0].className = className + "-container";
        }
    }
    $(document.body).css('visibility', 'visible');
    return theme;
}

function initSimulator(id, settings) {
    if ($.jqx.mobile.isTouchDevice()) {        
        if (id == "scheduler") {
            $("#scheduler").jqxScheduler(settings);
        }
        return;
    }

    switch (id) {
        case "calendar":
            if ($("#fromCalendar").length > 0) {
                $("#fromCalendar").jqxCalendar({ enableHover: false, keyboardNavigation: false });
                $("#toCalendar").jqxCalendar({ enableHover: false, keyboardNavigation: false });
            }
            break;
        case "listbox":
            $("#listbox").jqxListBox({ touchMode: true, keyboardNavigation: false, enableMouseWheel: false });
            break;
        case "splitter":
            $("#splitter").jqxSplitter({ touchMode: true });
            if ($("#listbox").length > 0) {
                $("#listbox").jqxListBox({ touchMode: true, keyboardNavigation: false, enableMouseWheel: false });
                $("#ContentPanel").jqxPanel({ touchMode: true });
            }
            else {
                $('#rightSplitter').jqxSplitter({ touchMode: true });
            }
            break;
        case "menu":
            $("#menu").jqxMenu({enableHover: false, clickToOpen: true, touchMode: true });
            break;
        case "tree":
            $("#tree").jqxTree({ touchMode: true, keyboardNavigation: false });
            break;
        case "dropdownlist":
            $("#dropdownlist").jqxDropDownList('listBox').host.jqxListBox({ touchMode: true, keyboardNavigation: false });
            break;
        case "adapter":
            $("#jqxDropDownList").jqxDropDownList('listBox').host.jqxListBox({ touchMode: true, keyboardNavigation: false });
            break;
        case "combobox":
            $("#combobox").jqxComboBox({ touchMode: true});
            break;
        case "dropDownButton":
            $("#tree").jqxTree({ touchMode: true, keyboardNavigation: false });
            break;
        case "numberInput":
            $("#numericInput").jqxNumberInput({touchMode: true});
            $("#percentageInput").jqxNumberInput({ touchMode: true });
            $("#currencyInput").jqxNumberInput({ touchMode: true });
            break;
        case "tabs":
            $("#tabs").jqxTabs({ touchMode: true, keyboardNavigation: false });
            $("#jqxGrid").jqxGrid({ touchmode: true, keyboardnavigation: false, enablemousewheel: false });
            break;
        case "grid":
            $("#grid").jqxGrid({ touchmode: true, keyboardnavigation: false, enablemousewheel: false });
            break;
        case "treeGrid":
            $("#treeGrid").jqxTreeGrid({ touchMode: true, enableHover: false });
            break;
        case "dataTable":
            $("#dataTable").jqxDataTable({touchMode: true, enableHover: false});
            break;
        case "panel":
            $("#panel").jqxPanel({ touchMode: true });
            break;
        case "scheduler":
            settings.touchMode = true;
            $("#scheduler").jqxScheduler(settings);
            break;
        case "editor":
            $("#editor").jqxEditor({ touchMode: true });
            break;
    }
}