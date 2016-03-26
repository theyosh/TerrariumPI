
//Colour constants
var fc_cmt = "#080";
var fc_html = "#11a";
var fc_quot = "#080";
var fc_kwds = "#11a";

//Language keywords
var fc_java_kwds = "public|int|float|double|private|new|void|synchronized|if|for|byte|break|else";

var pres = document.getElementsByTagName("pre");
for (var a = 0; a < pres.length; a++) {
    var elem = pres[a];
    if (elem.className.toLowerCase() == 'code') formatCode(elem);
}

function formatCode(precode) {
    var lang = 'html';
    var textlines = precode.split(/\r|\n/);
    var linecount = 1;
    var newcode = "";
    var keywords = "debugger|export|function|return|null|for|set|undefined|var|with|true|false|switch|this|case";
    for (var b = 0; b < textlines.length; b++) {
        var code = textlines[b];
        code = code.replace(/\f|\n/g, "");
        if (code.indexOf("if (") == -1 && code.indexOf("for (") == -1)
        {
            code = code.replace(/&/g, '&amp;');
            code = code.replace(/</g, '&lt;');
            code = code.replace(/>/g, '&gt;');
        }
        code = code.replace(/(".+")/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_quot + ";\">$1</span>");
        code = code.replace(/('.+')/g, "<span style=\" clear: both; padding: 0px; margin: 0px; color: " + fc_quot + ";\">$1</span>");
        code = code.replace(/&lt;(\S.*?)&gt;/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_html + ";\">&lt;$1&gt;</span>");
        code = code.replace(/&lt;!--/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_cmt + ";\">&lt;!--");
        code = code.replace(/--&gt;/g, "--&gt;</span>");        

        code = colourKeywords(keywords, code);
        code = colourCodeKeywordsCustom("width:|disabled:|height:|uploadUrl:|datafield:|dataField:|text:|minwidth:|cellsformat:|cellsalign:|cellsformat:|columntype:", code);
        code = colourKeywordsCustom("jqxButton|jqxRepeatButton|jqxButtonGroup|jqxRadioButton|jqxGrid|jqxTree|jqxTreeGrid|jqxInput|jqxCalendar|jqxBulletChart|jqxToggleButton|jqxLinkButton|jqxSwitchButton|jqxChart|jqxDataTable|jqxDateTimeInput|jqxCheckBox|jqxScheduler|jqxRadioButton|jqxComplexInput|jqxListBox|jqxDropDownList|jqxCombobox|jqxFileUpload|jqxEditor|jqxExpander|jqxNavBar|jqxNavigationBar|jqxTooltip|jqxToolbar|jqxScrollBar|jqxSlider|jqxRangeSelector|jqxGauge|jqxFormattedInput|jqxComplexInput|jqxNumberInput|jqxDragDrop|jqxWindow|jqxTreemap|jqxValidator|jqxTouch|jqxTextArea|jqxTagCloud|jqxTabs|jqxSplitter|jqxScrollView|jqxListView|jqxRibbon|jqxRating|jqxProgressBar|jqxPanel|jqxLayout|jqxDockingLayout|jqxNotification|jqxMenu|jqxMaskedInput|jqxLoader", code);
        if (code.indexOf("//") >= 0) {
            code = "<span style=\"clear: both; padding: 0px; margin: 0px; color: #a533d4;\">" + code + "</span>";
        }

        var formatline = ("   " + linecount).slice(-3);
        newcode += code + "<div/>";
        linecount++;
    }
 
    return "<pre style='border:none !important; padding: 0px !important; overflow: auto; margin-top: 5px; margin-bottom: 5px;' class='code'>" + newcode + "</pre>";
}

var colourKeywordsCustom = function (keywords, codeline) {
    var words = keywords.split("|");
    var newString = codeline;
    for (var i = 0; i < words.length; i++) {
        if (newString.indexOf(words[i] + "(") >= 0) {
            newString = newString.replace(words[i] + "(", "<span style=\"color: #666b74;\">" + words[i] + "</span>(");
        }
    }
    return newString;
}

var colourCodeKeywordsCustom = function (keywords, codeline) {
    var words = keywords.split("|");
    var newString = codeline;
    for (var i = 0; i < words.length; i++) {
        if (newString.indexOf(words[i]) >= 0) {
            newString = newString.replace(words[i] + "", "<span style=\"color: #666b74;\">" + words[i] + "</span>");
        }
    }
    return newString;
}

function colourKeywords(keywords, codeline) {
    var wordre = new RegExp("(" + keywords + ") ", "gi");
    return codeline.replace(wordre, "<span style=\"color: " + fc_kwds + ";\">$1 </span>");
}
  