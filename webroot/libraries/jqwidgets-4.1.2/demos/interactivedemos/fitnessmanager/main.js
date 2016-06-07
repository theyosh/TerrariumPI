$(document).ready(function ()
{
    'use strict';

    var response = new $.jqx.response();
    response.responsive({
        container: $("#row"),
        deviceTypes: "Desktop, Tablet, Phone",
        margin: { left: 0, top: 0, right: 0,  bottom: 0 },
        padding: { left: 0, top: 0, right: 0, bottom: 0 },
        colWidths: [0.8],
        colOffsets: [0.1],
        colClass: "big",
        breakpoints: [{
            colClass: "big",
            colWidths: [1],
            colOffsets: [0],
            width: 1440
        }, {
            colClass: "small",
            colWidths: [1],
            colOffsets: [0],
            width: 1200
        }]
    });

    var source = [{
        label: "Dashboard"
    }, {
        label: "Schedules",
        items: [{
            label: "Rooms"
        }, {
            label: "Instructors"
        }]
    },{
        label: "Fitness instructors"
    }, {
        label: "Workload chart"
    }, {
        label: "Administrative tasks"
    }, {
        label: "Quick notes"
    }];

    $("#jqxMenu").jqxMenu({
        source: source,
        width: 680,
        theme: 'light'
    });

    var minimized = false;
    if (document.documentElement.clientWidth < 890)
    {
        $("#jqxMenu").jqxMenu('minimize');
        minimized = true;
    }

    $(window).on("resize", function ()
    {
        if ((document.documentElement.clientWidth < 890)&& (minimized === false))
        {
            $("#jqxMenu").jqxMenu('minimize');
            minimized = true;
        } else if((document.documentElement.clientWidth >= 890) && (minimized === true))
        {
            $("#jqxMenu").jqxMenu('restore');
            minimized = false;
        }
    });

    $('#jqxMenu').on('itemclick', function (event)
    {
        var element = event.args;
        var label = $(element).attr("item-label");

        if (label !== "Schedules")
        {
            $(".page").addClass("page-hidden");
            if (label==="Dashboard")
            {
                $("#page1").removeClass("page-hidden");
                $("#page").html('Dashboard');
                dashboard();
            }

            switch(label){
                case 'Dashboard':
                    $("#page1").removeClass("page-hidden");
                    $("#page").html('Dashboard');
                    break;
                case 'Rooms':
                    $("#page2").removeClass("page-hidden");
                    $("#page").html('Rooms schedules');
                    roomsSheduler();
                    break;
                case 'Instructors':
                    $("#page3").removeClass("page-hidden");
                    $("#page").html('Instructors schedules');
                    instructorsSheduler();
                    break;
                case 'Fitness instructors':
                    $("#page5").removeClass("page-hidden");
                    $("#page").html('Fitness instructors list');
                    instructorsGrid();
                    break;
                case 'Workload chart':
                    $("#page6").removeClass("page-hidden");
                    $("#page").html('Workload chart of the fitness instructors');
                    workloadChartTreeTagcloud();
                    break;
                case 'Administrative tasks':
                    $("#page7").removeClass("page-hidden");
                    $("#page").html('Administrative tasks');
                    tasksKanban();
                    break;
                case 'Quick notes':
                    $("#page8").removeClass("page-hidden");
                    $("#page").html('Quick notes');
                    quickNotesListBox();
                    break;
                default:
                    $("#page1").removeClass("page-hidden");
                    $("#page").html('Dashboard');
                    dashboard();
   
            }
        }
    });

    var dockingWindows = ['window1', 'window2', 'window4'];
    $('#docking').jqxDocking({ theme: 'light', orientation: 'horizontal', width: '100%', mode: 'docked' });
    for (var i = 0; i < dockingWindows.length; i++)
    {
        $('#docking').jqxDocking('disableWindowResize', dockingWindows[i]);
    }

    var listBoxSource = [
        'Repair of broken gym equipment',
        'Staff recruitment',
        'Instructors course',
        'Buy a new bench press'];
    $('#dashboardListbox').jqxListBox({
        source: listBoxSource, width: "100%", height: "100%", theme: 'light', renderer: function (index)
        {
            var datarecord = listBoxSource[index];
            return "<div style='padding:10px 10px 10px 20px;'>" + datarecord + "</div>";
        }
    });

    function dashboard()
    {
        if ($("#hours").hasClass("jqx-widget")===false)
        {
        var selectedThermometer = 1;

        function createTemperatureKnob()
        {
            $('#themperatureKnob').jqxKnob({
                width: 330,
                height: 330,
                value: 16,
                min: 15,
                max: 95,
                startAngle: 120,
                endAngle: 420,
                snapToStep: true,
                rotation: 'clockwise',
                style: { stroke: '#dfe3e9', strokeWidth: 3, fill: { color: '#fefefe', gradientType: "linear", gradientStops: [[0, 1], [50, 0.9], [100, 1]] } },
                marks: {
                    colorRemaining: { color: 'grey', border: 'grey' },
                    colorProgress: { color: '#00a4e1', border: '#00a4e1' },
                    type: 'line',
                    offset: '71%',
                    thickness: 3,
                    size: '6%',
                    majorSize: '9%',
                    majorInterval: 10,
                    minorInterval: 2
                },
                labels: {
                    offset: '88%',
                    step: 10,
                    visible: true
                },
                progressBar: {
                    style: { fill: '#00a4e1', stroke: 'grey' },
                    size: '9%',
                    offset: '60%',
                    background: { fill: 'grey', stroke: 'grey' }
                },
                pointer: { type: 'arrow', style: { fill: '#00a4e1', stroke: 'grey' }, size: '59%', offset: '49%', thickness: 20 }
            });

            $('#themperatureKnob').on('change', function ()
            {
                var colorScheme = 'scheme02';
                var textCondition = '<div style="text-align: center; color: green; font-size: 10px;">Temp. in range</div>';
                var newValue = $('#themperatureKnob').val();
                var gaugesValueForComparisson = $('#gauge' + selectedThermometer).jqxLinearGauge("val");

                if ((newValue - 1.5) > gaugesValueForComparisson)
                {
                    colorScheme = 'scheme01';
                    textCondition = '<div style="text-align: center; color: blue; font-size:10px;">Low temp.</div>';
                } else if ((newValue + 2.5) < gaugesValueForComparisson)
                {
                    colorScheme = 'scheme03';
                    textCondition = '<div style="text-align: center; color: red; font-size: 10px; ">High temp.</div>';
                }

                $('#gauge' + selectedThermometer).parent().find(".temperatureText").html(textCondition);
                $('#gauge' + selectedThermometer).jqxLinearGauge({
                    colorScheme: colorScheme,
                    ranges: [
                        { startValue: (newValue - 1.5), endValue: (newValue + 2.5), style: { fill: '#FFA200', stroke: '#FFA200', opacity: 0.5, 'stroke-width': 8 } },
                        { startValue: newValue, endValue: (newValue + 0.5), style: { fill: '#0000FF', stroke: '#0000FF', opacity: 0.5, 'stroke-width': 8 } }
                    ]
                });
            });
        }

        function createTemperatureThermometer()
        {
            var majorTicks = { size: '10%', interval: 5 },
                minorTicks = { size: '5%', interval: 1, style: { 'stroke-width': 1, stroke: '#aaaaaa' } },
                labels = { interval: 20 };

            function createLinearGaugeThermometer(gaugeId, colorScheme, startVal1, endVal1, startVal2, endVal2)
            {
                $('#' + gaugeId).jqxLinearGauge({
                    rangesOffset: 5,
                    width: "100%",
                    orientation: 'vertical',
                    labels: labels,
                    ticksMajor: majorTicks,
                    ticksMinor: minorTicks,
                    max: 95,
                    min: 0,
                    value: 0,
                    pointer: { size: '6%' },
                    colorScheme: colorScheme,
                    ranges: [
                    { startValue: startVal1, endValue: endVal1, style: { fill: '#FFA200', stroke: '#FFA200', opacity: 0.5, 'stroke-width': 8 } },
                    { startValue: startVal2, endValue: endVal2, style: { fill: '#0000FF', stroke: '#0000FF', opacity: 0.5, 'stroke-width': 8 } }]
                });
            }

            createLinearGaugeThermometer('gauge1', 'scheme01', 18, 22, 19.5, 20);
            createLinearGaugeThermometer('gauge2', 'scheme02', 16, 20, 17.5, 18);
            createLinearGaugeThermometer('gauge3', 'scheme03', 80, 86, 82.5, 83);

            $('#gauge1').parent().addClass("linear-gauge-selected");
            $('#gauge1').jqxLinearGauge('value', 16);
            $('#gauge2').jqxLinearGauge('value', 19);
            $('#gauge3').jqxLinearGauge('value', 90);

            $("#jqxRadioButton1").jqxRadioButton({ theme: 'light', width: 100, height: 25, checked: true });
            $("#jqxRadioButton2").jqxRadioButton({ theme: 'light', width: 100, height: 25 });
            $("#jqxRadioButton3").jqxRadioButton({ theme: 'light', width: 100, height: 25 });

            $('.themperatureRadioButton').on('checked', function ()
            {
                var idNumber = $(this).attr("id").slice(-1);
                $('#gauge1, #gauge2, #gauge3').parent().removeClass("linear-gauge-selected");
                $('#gauge' + idNumber).parent().addClass("linear-gauge-selected");
                selectedThermometer = idNumber;
                var ranges = $('#gauge' + idNumber).jqxLinearGauge('ranges');
                $('#themperatureKnob').jqxKnob('val', ranges[1].startValue);
            });
        }

        createTemperatureKnob();
        createTemperatureThermometer();
    }
}

    dashboard();
    
    function roomsSheduler(){
        if (!$("#roomsSheduler").hasClass("jqx-widget"))
        {
            var source =
            {
                dataType: "json",
                dataFields: [
                    { name: 'id', type: 'string' },
                    { name: 'description', type: 'string' },
                    { name: 'location', type: 'string' },
                    { name: 'subject', type: 'string' },
                    { name: 'calendar', type: 'string' },
                    { name: 'start', type: 'date', format: "yyyy-MM-dd HH:mm" },
                    { name: 'end', type: 'date', format: "yyyy-MM-dd HH:mm" }
                ],
                id: 'id',
                url: "data.php?usedwidget=roomsscheduler"
            };

            var adapter = new $.jqx.dataAdapter(source);

            $("#roomsSheduler").jqxScheduler({
                date: new $.jqx.date(2015, 11, 23),
                width: "100%",
                height: window.innerHeight - 150,
                theme: 'light',
                source: adapter,
                view: 'weekView',
                appointmentOpacity: 0.7,
                showLegend: true,
                ready: function ()
                {
                    $("#roomsSheduler").jqxScheduler('ensureAppointmentVisible', 'id2');
                },
                resources:
                {
                    colorScheme: "scheme05",
                    dataField: "calendar",
                    source: new $.jqx.dataAdapter(source)
                },
                appointmentDataFields:
                {
                    from: "start",
                    to: "end",
                    id: "id",
                    description: "description",
                    location: "place",
                    subject: "subject",
                    resourceId: "calendar"
                },
                views: ['weekView']
            });
        }
    }

    function instructorsSheduler()
    {
        if (!$("#instructorsSheduler").hasClass("jqx-widget"))
        {
            var source =
            {
                dataType: "json",
                dataFields: [
                    { name: 'id', type: 'string' },
                    { name: 'description', type: 'string' },
                    { name: 'location', type: 'string' },
                    { name: 'subject', type: 'string' },
                    { name: 'calendar', type: 'string' },
                    { name: 'start', type: 'date', format: "yyyy-MM-dd HH:mm" },
                    { name: 'end', type: 'date', format: "yyyy-MM-dd HH:mm" }
                ],
                id: 'id',
                url: "data.php?usedwidget=instructorsscheduler"
            };

            var adapter = new $.jqx.dataAdapter(source);

            $("#instructorsSheduler").jqxScheduler({
                date: new $.jqx.date(2015, 11, 23),
                width: "100%",
                height: window.innerHeight - 150,
                theme: 'light',
                source: adapter,
                view: 'weekView',
                appointmentOpacity: 0.7,
                showLegend: true,
                ready: function ()
                {
                    $("#instructorsSheduler").jqxScheduler('ensureAppointmentVisible', 'id2');
                },
                resources:
                {
                    colorScheme: "scheme05",
                    dataField: "calendar",
                    source: new $.jqx.dataAdapter(source)
                },
                appointmentDataFields:
                {
                    from: "start",
                    to: "end",
                    id: "id",
                    description: "description",
                    location: "place",
                    subject: "subject",
                    resourceId: "calendar"
                },
                views:['weekView']
            });
        }
    }

    function instructorsGrid()
    {
        if (!$("#instructorsGrid").hasClass("jqx-widget"))
        {
            var source = {
                datatype:'json',
                datafields: [
                    { name: "id", type: "string" },
                    { name: "lastname", type: "string" },
                    { name: "firstname", type:"string" },
                    { name: "phone", type: "string" },
                    { name: "image", type: "string" }
                ],
                url: "data.php?usedwidget=instructorsgrid"
            };

            var dataAdapter = new $.jqx.dataAdapter(source);

            $("#instructorsGrid").jqxGrid({
                width: "100%",
                autoheight:true,
                theme:"light",
                rowsheight: 110,
                showheader: false,
                source: dataAdapter,
                columns: [
                    {
                        text: 'Picture', datafield: 'image', width:110,
                        createwidget: function (row, column, value, htmlElement)
                        {
                            var img = '<img style="margin: 10px;" height="90" width=90" src="' + value + '"/>';
                            $(htmlElement).append(img);
                        },
                        initwidget: function (){ }
                    },
                    { text: 'First Name', datafield: 'firstname', width: 100, cellsalign:"center", cellclassname: "instructors-grid-cell" },
                    { text: 'Last Name', datafield: 'lastname', width: 100, cellsalign: "center", cellclassname: "instructors-grid-cell" },
                    { text: 'Phone', datafield: 'phone', cellsalign: "center", cellclassname: "instructors-grid-cell" }
                ]
            });
        }
    }

    function workloadChartTreeTagcloud()
    {
        if (!$("#jqxChart").hasClass("jqx-widget"))
        {
        var workloadResponse = new $.jqx.response();
        workloadResponse.responsive({
            container: $("#workloadResponsiveContainer"),
            deviceTypes: "Desktop, Tablet, Phone",
            margin: {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            },
            padding: {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            },
            colWidths: [0.3, 0.7],
            colClass: "workloadBig",
            breakpoints: [{
                colClass: "workloadSmall",
                colWidths: [1, 1],
                width: 500
            }]
        });

        var source =
        {
            datatype: "json",
            datafields: [
                { name: 'id' },
                { name: 'parentid' },
                { name: 'text' },
                { name: 'html' },
                { name: 'value' },
                { name: 'icon' }
            ],
            id: 'id',
            url: "data.php?usedwidget=workloadtree"
        };

        var dataAdapter = new $.jqx.dataAdapter(source, {
            loadComplete: function ()
            {
                var records1 = dataAdapter.getRecordsHierarchy('id', 'parentid', 'items',[{ name: 'text', map: 'label' }]);
                $('#jqxTree').jqxTree({ theme: 'light', source: records1, allowDrag: false, width: '100%' });
            }
        });
        dataAdapter.dataBind();
        $('#instructorsJqxExpander').jqxExpander({ theme: 'light', showArrow: false, toggleMode: 'none', width: '100%', height: window.innerHeight - 150 });

        var tagCloudSource =
        {
            datatype: "json",
            datafields: [
                { name: 'fitnessInstructorName' },
                { name: 'clientsPerWeek' }
            ],
            url: "data.php?usedwidget=workloadtaglloud"
        };
        var tagCloudDataAdapter = new $.jqx.dataAdapter(tagCloudSource);
        $('#jqxTagCloud').jqxTagCloud({
            width: '100%',
            source: tagCloudDataAdapter,
            displayMember: 'fitnessInstructorName',
            theme: 'light',
            valueMember: 'clientsPerWeek',
            minFontSize: 12,
            maxFontSize: 56,
            minColor: '#00AA99',
            maxColor: '#FF0000'
        });

        var chartSource =
        {
            datatype: "json",
            datafields: [
                { name: 'Day' },
                { name: 'Andrew' },
                { name: 'Nancy' },
                { name: 'Janet' },
                { name: 'Margaret' }
            ],
            url: "data.php?usedwidget=workloadchart"
        };
        var chartDataAdapter = new $.jqx.dataAdapter(chartSource);
        var jqxChartSettings = {
            title: "",
            description: "",
            enableAnimations: true,
            showBorderLine: false,
            showLegend: true,
            padding: { left: 10, top: 10, right: 15, bottom: 10 },
            titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
            source: chartDataAdapter,
            colorScheme: 'scheme05',
            xAxis: {
                dataField: 'Day',
                unitInterval: 1,
                tickMarks: { visible: true, interval: 1 },
                valuesOnTicks: false,
                padding: { bottom: 10 },
                gridLines: {
                    visible: false
                }
            },
            valueAxis: {
                unitInterval: 1,
                minValue: 0,
                maxValue: 5,
                title: { text: 'Clients per day<br><br>' },
                labels: { horizontalAlignment: 'right' },
                gridLines: {
                    visible: false
                }
            },
            seriesGroups:
                [
                    {
                        type: 'line',
                        series:
                        [
                            {
                                dataField: 'Andrew',
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
                                dataField: 'Nancy',
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
                                dataField: 'Janet',
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
                                dataField: 'Margaret',
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

        $('#jqxChart').jqxChart(jqxChartSettings);
        }
    }

    function tasksKanban()
    {
        if (!$("#jqxKanban").hasClass("jqx-widget"))
        {
            var source =
             {
                 dataType: "json",
                 dataFields: [
                         { name: "id", type: "string" },
                         { name: "status", map: "state", type: "string" },
                         { name: "text", map: "label", type: "string" },
                         { name: "tags", type: "string" },
                         { name: "color", map: "hex", type: "string" },
                         { name: "resourceId", type: "number" }
                 ],
                 url: "data.php?usedwidget=taskskanban"
             };
            var dataAdapter = new $.jqx.dataAdapter(source);
            var resourcesAdapterFunc = function ()
            {
                var resourcesSource =
                {
                    dataType: "json",
                    dataFields: [
                         { name: "id", type: "number" },
                         { name: "name", type: "string" },
                         { name: "image", type: "string" },
                         { name: "common", type: "boolean" }
                    ],
                    url: "data.php?usedwidget=taskskanbanusers"
                };
                var resourcesDataAdapter = new $.jqx.dataAdapter(resourcesSource);
                return resourcesDataAdapter;
            };

            var getIconClassName = function ()
            {
                return "jqx-icon-plus-alt";
            };

            $('#jqxKanban').jqxKanban({
                template: "<div class='jqx-kanban-item' id=''>" +
                    "<div class='jqx-kanban-item-color-status'></div>" +
                    "<div style='display: none;' class='jqx-kanban-item-avatar'></div>" +
                    "<div class='jqx-icon jqx-icon-close jqx-kanban-item-template-content jqx-kanban-template-icon'></div>" +
                    "<div class='jqx-kanban-item-text'></div>" +
                    "<div style='display: none;' class='jqx-kanban-item-footer'></div>" +
                    "</div>",
                resources: resourcesAdapterFunc(),
                width: "100%",
                //height: window.innerHeight - 150,
                height: "100%",
                source: dataAdapter,
                theme: 'light',
                itemRenderer: function (item, data, resource)
                {
                    $(item).find(".jqx-kanban-item-color-status").html("<span style='line-height: 23px; margin-left: 5px;'>" + resource.name + "</span>");
                    $(item).find(".jqx-kanban-item-text").css('background', item.color);
                    item.on('dblclick', function (event)
                    {
                        var input = $("<textarea placeholder='(No Title)' style='border: none; width: 100%;' class='jqx-input'></textarea>");
                        var addToHeader = false;
                        var header = null;
                        if (event.target.nodeName === "SPAN" && $(event.target).parent().hasClass('jqx-kanban-item-color-status'))
                        {
                            input = $("<input placeholder='(No Title)' style='border: none; background: transparent; width: 80%;' class='jqx-input'/>");
                            header = event.target;
                            header.innerHTML = "";
                            input.val($(event.target).text());
                            $(header).append(input);
                            addToHeader = true;
                        }
                        if (!addToHeader)
                        {
                            var textElement = item.find(".jqx-kanban-item-text");
                            input.val(textElement.text());
                            textElement[0].innerHTML = "";
                            textElement.append(input);
                        }
                        input.mousedown(function (event)
                        {
                            event.stopPropagation();
                        });
                        input.mouseup(function (event)
                        {
                            event.stopPropagation();
                        });
                        input.blur(function ()
                        {
                            var value = input.val();
                            if (!addToHeader)
                            {
                                $("<span>" + value + "</span>").appendTo(textElement);
                            }
                            else
                            {
                                header.innerHTML = value;
                            }
                            input.remove();
                        });
                        input.keydown(function (event)
                        {
                            if (event.keyCode === 13)
                            {
                                if (!header)
                                {
                                    $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
                                    $(event.target).remove();
                                }
                                else
                                {
                                    header.innerHTML = $(event.target).val();
                                }
                            }
                        });
                        input.focus();
                    });


                    $(window).on("resize", function ()
                    {
                      //  $('#jqxKanban').jqxKanban({ height: window.innerHeight - 150 });
                    });
                },
                columns: [
                    { text: "Backlog", iconClassName: getIconClassName(), dataField: "new", maxItems: 6 },
                    { text: "In Progress", iconClassName: getIconClassName(), dataField: "work", maxItems: 6 },
                    { text: "Done", iconClassName: getIconClassName(), dataField: "done", maxItems: 6 }
                ],
                columnRenderer: function (element, collapsedElement, column)
                {
                    var columnItems = $("#jqxKanban").jqxKanban('getColumnItems', column.dataField).length;
                    element.find(".jqx-kanban-column-header-status").html(" (" + columnItems + "/" + column.maxItems + ")");
                    collapsedElement.find(".jqx-kanban-column-header-status").html(" (" + columnItems + "/" + column.maxItems + ")");
                }
            });
            $('#jqxKanban').on("itemAttrClicked", function (event)
            {
                var args = event.args;
                if (args.attribute === "template")
                {
                    $('#jqxKanban').jqxKanban('removeItem', args.item.id);
                }
            });
            var itemIndex = 0;
            $('#jqxKanban').on('columnAttrClicked', function (event)
            {
                var args = event.args;
                if (args.attribute === "button")
                {
                    args.cancelToggle = true;
                    if (!args.column.collapsed)
                    {
                        var colors = ['#f19b60', '#5dc3f0', '#6bbd49', '#dddddd'];
                        $('#jqxKanban').jqxKanban('addItem', { status: args.column.dataField, text: "<textarea placeholder='(No Title)' style='width: 96%; margin-top:2px; border-radius: 3px; border:none; line-height:20px; height: 50px;' class='jqx-input' id='newItem" + itemIndex + "' value=''></textarea>", tags: "new task", color: colors[Math.floor(Math.random() * 4)], resourceId: null });
                        var input = $("#newItem" + itemIndex);
                        input.mousedown(function (event)
                        {
                            event.stopPropagation();
                        });
                        input.mouseup(function (event)
                        {
                            event.stopPropagation();
                        });
                        input.keydown(function (event)
                        {
                            if (event.keyCode === 13)
                            {
                                $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
                                $(event.target).remove();
                            }
                        });
                        input.focus();
                        itemIndex++;
                    }
                }
            });
        }
    }

    function quickNotesListBox()
    {
        var noteId = -1;
        if (!$("#jqxListBox").hasClass("jqx-widget"))
        {
            var data;
            $("#splitter").jqxSplitter({ theme: 'light', resizable: false, showSplitBar: false, width: "99%",height: window.innerHeight - 150, panels: [{ size: '25%', min: 250 }] });

            var source =
            {
                datatype: "json",
                dataFields: [
                         { name: "id", type: "number" },
                         { name: "image", type: "string" },
                         { name: "firstname", type: "string" },
                         { name: "lastname", type: "string" },
                         { name: "job", type: "string" },
                         { name: "title", type: "string" },
                         { name: "notes", type: "string" }
                ],
                url: "data.php?usedwidget=quicknotesdata"
            };
            var dataAdapter = new $.jqx.dataAdapter(source, {
                beforeLoadComplete: function (records)
                {
                    data = records;
                },
                loadComplete: function ()
                {
                    updatePanel(0);
                    noteId = 1;
                }
            });

            var dataAdapter2 = new $.jqx.dataAdapter(source);
            $('#dropdownlist').jqxDropDownList({
                selectedIndex: 0, theme: 'light', source: dataAdapter2, displayMember: "firstname", valueMember: "id", itemHeight: 70, height: 25, width: "99%", disabled: false,
                renderer: function (index)
                {
                    var datarecord = data[index];
                    var imgurl = datarecord.image;
                    var img = '<img height="50" width="45" src="' + imgurl + '"/>';
                    var table = '<table style="min-width: 150px;"><tr><td style="width: 55px;" rowspan="2">' + img + '</td><td>' + datarecord.firstname + " " + datarecord.lastname + '</td></tr><tr><td>' + datarecord.job + '</td></tr></table>';
                    return table;
                }
            });

            var updatePanel = function (index)
            {
                var datarecord = data[index];

                $("#dropdownlist").jqxDropDownList({ disabled: false });
                $("#dropdownlist").jqxDropDownList('selectIndex', index);
                $("#dropdownlist").jqxDropDownList({ disabled: true });
                $("#subject").jqxInput("val", datarecord.title);
                $('#editor').jqxEditor("val", datarecord.notes);
            };

            $('#jqxListBox').on('select', function (event)
            {
                updatePanel(event.args.index);
                noteId = event.args.index;
            });

            $("#subject").jqxInput({ theme: 'light', width: "99%", height: 25, placeHolder: "Enter text", disabled: true });

            $('#editor').jqxEditor({
                theme: 'light',
                height: "80%",
                width: '100%'
            });

            $("#add").jqxButton({ width: "100%", height: 50, theme: 'light' });
            $("#add").on("click", function ()
            {
                data[noteId].notes = $('#editor').jqxEditor("val");
            });

            $('#jqxListBox').jqxListBox({
                selectedIndex: 0, theme: 'light', source: dataAdapter, displayMember: "firstname", valueMember: "notes", itemHeight: 120, height: '100%', width: '100%',
                renderer: function (index)
                {
                    var datarecord = data[index];
                    var imgurl = datarecord.image;
                    var img = '<img height="100" width="100" src="' + imgurl + '"/>';
                    var table = '<table style="min-width: 130px;"><tr><td style="width: 120px;" rowspan="2">' + img + '</td><td>' + datarecord.firstname + " " + datarecord.lastname + '</td></tr><tr><td>' + datarecord.job + '</td></tr></table>';
                    return table;
                }
            });
        }
    }
});
