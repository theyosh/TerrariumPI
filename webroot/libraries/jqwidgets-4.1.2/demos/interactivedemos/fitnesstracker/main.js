$(document).ready(function ()
{
    /*
     * Generate Personal Info
     *
     * @param {String} firstname - this person.
     * @param {String} lastname - of the same person.
     * @param {Number} height
     * @param {Number} age
     */
    function generatePersonalInfo(firstname, lastname, height, age)
    {
        var name = firstname + ' ' + lastname;

        var personContent = $('#person');
        var picture = $('<div/>');
        picture.addClass('personpicture');

        var personInfo = $('<div/>');
        personInfo.addClass('personinfo');

        var personName = $('<div/>');
        personName.addClass('fullname');
        personName.text(name);

        var personalCharacteristics = $('<div/>');
        personalCharacteristics.text(age + ' years / ' + height + ' cm');
        personInfo.append(personName);
        personInfo.append(personalCharacteristics);

        personContent.append(personInfo);
        personContent.append(picture);
    }

    generatePersonalInfo('Janet', 'Leverling', 165, 24, 'female');

    function getLastNumberFromTitle(title)
    {
        var number = -1;
        number = title.substr(title.indexOf('/') + 1) | 0;

        return number;
    }

    /**
     *
     * Create an instance of the BarGauge.
     *
     * @constructor
     * @param {String} id The name from DOM.
     * @param {Number} value
     * @param {String} color
     * @param {String} backgroundColor
     * @param {String} title
     * @param {String} subtitle
     * @param {Boolean} isHalf Determine geometry of the BarGauge.
     * @generate {Object} - BarGauge
     */
    function generateBarGauge(id, value, color, backgroundColor, title, subtitle, isHalf)
    {
        var endValue = getLastNumberFromTitle(title);
        isHalf = isHalf || false;
        $('#' + id).jqxBarGauge({
            width: "100%",
            height: 300,
            min: 0,
            max: endValue,
            useGradient: false,
            backgroundColor: backgroundColor,
            customColorScheme: {
                name: 'newScheme',
                colors: [color]
            },
            colorScheme: 'newScheme',
            relativeInnerRadius: 0.8,
            geometry: {
                startAngle: isHalf ? 180 : 90,
                endAngle: isHalf ? 0 : 90
            },
            labels: { precision: 0, indent: 10 },
            title: {
                text: title,
                font: { size: 20 },
                verticalAlignment: 'bottom',
                margin: { top: 0, bottom: 5 },
                subtitle: {
                    text: subtitle,
                    font: { size: 13 }
                }
            },
            values: value
        });
    }

    //              (id,          value,color,     bgColor,   title,                      subtitle,               isHalf)
    generateBarGauge('bargauge1', [0], '#3AB54B', '#B0D2C8', 'Calories intake - 0/2200', '2200 calories pending', true);
    generateBarGauge('bargauge2', [0], '#B24848', '#C9A5A6', 'Calories burnt - 0/1000', '1000 calories pending', true);
    generateBarGauge('bargauge3', [0], '#D2AACE', '#DBCDDC', 'Exercises - 0/7', '7 sets pending');
    generateBarGauge('bargauge4', [0], '#978CC2', '#CBCBE0', 'Sets - 0/4', '10 sets pending');

    var sourceGauges =
    {
        url: "data.php?usedwidget=bargauges",
        datatype: "json"
    };

    var changesBarGauge = function (id, titleText, subtitleText, values)
    {
        $('#' + id).jqxBarGauge({
            title: { text: titleText, subtitle: subtitleText },
            values: values
        });
    };

    var dataAdapterGauges = new $.jqx.dataAdapter(sourceGauges, {
        loadComplete: function (records)
        {
            changesBarGauge('bargauge1', 'Calories intake - ' + records[0].now + '/' + records[0].total, (records[0].total - records[0].now) + ' calories pending', [records[0].now]);
            changesBarGauge('bargauge2', 'Calories burnt - ' + records[1].now + '/' + records[1].total, (records[1].total - records[1].now) + ' calories pending', [records[1].now]);
            changesBarGauge('bargauge3', 'Exercises - ' + records[2].now + '/' + records[2].total, (records[2].total - records[2].now) + ' exercises pending', [records[2].now]);
            changesBarGauge('bargauge4', 'Sets - ' + records[3].now + '/' + records[3].total, (records[3].total - records[3].now) + ' sets pending', [records[3].now]);
        }
    });
    dataAdapterGauges.dataBind();

    /**
     * Start the Chart (Donut) initialization
     */
    // Create initial data. Prevent visualization
    var dataDonut = [
        { "name": "Fat", "value": 0 },
        { "name": "Protein", "value": 0 },
        { "name": "Carb", "value": 0 }
    ];

    var sourceDonut = {
        datatype: "array",
        datafields: [
               { name: 'name' },
               { name: 'value' }
        ],
        localdata: dataDonut
    };

    var dataAdapterDonut = new $.jqx.dataAdapter(sourceDonut);

    var settingsDonut = {
        title: "",
        description: "",
        showToolTips: true,
        enableAnimations: false,
        showLegend: true,
        showBorderLine: false,
        source: dataAdapterDonut,
        seriesGroups: [{
            type: 'donut',
            showLabels: true,
            colorScheme: 'scheme04',
            useGradient: false,
            series: [{
                dataField: 'value',
                displayText: 'name',
                labelRadius: '100%',
                initialAngle: 30,
                radius: '80%',
                innerRadius: '45%',
                centerOffset: 0,
                formatSettings: { sufix: ' (g)', decimalPlaces: 0 }
            }]
        }]
    };
    $("#chartDonut").jqxChart(settingsDonut);

    /**
     * Start the Grid (Food) initialization
     */
    var theme = 'light';

    var sourceFoodGrid =
    {
        url: "data.php?usedwidget=foodgrid",
        datatype: "json",
        datafields:
        [
            { name: 'time', type: 'date', format: 'HH:mm' },
            { name: 'food', type: 'string' },
            { name: 'fat', type: 'number' },
            { name: 'carb', type: 'number' },
            { name: 'protein', type: 'number' },
            { name: 'calories', type: 'number' }
        ],
        sortcolumn: 'food',
        sortdirection: 'asc',
        updaterow: function (rowid, rowdata, commit)
        {
            commit(true);
        }
    };

    var dataAdapterFoodGrid = new $.jqx.dataAdapter(sourceFoodGrid);

    var updateDonut = function ()
    {
        var fatSum = $("#foodGridValues").jqxGrid('getcolumnaggregateddata', 'fat', ['sum']).sum;
        var carbSum = $("#foodGridValues").jqxGrid('getcolumnaggregateddata', 'carb', ['sum']).sum;
        var proteinSum = $("#foodGridValues").jqxGrid('getcolumnaggregateddata', 'protein', ['sum']).sum;
        var newSource = [
            { "name": "Fat", "value": fatSum || 0.1 },
            { "name": "Protein", "value": proteinSum || 0.1 },
            { "name": "Carb", "value": carbSum || 0.1 }
        ];
        $("#chartDonut").jqxChart({ source: newSource });
        $('#chartDonut').jqxChart('update');
    };

    var setBargaugeCalories = function ()
    {
        // Set new value
        var totalCalories = $("#foodGridValues").jqxGrid('getcolumnaggregateddata', 'calories', ['sum']).sum;
        if (!totalCalories) totalCalories = 0;
        $('#bargauge1').jqxBarGauge('val', [totalCalories]);
        
        if (totalCalories > 2700) {
            changesBarGauge('bargauge1', 'Calories intake - ' + totalCalories + '/' + 2700,  '0 calories pending', [totalCalories]);
        }
        else {
            changesBarGauge('bargauge1', 'Calories intake - ' + totalCalories + '/' + 2700, (2700 - totalCalories) + ' calories pending', [totalCalories]);
        }
    };

    $('#foodGridValues').on('bindingcomplete', function ()
    {
        setBargaugeCalories();
    });

    var addMealToGrid = function (row, foodObject)
    {
        $('#foodGridValues').jqxGrid('addrow', row, foodObject);
        setBargaugeCalories();
    };

    var deleteSelectedRow = function ()
    {
        var selectedrowindex = $("#foodGridValues").jqxGrid('getselectedrowindex');
        var rowscount = $("#foodGridValues").jqxGrid('getdatainformation').rowscount;
        if (selectedrowindex >= 0 && selectedrowindex < rowscount)
        {
            var id = $("#foodGridValues").jqxGrid('getrowid', selectedrowindex);
            var commit = $("#foodGridValues").jqxGrid('deleterow', id);
        }
        setBargaugeCalories();
    };

    var getDataIntakeBurn = function (array)
    {
        var length = array.length;
        // Prevent the Chart from empty visualization.
        var totalIntake = 0.01;
        var totalBurn = 0.01;
        var total = {};
        var totalCalories = [];
        for (var i = 0; i < length; i++)
        {
            if (array[i].set)
            {
                totalIntake += array[i].intake;
                totalBurn += array[i].burn;
            }
        }

        totalCalories.push({ calories: totalIntake, type: 'Intake' });
        totalCalories.push({ calories: totalBurn, type: 'Burn' });
        return totalCalories;
    };

    $("#foodGridValues").jqxGrid(
    {
        width: '95%',
        theme: theme,
        autoHeight: true,
        showstatusbar: true,
        statusbarheight: 25,
        source: dataAdapterFoodGrid,
        showaggregates: true,
        ready: function ()
        {
            updateDonut();
        },
        columns: [
            {
                text: 'Time',
                datafield: 'time',
                width: '10%',
                cellsformat: 'HH:mm',
                cellsalign: 'center',
            },
            {
                text: 'Food Type', datafield: 'food',
                width: '20%',
                cellsalign: 'center',
            },
            {
                text: 'Fat', datafield: 'fat', width: '15%',
                filtertype: 'number', cellsalign: 'right', cellsformat: 'f2',
                aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }]
            },
            {
                text: 'Carbs', datafield: 'carb', filtertype: 'number', cellsalign: 'right', cellsformat: 'f2',
                aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }]
            },
            {
                text: 'Protein', datafield: 'protein', filtertype: 'number', cellsalign: 'right', cellsformat: 'f2',
                aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }]
            },
            {
                text: 'Calories', datafield: 'calories', filtertype: 'number', cellsalign: 'right', cellsformat: 'f2',
                aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }]
            },
            {
                text: '', datafield: '', columntype: 'button', width: '5%',
                cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                {
                    return "X";
                },
                buttonclick: function (row)
                {
                    deleteSelectedRow();
                    updateDonut();
                }
            }
        ]
    });

    var addMealSource = {
        url: "data.php?usedwidget=fooddropdown",
        datatype: "json",
        datafields:
        [
            { name: 'food', type: 'string' },
            { name: 'fat', type: 'number' },
            { name: 'carb', type: 'number' },
            { name: 'protein', type: 'number' },
            { name: 'calories', type: 'number' }
        ],
        updaterow: function (rowid, rowdata, commit)
        {
            commit(true);
        }
    };

    $('#addMeal').jqxButton({ disabled: true, width: 60, height: 25, theme: theme });
    var newMealDropdownAdapter = new $.jqx.dataAdapter(addMealSource);
    $("#newMealDropdown").jqxDropDownList({ placeHolder: "Please Choose Meal:", autoDropDownHeight: true, source: newMealDropdownAdapter, selectedIndex: -1, width: '30%', height: 23, theme: theme, displayMember: "food" });
    var selctedFood = {};
    $('#newMealDropdown').on('select', function (event)
    {
        var args = event.args;
        if (args)
        {
            $('#addMeal').jqxButton({ disabled: false });
            var records = newMealDropdownAdapter.getrecords();
            var index = args.index;
            var item = args.item;
            var label = item.label;
            var value = item.value;
            var type = args.type;
            selctedFood = records[index];
        }
    });

    var deepCopyOfFood = function (food, time)
    {
        var newFood = {};
        for (var item in food)
        {
            newFood[item] = food[item];
        }
        newFood.time = time;
        return newFood;
    }

    $('#addMeal').click(function ()
    {
        var isEmptyFoodObject = Object.getOwnPropertyNames(selctedFood).length === 0;
        if (!isEmptyFoodObject)
        {
            var length = newMealDropdownAdapter.getrecords().length;
            var lastRowId = length - 1;
            var currentDateTime = new Date();
            var minutes = currentDateTime.getMinutes();
            var time = '' + currentDateTime.getHours() + ':' + ((minutes < 10) ? '0' + minutes : minutes);
            var foodObject = deepCopyOfFood(selctedFood, time);
            addMealToGrid(lastRowId, foodObject);
            updateDonut();
        }
    });

    /* - Start Second ROW [the Pie Chart and the Grid] - */

    /**
     * Start the Grid (Calories) initialization with checkboxes
     */
    var caloriesSource = {
        datatype: "json",
        datafields: [
            { name: 'date', type: 'date', format: 'dd/MM/yyyy' },
            { name: 'intake', type: 'number' },
            { name: 'burn', type: 'number' },
            { name: 'set', type: 'bool' }
        ],
        url: "data.php?usedwidget=dailycaloriesgrid"
    };

    var caloriesAdapter = new $.jqx.dataAdapter(caloriesSource, {
        beforeLoadComplete: function (records)
        {
            var data = new Array();
            for (var i = 0; i < records.length; i++)
            {
                var dateBalance = records[i];
                var set = true;
                // Check calories are more than 2000 cal.
                set = dateBalance.intake >= 2000 ? true : false;
                dateBalance.set = set;
                data.push(dateBalance);
            }
            return data;
        }
    });

    // Prevent visualization
    var dailyCalories = [{ calories: 0, type: 'intake' }, { calories: 0, type: 'burn' }];
    $('#dailyCaloriesGrid').jqxGrid({
        width: '95%',
        theme: theme,
        autoHeight: true,
        editable: true,
        source: caloriesAdapter,
        showstatusbar: true,
        statusbarheight: 25,
        showaggregates: true,
        ready: function ()
        {
            var rows = $('#dailyCaloriesGrid').jqxGrid('getboundrows');
            dailyCalories = getDataIntakeBurn(rows);
            $('#piechart').jqxChart({ source: dailyCalories });
        },
        columns: [
            { text: 'Set', datafield: 'set', width: '10%', columntype: 'checkbox', filtertype: 'bool', editable: true },
            {
                text: 'Date',
                datafield: 'date',
                width: '20%',
                editable: false,
                cellsformat: 'ddd d/MM/yy',
                cellsalign: 'center'
            },
            {
                text: 'Intake', datafield: 'intake', width: '35%', cellsalign: 'center', editable: false, aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }],
            },
            { text: 'Burn', datafield: 'burn', width: '35%', cellsalign: 'center', editable: false, aggregates: [{ '<b>Total</b>': function (aggregatedValue, currentValue, column, record) { return aggregatedValue + currentValue; } }] }
        ]
    });

    var stopAnimation = true;
    $("#dailyCaloriesGrid").on('cellvaluechanged', function (event)
    {
        var rows = $('#dailyCaloriesGrid').jqxGrid('getboundrows');
        dailyCalories = getDataIntakeBurn(rows);
        if (stopAnimation)
        {
            $('#piechart').jqxChart({ enableAnimations: false });
        }

        $('#piechart').jqxChart({ source: dailyCalories });
        stopAnimation = false;
    });

    /**
     * Start the Pie Chart initialization
     */
    var intakeBurnSource = {
        datatype: "array",
        datafields: [
            { name: 'calories' },
            { name: 'type' }
        ],
        localdata: dailyCalories
    };

    var intakeBurnAdapter = new $.jqx.dataAdapter(intakeBurnSource, {
        autoBind: true,
        async: false
    });

    var intakeBurnSettings = {
        backgroundColor: 'transparent',
        source: intakeBurnAdapter,
        colorScheme: 'scheme02',
        title: '',
        description: '',
        showLegend: true,
        showToolTips: true,
        showBorderLine: false,
        seriesGroups: [{
            type: 'pie',
            showLabels: true,
            useGradient: false,
            series: [{
                dataField: 'calories', displayText: 'type',
                labelRadius: 30,
                initialAngle: 90,
                radius: '80%',
                centerOffset: 3,
                formatSettings: { sufix: '', decimalPlaces: 0 }
            }]
        }]
    };

    $('#piechart').jqxChart(intakeBurnSettings);

    // Calories Chart
    var caloriesSource = {
        datatype: "json",
        datafields: [
            { name: 'date', type: 'date', format: 'dd/MM/yyyy' },
            { name: 'intake', type: 'number' },
            { name: 'burn', type: 'number' },
            { name: 'set', type: 'bool' }
        ],
        url: "data.php?usedwidget=dailycalorieschart"
    };

    var caloriesAdapter = new $.jqx.dataAdapter(caloriesSource);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var caloriesSettings = {
        title: "",
        description: "",
        enableAnimations: true,
        showLegend: true,
        animationDuration: 1000,
        borderLineWidth: 0,
        enableCrosshairs: true,
        padding: { left: 5, top: 5, right: 20, bottom: 5 },
        colorScheme: 'scheme02',
        source: caloriesAdapter,
        xAxis:
        {
            dataField: 'date',
            displayText: 'Date',
            type: 'date',
            baseUnit: 'day',
            minValue: new Date(2016, 1, 1),
            maxValue: new Date(2016, 1, 17),
            flip: false,
            valuesOnTicks: true,
            labels:
            {
                angle: -90, offset: { x: 0, y: 0 },

                formatFunction: function (value)
                {
                    return value.getDate() + '-' + months[value.getMonth()] + '-' + value.getFullYear();
                }
            }
        },
        seriesGroups:
        [
            {
                type: 'line',
                valueAxis:
                {
                    flip: false,
                    title: { text: 'Calories<br><br>' }
                },
                series: [
                    {
                        dataField: 'intake',
                        displayText: 'Intake',
                        lineWidth: 3,
                        lineWidthSelected: 1
                    },
                    {
                        dataField: 'burn',
                        displayText: 'Burn',
                        lineWidth: 3,
                        lineWidthSelected: 1
                    }
                ]
            }
        ]
    };

    $('#chartCalories').jqxChart(caloriesSettings);

    /// Start the last Chart - "Nutritional Values"
    var nutritionalData = [
        { Date: '12/02/2016', fat: 4, carb: 35, protein: 10 },
        { Date: '13/02/2016', fat: 2, carb: 14, protein: 15 },
        { Date: '14/02/2016', fat: 1.8, carb: 24, protein: 11 }
    ];

    var nutritionalSource =
    {
        datatype: "json",
        datafields: [
            { name: 'Date', type: 'date', format: 'dd/MM/yyyy' },
            { name: 'fat' },
            { name: 'carb' },
            { name: 'protein' }
        ],
        url: "data.php?usedwidget=calorieschart"
    };

    var nutritionalAdapter = new $.jqx.dataAdapter(nutritionalSource);

    var settings = {
        title: "",
        description: "",
        colorScheme: 'scheme04',
        source: nutritionalAdapter,
        borderLineWidth: 0,
        enableAnimations: true,
        categoryAxis: {
            dataField: '',
            description: '',
            showGridLines: true,
            showTickMarks: true
        },
        seriesGroups: [{
            useGradient: false,
            type: 'column',
            xAxis: {
                dataField: 'Date',
                type: 'date',
                baseUnit: 'day',
                labels: { angle: -45, offset: { x: -17, y: 0 } }
            },
            valueAxis: {
                description: 'Calories',
                logarithmicScale: true,
                logarithmicScaleBase: 2,
                unitInterval: 1,
                gridLinesInterval: 1
            },
            series: [{
                dataField: 'fat',
                displayText: 'Fat'
            }, {
                dataField: 'protein',
                displayText: 'Protein'
            }, {
                dataField: 'carb',
                displayText: 'Carbohydrate'
            }]
        }]
    };

    $('#nutritionalValues').jqxChart(settings);
});