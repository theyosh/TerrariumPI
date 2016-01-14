
//Colour constants
var fc_cmt = "#888";
var fc_html = "#11a";
var fc_quot = "#a24";
var fc_kwds = "#008";

//Language keywords
var fc_java_kwds = "public|int|float|double|private|new|void|synchronized|if|for|byte|break|else";

var pres = document.getElementsByTagName("pre");
for (var a = 0; a < pres.length; a++) {
    var elem = pres[a];
    if (elem.className.toLowerCase() == 'code') formatCode(elem);
}

function formatCode(precode) {
    var lang = 'html';
    if (!precode.split) return;
    var textlines = precode.split(/\r|\n/);
    var linecount = 1;
    var newcode = "";
    for (var b = 0; b < textlines.length; b++) {
        var code = textlines[b];
        code = code.replace(/\f|\n/g, "");
        code = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        code = code.replace(/(".+")/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_quot + ";\">$1</span>");
        code = code.replace(/('.+')/g, "<span style=\" clear: both; padding: 0px; margin: 0px; color: " + fc_quot + ";\">$1</span>");
        code = code.replace(/&lt;(\S.*?)&gt;/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_html + ";\">&lt;$1&gt;</span>");
        code = code.replace(/&lt;!--/g, "<span style=\"clear: both; padding: 0px; margin: 0px; color: " + fc_cmt + ";\">&lt;!--");
        code = code.replace(/--&gt;/g, "--&gt;</span>");        
        var formatline = ("   " + linecount).slice(-3);
        newcode += code + "<div/>";
        linecount++;
    }

    return "<pre style='width: 700px; max-width: 700px; margin: 5px;' class='code'>" + newcode + "</pre>";
}

function colourKeywords(keywords, codeline) {
    var wordre = new RegExp("(" + keywords + ") ", "gi");
    return codeline.replace(wordre, "<span style=\"color: " + fc_kwds + ";\">$1 </span>");
}
  