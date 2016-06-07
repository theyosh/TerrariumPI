var profitTabInit = false;

function overviewChart()
{
    'use strict';
    var source =
                    {
                        datafields: [
                            { name: 'day' },
                            { name: 'spline1' },
                            { name: 'spline2' }
                        ],
                        url: 'data.php?usedwidget=chartdataclicks',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        return '<div style="text-align:left"><b><i>' + categoryValue + ' : ' + value + '</i></b></div>';
    };

    var settings = {
        title: '',
        description: '',
        showBorderLine: false,
        showLegend: false,
        enableAnimations: true,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 10, top: 10, right: 15, bottom: 10 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: dataAdapter,
        colorScheme: 'scheme05',
        xAxis: {
            dataField: 'day',
            unitInterval: 1,
            tickMarks: { visible: true, interval: 1 },
            gridLinesInterval: { visible: true, interval: 1 },
            valuesOnTicks: false,
            padding: { bottom: 10 }
        },
        valueAxis: {
            unitInterval: 10,
            minValue: 0,
            maxValue: 50,
            title: { text: '' },
            labels: { horizontalAlignment: 'right' }
        },
        seriesGroups:
            [
                {
                    type: 'spline',
                    series:
                    [
                        {
                            dataField: 'spline1',
                            symbolType: 'square',
                            labels:
                            {
                                visible: true,
                                backgroundColor: '#FEFEFE',
                                backgroundOpacity: 0.2,
                                borderColor: '#7FC4EF',
                                borderOpacity: 0.7,
                                padding: { left: 5, right: 5, top: 0, bottom: 0 }
                            }
                        },
                        {
                            dataField: 'spline2',
                            symbolType: 'square',
                            labels:
                            {
                                visible: true,
                                backgroundColor: '#FEFEFE',
                                backgroundOpacity: 0.2,
                                borderColor: '#7FC4EF',
                                borderOpacity: 0.7,
                                padding: { left: 5, right: 5, top: 0, bottom: 0 }
                            }
                        }
                    ]
                }
            ]
    };
    $('#overviewChart').jqxChart(settings);
}

function overviewBarGauges()
{
    'use strict';
    var createSettings = function (values, color)
    {
        var settings =
            {
                width: 155, height: 130, relativeInnerRadius: 0.77, startAngle: 90, baseValue: 0,
                endAngle: 90,
                labels: {
                    indent: 0.1,
                    visible: false
                },
                colorScheme: 'customColors',
                values: values,
                customColorScheme: {
                    name: 'customColors',
                    colors: color
                },
                tooltip: {
                    visible: false
                }
            };
        return settings;
    };

    $('#leftBarGauge').jqxBarGauge(createSettings([25], ['#6BBD49']));
    $('#rightBarGauge').jqxBarGauge(createSettings([50], ['#667B82']));
}

function overviewProgressBars()
{
    'use strict';
    function createSittings(stop, color)
    {
        var sittings = {
            width: 1093, height: 6, value: 100, colorRanges: [{ stop: stop, color: color }, { stop: 100, color: '#f1f2f3' }]
        };
        return sittings;
    }

    $('#jqxProgressBar1').jqxProgressBar(createSittings(20, '#6BBD49'));
    $('#jqxProgressBar2').jqxProgressBar(createSittings(40, '#C8C8C8'));
    $('#jqxProgressBar3').jqxProgressBar(createSittings(60, '#667B82'));
}

function performanceChart()
{
    'use strict';
    var source =
                    {
                        datafields: [
                            { name: 'day' },
                            { name: 'SPOpen' },
                            { name: 'SPHigh' },
                            { name: 'SPLow' },
                            { name: 'SPClose' }
                        ],
                        url: 'data.php?usedwidget=chartperformance1',
                        datatype: 'json'
                    };

    var dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value)
    {
        return '<div style="text-align:left;padding-bottom:6px;"><b><i>Close: $' + value.close +
            '<br />Open: $' + value.open + '<br />High: $' + value.high + '<br />Low: $' + value.low + '</i></b></div>';
    };

    var settings = {
        title: '',
        description: '',
        enableAnimations: true,
        animationDuration: 1500,
        enableCrosshairs: true,
        showLegend: false,
        showBorderLine: false,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 5, top: 5, right: 5, bottom: 55 },
        source: dataAdapter,
        xAxis: {
            dataField: 'day',
            unitInterval: 1,
            tickMarks: { visible: true, interval: 1 },
            gridLinesInterval: { visible: true, interval: 1 },
            valuesOnTicks: false,
            padding: { bottom: 20 }
        },
        colorScheme: 'scheme06',
        seriesGroups:
            [
                {
                    type: 'candlestick',
                    columnsMaxWidth: 18,
                    columnsMinWidth: 8,
                    valueAxis:
                    {
                        description: ''
                    },
                    series: [
                        {
                            dataFieldClose: 'SPClose',
                            displayTextClose: 'S&P Close price',
                            dataFieldOpen: 'SPOpen',
                            displayTextOpen: 'S&P Open price',
                            dataFieldHigh: 'SPHigh',
                            displayTextHigh: 'S&P High price',
                            dataFieldLow: 'SPLow',
                            displayTextLow: 'S&P Low price',
                            displayText: 'AAPL',
                            lineWidth: 1
                        }
                    ]
                }
            ]
    };

    $('#performanceChart').jqxChart(settings);
}

function profitDropDowns()
{
    'use strict';
    if (profitTabInit)
    {
        return;
    }

    profitTabInit = true;

    var sourceQuater =
    [
        'Q1 2014',
        'Q2 2014',
        'Q3 2014',
        'Q4 2014'
    ];

    var sourceRegion =
    [
        'ASIA',
        'EUROPE',
        'AUSTRALIA',
        'NORTH AMERICA',
        'SOUTH AMERICA'
    ];

    $('#profitDropDownOne').jqxDropDownList({
        selectionRenderer: function ()
        {
            return 'QUARTER';
        },
        autoOpen: true, template: 'info', checkboxes: true, source: sourceQuater, width: '160', height: '35', autoDropDownHeight: true
    });
    $('#profitDropDownTwo').jqxDropDownList({
        selectionRenderer: function ()
        {
            return 'REGION';
        },
        autoOpen: true, template: 'info', checkboxes: true, source: sourceRegion, width: '160', height: '35', autoDropDownHeight: true
    });

    $('#profitDropDownOne').jqxDropDownList('checkAll');
    $('#profitDropDownTwo').jqxDropDownList('checkAll');

    var lastCheckedItem;
    var lastCheckedItemTwo;
    $('#profitDropDownOne').on('checkChange', function (event)
    {
        var items = $('#profitDropDownOne').jqxDropDownList('getCheckedItems');
        if (items.length === 0)
        {
            $('#profitDropDownOne').jqxDropDownList('checkIndex', lastCheckedItem);
            return false;
        } else
        {
            for (var i = 0; i < items.length; i++)
            {
                lastCheckedItem = items[i].index;
            }
        }

        var dataField = event.args.label.substr(0, 2).toLowerCase();

        if (event.args.checked === false)
        {
            $('#profitGrid').jqxGrid('hidecolumn', dataField);
        } else
        {
            $('#profitGrid').jqxGrid('showcolumn', dataField);
        }

    });

    $('#profitDropDownTwo').on('checkChange', function ()
    {
        var items = $('#profitDropDownTwo').jqxDropDownList('getCheckedItems');
        if (items.length === 0)
        {
            $('#profitDropDownTwo').jqxDropDownList('checkIndex', lastCheckedItemTwo);
            return false;
        } else
        {
            for (var i = 0; i < items.length; i++)
            {
                lastCheckedItemTwo = items[i].index;
            }
        }

        function gridFilter()
        {
            $('#profitGrid').jqxGrid('clearfilters');
            var filtertype = 'stringfilter';
            var filtergroup = new $.jqx.filter();
            for (var i = 0; i < items.length; i++)
            {
                var filterOrOperator = 1;
                var filtervalue = items[i].label;
                var filtercondition = 'equal';
                var filter = filtergroup.createfilter(filtertype, filtervalue, filtercondition);
                filtergroup.addfilter(filterOrOperator, filter);
            }
            $('#profitGrid').jqxGrid('addfilter', 'region', filtergroup);
            $('#profitGrid').jqxGrid('applyfilters');
        }

        gridFilter();
    });
}

function profitGrid()
{
    'use strict';
    var source =
                    {
                        datafields: [
                            { name: 'region' },
                            { name: 'account' },
                            { name: 'q1' },
                            { name: 'q2' },
                            { name: 'q3' },
                            { name: 'q4' }
                        ],
                        url: 'data.php?usedwidget=profitloss',
                        datatype: 'json'
                    };

    var dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var groupsrenderer = function (text)
    {
        return '<p class="profitGridGroups">' + text.substr(40).toUpperCase() + '</p>';
    };

    $('#profitGrid').jqxGrid({
        width: '100%',
        height: '92%',
        theme: 'metro',
        source: dataAdapter,
        groupable: true,
        columnsheight: 50,
        groupsheaderheight: 50,
        rowsheight: 40,
        groupsexpandedbydefault: true,
        groupsrenderer: groupsrenderer,
        showgroupsheader: false,
        groups: ['account'],
        columns: [{
            text: '<p class="profitGridHeaders">REGION</p>',
            datafield: 'account',
            width: '20%',
            displayfield: 'region',
            cellsrenderer: function (row, columnfield, value)
            {
                return '<p class="profitGridCells">' + value.toUpperCase() + '</p>';
            }
        }, {
            text: '<p class="profitGridHeaders">Q1 2014</p>',
            datafield: 'q1',
            cellsrenderer: function (row, columnfield, value)
            {
                return '<p class="profitGridCells">$' + value + '</p>';
            }
        }, {
            text: '<p class="profitGridHeaders">Q2 2014</p>',
            datafield: 'q2',
            cellsrenderer: function (row, columnfield, value)
            {
                return '<p class="profitGridCells">$' + value + '</p>';
            }
        }, {
            text: '<p class="profitGridHeaders">Q3 2014</p>',
            datafield: 'q3',
            cellsrenderer: function (row, columnfield, value)
            {
                return '<p class="profitGridCells">$' + value + '</p>';
            }
        }, {
            text: '<p class="profitGridHeaders">Q4 2014</p>',
            datafield: 'q4',
            cellsrenderer: function (row, columnfield, value)
            {
                return '<p class="profitGridCells">$' + value + '</p>';
            }
        }]
    });

    $('#profitGrid').on('rowclick', function ()
    {
        return false;
    });
}

function newsDropDown()
{
    'use strict';
    var source =
    [
        'ALL POSTS',
        'NEWS',
        'FORUM'
    ];

    $('#newsDropDown').jqxDropDownList({ autoOpen: true, template: 'info', source: source, placeHolder: 'ALL POSTS', width: '160', height: '35', autoDropDownHeight: true, itemHeight: 35 });
    $('#newsDropDown').jqxDropDownList('checkIndex', 0);

}

function newsExpanders()
{
    'use strict';
    $('.expander').jqxExpander({ width: '100%', expanded: false, animationType: 'none' });
}

$(document).ready(function ()
{
    'use strict';
    $('#mainSplitter').jqxSplitter({
        width: '100%',
        height: '100%',
        orientation: 'vertical',
        resizable: false,
        showSplitBar: false,
        panels: [
           { size: 250},
           { size: '87%'}]
    });
    $('#mainSplitter').css('visibility', 'visible');
    $('nav a').on('click', function (event)
    {
        $('nav a').removeClass('active');
        $('#' + event.currentTarget.id).addClass('active');
        
        $('#overview').css('display', 'none');
        $('#performance').css('display', 'none');
        $('#profit').css('display', 'none');
        $('#news').css('display', 'none');


        if (event.currentTarget.id === '1')
        {
            $('#overview').css('display', 'block');
            $('#newsDropDown').jqxDropDownList({ selectedIndex: 0 });
            overviewHeight();
        } else if (event.currentTarget.id === '2')
        {
            performanceChart();
            $('#performance').css('display', 'block');
            $('#newsDropDown').jqxDropDownList({ selectedIndex: 0 });
            performanceHeight();
        } else if (event.currentTarget.id === '3')
        {
            profitDropDowns();
            profitGrid();
            $('#profit').css('display', 'block');
            $('#newsDropDown').jqxDropDownList({ selectedIndex: 0 });
            profitHeight();
        } else if (event.currentTarget.id === '4')
        {
            newsDropDown();
            newsExpanders();
            $('#news').css('display', 'block');
            companyNewsHeight();
        }
    });

    $('#logo').on('click', function ()
    {
        $('#overview').css('display', 'block');
        $('#newsDropDown').jqxDropDownList({ selectedIndex: 0 });
        overviewHeight();
    });
   
    $('#overviewChartList ul li').on('click', function (event)
    {
        $('#overviewChartList ul li').removeClass('active-overview');
        $('#' + event.currentTarget.id).addClass('active-overview');

        var dataToDisplay, source, dataAdapter, overviewChart = $('#overviewChart').jqxChart('getInstance');

        if (event.currentTarget.id === '5')
        {
            dataToDisplay = 'chartdataclicks';
        } else if (event.currentTarget.id === '6')
        {
            dataToDisplay = 'chartdatawon';
        } else if (event.currentTarget.id === '7')
        {
            dataToDisplay = 'chartdatasales';
        } else if (event.currentTarget.id === '8')
        {
            dataToDisplay = 'chartdatagoals';
        }      
 
        source =
            {
                datafields: [
                    { name: 'day' },
                    { name: 'spline1' },
                    { name: 'spline2' }
                ],
                url: 'data.php?usedwidget=' + dataToDisplay,
                datatype: 'json'
            };

        dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });
        overviewChart.source = dataAdapter;
        overviewChart.refresh();
        
    });

    $('.dropdown-content a').on('click', function (event)
    {
        var dataToDisplay, description, source, dataAdapter, performanceChart = $('#performanceChart').jqxChart('getInstance');

        if (event.currentTarget.innerHTML === 'AAPL')
        {
            dataToDisplay = 'chartperformance1';
            description = 'AAPL';
            $('.11 div').html('+16.21<p>(+1.47%)</p>');
            $('.12 div').html('591.45');
            $('.13 div').html('599.00/584.35');
            $('.14 div').html('159.3 m');   
        } else if (event.currentTarget.innerHTML === 'GOOG')
        {
            dataToDisplay = 'chartperformance2';
            description = 'GOOG';
            $('.11 div').html('+05.21<p>(+3.29%)</p>');
            $('.12 div').html('313.66');
            $('.13 div').html('317.03/294.35');
            $('.14 div').html('221.6 m');
        } 

        source =
            {
                datafields:
                [
                    { name: 'day' },
                    { name: 'SPOpen' },
                    { name: 'SPHigh' },
                    { name: 'SPLow' },
                    { name: 'SPClose' }
                ],
                url: 'data.php?usedwidget=' + dataToDisplay,
                datatype: 'json'
            };

        dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });
        performanceChart.source = dataAdapter;
        performanceChart.seriesGroups[0].series[0].displayText = description;
        performanceChart.refresh();
    });

    var response = new $.jqx.response();
    var documentWidth = window.innerWidth;
    if (documentWidth < 979)
    {
        $('#mainSplitter').jqxSplitter({ orientation: 'horizontal' });
        $('#listContainer').addClass('header-right');
    }

    var timeOut;
    response.resize(function ()
    {
        $('.freeSpace').css('display', 'none');
        $('#listContainer').removeClass('collapsedListContainer');
        $('#overview').css('margin-top', '0');
        clearTimeout(timeOut);
        timeOut = setTimeout(function ()
        {
            documentWidth = window.innerWidth;

            if (documentWidth < 979)
            {
                $('#mainSplitter').jqxSplitter({ orientation: 'horizontal' });
                $('#listContainer').addClass('header-right');
            } else
            {
                $('#mainSplitter').jqxSplitter({ orientation: 'vertical' });
                $('#mainSplitter').jqxSplitter({ panels: [{ size: 250 }, { size: '87%' }] });
                $('#listContainer').removeClass('header-right');
            }

            if ($('#news').css('display') === 'block')
            {
                companyNewsHeight();
            }
            if ($('#performance').css('display') === 'block')
            {
                performanceHeight();
            }
            if ($('#overview').css('display') === 'block')
            {              
                overviewHeight();
            }
            if ($('#profit').css('display') === 'block')
            {
                profitHeight();
            }      
        }, 1);        
    });

    $('.hidden-desktop').on('click', function ()
    {
        var panels = $('#mainSplitter').jqxSplitter('panels');
        var height = $('#mainSplitter').jqxSplitter('height');
        var newHeight, temp;
        if (panels[0].size === '13%' || panels[0].size === 113)
        {
            newHeight = height + 160;
            $('#mainSplitter').jqxSplitter({ height: newHeight });
            temp = newHeight - 273;
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 273 }, { size: temp }] });
            $('.freeSpace').css('display', 'block');
            $('#listContainer').addClass('collapsedListContainer');
            $('#overview').css('margin-top', '2em');
        } else
        {
            newHeight = height - 160;
            $('#mainSplitter').jqxSplitter({ height: newHeight });
            temp = newHeight - 113;
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 113 }, { size: temp }] });
            $('.freeSpace').css('display', 'none');
            $('#listContainer').removeClass('collapsedListContainer');

            $('#overview').css('margin-top', '0');
        }
    });

    $('.dropdown-content a').on('click', function (e)
    {
        $('.dropbtn').html(e.target.innerHTML + '<span class="glyphicon glyphicon-triangle-bottom"></span>');
    });

    function expandersActions(eventType, eventTarget, expanderNumber)
    {
        var oldHeight, newHeight, heightDifference, currentSplitterHeight;
        if (eventType === 'expanding')
        {
            oldHeight = eventTarget.clientHeight;
            $('.toHide' + expanderNumber).css('display', 'none');
            $('#expander' + expanderNumber).jqxExpander('refresh');
            newHeight = eventTarget.clientHeight + $('#expander' + expanderNumber + ' div.jqx-widget-content').height(); 
            heightDifference = newHeight - oldHeight;
            currentSplitterHeight = $('#mainSplitter').jqxSplitter('height');      
            $('#mainSplitter').jqxSplitter({ height: currentSplitterHeight + heightDifference + 7 });
        } else
        {
            oldHeight = eventTarget.clientHeight;
            $('.toHide' + expanderNumber).css('display', 'block');
            $('#expander' + expanderNumber).jqxExpander('refresh');
            newHeight = eventTarget.clientHeight - $('#expander' + expanderNumber + ' div.jqx-widget-content').height();
            heightDifference = oldHeight - newHeight;
            currentSplitterHeight = $('#mainSplitter').jqxSplitter('height');
            $('#mainSplitter').jqxSplitter({ height: currentSplitterHeight - heightDifference - 7 });
        }
    }

    $('#expander1').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 1); 
    });
    $('#expander1').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 1); 
    });

    $('#expander2').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 2);
    });
    $('#expander2').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 2);
    });

    $('#expander3').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 3);
    });
    $('#expander3').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 3);
    });

    $('#expander4').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 4);
    });
    $('#expander4').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 4);
    });

    $('#expander5').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 5);
    });
    $('#expander5').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 5);
    });

    $('#expander6').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 6);
    });
    $('#expander6').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 6);
    });

    $('#expander7').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 7);
    });
    $('#expander7').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 7);
    });

    $('#expander8').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 8);
    });
    $('#expander8').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 8);
    });

    $('#expander9').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 9);
    });
    $('#expander9').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 9);
    });

    $('#expander10').on('expanding', function (e)
    {
        expandersActions('expanding', e.target, 10);
    });
    $('#expander10').on('collapsing', function (e)
    {
        expandersActions('collapsing', e.target, 10);
    });


    $('#newsDropDown').on('select', function (event)
    {
        for (var i = 1 ; i < 11; i++)
        {
            $('#expander' + i).jqxExpander('collapse');
        }

        var index = event.args.index;
        if (index === 0)
        {
            $('.newsContainer,.forumContainer').css('display', 'block');
        } else if (index === 1)
        {
            $('.forumContainer').css('display', 'none');
            $('.newsContainer').css('display', 'block');
        } else if(index === 2)
        {
            $('.newsContainer').css('display', 'none');
            $('.forumContainer').css('display', 'block');
        }
        companyNewsHeight();
    });

    function companyNewsHeight()
    {
        var newsHeight = 0, forumHeight = 0;

        if ($('.newsContainer').css('display') === 'block')
        {
            newsHeight = $('.newsContainer').height();
        }
        if ($('.forumContainer').css('display') === 'block')
        {
            forumHeight = $('.forumContainer').height();
        }

        var newsContainerHeight = newsHeight + forumHeight + 197;

        if ($('#mainSplitter').jqxSplitter('orientation') === 'vertical')
        {                     
            $('#mainSplitter').jqxSplitter({ height: newsContainerHeight });
        } else
        {
            $('#mainSplitter').jqxSplitter({ height: newsContainerHeight + 113 });
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 113 }, { size: newsContainerHeight }] });
        }      
    }

    function performanceHeight()
    {
        var bottomContainerHeight = $('.bottomContainer').height();
        var topContainerHeight = $('.topContainer').height();
        var performanceTabHeight = bottomContainerHeight + topContainerHeight + 10 + 2*parseInt($("#performance").css('padding-top'));
        if (performanceTabHeight < $(window).height()) {
            performanceTabHeight = $(window).height();
        }

        if ($('#mainSplitter').jqxSplitter('orientation') === 'vertical')
        {
            $('#mainSplitter').jqxSplitter({ height: performanceTabHeight });
        } else
        {
            $('#mainSplitter').jqxSplitter({ height: performanceTabHeight + 113 });
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 113 }, { size: performanceTabHeight }] });
        }       
    }

    function overviewHeight()
    {

        var overviewTabHeight = $(window).height();
        if (overviewTabHeight < 979) {
            overviewTabHeight = 979;
        }
        var documentWidth = window.innerWidth;

        var progressBarContainerWidth = documentWidth - 664;
        var progressBarsWidth = documentWidth - 811;

        if ($('#mainSplitter').jqxSplitter('orientation') === 'vertical')
        {
            $('#mainSplitter').jqxSplitter({ height: overviewTabHeight});
            $('.overviewBottomRight').css('width', progressBarContainerWidth + 55);
            $('#jqxProgressBar1').jqxProgressBar({ width: progressBarsWidth });
            $('#jqxProgressBar2').jqxProgressBar({ width: progressBarsWidth });
            $('#jqxProgressBar3').jqxProgressBar({ width: progressBarsWidth });
        } else
        {
            $('#mainSplitter').jqxSplitter({ height: overviewTabHeight + 112 });
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 112 }, { size: overviewTabHeight }] });
            progressBarContainerWidth = documentWidth - 414;
            progressBarsWidth = documentWidth - 561;
            $('.overviewBottomRight').css('width', progressBarContainerWidth);
            $('#jqxProgressBar1').jqxProgressBar({ width: progressBarsWidth });
            $('#jqxProgressBar2').jqxProgressBar({ width: progressBarsWidth });
            $('#jqxProgressBar3').jqxProgressBar({ width: progressBarsWidth });
            if (documentWidth < 736)
            {
                $('#mainSplitter').jqxSplitter({ height: overviewTabHeight + 360 });
                $('#mainSplitter').jqxSplitter({ panels: [{ size: 113 }, { size: overviewTabHeight }] });
                $('#jqxProgressBar1').jqxProgressBar({ width: progressBarsWidth + 340 });
                $('#jqxProgressBar2').jqxProgressBar({ width: progressBarsWidth + 340 });
                $('#jqxProgressBar3').jqxProgressBar({ width: progressBarsWidth + 340 });
            }
        }              
    }

    function profitHeight()
    {
        if ($('#mainSplitter').jqxSplitter('orientation') === 'vertical')
        {
            $('#mainSplitter').jqxSplitter({ height: Math.max(979, $(window).height()) });
        } else
        {
            $('#mainSplitter').jqxSplitter({ height: 1102 });
            $('#mainSplitter').jqxSplitter({ panels: [{ size: 113 }, { size: 989 }] });
        }
    }

    overviewChart();
    overviewBarGauges();
    overviewProgressBars();
    overviewHeight();

    $('#sortableFirst').jqxSortable();
    $('#sortableSecond').jqxSortable();
    $('#sortableThird').jqxSortable();
});