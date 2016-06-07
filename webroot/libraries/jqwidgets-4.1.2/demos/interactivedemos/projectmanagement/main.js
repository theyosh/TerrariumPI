$(document).ready(function ()
{
    "use strict";

    var filterIssuesTypes = [
        { name: 'Bug', value: false },
        { name: 'Feature', value: false },
        { name: 'Enhancement', value: false },
        { name: 'Invalid', value: false },
        { name: 'Question', value: false },
        { name: 'Duplicate', value: false },
        { name: 'Not Confirmed', value: false }
    ];

    var allIssues = true;
    var assignedBy = ""; 
    var addedBy = "Else"; 
    var filterOpenCondition = false;
    var filterMilestonesOpenValue = null;

    function applyFilter()
    {
        $("#jqxFirstPanelGrid").jqxGrid('clearfilters');
        var filtertype = 'stringfilter';
        var filtertype2 = 'booleanfilter';
        var filtertype3 = 'stringfilter';
        var filtertype4 = 'stringfilter';

        var filtergroup = new $.jqx.filter();

        var filter_or_operator = 0;
        var filtercondition = 'contains';
        var datafield = 'issueType';

        var filtervalue = "";
        var filter = filtergroup.createfilter(filtertype, filtervalue, filtercondition);
        filtergroup.addfilter(filter_or_operator, filter);

        var filterIssuesTypesLength = filterIssuesTypes.length;
        for (var i = 0; i < filterIssuesTypesLength; i++)
        {
            if (filterIssuesTypes[i].value === true)
            {
                filtervalue = filterIssuesTypes[i].name;
                filter = filtergroup.createfilter(filtertype, filtervalue, filtercondition);
                filtergroup.addfilter(filter_or_operator, filter);
            }
        }

        var filtergroup2 = new $.jqx.filter();
        var filter_or_operator2 = 1;
        var filtercondition2 = 'equal';
        var datafield2 = 'closed';
        var filtervalue2 = filterOpenCondition;
        var filter2 = filtergroup.createfilter(filtertype2, filtervalue2, filtercondition2);
        filtergroup2.addfilter(filter_or_operator2, filter2);

        if(allIssues === false){
            var filtergroup3 = new $.jqx.filter();
            var filter_or_operator3 = 1;
            var filtercondition3 = 'equal';
            var datafield3 = 'assignedTo';
            var filtervalue3 = assignedBy;
            var filter3 = filtergroup.createfilter(filtertype3, filtervalue3, filtercondition3);
            filtergroup3.addfilter(filter_or_operator3, filter3);
            $("#jqxFirstPanelGrid").jqxGrid('addfilter', datafield3, filtergroup3);
            var filtergroup4 = new $.jqx.filter();
            var filter_or_operator4 = 1;
            var filtercondition4 = 'equal';
            var datafield4 = 'reporterBy';
            var filtervalue4 = addedBy;
            var filter4 = filtergroup.createfilter(filtertype4, filtervalue4, filtercondition4);
            filtergroup3.addfilter(filter_or_operator4, filter4);
            $("#jqxFirstPanelGrid").jqxGrid('addfilter', datafield4, filtergroup4);
        }

        $("#jqxFirstPanelGrid").jqxGrid('addfilter', datafield, filtergroup);
        $("#jqxFirstPanelGrid").jqxGrid('addfilter', datafield2, filtergroup2);

        $("#jqxFirstPanelGrid").jqxGrid('applyfilters');
    }

    function applyMilestonesFilter()
    {
        $("#jqxSecondPanelGrid").jqxGrid('clearfilters');

        if (filterMilestonesOpenValue !== null)
        {
            var filtertype = 'booleanfilter';
            var filtergroup = new $.jqx.filter();
            var filter_or_operator = 0;
            var filtercondition = 'equal';
            var datafield = 'closed';
            var filter = filtergroup.createfilter(filtertype, filterMilestonesOpenValue, filtercondition);
            filtergroup.addfilter(filter_or_operator, filter);
            $("#jqxSecondPanelGrid").jqxGrid('addfilter', datafield, filtergroup);

            $("#jqxSecondPanelGrid").jqxGrid('applyfilters');
        }
    }

    var initLayout1 = function ()
    {
        var layout1 = [{
            type: 'layoutGroup',
            orientation: 'horizontal',
            items: [{
                type: 'tabbedGroup',
                alignment: 'left',
                pinnedWidth: '5%',
                width: '20%',
                items: [{
                    type: 'layoutPanel',
                    title: 'Issues Filter',
                    contentContainer: 'IssuesPanelLeft',
                    initContent: function ()
                    {
                        var issuesButtonsArray = ['#buttonAllIssues', '#buttonAssignedToYou', '#buttonAddedByYou', '#buttonNotAssigned'];
                        $('.issues-buttons-group').jqxToggleButton({ width: '97%', height: 50, theme: 'metro' });
                        $('#buttonAllIssues').jqxToggleButton({ toggled: true });
                        $('.issues-buttons-group').on('click', function ()
                        {
                            var id1 = $(this).attr("id");
                            var id = '#' + id1;
                            var index = issuesButtonsArray.indexOf(id);
                            var otherButtonsArray = issuesButtonsArray.slice();
                            otherButtonsArray.splice(index, 1);
                            var otherButtonsString = otherButtonsArray.join(", ");

                            if ($(id).jqxToggleButton('toggled') === true)
                            {
                                if (id === '#buttonAllIssues')
                                {
                                    $(otherButtonsString).jqxToggleButton({ toggled: false });
                                    allIssues = true;
                                } else
                                {
                                    $('#buttonAllIssues').jqxToggleButton({ toggled: false });
                                    allIssues = false;
                                }

                                if (id === '#buttonNotAssigned')
                                {
                                    $('#buttonAssignedToYou').jqxToggleButton({ toggled: false });
                                    assignedBy = "";
                                } else if (id === '#buttonAssignedToYou')
                                {
                                    $('#buttonNotAssigned').jqxToggleButton({ toggled: false });
                                    assignedBy = "You";
                                }
                            }


                            applyFilter();

                        });

                        $('#featuresList').jqxListBox({autoHeight: true, itemHeight: 30, width: '97%', checkboxes: true,  theme: 'metro' });
                        $('#featuresList').on('checkChange', function(event)
                        {
                            var items = $('#featuresList').jqxDropDownList('getCheckedItems');
                            filterIssuesTypes[event.args.item.index].value = event.args.checked;
                            applyFilter();
                        });
                    }
                }]
            }, {
                type: 'tabbedGroup',
                width: '80%',
                minWidth: 200,
                items: [{
                    type: 'layoutPanel',
                    title: 'Issues',
                    contentContainer: 'IssuesPanelRight',
                    initContent: function ()
                    {
                        $("#jqxButtonGroup").jqxButtonGroup({ mode: 'radio', theme: 'metro', height: 50 });
                        $('#jqxButtonGroup').jqxButtonGroup('setSelection', 0);

                        $('#jqxButtonGroup').on('selected', function (event)
                        {
                            filterOpenCondition = !!(event.args.index);
                            applyFilter();
                        });

                        var source =
                        {
                            datatype: "json",
                            datafields: [
                                { name: 'issueId', type: 'int' },
                                { name: 'closed', type: 'bool' },
                                { name: 'reporterBy', type: 'string' },
                                { name: 'assignedTo', type: 'string' },
                                { name: 'issueContent', type: 'string' },
                                { name: 'issueType', type: 'string' }
                            ],
                            url: "data.php?usedwidget=issuesgrid"
                        };

                        var dataAdapterFirstPanelGrid = new $.jqx.dataAdapter(source);
                        $("#jqxFirstPanelGrid").jqxGrid({
                            theme: 'metro',
                            width: "95%",
                            height: "85%",
                            rowsheight: 50,
                            showheader: false,
                            source: dataAdapterFirstPanelGrid,
                            columns: [
                                 {
                                     text: 'Issue Id', datafield: 'issueId', width: 95,
                                     cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                     {
                                         return '<div style="font-weight:bold; font-size:16px; margin-left:20px; margin-top:18px;">' + value + '</div>';
                                     }
                                 },
                                 {
                                     text: 'Issue Content', datafield: 'issueContent',
                                     cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                     {
                                         return '<div style="font-size:14px; margin-left:20px; margin-top:10px;">' + value + '</div>';
                                     }
                                 },
                                 {
                                     text: 'Issue Type', datafield: 'issueType', width: 300,
                                     cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                     {
                                         var modifiedContent = "";
                                         var valuesArray = value.split(", ");
                                         var valuesArrayLength = valuesArray.length;

                                         for (var i = 0; i < valuesArrayLength; i++)
                                         {
                                             modifiedContent = modifiedContent + ' <span class="issue-type issue-type-' + valuesArray[i] + '">' + valuesArray[i].charAt(0).toUpperCase() + valuesArray[i].substr(1) + '</span>';
                                         }

                                         return '<div class="issue-type-container">' + modifiedContent + '</div>';
                                     }
                                 },
                                 {
                                     text: 'closed', datafield: 'closed', hidden: true
                                 },
                                 {
                                     text: 'reporterBy', datafield: 'reporterBy', hidden: true
                                 },
                                 {
                                     text: 'assignedTo', datafield: 'assignedTo', hidden: true
                                 }
                            ]
                        });
                    }
                }]
            }]
        }];

        $('#jqxLayout1').jqxLayout({ theme: 'metro', width: '100%', height: '100%', layout: layout1 });
    };

    var initLayout2 = function ()
    {
        var layout2 = [{
            type: 'layoutGroup',
            orientation: 'horizontal',
            items: [{
                type: 'tabbedGroup',
                alignment: 'left',
                width: '20%',
                unpinnedWidth: 200,
                items: [{
                    type: 'layoutPanel',
                    title: 'Milestones Filter',
                    contentContainer: 'MilestonesPanelLeft',
                    initContent: function ()
                    {
                        var issuesButtonsArray = ['#buttonAllMilestones', '#buttonOpenMilestones', '#buttonClosedMilestones'];
                        $('.milestones-button-group').jqxToggleButton({ width: '97%', height: 50, theme: 'metro' });
                        $('#buttonAllMilestones').jqxToggleButton({ toggled: true });
                        $('.milestones-button-group').on('click', function ()
                        {
                            var id1 = $(this).attr("id");
                            var id = '#' + id1;
                            var index = issuesButtonsArray.indexOf(id);
                            var otherButtonsArray = issuesButtonsArray.slice();
                            otherButtonsArray.splice(index, 1);
                            var otherButtonsString = otherButtonsArray.join(", ");

                            if ($(id).jqxToggleButton('toggled') === true)
                            {
                                if (index === 1)
                                {
                                    filterMilestonesOpenValue = false;
                                } else if (index === 2)
                                {
                                    filterMilestonesOpenValue = true;
                                } else
                                {
                                    filterMilestonesOpenValue = null;
                                }

                                $(otherButtonsString).jqxToggleButton({ toggled: false });
                            }

                            applyMilestonesFilter();
                        });
                    }
                }]
            }, {
                type: 'tabbedGroup',
                width: '80%',
                minWidth: 200,
                items: [{
                    type: 'layoutPanel',
                    title: 'Milestones',
                    contentContainer: 'MilestonesPanelRight',
                    initContent: function ()
                    {
                        var source =
                        {
                            datatype: "json",
                            datafields: [
                                { name: 'milestoneId', type: 'int' },
                                { name: 'closed', type: 'bool' },
                                { name: 'milestoneContent', type: 'string' },
                                { name: 'milestoneDate', type: 'date' }
                            ],
                            url: "data.php?usedwidget=milestonesgrid"
                        };

                        var dataAdapterFirstPanelGrid = new $.jqx.dataAdapter(source);
                        $("#jqxSecondPanelGrid").jqxGrid({
                            theme: 'metro',
                            width: "95%",
                            height: "85%",
                            rowsheight: 50,
                            showheader: false,
                            source: dataAdapterFirstPanelGrid,
                            columns: [
                                 {
                                     text: 'Milestone Id', datafield: 'milestoneId', width: 95,
                                     cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                     {
                                         return '<div style="font-weight:bold; font-size:16px; margin-left:20px; margin-top:18px;">' + value + '</div>';
                                     }
                                 },
                                 {
                                     text: 'Milestone Content', datafield: 'milestoneContent',
                                     cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                     {
                                         return '<div style="font-size:14px; margin-left:20px; margin-top:18px;">' + value + '</div>';
                                     }
                                 },
                                 {
                                     text: 'Milestone Date', datafield: 'milestoneDate', width: 300, cellsformat: 'dd-MMMM-yyyy'
                                 },
                                 {
                                     text: 'closed', datafield: 'closed', hidden: true
                                 }
                            ]
                        });
                    }
                }]
            }]
        }];

        $('#jqxLayout2').jqxLayout({ theme: 'metro', width: '100%', height: '100%', layout: layout2 });
    };

    var initWidgets = function (tab)
    {
        switch (tab)
        {
            case 0:
                initLayout1();
                break;
            case 1:
                initLayout2();
                break;
        }
    };
    $('#jqxTabs').jqxTabs({ theme: 'metro', width: "100%", height: "100%", initTabContent: initWidgets });
});