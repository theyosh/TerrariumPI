$(document).ready(function ()
{
    "use strict";

    var CONST_URL_SUFFIX = {
        employeedropdown: 'employeedropdown',
        salesgrid: 'salesgrid',
        yearpiechart: 'yearpiechart',
        monthpiechart: 'monthpiechart'
    };
    var CONST_URL_PREFIX = 'data.php';
    var currentEmplyeeID = 1; // default value
    var currentMonth = 1; // default value

    var getEmployeeID = function (id)
    {
        id = id || currentEmplyeeID;
        return id;
    };

    var getMonth = function (month)
    {
        month = month || currentMonth;
        var exportMonth = month.toString().length > 1 ? "" + month : "0" + month;
        return exportMonth;
    };

    var createElement = function (element)
    {
        element = element || 'div';
        return document.createElement(element);
    };

    var theme = 'light';
    var theme2 = 'dark';
    var months = ["Q1", "Q2", "Q3", "Q4"];
    var messageChartDescription = " ";
    var monthsNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var clearOldData = false;

    /*
     * Generate Personal Info
     *
     * @param {String} name - fullname of the person.
     * @param {String} pictureUrl
     * @param {String} personalInfo
     */
    function generatePersonalInfo(name, pictureUrl, personalInfo)
    {
        var domId = 'person';
        var personContent = document.getElementById(domId);
        if (clearOldData)
        {
            personContent.innerHTML = "";
        }

        var picture = document.createElement('div');
        picture.className = 'personpicture';
        picture.style.margin = 0;
        var url = '../../../images/' + pictureUrl;
        picture.style.background = "url('" + url + "')";

        var personInfo = document.createElement('div');
        personInfo.className = 'personinfo';

        var personName = document.createElement('div');
        personName.className = 'fullname';
        personName.innerText = name;

        var personalContacts = document.createElement('div');
        personalContacts.className = 'contacts';
        personalContacts.innerText = 'Phone: xxxx-xxx-xxx' +
            ' \nID: ' +
            personalInfo;

        personInfo.appendChild(personName);
        personInfo.appendChild(personalContacts);
        personContent.appendChild(picture);
        personContent.appendChild(personInfo);
    }

    var sourceDropdownlist = {
        datatype: "json",
        datafields: [
               { name: 'fullname', type: 'string', map: 'employeeName' },
               { name: 'picture', type: 'string', map: 'employeePhoto' },
               { name: 'employeeId' }
        ],
        url: CONST_URL_PREFIX
    };

    var dataAdapterDropdownlist = new $.jqx.dataAdapter(sourceDropdownlist, {
        formatData: function (data)
        {
            // Default settings
            $.extend(data, {
                employeeid: getEmployeeID(), //'5',
                month: getMonth(), //'07',
                usedwidget: 'employeedropdown'
            });
            return data;
        }
    });

    $('#dropdownlist').jqxDropDownList({
        width: 250,
        height: 30,
        source: dataAdapterDropdownlist,
        theme: theme2,
        displayMember: 'fullname',
        valueMember: 'employeeId',
        placeHolder: "Please choose employee: ",
        renderer: function (index, label, value)
        {
            var data = dataAdapterDropdownlist.getrecords();
            var datarecord = data[index];
            var imgurl = '../../../images/' + datarecord.picture;
            var img = '<img height="50" width="45" src="' + imgurl + '"/>';
            var table = '<table style="min-width: 150px;"><tr><td style="width: 55px;" rowspan="2">' + img + '</td><td>' + datarecord.fullname + " - ID: " + value + '</td></tr>' +
                '</table>';

            return table;
        }
    });

    $('#dropdownlist').on('select', function (event)
    {
        if (event.args)
        {
            var item = event.args.item;

            if (item)
            {
                currentMonth = 1;
                var data = dataAdapterDropdownlist.getrecords();
                var index = item.index;
                var name = item.label;
                var pictureUrl = data[index].picture;
                var personalInfo = item.value;
                generatePersonalInfo(name, pictureUrl, personalInfo);
                clearOldData = true;
                currentEmplyeeID = index + 1;
                
                $('#monthCombobox').jqxComboBox({
                    selectedIndex: currentMonth - 1
                });

                refreshGrid();
                refreshChart();
                refreshPurchase();
                isTurnOnDetails = false;
            }
        }
    });

    // Fill table amount
    var purchaseFormFill = function (ordersValue, amountValue, period)
    {
        var descriptionVal = $('.total-val');
        descriptionVal.text(period);

        var ordersAmount = $('.orders-val');
        ordersAmount.text(ordersValue);
        var ordersText = $('.orders-text');
        ordersText.text('Orders');

        var amount = $('.amount-val');
        amount.text('$' + amountValue.toFixed(2));
        var amountText = $('.amount-text');
        amountText.text('Amount');
    };

    /* Generate initial data loading */
    purchaseFormFill(0, 0, months[currentMonth - 1]);

    var amountFormFill = function (smallAmount, smallAmountMonth, bigAmount, bigAmountMonth, average)
    {
        if (!isTurnOnDetails)
        {
            var bigValueAmt = $('.big-value-amt');
            bigValueAmt.text('$' + bigAmount.toFixed(2) + ' on ' + bigAmountMonth);

            var smallValueAmt = $('.small-value-amt');
            smallValueAmt.text('$' + smallAmount.toFixed(2) + ' on ' + smallAmountMonth);

            var avgValueAmt = $('.avg-value-amt');
            avgValueAmt.text('$' + average.toFixed(2) + '/month');
        }

    };

    amountFormFill(0, '', 0, '', 0);

    $('#monthCombobox').jqxComboBox({
        source: months,
        width: 150,
        height: 30,
        theme: theme,
        dropDownHeight: '115px',
        selectedIndex: currentMonth - 1
    });

    $('#monthCombobox').on('select', function (event)
    {
        var args = event.args;
        if (args)
        {
            var index = args.index;
            currentMonth = index + 1;
            refreshGrid();
            refreshPurchase();
        }
    });

    var refreshPurchase = function ()
    {
        var allMonthsMember = months.length;
        var orders = 0;
        var amountValue = 0;

        var source = {
            datatype: "json",
            datafields: [
                   { name: 'ShippedDate', type: 'date' },
                   { name: 'ShipAddress' },
                   { name: 'Customer', type: 'string' },
                   { name: 'Amount', type: 'number' }
            ],
            url: CONST_URL_PREFIX
        };
        var dataAdapter = new $.jqx.dataAdapter(source, {
            formatData: function (data)
            {
                $.extend(data, {
                    employeeid: getEmployeeID(),
                    month: getMonth(),
                    usedwidget: CONST_URL_SUFFIX.salesgrid
                });
                return data;
            },
            loadComplete: function (records)
            {
                var records = dataAdapter.records;

                orders = records.length;

                for (var j = 0; j < orders; j += 1)
                {
                    amountValue += records[j].Amount;
                }
                purchaseFormFill(orders, amountValue, months[currentMonth - 1]);
            }
        });
        dataAdapter.dataBind();
    };
    refreshPurchase();

    var refreshGrid = function ()
    {
        $("#personalSalesGrid").jqxGrid('updatebounddata', 'cells');
    };

    var refreshChart = function (isMonthSettings)
    {
        if (isMonthSettings)
        {
            sourceChart.datafields = [
                { name: 'OrderID', type: 'string' },
                {
                    name: 'Subtotal',
                    map: 'OrderTotal',
                    type: 'string'
                }
            ];
            isYearPiechartUsedwidget = false;
            dataAdapterChart.dataBind();
            chart.description = monthsNames[currentMonth].toUpperCase();
            isYearPiechartUsedwidget = true;
        } else
        {
            // Initial settings
            chart.description = messageChartDescription;
            chart.seriesGroups = [{
                type: 'pie',
                showLabels: true,
                xAxis:
                {
                    formatSettings: { prefix: 'OrderID ' }
                },
                series: [{
                    dataField: 'Subtotal',
                    displayText: 'OrderID',
                    labelRadius: '95%',
                    initialAngle: 15,
                    radius: '85%',
                    centerOffset: 0,
                    formatFunction: function (value, element)
                    {
                        return monthsNames[element] + ' $' + value.toFixed(2);
                    },
                }]
            }];
            sourceChart.datafields = [
                { name: 'OrderID', type: 'string' },
                { name: 'Subtotal' }
            ];
            dataAdapterChart.dataBind();
        }
    };

    var arrayOfGridOrdersData = [];
    var sourceGrid = {
        datatype: "json",
        datafields: [
               { name: 'ShippedDate', type: 'date' },
               { name: 'ShipAddress' },
               { name: 'Customer', type: 'string' },
               { name: 'Amount', type: 'number' }
        ],
        beforeprocessing: function (data)
        {
            if (data)
            {
                for (var item in data)
                {
                    arrayOfGridOrdersData[item] = data[item];
                }
            }
        },
        updaterow: function (rowid, rowdata, commit)
        {
            commit(true);
        },
        url: CONST_URL_PREFIX
    };
    var dataAdapterGrid = new $.jqx.dataAdapter(sourceGrid, {
        formatData: function (data)
        {
            $.extend(data, {
                employeeid: getEmployeeID(),
                month: getMonth(),
                usedwidget: CONST_URL_SUFFIX.salesgrid
            });
            return data;
        },
        autoBind: true
    });

    $('#personalSalesGrid').jqxGrid({
        width: '100%',
        theme: theme,
        autoheight: true,
        clipboard: false,
        altrows: true,
        rowsheight: 35,
        pagermode: 'simple',
        ready: function ()
        {
            var localizationobj = {};
            localizationobj.thousandsseparator = "";
            $("#personalSalesGrid").jqxGrid('localizestrings', localizationobj);

            messageChartDescription = "for more information please click";
        },
        source: dataAdapterGrid,
        columns: [
            {
                text: 'Date',
                datafield: 'ShippedDate',
                width: '15%',
                cellsformat: 'MMM dd yyyy',
                cellsalign: 'center'
            },
            {
                width: '35%',
                text: 'Ship Address',
                datafield: 'ShipAddress',
                cellsalign: 'center'
            },
            {
                width: '15%',
                text: 'Customer',
                datafield: 'Customer',
                cellsalign: 'center'
            },
            {
                width: '35%',
                text: 'Amount',
                datafield: 'Amount',
                cellsformat: 'c2',
                cellsalign: 'right'
            }
        ]
    });

    var sourceChart = {
        datatype: 'json',
        datafields: [
            { name: 'OrderID', type: 'string' },
            { name: 'OrderEmployeeId' },
            { name: 'OrderDate', type: 'date' },
            { name: 'Subtotal' }
        ],
        url: CONST_URL_PREFIX
    };
    var isYearPiechartUsedwidget = true;
    var dataAdapterChart = new $.jqx.dataAdapter(sourceChart, {
        formatData: function (data)
        {
            $.extend(data, {
                employeeid: getEmployeeID(),
                month: getMonth(),
                usedwidget: isYearPiechartUsedwidget ? CONST_URL_SUFFIX.yearpiechart : CONST_URL_SUFFIX.monthpiechart
            });

            return data;
        },
        beforeLoadComplete: function (records, original)
        {
            var bigAmount = -1;
            var bigAmountMonth = '';
            var smallAmount = Number.MAX_VALUE;
            var smallAmountMonth = '';
            var average = -1;
            var sumAmount = 0;
            // Because the field 'Subtotal' is a string and need to be normalized.
            var newArray = [];
            for (var i = 0; i < records.length; i++)
            {
                var currentItem = records[i];
                var currentItemValue = currentItem.Subtotal;
                if (currentItemValue > bigAmount)
                {
                    bigAmount = currentItemValue;
                    bigAmountMonth = monthsNames[currentItem.uid];
                }

                if (currentItemValue < smallAmount)
                {
                    smallAmount = currentItemValue;
                    smallAmountMonth = monthsNames[currentItem.uid];
                }

                sumAmount += currentItemValue;
                newArray.push(currentItem);
            }

            average = sumAmount / records.length
            amountFormFill(smallAmount, smallAmountMonth, bigAmount, bigAmountMonth, average);

            return newArray;
        }
    });

    var itemIndex = -1;
    var settingsChart = {
        title: " ",
        backgroundColor: 'transparent',
        titlePadding: {
            top: 15,
            left: 0, right: 0,
            bottom: 10
        },
        enableAnimations: false,
        showLegend: false,
        showBorderLine: false,
        source: dataAdapterChart,
        showToolTips: false,
        colorScheme: 'scheme01',
        seriesGroups: [{
            type: 'pie',
            showLabels: true,
            xAxis:
            {
                formatSettings: { prefix: 'OrderID ' }
            },
            series: [{
                dataField: 'Subtotal',
                displayText: 'OrderID',
                labelRadius: '95%',
                initialAngle: 15,
                radius: '85%',
                formatFunction: function (value, element)
                {
                    return monthsNames[element] + ' $' + value.toFixed(2);
                }
            }]
        }]
    };

    $('#personalSalesChart').jqxChart(settingsChart);
    var chart = $('#personalSalesChart').jqxChart('getInstance');

    var isTurnOnDetails = false;

    setTimeout(function ()
    {
        var selectFirstEmployee = 0;
        $("#dropdownlist").jqxDropDownList('selectIndex', selectFirstEmployee);
        var item = $("#dropdownlist").jqxDropDownList('getItem', selectFirstEmployee);
        if (!!item)
        {
            currentEmplyeeID = item.value;
        }
    }, 300);
});