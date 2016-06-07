function showHideDivs(div1, div2, div3, div4)
{
    'use strict';
    $('#BarGaugeLegend').css('display', 'none');
    $('#YearComparisonRightBarGauge').css('display', 'none');
    $('#YearComparisonLeftBarGauge').css('display', 'none');
    $('#YearComparisonChart').css('display', 'none');
    $('#AvarageEmployeeSalaryChart').css('display', 'none');
    $('#AvarageEmployeeSalaryDataTable').css('display', 'none');
    $('#IncomeAndExpensesBar').css('display', 'none');
    $('#IncomeAndExpenseRatesChart').css('display', 'none');
    $('#IncomeAndExpenseRatesDataTable').css('display', 'none');
    $('#ExpensesPerMonthChart').css('display', 'none');
    $('#ExpensesPerMonthDataTable').css('display', 'none');
    $('#salesPerMonthTabs').css('display', 'none');
    $('#SalesPerMonthDataTable').css('display', 'none');

    div1.css('display', 'block');
    div2.css('display', 'block');
    if (div3 !== undefined)
    {
        div3.css('display', 'block');
    }
    if (div4 !== undefined)
    {
        div4.css('display', 'inline-block');
    }
    if (div2.attr('attr') === $('#YearComparisonRightBarGauge').attr('attr'))
    {
        div2.css('display', 'inline-block');
        div3.css('display', 'inline-block');
    }

}

function menuData()
{
    'use strict';
    var salesData = [{
        sales: 'Sales Comparison'
    }, {
        sales: 'Expenses Comparison'
    }, {
        sales: 'Employee Salary Comparison'
    }, {
        sales: 'Year Sales Comparison'
    }];

    var source = {
        dataType: 'json',
        dataFields: [{
            name: 'sales',
            type: 'string'
        }],
        localdata: salesData
    };
    var dataAdapter = new $.jqx.dataAdapter(source);

    $('#leftPannelDiv').jqxDataTable({
        width: '100%',
        height: '100%',
        showHeader: false,
        source: dataAdapter,
        theme: 'metro',
        ready: function ()
        {
            $('#leftPannelDiv').jqxDataTable('selectRow', 0);
        },
        columns: [{
            text: '',
            dataField: 'sales',
            width: '100%'
        }]
    });
}

function salesPerMonthTabOne()
{
    'use strict';
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');

    var leftChartSource =
                     {
                         datafields: [
                             { name: 'OrderDate' },
                             { name: 'Subtotal' }
                         ],
                         url: 'data.php?usedwidget=salespermonthchart&employeeid=1',
                         datatype: 'json'
                     };

    var rightChartSource =
                    {
                        datafields: [
                            { name: 'OrderDate' },
                            { name: 'Subtotal' }
                        ],
                        url: 'data.php?usedwidget=salespermonthchart&employeeid=2',
                        datatype: 'json'
                    };


    var leftChartDataAdapter = new $.jqx.dataAdapter(leftChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + leftChartSource.url + '" : ' + error); } });

    var RightChartDataAdapter = new $.jqx.dataAdapter(rightChartSource, {loadError: function (xhr, status, error) { alert('Error loading "' + rightChartSource.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        var newValue = value.toString().replace(/[.].*/, '');
        if (newValue.length > 3)
        {
            newValue = newValue.substr(0, newValue.length - 3) + ',' + newValue.substr(newValue.length - 3);
        }
        var month = months[categoryValue.getMonth()];
        return '<DIV style="text-align:left"><b>Sales: $' + newValue +
            '</b><br />Month: ' + month;
    };

    var settings = {
        title: DropDownListOneItem.label,
        description: '',
        enableAnimations: false,
        showLegend: false,
        showBorderLine: false,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 15, top: 5, right: 5, bottom: 5 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: leftChartDataAdapter,
        xAxis:
            {
                dataField: 'OrderDate',
                formatFunction: function (value)
                {
                    return months[value.getMonth()];
                },
                labels: { class: 'bold' },
                type: 'date',
                baseUnit: 'month',
                valuesOnTicks: true,
                minValue: '01-01-1997',
                maxValue: '31-12-1997'
            },
        colorScheme: 'scheme25',
        seriesGroups:
            [
                {
                    type: 'column',
                    columnsGapPercent: 50,
                    seriesGapPercent: 0,
                    valueAxis:
                    {
                        maxValue: 20000,
                        labels: {
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                            }
                        },
                        displayValueAxis: true,
                        description: '',
                        axisSize: 'auto',
                        tickMarksColor: '#888888'
                    },
                    series: [
                            { dataField: 'Subtotal', displayText: '' }
                    ]
                }
            ]
    };

    var settingsTwo = {
        title: DropDownListTwoItem.label,
        description: '',
        enableAnimations: false,
        showLegend: false,
        showBorderLine: false,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 5, top: 5, right: 5, bottom: 5 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: RightChartDataAdapter,
        xAxis:
            {
                dataField: 'OrderDate',
                formatFunction: function (value)
                {
                    return months[value.getMonth()];
                },
                labels: { class: 'bold' },
                type: 'date',
                baseUnit: 'month',
                valuesOnTicks: true,
                minValue: '01-01-1997',
                maxValue: '31-12-1997'
            },
        colorScheme: 'scheme03',
        seriesGroups:
            [
                {
                    type: 'column',
                    columnsGapPercent: 50,
                    seriesGapPercent: 0,
                    valueAxis:
                    {
                        maxValue: 20000,
                        labels: {
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                            }
                        },
                        displayValueAxis: true,
                        description: '',
                        axisSize: 'auto',
                        tickMarksColor: '#888888'
                    },
                    series: [
                            { dataField: 'Subtotal', displayText: '' }
                    ]
                }
            ]
    };

    $('#SalesPerMonthLeftChart').jqxChart(settings);
    $('#SalesPerMonthRightChart').jqxChart(settingsTwo);
}

function salesPerMonthTabTwo()
{
    'use strict';
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');

    var source =
                    {
                        datafields: [
                            { name: 'OrderDate', type: 'date' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=salespermonthgrid&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };

    var dataAdapter = new $.jqx.dataAdapter(source, {
        loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); }
    });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        var newValue = value.toString().replace(/[.].*/, '');
        if (newValue.length > 3)
        {
            newValue = newValue.substr(0, newValue.length - 3) + ',' + newValue.substr(newValue.length - 3);
        }
        var month = months[categoryValue.getMonth()];
        return '<DIV style="text-align:left"><b>Sales: $' + newValue +
            '</b><br />Month: ' + month;
    };

    var settings = {
        title: '',
        description: '',
        enableAnimations: false,
        showLegend: true,
        showBorderLine: false,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 5, top: 5, right: 5, bottom: 5 },
        titlePadding: { left: 0, top: 0, right: 0, bottom: 5 },
        source: dataAdapter,
        colorScheme: 'scheme05',
        xAxis:
        {
            dataField: 'OrderDate',
            formatFunction: function (value)
            {
                return months[value.getMonth()];
            },
            type: 'date',
            baseUnit: 'month',
            valuesOnTicks: true,
            minValue: '01-01-1997',
            maxValue: '31-12-1997',
            labels: { autoRotate: false }
        },
        valueAxis:
        {

            labels: {
                formatSettings: { decimalPlaces: 0 },
                formatFunction: function (value)
                {
                    return Math.round(value / 1000) + ' K';
                }
            }
        },
        seriesGroups:
            [
                {
                    spider: true,
                    startAngle: 0,
                    endAngle: 360,
                    radius: 140,
                    type: 'splinearea',
                    series: [
                            { dataField: 'Subtotal1', displayText: DropDownListOneItem.label, opacity: 0.6, radius: 2, lineWidth: 2, symbolType: 'circle' },
                            { dataField: 'Subtotal2', displayText: DropDownListTwoItem.label, opacity: 0.6, radius: 2, lineWidth: 2, symbolType: 'square' }
                    ]
                }
            ]
    };

    $('#SalesPerMonthSpiderChart').jqxChart(settings);
}

function salesPerMonthDataTable()
{
    'use strict';
    var source =
                    {
                        datafields: [
                            { name: 'OrderDate', type: 'date' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=salespermonthgrid&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };

    var dataAdapter = new $.jqx.dataAdapter(source, {
        loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); }
    });
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
 
    $('#SalesPerMonthDataTable').jqxDataTable(
    {
        width: '100%',
        height: '50%',
        columnsHeight: 50,
        theme: 'metro',
        source: dataAdapter,
        columnsResize: true,
        columns: [
            {
                text: '<p class="dataTableHeader">Month</p>', dataField: 'OrderDate', cellsFormat: 'MMMM', width: '25%', cellsRenderer: function (row, column, value)
                {
                    return '<b>' + value + '</b>';
                }
            },
            {
                text: '<p class="dataTableHeader">' + DropDownListOneItem.label + '</p>',
				renderer: function()
				{
				  var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
				  return '<p style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListOneItem.label + '</p>';
				},
				dataField: 'Subtotal1', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
                {
                    var valueAsString = value.toString();
                    return valueAsString.replace(/[.]/g, ',');
                }
            },
            {
                text: '<p class="dataTableHeader">' + DropDownListTwoItem.label + '</p>',
				renderer: function()
				{
				    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
					return '<p  style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListTwoItem.label + '</p>';
				},
				dataField: 'Subtotal2', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
                {
                    var valueAsString = value.toString();
                    return valueAsString.replace(/[.]/g, ',');
                }
            },
            {
                text: '<p class="dataTableHeader">Total</p>', editable: false, datafield: 'total',
                cellsRenderer: function (row, column, value, rowdata)
                {
                    var total = parseFloat(rowdata.Subtotal1) + parseFloat(rowdata.Subtotal2);
                    return '<div style="margin: 4px;" class="jqx-right-align">' + dataAdapter.formatNumber(total, 'c0').replace(/[.]/g, ',') + '</div>';
                }
            }

        ]
    });
}

function salesPerMonthFunction(init)
{
    'use strict';
    showHideDivs($('#salesPerMonthTabs'), $('#SalesPerMonthDataTable'));
    $('#salesPerMonthTabs').jqxTabs('select', 0);
	if (!init)
		return;
	
    salesPerMonthDataTable();
}

function expensesPerMonthChart()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    var source =
                    {
                        datafields: [
                            { name: 'OrderDate' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=expensespermonthgridchart&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, { loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        var newValue = value.toString().replace(/[.].*/, '');
        if (newValue.length > 3)
        {
            newValue = newValue.substr(0, newValue.length - 3) + ',' + newValue.substr(newValue.length - 3);
        }
        var month = months[categoryValue.getMonth()];
        return '<DIV style="text-align:left"><b>Sales: $' + newValue +
            '</b><br />Month: ' + month;
    };

    var settings = {
        title: 'Expenses Per Month Comparison',
        description: '',
        enableAnimations: false,
        showBorderLine: false,
        showLegend: true,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 15, top: 5, right: 5, bottom: 5 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: dataAdapter,
        colorScheme: 'scheme26',
        xAxis:
        {
            dataField: 'OrderDate',
            formatFunction: function (value)
            {
                return months[value.getMonth()];
            },
            labels: { class: 'bold' },
            type: 'date',
            baseUnit: 'month',
            valuesOnTicks: true,
            minValue: '01-01-1997',
            maxValue: '31-12-1997'
        },
        seriesGroups:
            [
                {
                    type: 'column',
                    valueAxis:
                    {
                        labels: {
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                            }
                        },
                        displayValueAxis: true,
                        description: '',
                        axisSize: 'auto',
                        tickMarksColor: '#888888'
                    },
                    columnsGapPercent: 50,
                    seriesGapPercent: 5,
                    series: [
                            { dataField: 'Subtotal1', displayText: DropDownListOneItem.label },
                            { dataField: 'Subtotal2', displayText: DropDownListTwoItem.label }
                    ]
                }

            ]
    };

    $('#ExpensesPerMonthChart').jqxChart(settings);
}

function expensesPerMonthDataTable()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var source =
                    {
                        datafields: [
                            { name: 'OrderDate', type: 'date' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=expensespermonthgridchart&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, { loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    $('#ExpensesPerMonthDataTable').jqxDataTable(
    {
        width: '100%',
        height: '50%',
        columnsHeight: 50,
        theme: 'metro',
        source: dataAdapter,
        columns: [
           {
               text: '<p class="dataTableHeader">Month</p>', dataField: 'OrderDate', cellsFormat: 'MMMM', width: '25%', cellsRenderer: function (row, column, value)
               {
                   return '<b>' + value + '</b>';
               }		
           },
           {
               text: '<p class="dataTableHeader">' + DropDownListOneItem.label + '</p>', dataField: 'Subtotal1', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
               {
                   var valueAsString = value.toString();
                   return valueAsString.replace(/[.]/g, ',');
               },
			   	renderer: function()
				{
				  var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
				  return '<p style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListOneItem.label + '</p>';
				}	
           },
           {
               text: '<p class="dataTableHeader">' + DropDownListTwoItem.label + '</p>', dataField: 'Subtotal2', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
               {
                   var valueAsString = value.toString();
                   return valueAsString.replace(/[.]/g, ',');
               },
			   renderer: function()
				{
				  var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
				  return '<p style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListTwoItem.label + '</p>';
				}
           },
           {
               text: '<p class="dataTableHeader">Total</p>', editable: false, datafield: 'total',
               cellsRenderer: function (row, column, value, rowdata)
               {
                   var total = parseFloat(rowdata.Subtotal1) + parseFloat(rowdata.Subtotal2);
                   return '<div style="margin: 4px;" class="jqx-right-align">' + dataAdapter.formatNumber(total, 'c0').replace(/[.]/g, ',') + '</div>';
               }
           }

        ]
    });
}

function expensesPerMonthFunction(init)
{
    'use strict';
    showHideDivs($('#ExpensesPerMonthChart'), $('#ExpensesPerMonthDataTable'));
	if (init)
	return;
    expensesPerMonthChart();
    expensesPerMonthDataTable();
}

function avarageEmployeeSalaryChart()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    var source =
                    {
                        datafields: [
                            { name: 'OrderDate' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=salarygridchart&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, { loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        var newValue = value.toString().replace(/[.].*/, '');
        if (newValue.length > 3)
        {
            newValue = newValue.substr(0, newValue.length - 3) + ',' + newValue.substr(newValue.length - 3);
        }
        var month = months[categoryValue.getMonth()];
        return '<DIV style="text-align:left"><b>Sales: $' + newValue +
            '</b><br />Month: ' + month;
    };

    var settings = {
        title: 'Salary Per Month Comparison',
        description: '',
        enableAnimations: false,
        showBorderLine: false,
        showLegend: true,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 15, top: 10, right: 15, bottom: 10 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: dataAdapter,
        colorScheme: 'scheme05',
        xAxis: {
            dataField: 'OrderDate',
            formatFunction: function (value)
            {
                return months[value.getMonth()];
            },
            labels: { class: 'bold' },
            type: 'date',
            baseUnit: 'month',
            valuesOnTicks: true,
            minValue: '01-01-1997',
            maxValue: '31-12-1997'
        },
        seriesGroups:
            [
                {
                    type: 'line',
                    valueAxis:
                    {
                        labels: {
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                            }
                        },
                        displayValueAxis: true,
                        description: '',
                        axisSize: 'auto',
                        tickMarksColor: '#888888'
                    },
                    series:
                    [
                        {
                            dataField: 'Subtotal1',
                            displayText: DropDownListOneItem.label,
                            symbolType: 'square',
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/[.].*/, '');
                            },
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
                            dataField: 'Subtotal2',
                            displayText: DropDownListTwoItem.label,
                            symbolType: 'square',
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/[.].*/, '');
                            },
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

    $('#AvarageEmployeeSalaryChart').jqxChart(settings);
    $('#AvarageEmployeeSalaryChart').jqxChart('addColorScheme', 'myScheme', ['#008ae6', '#E35912']);
    $('#AvarageEmployeeSalaryChart').jqxChart('colorScheme', 'myScheme');
}

function avarageEmployeeSalaryDataTable()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var source =
                     {
                         datafields: [
                             { name: 'OrderDate', type: 'date' },
                             { name: 'Subtotal1' },
                             { name: 'Subtotal2' }
                         ],
                         url: 'data.php?usedwidget=salarygridchart&employeeid1=1&employeeid2=2',
                         datatype: 'json'
                     };


    var dataAdapter = new $.jqx.dataAdapter(source, { loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    $('#AvarageEmployeeSalaryDataTable').jqxDataTable(
    {
        width: '100%',
        height: '50%',
        columnsHeight: 50,
        theme: 'metro',
        source: dataAdapter,
        columns: [
           {
               text: '<p class="dataTableHeader">Month</p>', dataField: 'OrderDate', cellsFormat: 'MMMM', width: '25%', cellsRenderer: function (row, column, value)
               {
                   return '<b>' + value + '</b>';
               }
           },
           {
               text: '<p class="dataTableHeader">' +  DropDownListOneItem.label + '</p>', dataField: 'Subtotal1', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
               {
                   var valueAsString = value.toString();
                   return valueAsString.replace(/[.]/g, ',');
               },
			   renderer: function()
				{
				  var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
				  return '<p style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListOneItem.label + '</p>';
				}	
           },
           {
               text: '<p class="dataTableHeader">' + DropDownListTwoItem.label + '</p>', dataField: 'Subtotal2', width: '25%', cellsalign: 'right', cellsFormat: 'c0', cellsRenderer: function (row, column, value)
               {
                   var valueAsString = value.toString();
                   return valueAsString.replace(/[.]/g, ',');
               },
				renderer: function()
				{
				  var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
				  return '<p style="margin-top:17px; margin-left: 4px;" class="dataTableHeader">' + DropDownListTwoItem.label + '</p>';
				}	
           },
           {
               text: '<p class="dataTableHeader">Total</p>', editable: false, datafield: 'total',
               cellsRenderer: function (row, column, value, rowdata)
               {
                   var total = parseFloat(rowdata.Subtotal1) + parseFloat(rowdata.Subtotal2);
                   return '<div style="margin: 4px;" class="jqx-right-align">' + dataAdapter.formatNumber(total, 'c0').replace(/[.]/g, ',') + '</div>';
               }
           }

        ]
    });
}

function avarageEmployeeSalaryFunction(init)
{
    'use strict';
    showHideDivs($('#AvarageEmployeeSalaryChart'), $('#AvarageEmployeeSalaryDataTable'));
	if (init)
	return;
    avarageEmployeeSalaryChart();
    avarageEmployeeSalaryDataTable();
}

function yearComparisonChart()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var year = ['1996', '1997', '1998'];

    var source =
                    {
                        datafields: [
                            { name: 'OrderDate' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=yearcomparisonchart&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, {loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue)
    {
        var newValue = value.toString().replace(/[.].*/, '');
        if (newValue.length > 3)
        {
            newValue = newValue.substr(0, newValue.length - 3) + ',' + newValue.substr(newValue.length - 3);
        }
        var yearValue = year[year.indexOf('19' + categoryValue.getYear())];
        return '<DIV style="text-align:left"><b>Sales: $' + newValue +
            '</b><br />Year: ' + yearValue;
    };

    var settings = {
        title: 'Year Sales Comparison',
        description: '',
        enableAnimations: false,
        showBorderLine: false,
        showLegend: true,
        toolTipFormatFunction: toolTipCustomFormatFn,
        padding: { left: 60, top: 5, right: 60, bottom: 5 },
        titlePadding: { left: 70, top: 0, right: 0, bottom: 10 },
        source: dataAdapter,
        colorScheme: 'scheme02',
        xAxis:
        {
            dataField: 'OrderDate',
            formatFunction: function (value)
            {
                return year[value.getYear() - 96];
            },
            labels: { class: 'bold' },
            type: 'date',
            baseUnit: 'year',
            valuesOnTicks: true,
            minValue: '01-01-1996',
            maxValue: '01-01-1998'
        },
        seriesGroups:
            [
                {
                    type: 'spline',
                    alignEndPointsWithIntervals: false,
                    valueAxis:
                    {
                        labels: {
                            formatFunction: function (value)
                            {
                                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                            }
                        },
                        displayValueAxis: true,
                        description: '',
                        axisSize: 'auto',
                        tickMarksColor: '#888888'
                    },
                    series: [
                            { dataField: 'Subtotal1', displayText: DropDownListOneItem.label, opacity: 0.4 },
                            { dataField: 'Subtotal2', displayText: DropDownListTwoItem.label, opacity: 0.5 }
                    ]
                }

            ]
    };

    $('#YearComparisonChart').jqxChart(settings);
    $('#YearComparisonChart').jqxChart('addColorScheme', 'myScheme', ['#008ae6', '#E35912']);
    $('#YearComparisonChart').jqxChart('colorScheme', 'myScheme');
}

function yearComparisonBarGauges()
{
    'use strict';
    var DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    var DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');
    var source =
                    {
                        datafields: [
                            { name: 'OrderDate' },
                            { name: 'Subtotal1' },
                            { name: 'Subtotal2' }
                        ],
                        url: 'data.php?usedwidget=yearcomparisonchart&employeeid1=1&employeeid2=2',
                        datatype: 'json'
                    };


    var dataAdapter = new $.jqx.dataAdapter(source, { async: false, autoBind: true, loadError: function (xhr, status, error) { alert('Error loading "' + source.url + '" : ' + error); } });

    var TotalPersonOne = dataAdapter.records[0].Subtotal1 + dataAdapter.records[1].Subtotal1 + dataAdapter.records[2].Subtotal1;
    var TotalPersonTwo = dataAdapter.records[0].Subtotal2 + dataAdapter.records[1].Subtotal2 + dataAdapter.records[2].Subtotal2;

    $('#YearComparisonLeftBarGauge').jqxBarGauge({
        title: {
            text: DropDownListOneItem.label,
            font: {
                color: 'black',
                size: 25,
                opacity: 0.7,
                family: '"Helvetica Neue", "Arial"',
                weight: 200
            },
            horizontalAlignment: 'center',
            margin: {
                bottom: 30,
                left: 0,
                right: 0,
                top: 50
            },
            verticalAlignment: 'top'
        },
        colorScheme: 'customColors',
        relativeInnerRadius: 0.5,
        customColorScheme: {
            name: 'customColors',
            colors: ['#80ccff', '#33adff', '#008ae6']
        },
        width: '48%',
        height: '49%',
	    values: [dataAdapter.records[0].Subtotal1, dataAdapter.records[1].Subtotal1, dataAdapter.records[2].Subtotal1],
        max: TotalPersonOne,
        labels: {

            indent: 1, formatFunction: function (value) {
                return "$" + value;
            }
        },
        tooltip: {
            visible: true, formatFunction: function (value, index)
            {
                var yearValue = dataAdapter.records[index].OrderDate.substr(0, 4);
                return '<DIV style="text-align:left"><b>Sales: $' + value + '</b><br />Year: ' + yearValue;
            }
        }
    });

    $('#YearComparisonRightBarGauge').jqxBarGauge({
        title: {
            text: DropDownListTwoItem.label,
            font: {
                color: 'black',
                size: 25,
                opacity: 0.7,
                family: '"Helvetica Neue", "Arial"',
                weight: 200
            },
            horizontalAlignment: 'center',
            margin: {
                bottom: 30,
                left: 0,
                right: 0,
                top: 50
            },
            verticalAlignment: 'top'
        },
    	relativeInnerRadius: 0.5,
        colorScheme: 'customColors',
        customColorScheme: {
            name: 'customColors',
            colors: ['#f5ad89', '#f07c42', '#e35912']
        },
        width: '48%',
        height: '49%',
        values: [dataAdapter.records[0].Subtotal2, dataAdapter.records[1].Subtotal2, dataAdapter.records[2].Subtotal2],
        max: TotalPersonTwo,
        labels: {

            indent: 1,
            formatFunction: function (value) {
                return "$" + value;
            }
        },
        tooltip: {
            visible: true, formatFunction: function (value, index)
            {
                var yearValue = dataAdapter.records[index].OrderDate.substr(0, 4);
                return '<b>Sales: $' + value + '</b><br/>Year: ' + yearValue;
            }
        }
    });
}

function yearComparisonFunction(init)
{
    'use strict';
    showHideDivs($('#YearComparisonChart'), $('#YearComparisonRightBarGauge'), $('#YearComparisonLeftBarGauge'), $('#BarGaugeLegend'));
	if (init)
	return;
    yearComparisonChart();
    yearComparisonBarGauges();
}

$(document).ready(function ()
{
    'use strict';

    var response = new $.jqx.response();

    var timeOut;
    response.resize(function ()
    {
        clearTimeout(timeOut);
        timeOut = setTimeout(function ()
        {
            yearComparisonGaugeWidthSetting();
        }, 1);
    });

    function yearComparisonGaugeWidthSetting()
    {
        var documentWidth = window.innerWidth;
        if (documentWidth < 1022)
        {
            $('#YearComparisonRightBarGauge').jqxBarGauge({ width: '100%' });
            $('#YearComparisonLeftBarGauge').jqxBarGauge({ width: '100%' });
        } else
        {
            $('#YearComparisonRightBarGauge').jqxBarGauge({ width: '48%' });
            $('#YearComparisonLeftBarGauge').jqxBarGauge({ width: '48%' });
        }
    }

    var sourceDropdownlist = {
        datatype: 'json',
        datafields: [
               { name: 'fullname', type: 'string', map: 'employeeName' },
               { name: 'picture', type: 'string', map: 'employeePhoto' },
               { name: 'employeeId' }
        ],
        async: false,
        url: 'data.php?usedwidget=employeedropdown'
    };

    var dataAdapterHeaderDropDownList = new $.jqx.dataAdapter(sourceDropdownlist, {
        loadComplete: function () { },
        beforeLoadComplete: function () { }
    });

    $('#headerDropdownListOne').jqxDropDownList({
        width: 250,
        height: 30,
        source: dataAdapterHeaderDropDownList,
        theme: 'metrodark',
        displayMember: 'fullname',
        valueMember: 'employeeId',
        selectedIndex: 1,
        renderer: function (index, label, value) {
            var data = dataAdapterHeaderDropDownList.getrecords();
            var datarecord = data[index];
            var imgurl = '../../../images/' + datarecord.picture;
            var img = '<img height="50" width="45" src="' + imgurl + '"/>';
            var table = '<table style="min-width: 150px;"><tr><td style="width: 55px;" rowspan="2">' + img + '</td><td>' + datarecord.fullname + ' - ID: ' + value + '</td></tr>' + '</table>';
            return table;
        }
    });

    $('#headerDropdownListTwo').jqxDropDownList({
        width: 250,
        height: 30,
        source: dataAdapterHeaderDropDownList,
        theme: 'metrodark',
        displayMember: 'fullname',
        valueMember: 'employeeId',
        selectedIndex: 2,
        renderer: function (index, label, value) {
            var data = dataAdapterHeaderDropDownList.getrecords();
            var datarecord = data[index];
            var imgurl = '../../../images/' + datarecord.picture;
            var img = '<img height="50" width="45" src="' + imgurl + '"/>';
            var table = '<table style="min-width: 150px;"><tr><td style="width: 55px;" rowspan="2">' + img + '</td><td>' + datarecord.fullname + ' - ID: ' + value + '</td></tr>' + '</table>';
            return table;
        }
    });

    var DropDownListOneItem, DropDownListTwoItem;
    var salesPerMonthLeftChartSource, salesPerMonthLeftChartDataAdapter, SalesPerMonthDataTableSource, SalesPerMonthDataTableDataAdapter,
        SalesPerMonthSpiderChartSource, SalesPerMonthSpiderChartDataAdapter, salesPerMonthRightChartSource, SalesPerMonthRightChartDataAdapter;
    var ExpensesPerMonthChartSource, ExpensesPerMonthChartDataAdapter, ExpensesPerMonthDataTableSource, ExpensesPerMonthDataTableDataAdapter;
    var SalaryPerMonthChartSource, SalaryPerMonthChartDataAdapter, SalaryPerMonthDataTableSource, SalaryPerMonthDataTableDataAdapter;
    var YearComparisonChartSource, YearComparisonChartDataAdapter;

    DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
    DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');


    var layout = [{
        type: 'layoutGroup',
        orientation: 'horizontal',
        items: [
        {
            type: 'layoutGroup',
            orientation: 'vertical',
            width: '15%',
            items: [{
                type: 'tabbedGroup',
                height: '100%',
                items: [{
                    type: 'layoutPanel',
                    title: 'Report Filter',
                    contentContainer: 'LeftPannel',
                    initContent: function ()
                    {
                        menuData();
                    }
                }]
            }]
        }, {
            type: 'layoutGroup',
            orientation: 'vertical',
            width: '85%',
            items: [{
                type: 'tabbedGroup',
                height: '100%',
                items: [{
                    type: 'layoutPanel',
                    title: '',
                    contentContainer: 'RightPannel',
                    initContent: function ()
                    {
                        salesPerMonthFunction(true);
                    }
                }]
            }]
        }]
    }];
    $('#jqxLayout').jqxLayout({ width: '100%', height: 882, layout: layout, contextMenu: true, resizable: false, theme: 'metro' });

    $('#salesPerMonthTabs').jqxTabs({
        width: '100%', height: '50%', theme: 'metro',
        initTabContent:
            function (tab)
            {
               
                if (tab === 0)
                {
                    salesPerMonthTabOne();
                    salesPerMonthTabTwo();
                } else
                {
                    
                }
            }
    });

    $('.buttons').on('click', function (event)
    {
        $('#firstButton').removeClass('active');
        $('#secondButton').removeClass('active');
        $('#thirdButton').removeClass('active');
        $('#' + event.target.id).addClass('active');
    });

    var updateSources = function () {    
        WhichTabToUpdate();
    }

    $('#headerDropdownListOne').on('select', function (event)
    {
        updateSources();
    });

    $('#headerDropdownListTwo').on('select', function (event)
    {
        updateSources();
    });

    function SalesPerMonthDataUpdate()
    {
        if (salesPerMonthLeftChartDataAdapter === undefined)
        {
            return;
        }
        var salesPerMonthSpiderChart = $('#SalesPerMonthSpiderChart').jqxChart('getInstance');
        
        var leftChartTitle = $('#SalesPerMonthLeftChart').jqxChart('title');
        var rightChartTitle = $('#SalesPerMonthRightChart').jqxChart('title');
        if (leftChartTitle !== DropDownListOneItem.label) {
            $('#SalesPerMonthLeftChart').jqxChart({ title: DropDownListOneItem.label, source: salesPerMonthLeftChartDataAdapter });
        }
        if (rightChartTitle !== DropDownListTwoItem.label) {
            $('#SalesPerMonthRightChart').jqxChart({ title: DropDownListTwoItem.label, source: SalesPerMonthRightChartDataAdapter });
        }

        salesPerMonthSpiderChart.seriesGroups[0].series[0].displayText = DropDownListOneItem.label;
        salesPerMonthSpiderChart.seriesGroups[0].series[1].displayText = DropDownListTwoItem.label;
        $('#SalesPerMonthSpiderChart').jqxChart({ source: SalesPerMonthSpiderChartDataAdapter });

     
        $('#SalesPerMonthDataTable').jqxDataTable({ source: SalesPerMonthDataTableDataAdapter });
     }
    
    function ExpensesPerMonthDataUpdate()
    {
        if (ExpensesPerMonthChartDataAdapter === undefined)
        {
            return;
        }
        var expensesPerMonthChart = $('#ExpensesPerMonthChart').jqxChart('getInstance');
        expensesPerMonthChart.seriesGroups[0].series[0].displayText = DropDownListOneItem.label;
        expensesPerMonthChart.seriesGroups[0].series[1].displayText = DropDownListTwoItem.label;
        $('#ExpensesPerMonthChart').jqxChart({ source: ExpensesPerMonthChartDataAdapter });
        $('#ExpensesPerMonthDataTable').jqxDataTable({ source: ExpensesPerMonthDataTableDataAdapter });
    }

    function SalarPerMonthDataUpdate()
    {
        if (SalaryPerMonthChartDataAdapter === undefined)
        {
            return;
        }
        var salaryPerMonthChart = $('#AvarageEmployeeSalaryChart').jqxChart('getInstance');
        salaryPerMonthChart.seriesGroups[0].series[0].displayText = DropDownListOneItem.label;
        salaryPerMonthChart.seriesGroups[0].series[1].displayText = DropDownListTwoItem.label;
        $('#AvarageEmployeeSalaryChart').jqxChart({ source: SalaryPerMonthChartDataAdapter });
        $('#AvarageEmployeeSalaryDataTable').jqxDataTable({ source: SalaryPerMonthDataTableDataAdapter });
    }

    function YearComparisonDataUpdate()
    {
        if (YearComparisonChartDataAdapter === undefined)
        {
            return;
        }
        var yearComparisonChart = $('#YearComparisonChart').jqxChart('getInstance');
        yearComparisonChart.seriesGroups[0].series[0].displayText = DropDownListOneItem.label;
        yearComparisonChart.seriesGroups[0].series[1].displayText = DropDownListTwoItem.label;	
		$('#YearComparisonChart').jqxChart({source: YearComparisonChartDataAdapter});
    }

    function WhichTabToUpdate()
    {
        var leftEmployeeID = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem').value;
        var rightEmployeeID = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem').value;
     
        DropDownListOneItem = $('#headerDropdownListOne').jqxDropDownList('getSelectedItem');
        DropDownListTwoItem = $('#headerDropdownListTwo').jqxDropDownList('getSelectedItem');

        if ($('#salesPerMonthTabs').css('display') === 'block')
        {
            //SalesPerMonth
            salesPerMonthLeftChartSource =
                         {
                             datafields: [
                                 { name: 'OrderDate' },
                                 { name: 'Subtotal' }
                             ],
                             url: 'data.php?usedwidget=salespermonthchart&employeeid=' + leftEmployeeID,
                             datatype: 'json'
                         };

            salesPerMonthLeftChartDataAdapter = new $.jqx.dataAdapter(salesPerMonthLeftChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + salesPerMonthLeftChartSource.url + '" : ' + error); } });

            salesPerMonthRightChartSource =
                        {
                            datafields: [
                                { name: 'OrderDate' },
                                { name: 'Subtotal' }
                            ],
                            url: 'data.php?usedwidget=salespermonthchart&employeeid=' + leftEmployeeID,
                            datatype: 'json'
                        };

            SalesPerMonthRightChartDataAdapter = new $.jqx.dataAdapter(salesPerMonthRightChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + salesPerMonthRightChartSource.url + '" : ' + error); } });

            SalesPerMonthDataTableSource =
                        {
                            datafields: [
                                { name: 'OrderDate', type: 'date' },
                                { name: 'Subtotal1' },
                                { name: 'Subtotal2' }
                            ],
                            url: 'data.php?usedwidget=salespermonthgrid&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                            datatype: 'json'
                        };

            SalesPerMonthDataTableDataAdapter = new $.jqx.dataAdapter(SalesPerMonthDataTableSource, {
                async: true,
                loadError: function (xhr, status, error) { alert('Error loading "' + SalesPerMonthDataTableSource.url + '" : ' + error); }
            });

            SalesPerMonthSpiderChartSource =
                       {
                           datafields: [
                               { name: 'OrderDate', type: 'date' },
                               { name: 'Subtotal1' },
                               { name: 'Subtotal2' }
                           ],
                           url: 'data.php?usedwidget=salespermonthgrid&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                           datatype: 'json'
                       };

            SalesPerMonthSpiderChartDataAdapter = new $.jqx.dataAdapter(SalesPerMonthSpiderChartSource, {
                loadError: function (xhr, status, error) { alert('Error loading "' + SalesPerMonthSpiderChartSource.url + '" : ' + error); }
            });


            SalesPerMonthDataUpdate();
        } else if ($('#ExpensesPerMonthChart').css('display') === 'block')
        {
            ExpensesPerMonthChartSource =
               {
                   datafields: [
                       { name: 'OrderDate' },
                      { name: 'Subtotal1' },
                      { name: 'Subtotal2' }
                   ],
                   url: 'data.php?usedwidget=expensespermonthgridchart&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                   datatype: 'json'
               };

            ExpensesPerMonthChartDataAdapter = new $.jqx.dataAdapter(ExpensesPerMonthChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + ExpensesPerMonthChartSource.url + '" : ' + error); } });

            ExpensesPerMonthDataTableSource =
                        {
                            datafields: [
                                { name: 'OrderDate', type: 'date' },
                                { name: 'Subtotal1' },
                                { name: 'Subtotal2' }
                            ],
                            url: 'data.php?usedwidget=expensespermonthgridchart&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                            datatype: 'json'
                        };

            ExpensesPerMonthDataTableDataAdapter = new $.jqx.dataAdapter(ExpensesPerMonthDataTableSource, {
               loadError: function (xhr, status, error) { alert('Error loading "' + ExpensesPerMonthDataTableSource.url + '" : ' + error); }
            });

            ExpensesPerMonthDataUpdate();
        } else if ($('#AvarageEmployeeSalaryChart').css('display') === 'block')
        {
            SalaryPerMonthChartSource =
                          {
                              datafields: [
                                  { name: 'OrderDate' },
                                 { name: 'Subtotal1' },
                                 { name: 'Subtotal2' }
                              ],
                              url: 'data.php?usedwidget=salarygridchart&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                              datatype: 'json'
                          };

            SalaryPerMonthChartDataAdapter = new $.jqx.dataAdapter(SalaryPerMonthChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + SalaryPerMonthChartSource.url + '" : ' + error); } });

            SalaryPerMonthDataTableSource =
                        {
                            datafields: [
                                { name: 'OrderDate', type: 'date' },
                                { name: 'Subtotal1' },
                                { name: 'Subtotal2' }
                            ],
                            url: 'data.php?usedwidget=salarygridchart&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                            datatype: 'json'
                        };

            SalaryPerMonthDataTableDataAdapter = new $.jqx.dataAdapter(SalaryPerMonthDataTableSource, {
                loadError: function (xhr, status, error) { alert('Error loading "' + SalaryPerMonthDataTableSource.url + '" : ' + error); }
            });


            SalarPerMonthDataUpdate();
        } else if ($('#YearComparisonChart').css('display') === 'block')
        {
            YearComparisonChartSource =
                         {
                             datafields: [
                                 { name: 'OrderDate' },
                                { name: 'Subtotal1' },
                                { name: 'Subtotal2' }
                             ],
                             url: 'data.php?usedwidget=yearcomparisonchart&employeeid1=' + leftEmployeeID + '&employeeid2=' + rightEmployeeID,
                             datatype: 'json'
                         };

            YearComparisonChartDataAdapter = new $.jqx.dataAdapter(YearComparisonChartSource, { loadError: function (xhr, status, error) { alert('Error loading "' + YearComparisonChartSource.url + '" : ' + error); },
			loadComplete: function()
			{
			    var TotalPersonOne = YearComparisonChartDataAdapter.records[0].Subtotal1 + YearComparisonChartDataAdapter.records[1].Subtotal1 + YearComparisonChartDataAdapter.records[2].Subtotal1;
				var TotalPersonTwo = YearComparisonChartDataAdapter.records[0].Subtotal2 + YearComparisonChartDataAdapter.records[1].Subtotal2 + YearComparisonChartDataAdapter.records[2].Subtotal2;
				$('#YearComparisonLeftBarGauge').jqxBarGauge({ title: { text: DropDownListOneItem.label } });
				$('#YearComparisonRightBarGauge').jqxBarGauge({ title: { text: DropDownListTwoItem.label } });
				$('#YearComparisonLeftBarGauge').jqxBarGauge({ values: [YearComparisonChartDataAdapter.records[0].Subtotal1, YearComparisonChartDataAdapter.records[1].Subtotal1, YearComparisonChartDataAdapter.records[2].Subtotal1] });
				$('#YearComparisonRightBarGauge').jqxBarGauge({ values: [YearComparisonChartDataAdapter.records[0].Subtotal2, YearComparisonChartDataAdapter.records[1].Subtotal2, YearComparisonChartDataAdapter.records[2].Subtotal2] });
				$('#YearComparisonLeftBarGauge').jqxBarGauge({ max: TotalPersonOne });
				$('#YearComparisonRightBarGauge').jqxBarGauge({ max: TotalPersonTwo });
				$('#YearComparisonLeftBarGauge').jqxBarGauge('refresh');
				$('#YearComparisonRightBarGauge').jqxBarGauge('refresh');
			}
			});
            YearComparisonDataUpdate();
        }
    }
	var init = [];
	var lastIndex = -1;

    $('#leftPannelDiv').on('rowSelect', function (event)
    {
        var boundIndex = event.args.boundIndex;	
		if (lastIndex === boundIndex)
			return;
		lastIndex = boundIndex;
	    
        if (boundIndex === 0)
        {
		    salesPerMonthFunction(init[boundIndex]);
        }
        else if (boundIndex === 1)
        {
            expensesPerMonthFunction(init[boundIndex]);
        }
        else if (boundIndex === 2)
        {
            avarageEmployeeSalaryFunction(init[boundIndex]);
        }
        else if (boundIndex === 3)
        {
            yearComparisonFunction(init[boundIndex]);
            yearComparisonGaugeWidthSetting(init[boundIndex]);
        }
    	init[boundIndex] = true;
        WhichTabToUpdate();
    });
});