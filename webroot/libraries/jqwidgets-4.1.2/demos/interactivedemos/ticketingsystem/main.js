$(document).ready(function ()
{
    'use strict';
    var themeL = 'light';
    var themeD = 'dark';
    var theme = themeL;
    var isInitialFiltering = true;
    // If there is an incorrect login.
    var logInUser = { UserId: 1005, Name: 'Peter' };
    var isLogInUser = true;
    var loadedProject = 0;
    var capitalize = function (word)
    {
        return word[0].toUpperCase() + word.slice(1);
    };
    var today = new Date();
    var thisYear = today.getFullYear();
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var initialData = {
        Projects: [
            {
                ProjectId: 1,
                ProjectName: 'IT',
                Lead: 1005,
                UsersIdList: [1005, 1008, 1009, 1010, 1011, 1012],
                sampleData: [{
                    a: 0.35,
                    b: 14.5,
                    c: 6.15
                }, {
                    a: 1,
                    b: 2.5,
                    c: 12
                }, {
                    a: 10,
                    b: 0.2,
                    c: 4.21
                }, {
                    a: 100,
                    b: 205,
                    c: 41.45
                }, {
                    a: 1,
                    b: 100,
                    c: 12.1
                }, {
                    a: 5.11,
                    b: 10.13,
                    c: 18.95
                }, {
                    a: 42.12,
                    b: 37,
                    c: 17.97
                }, {
                    a: 20.13,
                    b: 10.13,
                    c: 12.22
                }, {
                    a: 1.9,
                    b: 2.5,
                    c: 2
                }, {
                    a: 10,
                    b: 2,
                    c: 4
                }, {
                    a: 17,
                    b: 5,
                    c: 11
                }, {
                    a: 18.35,
                    b: 15.29,
                    c: 27.21
                }]
            }, {
                ProjectId: 2,
                ProjectName: 'SDK',
                Lead: 1002,
                UsersIdList: [1001, 1002, 1003, 1004, 1005, 1006, 1007],
                sampleData: [{
                    a: 1.05,
                    b: 2.5,
                    c: 0.15
                }, {
                    a: 1.9,
                    b: 2.5,
                    c: 2
                }, {
                    a: 107,
                    b: 25,
                    c: 43
                }, {
                    a: 13,
                    b: 10,
                    c: 2.1
                }, {
                    a: 15.27,
                    b: 20,
                    c: 13.05
                }, {
                    a: 10.35,
                    b: 5.29,
                    c: 7.21
                }, {
                    a: 10,
                    b: 25,
                    c: 16.45
                }, {
                    a: 6.24,
                    b: 10.9,
                    c: 11.18
                }, {
                    a: 15.11,
                    b: 10.13,
                    c: 18.95
                }, {
                    a: 10.83,
                    b: 30.13,
                    c: 19.36
                }, {
                    a: 18.77,
                    b: 50,
                    c: 12.1
                }, {
                    a: 44,
                    b: 30,
                    c: 17
                }]
            }
        ],
        Groups: [
            {
                GroupId: 110,
                GroupName: 'Admins',
                UsersIdList: [1002, 1005, 1010]
            }, {
                GroupId: 111,
                GroupName: 'Support',
                UsersIdList: [1001, 1003, 1005, 1006, 1007, 1011, 1012]
            }, {
                GroupId: 112,
                GroupName: 'QA',
                UsersIdList: [1001, 1002, 1005, 1009, 1011]
            }, {
                GroupId: 113,
                GroupName: 'Sales',
                UsersIdList: [1002, 1003, 1008]
            }, {
                GroupId: 114,
                GroupName: 'Development',
                UsersIdList: [1002, 1005, 1006, 1007, 1008, 1011]
            }
        ],
        Users: [
            {
                UserId: 1001,
                Name: 'Len'
            }, {
                UserId: 1002,
                Name: 'Ann'
            }, {
                UserId: 1003,
                Name: 'Lee'
            }, {
                UserId: 1004,
                Name: 'Bob'
            }, {
                UserId: 1005,
                Name: 'Peter'
            }, {
                UserId: 1006,
                Name: 'Don'
            }, {
                UserId: 1007,
                Name: 'George'
            }, {
                UserId: 1008,
                Name: 'Maria'
            }, {
                UserId: 1009,
                Name: 'Mike'
            }, {
                UserId: 1010,
                Name: 'John'
            }, {
                UserId: 1011,
                Name: 'Bryan'
            }, {
                UserId: 1012,
                Name: 'Aaron'
            }
        ],
        Tickets: [
            {
                TicketId: 10020,
                Title: 'Fiant adipiscing clari nunc molestie per placerat vero insitam. ullamcorper saepius etiam claritatem quod.',
                CreatedOn: thisYear + '-01-06 00:24',
                ModifiedOn: '2016-01-06 00:24',
                UserId: 1005,
                Status: 'Pending',
                ProjectId: 1
            }, {
                TicketId: 10035,
                Title: 'Possim soluta nisl ex volutpat possim est legere.',
                CreatedOn: thisYear + '-01-06 02:14',
                ModifiedOn: '2016-01-06 03:57',
                UserId: 1005,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10050,
                Title: 'Nulla tempor liber option nihil feugiat congue facit quinta.',
                CreatedOn: thisYear + '-01-06 05:51',
                ModifiedOn: thisYear + '-01-06 11:43',
                UserId: 1005,
                Status: 'Close',
                ProjectId: 2
            }, {
                TicketId: 10070,
                Title: 'Ut possim tempor parum ad eros.',
                CreatedOn: thisYear + '-01-06 11:26',
                ModifiedOn: thisYear + '-01-06 19:21',
                UserId: 1001,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10475,
                Title: 'Lip in solum deterruisset.',
                CreatedOn: thisYear + '-01-06 06:03',
                ModifiedOn: thisYear + '-01-06 07:21',
                UserId: 1001,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10075,
                Title: 'Pro in solum deterruisset.',
                CreatedOn: thisYear + '-01-06 06:03',
                ModifiedOn: thisYear + '-01-06 07:21',
                UserId: 1002,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10076,
                Title: 'Sed at choro sensibus efficiantur, liber vitae blandit no mei.',
                CreatedOn: thisYear + '-01-04 10:51',
                ModifiedOn: thisYear + '-01-06 16:34',
                UserId: 1003,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10077,
                Title: 'Oporteat sadipscing no sit, quo vocibus legendos interpretaris no, cum at eius nostro vulputate.',
                CreatedOn: thisYear + '-01-05 11:00',
                ModifiedOn: thisYear + '-01-05 13:41',
                UserId: 1004,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10078,
                Title: 'Ex dicant verterem menandri est, te est dicat tempor. In sed modus option suscipit.',
                CreatedOn: thisYear + '-01-06 12:43',
                ModifiedOn: thisYear + '-01-07 01:01',
                UserId: 1005,
                Status: 'Pending',
                ProjectId: 1
            }, {
                TicketId: 10079,
                Title: 'Eos utroque principes persecuti eu, ea nominavi perfecto comprehensam vel, usu te saepe audiam deleniti.',
                CreatedOn: thisYear + '-01-07 12:26',
                ModifiedOn: thisYear + '-01-08 15:41',
                UserId: 1006,
                Status: 'Open',
                ProjectId: 2
            }, {
                TicketId: 10123,
                Title: 'Qui maiorum convenire necessitatibus ex. Vix ex eripuit eruditi debitis, fabellas maluisset philosophia ius et, causae perfecto dissentias sea ea. Nec nibh idque expetenda ei, veri consectetuer mea eu. Invidunt urbanitas ut his.',
                CreatedOn: thisYear + '-01-04 16:10',
                ModifiedOn: thisYear + '-01-06 07:52',
                UserId: 1009,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10125,
                Title: 'Posse propriae salutandi ad his.',
                CreatedOn: thisYear + '-01-05 06:03',
                ModifiedOn: thisYear + '-01-06 07:21',
                UserId: 1008,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10175,
                Title: 'Prima tacimates perpetua cu usu, eu vix saepe soluta sapientem, zril eripuit fierent et eos.',
                CreatedOn: thisYear + '-01-04 06:35',
                ModifiedOn: thisYear + '-01-04 07:41',
                UserId: 1008,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10175,
                Title: 'Ea pro tale veri melius. Pro in solum deterruisset.',
                CreatedOn: thisYear + '-01-04 09:25',
                ModifiedOn: thisYear + '-01-06 17:22',
                UserId: 1010,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10120,
                Title: 'Litterarum aliquam quarta quis id in sit.',
                CreatedOn: thisYear + '-01-06 18:12',
                ModifiedOn: thisYear + '-01-06 19:31',
                UserId: 1005,
                Status: 'Pending',
                ProjectId: 1
            }, {
                TicketId: 10122,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1005,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10223,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1002,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10224,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1003,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10225,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1004,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10226,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1005,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10227,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1006,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10228,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1007,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10229,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1008,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10230,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1009,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10231,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1010,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10232,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1011,
                Status: 'Open',
                ProjectId: 1
            }, {
                TicketId: 10233,
                Title: 'Te quo postea regione aperiam, te illud reque vivendum vis, sumo dissentias est no. Duo viderer equidem assueverit ne. Illum assentior vix te, sed deleniti elaboraret temporibus ne, et debitis intellegam vim.',
                CreatedOn: thisYear + '-01-06 14:45',
                ModifiedOn: thisYear + '-01-07 10:52',
                UserId: 1012,
                Status: 'Open',
                ProjectId: 1
            }
        ],
        Comments: [
            {
                TicketId: 10020,
                Date: thisYear + '-01-06 09:03',
                By: 'George',
                Description: 'Te dicunt fierent cum, aperiri vivendo tacimates sea ut. At atqui repudiare forensibus mea, quas ridens cu pro. Minim legimus te vel. Sit an atqui dissentias, qui in moderatius neglegentur.'
            }, {
                TicketId: 10020,
                Date: thisYear + '-01-06 11:14',
                By: 'Lee',
                Description: 'Te nostrud mnesarchum comprehensam pri, no cum vocent eloquentiam.'
            }, {
                TicketId: 10120,
                Date: thisYear + '-01-07 07:25',
                By: 'Bryan',
                Description: 'Mei ex suas altera assueverit, scaevola phaedrum contentiones sed cu.'
            }
        ]
    };
    var sourcesOfChartsForUpdates = [];
    var adaptersOfChartsForUpdates = [];
    var getGroupsRelatedUserId = function (id)
    {
        var groups = initialData.Groups;
        var matchedGroups = [];
        var length = groups.length;
        for (var i = 0; i < length; i += 1)
        {
            var group = groups[i];
            var groupUsers = group.UsersIdList;
            if (groupUsers.indexOf(id) !== -1)
            {
                matchedGroups.push(group);
            }
        }

        return matchedGroups;
    }
    var arrayGroupsSelectedUser = [];
    var currentEditUser = { UserId: -1, Name: '' };
    var VALIDATION = {
        emptyString: function (stringValue)
        {
            if (!stringValue && typeof (stringValue) !== 'string')
            {
                return false;
            }

            if (typeof (stringValue) === 'string' && !stringValue.trim())
            {
                return false;
            }

            if (stringValue.length < 1)
            {
                return false;
            }

            return true;
        }
    };
    var addUserIdToBaseData = function (userId, groupId)
    {
        var baseGroups = initialData.Groups;
        for (var i = 0; i < baseGroups.length; i += 1)
        {
            if (baseGroups[i].GroupId === groupId)
            {
                // ADD userId
                if (initialData.Groups[i].UsersIdList.indexOf(userId) < 0)
                {
                    initialData.Groups[i].UsersIdList.push(userId);
                    initialData.Groups[i].UsersIdList.sort();
                    break;
                }
            }
        }
    };
    var deleteUserIdToBaseData = function (userId, groupId)
    {
        var baseGroups = initialData.Groups;
        for (var i = 0; i < baseGroups.length; i += 1)
        {
            if (baseGroups[i].GroupId === groupId)
            {
                // DELETE userId
                var idArray = baseGroups[i].UsersIdList;
                var index = idArray.indexOf(userId);
                if (index !== -1)
                {
                    idArray.splice(index, 1);
                }
                initialData.Groups[i].UsersIdList = idArray;
                break;
            }
        }
    };

    /*
        WINDOW Login
    */
    $('#loginWindow').jqxWindow({
        autoOpen: true,
        isModal: true,
        width: 290,
        height: 205,
        draggable: false,
        resizable: false,
        theme: theme,
        initContent: function ()
        {
           var  Users = [
         {
             UserId: 1001,
             Name: 'Len'
         }, {
             UserId: 1002,
             Name: 'Ann'
         }, {
             UserId: 1003,
             Name: 'Lee'
         }, {
             UserId: 1004,
             Name: 'Bob'
         }, {
             UserId: 1005,
             Name: 'Peter'
         }, {
             UserId: 1006,
             Name: 'Don'
         }, {
             UserId: 1007,
             Name: 'George'
         }, {
             UserId: 1008,
             Name: 'Maria'
         }, {
             UserId: 1009,
             Name: 'Mike'
         }, {
             UserId: 1010,
             Name: 'John'
         }, {
             UserId: 1011,
             Name: 'Bryan'
         }, {
             UserId: 1012,
             Name: 'Aaron'
         }
            ]

            $('#loginUserNameInput').jqxDropDownList({
                theme: theme,
                placeHolder: ' Enter username',
                width: 156,
                source: Users,
                selectedIndex: 4,
                displayMember: "Name",
                valueMember: "UserId",
                height: 25
            });
            $('#loginUserPasswordInput').jqxInput({
                theme: theme,
                placeHolder: ' Enter password',
                width: 150,
                height: 25
            });
            $('#loginOrganizationDropDown').jqxDropDownList({
                theme: theme,
                selectedIndex: 0,
                autoDropDownHeight: true,
                width: 156,
                height: 25
            });
            $('#loginSubmitButton').jqxButton({
                theme: theme,
                width: 80,
                height: 25,
                disabled: true
            });
        }
    });

    $('#loginUserPasswordInput').on('keyup', function ()
    {
        $('#loginWindow').jqxValidator('validate');
    });

    $('#loginUserPasswordInput').on('change', function ()
    {
        $('#loginWindow').jqxValidator('validate');
    });

    $('#loginWindow').jqxValidator({
        hintType: 'label',
        rules: [
            {
                input: '#loginUserPasswordInput',
                message: 'Password is required!',
                action: 'change, blur',
                rule: 'required'
            }
        ],
        onSuccess: function ()
        {
            $('#loginSubmitButton').jqxButton({
                disabled: false
            });

            var inputUsername = $('#loginUserNameInput').jqxDropDownList('getSelectedItem');
            logInUser.Name = inputUsername.label;
            logInUser.UserId = inputUsername.value;
            changeHeaderUserName(logInUser.Name);
        },
        onError: function ()
        {
            $('#loginSubmitButton').jqxButton({
                disabled: true
            });
        }
    });

    $('#loginSubmitButton').on('click', function ()
    {
        $('#loginWindow').jqxWindow('close');
        initializeWidget();
        $('#loginSubmitButton').off('click');
    });

    /*
        WINDOW Edit user
    */
    var changeUserName = function (newName, userId)
    {
        var users = initialData.Users;
        for (var u = 0; u < users.length; u += 1)
        {
            if (users[u].UserId === userId)
            {
                initialData.Users[u].Name = newName;
                break;
            }
        }
    };

    var collapseEditUser = 300;
    var expandEditUser = 560;
    var factorEditUser = 0.95;
    var editUserWindowWidth = { collapse: collapseEditUser, expand: expandEditUser, collapseWidgets: collapseEditUser * factorEditUser, expandWidgets: expandEditUser * factorEditUser };
    $('#editUserWindow').jqxWindow({
        autoOpen: false,
        resizable: false,
        width: editUserWindowWidth.collapse,
        isModal: true,
        height: 300,
        theme: theme,
        draggable: false,
        initContent: function ()
        {
            var editUserGroupsGridSource =
            {
                datatype: 'json',
                datafields: [
                    { name: 'groups', type: 'string', map: 'GroupName' },
                    { name: 'id', type: 'number', map: 'GroupId' },
                    { name: 'userslist', type: 'number', map: 'UsersIdList' }
                ],
                localdata: initialData.Groups
            };

            var editUserGroupsGridDataAdapter = new $.jqx.dataAdapter(editUserGroupsGridSource);

            $('#editUserGroupsGrid').jqxGrid({
                width: editUserWindowWidth.collapseWidgets,
                autoheight: true,
                theme: theme,
                showheader: false,
                showstatusbar: false,
                showtoolbar: false,
                source: editUserGroupsGridDataAdapter,
                columns: [
                    { text: 'groups', datafield: 'groups' },
                    {
                        text: 'remove', datafield: 'remove', width: '20%', cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                        {
                            return '<div style="text-align: center; margin-top: 7px;"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></div>'
                        }
                    },
                ]
            });
            $('#editUserGroupsGrid').on('cellclick', function (event)
            {
                var args = event.args;
                var rowBoundIndex = args.rowindex;
                var dataField = args.datafield;
                if (dataField === 'remove')
                {
                    var data = $('#editUserGroupsGrid').jqxGrid('getrowdata', rowBoundIndex);
                    var groupId = data.id;
                    var groupName = data.groups;
                    var updatedArrayGroupsSelected = new Array();
                    for (var i in arrayGroupsSelectedUser)
                    {
                        if (arrayGroupsSelectedUser[i].GroupId !== groupId)
                        {
                            updatedArrayGroupsSelected.push(arrayGroupsSelectedUser[i]);
                        }
                    }

                    var initGroups = initialData.Groups;
                    for (var k = 0; k < initGroups.length; k += 1)
                    {
                        if (initGroups[k].GroupId === groupId)
                        {
                            $('#listboxGroups').jqxListBox('unselectIndex', k);
                        }
                    }

                    deleteUserIdToBaseData(currentEditUser.UserId, groupId);
                    arrayGroupsSelectedUser = updatedArrayGroupsSelected;
                    getFilteringGroups();
                }
            });

            $('#editUserNameInput').jqxInput({
                theme: theme,
                placeHolder: ' Enter username',
                width: 216,
                height: 25
            });
            $('#editUserNameInput').val(logInUser.Name);

            $('#editUserNameInput').on('keyup', function ()
            {
                var username = $('#editUserNameInput').val();
                if (VALIDATION.emptyString(username))
                {
                    changeEditUserNameInput(username);
                    changeUserName(username, currentEditUser.UserId);
                    $('#dashboardProjectMembersGrid').jqxGrid('updatebounddata');
                } else
                {
                    changeEditUserNameInput('');
                }

                if (isLogInUser)
                {
                    changeHeaderUserName(username);
                }
            });

            $('#editUserAddGroupButton').jqxButton({
                theme: theme,
                width: editUserWindowWidth.collapseWidgets,
                height: 30,
                disabled: false
            });

            $('#editUserAddGroupButtonGroups').jqxButton({
                theme: theme,
                width: 80,
                height: 25,
                disabled: false
            });

            $('#editUserAddGroupButtonClose').jqxButton({
                theme: theme,
                width: 80,
                height: 25,
                disabled: false
            });
        }
    });

    var revertStateEditUserWindow = function ()
    {
        $('#listboxGroups').hide();
        $('#editUserWindow').jqxWindow({ width: editUserWindowWidth.collapse });
        $('#buttonsGroupsClose').css('left', 5 + 'px');
    };

    $('#editUserWindowContent').on('dblclick', function ()
    {
        revertStateEditUserWindow();
    });

    $('#editUserWindow').on('close', function (event)
    {
        revertStateEditUserWindow();
    });

    var getFilteringGroups = function ()
    {
        var filtergroup = new $.jqx.filter();
        var filter_or_operator = 1;
        var filtercondition = 'contains';
        for (var j = 0; j < arrayGroupsSelectedUser.length; j += 1)
        {
            var currentGroup = arrayGroupsSelectedUser[j];
            var filtervalue = currentGroup.GroupName;
            var filter = filtergroup.createfilter('stringfilter', filtervalue, filtercondition);
            filtergroup.addfilter(filter_or_operator, filter);
        }
        $('#editUserGroupsGrid').jqxGrid('addfilter', 'groups', filtergroup);
        $('#editUserGroupsGrid').jqxGrid('applyfilters');
    };

    var isFirstInitListbox = true;
    var isInOperationProcess = false;
    var checkContainThatGroup = function (groupsArray, groupId)
    {
        for (var i = 0; i < groupsArray.length; i += 1)
        {
            if (groupsArray.GroupId === groupId)
            {
                return true;
            }
        }

        return false;
    };

    $('#editUserAddGroupButton').on('click', function ()
    {
        if (isFirstInitListbox)
        {
            var groupsListboxSource = {
                datatype: 'json',
                datafields: [
                    { name: 'id', type: 'number', map: 'GroupId' },
                    { name: 'groups', type: 'string', map: 'GroupName' }
                ],
                root: 'Groups',
                localdata: initialData
            };
            var groupsListboxDataAdapter = new $.jqx.dataAdapter(groupsListboxSource);
            $('#listboxGroups').jqxListBox({
                width: 235,
                height: 190,
                source: groupsListboxDataAdapter,
                displayMember: 'groups',
                valueMember: 'id',
                theme: theme,
                multiple: true,
                filterable: true
            });

            isFirstInitListbox = false;
        }

        isInOperationProcess = true;
        $('#listboxGroups').jqxListBox('clearSelection');
        for (var i = 0; i < arrayGroupsSelectedUser.length; i += 1)
        {
            var currentGroup = arrayGroupsSelectedUser[i];
            for (var g = 0; g < initialData.Groups.length; g += 1)
            {
                var group = initialData.Groups[g];
                if (group.GroupId === currentGroup.GroupId)
                {
                    $('#listboxGroups').jqxListBox('selectIndex', g);
                    break;
                }
            }
        }

        isInOperationProcess = false;
        $('#editUserWindow').jqxWindow({ width: editUserWindowWidth.expand });
        $('#buttonsGroupsClose').css('left', 150 + 'px');

        // Add / Delete user in one group, when editUser
        $('#listboxGroups').on('select', function (event)
        {
            var args = event.args;
            if (args)
            {
                var item = args.item;
                var label = item.label;
                var groupId = item.value;
                addUserIdToBaseData(currentEditUser.UserId, groupId);
                var updatedArrayGroupsSelected = new Array();
                if (!isInOperationProcess)
                {
                    if (!checkContainThatGroup(arrayGroupsSelectedUser, groupId))
                    {
                        for (var i in initialData.Groups)
                        {
                            if (initialData.Groups[i].GroupId === groupId)
                            {
                                arrayGroupsSelectedUser.push(initialData.Groups[i]);
                            }
                        }
                    }
                }

                $('#editUserGroupsGrid').jqxGrid('updatebounddata');
                getFilteringGroups();
            }
        });
        $('#listboxGroups').on('unselect', function (event)
        {
            var args = event.args;
            if (args)
            {
                var item = args.item;
                var groupId = item.value;
                deleteUserIdToBaseData(currentEditUser.UserId, groupId);
                if (!isInOperationProcess)
                {
                    var updatedArrayGroupsSelected = new Array();
                    for (var i in arrayGroupsSelectedUser)
                    {
                        if (arrayGroupsSelectedUser[i].GroupId !== groupId)
                        {
                            updatedArrayGroupsSelected.push(arrayGroupsSelectedUser[i]);
                        }
                    }

                    // Prevent filtering
                    if (updatedArrayGroupsSelected.length === 0)
                    {
                        updatedArrayGroupsSelected.push("");
                    }

                    arrayGroupsSelectedUser = updatedArrayGroupsSelected;
                    getFilteringGroups();
                }
            }
        });

        $('#listboxGroups').show();
    });

    $('#editUserAddGroupButtonGroups').on('click', function ()
    {
        $('#editGroupsWindow').jqxWindow('open');
        $('#editGroupsWindow').jqxWindow('focus');
    });

    $('#editUserAddGroupButtonClose').on('click', function ()
    {
        $('#editUserWindow').jqxWindow('close');
    });

    var getFiltering = function (array, filtergroup)
    {
        // 0 for "and" and 1 for "or"
        var filter_or_operator = 1;
        // numericfilter, stringfilter, datefilter or booelanfilter
        var filtertype = 'numericfilter';
        var filtercondition = isInitialFiltering ? 'NULL' : 'EQUAL';

        for (var i in array)
        {
            var key = array[i];
            var filter = filtergroup.createfilter(filtertype, key, filtercondition);
            filtergroup.addfilter(filter_or_operator, filter);
        }

        return filtergroup;
    };
    var isItSecnodOpenGroupsUsers = false;
    var currenSelectedGroup = -1;
    var currenSelectedGroupName = '';
    var editGroupsWindowWidth = { collapse: 540, expand: 750 };
    var correctionContainerButtons = { collapse: '125px', expand: '255px' };

    /*
        WINDOW Edit group
    */
    $('#editGroupsWindow').jqxWindow({
        autoOpen: false,
        isModal: true,
        width: editGroupsWindowWidth.collapse,
        height: 250,
        theme: theme,
        draggable: false,
        resizable: false,
        initContent: function ()
        {
            var groupsGridSource =
            {
                datatype: 'json',
                datafields: [
                    { name: 'id', type: 'number', map: 'GroupId' },
                    { name: 'groups', type: 'string', map: 'GroupName' },
                    { name: 'usersId', type: 'number', map: 'UsersIdList' }
                ],
                root: 'Groups',
                localdata: initialData,
                addrow: function (rowid, rowdata, position, commit)
                {
                    commit(true);
                },
                deleterow: function (rowid, commit)
                {
                    commit(true);
                },
                updaterow: function (rowid, rowdata, commit)
                {
                    commit(true);
                }
            };

            // Calculate buttons position
            $('#editGroupsWindowContainerButtons').css('left', correctionContainerButtons.collapse);

            var groupsGridDataAdapter = new $.jqx.dataAdapter(groupsGridSource);
            var gridWidth = 250;
            var gridHeight = 171;
            $('#groupsGrid').jqxGrid({
                width: gridWidth,
                height: gridHeight,
                theme: theme,
                source: groupsGridDataAdapter,
                columns: [
                    { text: 'Groups', datafield: 'groups' }
                ]
            });

            var isOpenUsersListbox = false;
            $('#groupsGrid').on('rowselect', function (event)
            {
                $('#listboxUsernames').hide();
                $('#editGroupsWindowContainerButtons').css('left', correctionContainerButtons.collapse);
                $('#editGroupsWindow').jqxWindow({ width: editGroupsWindowWidth.collapse });

                var args = event.args;
                var rowBoundIndex = args.rowindex;
                var rowData = args.row;
                currenSelectedGroup = rowBoundIndex;

                var currentGroup = rowData['groups'];
                currenSelectedGroupName = currentGroup;
                $('#usersGrid').jqxGrid('setcolumnproperty', 'user', 'text', 'Users [' + currentGroup + ']');
                isInitialFiltering = false;
                var usersIdList = rowData['usersId'];
                if (!groupsUsersListState[currentGroup])
                {
                    groupsUsersListState[currentGroup] = usersIdList;
                }

                var filtergroup = new $.jqx.filter();
                if (usersIdList.length == 0)
                {
                    usersIdList = [''];
                }

                filtergroup = getFiltering(usersIdList, filtergroup);
                $('#usersGrid').jqxGrid('addfilter', 'id', filtergroup);
                $('#usersGrid').jqxGrid('applyfilters');
            });

            /* Create listbox - usernames */
            var initializeListboxUsernames = function ()
            {
                var usersListboxSource = {
                    datatype: 'json',
                    datafields: [
                        { name: 'id', type: 'number', map: 'UserId' },
                        { name: 'user', type: 'string', map: 'Name' }
                    ],
                    root: 'Users',
                    localdata: initialData,
                    deleterow: function (rowid, commit)
                    {
                        // synchronize with the server - send delete command
                        // call commit with parameter true if the synchronization with the server was successful
                        // and with parameter false if the synchronization has failed.
                        commit(true);
                    }
                };

                var usersListboxDataAdapter = new $.jqx.dataAdapter(usersListboxSource);

                $('#listboxUsernames').jqxListBox({
                    source: usersListboxDataAdapter,
                    width: 202,
                    height: gridHeight,
                    theme: themeL,
                    displayMember: 'user',
                    valueMember: 'id',
                    multiple: true,
                    filterable: true
                });

                return $('#listboxUsernames');
            };

            var getIndexesForListbox = function (valueMembers, records)
            {
                var length = valueMembers.length;
                var indexes = new Array();

                for (var i = 0; i < records.length; i += 1)
                {
                    var currentUser = records[i];
                    var currentUserId = currentUser.id;
                    var coincidence = valueMembers.indexOf(currentUserId);
                    if (coincidence != -1)
                    {
                        var index = i;
                        indexes.push(index);
                    }
                }

                return indexes;
            };

            /* Information about current state of users in groups */
            var groupsUsersListState = {};
            var usersGridSource = {
                datatype: 'json',
                datafields: [
                    { name: 'id', type: 'number', map: 'UserId' },
                    { name: 'user', type: 'string', map: 'Name' }
                ],
                root: 'Users',
                localdata: initialData,
                deleterow: function (rowid, commit)
                {
                    // synchronize with the server - send delete command
                    // call commit with parameter true if the synchronization with the server was successful
                    // and with parameter false if the synchronization has failed.
                    commit(true);
                }
            };
            var usersGridDataAdapter = new $.jqx.dataAdapter(usersGridSource);
            var localizationobj = {};
            localizationobj.emptydatastring = 'Please select a group.';
            $('#usersGrid').jqxGrid({
                width: gridWidth,
                height: gridHeight,
                theme: theme,
                showstatusbar: false,
                showtoolbar: false,
                localization: localizationobj,
                ready: function ()
                {
                    var usersListbox = initializeListboxUsernames();
                    usersListbox.hide();
                    $('#usersGrid').jqxGrid('hidecolumn', 'id');

                    var filtergroup = new $.jqx.filter();
                    filtergroup = getFiltering([''], filtergroup);
                    $('#usersGrid').jqxGrid('addfilter', 'id', filtergroup);
                    $('#usersGrid').jqxGrid('applyfilters');
                    isInitialFiltering = false;

                    $('#usersGrid').on('columnclick', function (event)
                    {
                        $('#editGroupsWindowContainerButtons').css('left', correctionContainerButtons.expand);
                        isOpenUsersListbox = true;
                        var args = event.args;
                        var dataField = args.datafield;
                        if (dataField === 'changeUsers')
                        {
                            var rowsFromGroupsGrid = $('#groupsGrid').jqxGrid('getrows');
                            if (currenSelectedGroup != -1)
                            {
                                for (var row in rowsFromGroupsGrid)
                                {
                                    var currentGroup = rowsFromGroupsGrid[row];
                                    if (currentGroup['uid'] === currenSelectedGroup)
                                    {
                                        var currentUsersList = groupsUsersListState[currenSelectedGroupName];
                                        var records = usersGridDataAdapter.getrecords();
                                        var listboxIndexes = getIndexesForListbox(currentUsersList, records);
                                        usersListbox.jqxListBox('clearSelection');
                                        for (var i = 0; i < listboxIndexes.length; i += 1)
                                        {
                                            usersListbox.jqxListBox('selectIndex', listboxIndexes[i]);
                                        }

                                        usersListbox.show();
                                        $('#editGroupsWindow').jqxWindow({ width: editGroupsWindowWidth.expand });

                                        break;
                                    }
                                }
                            } else
                            {
                                usersListbox.show();
                                $('#editGroupsWindow').jqxWindow({ width: editGroupsWindowWidth.expand });
                            }

                        }
                    });

                    $('#listboxUsernames').on('select', function (event)
                    {
                        var args = event.args;
                        if (args)
                        {
                            var item = args.item;
                            var value = item.value;
                            if (currenSelectedGroupName.length !== 0)
                            {
                                if (groupsUsersListState[currenSelectedGroupName].indexOf(value) === -1)
                                {
                                    groupsUsersListState[currenSelectedGroupName].push(value);
                                    for (var l = 0; l < initialData.Groups.length; l += 1)
                                    {
                                        if (initialData.Groups[l].GroupName === currenSelectedGroupName && value === currentEditUser.UserId)
                                        {
                                            arrayGroupsSelectedUser.push(initialData.Groups[l]);
                                        }
                                    }
                                }
                            }
                            $('#editUserGroupsGrid').jqxGrid('updatebounddata');
                            getFilteringGroups();
                        }
                    });

                    $('#listboxUsernames').on('change', function ()
                    {
                        $('#usersGrid').jqxGrid('clearfilters');
                        var items = $('#listboxUsernames').jqxListBox('getSelectedItems');
                        var length = items.length;
                        var changeUsersId = new Array();

                        for (var n = 0; n < length; n += 1)
                        {
                            var currentUser = items[n];
                            changeUsersId.push(currentUser.value);
                        }

                        if (changeUsersId.length === 0)
                        {
                            changeUsersId.push('');
                        }

                        var filtergroup = new $.jqx.filter();
                        filtergroup = getFiltering(changeUsersId, filtergroup);
                        $('#usersGrid').jqxGrid('addfilter', 'id', filtergroup);
                        $('#usersGrid').jqxGrid('applyfilters');
                        $('#usersGrid').jqxGrid('refreshfilterrow');
                    });

                    // This event is used to catch click on 'trash icon'
                    $('#usersGrid').on('cellclick', function (event)
                    {
                        var args = event.args;
                        var rowBoundIndex = args.rowindex;
                        var dataField = args.datafield;
                        if (dataField === 'changeUsers')
                        {
                            // Delete users from current selected group
                            var rowId = $('#usersGrid').jqxGrid('getrowid', rowBoundIndex);
                            $('#listboxUsernames').jqxListBox('unselectIndex', rowId);
                            var data = $('#usersGrid').jqxGrid('getrowdatabyid', rowId);
                            var removeId = data.id;
                            var currentGroupUsersList = groupsUsersListState[currenSelectedGroupName];
                            var index = currentGroupUsersList.indexOf(removeId);
                            currentGroupUsersList.splice(index, 1);
                            // Create update on current group
                            groupsUsersListState[currenSelectedGroupName] = currentGroupUsersList;
                            var filtergroup = new $.jqx.filter();
                            if (currentGroupUsersList.length == 0)
                            {
                                currentGroupUsersList = [''];
                                localizationobj.emptydatastring = 'The group is empty.';
                                $('#usersGrid').jqxGrid('localizestrings', localizationobj);
                            }

                            filtergroup = getFiltering(currentGroupUsersList, filtergroup);
                            $('#usersGrid').jqxGrid('addfilter', 'id', filtergroup);
                            $('#usersGrid').jqxGrid('applyfilters');
                        }
                    });
                },
                source: usersGridDataAdapter,
                columns: [
                    { text: 'Users', datafield: 'user' },
                    { text: '', datafield: 'id' },
                    {
                        text: '', width: '25%',
                        datafield: 'changeUsers',
                        cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                        {
                            return '<div style="text-align: center; margin-top: 7px;"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></div>'
                        },
                        renderer: function (defaultText, alignment, height)
                        {
                            return '<div style="margin-top: 6px; margin-right: 5px; margin-left: 5px; text-align: right;" id="usersGridButtonHeader">Add &nbsp;<span class="glyphicon glyphicon-plus" aria-hidden="true"> </span></div>'
                        }
                    }
                ]
            });

            $('#editGroupsButtonNewGroup').jqxButton({
                theme: theme,
                width: 120,
                height: 25,
                disabled: false
            });

            $('#editGroupsButtonClose').jqxButton({
                theme: theme,
                width: 120,
                height: 25,
                disabled: false
            });

            isItSecnodOpenGroupsUsers = true;
        }
    });

    $('#editGroupsWindow').on('close', function ()
    {
        // Go back to the initial state
        isInitialFiltering = true;
        $('#listboxUsernames').hide();
        $('#editGroupsWindowContainerButtons').css('left', correctionContainerButtons.collapse);
        $('#editGroupsWindow').jqxWindow({ width: editGroupsWindowWidth.collapse });
        $('#groupsGrid').jqxGrid('unselectrow', currenSelectedGroup);
        $('#usersGrid').jqxGrid('setcolumnproperty', 'user', 'text', 'Users');
        var filtergroup = new $.jqx.filter();
        var usersIdList = [''];
        filtergroup = getFiltering(usersIdList, filtergroup);
        $('#usersGrid').jqxGrid('addfilter', 'id', filtergroup);
        $('#usersGrid').jqxGrid('applyfilters');
        $('#listboxUsernames').jqxListBox('clearSelection');
        currenSelectedGroup = -1;
        currenSelectedGroupName = '';
    });

    $('#editGroupsButtonClose').on('click', function ()
    {
        $('#editGroupsWindow').jqxWindow('close');
    });

    var specialContentSelectorCollection = [];

    /*
     * Create New Tab
     *
     * @param {String} title - title of the new tab.
     * @param {String} content - could create content from <tags>.
     */
    var addTab = function (title, content)
    {
        title = title || 'tabTitle';
        content = content || 'tabContent';
        $('#jqxTabs').jqxTabs('addLast', title, content);
    };

    /*
     * Create Ticket Content
     *
     * @param {String} id - ticket id.
     * @param {Object} data - ticket data is object with information about this.
     */
    var createTicketContent = function (id, data)
    {
        var div = function ()
        {
            return document.createElement('div');
        };

        var wrapper = div();

        var content = div();
        content.className = 'ticket-content';
        content.id = 'ticket-' + id;

        var headerTitle = div();
        headerTitle.className = 'ticket-header';
        headerTitle.id = 'ticketHeader-' + id;
        headerTitle.innerText = data.title;

        // User Controller Ticket Settings - Left / Right
        var settingsController = div();
        settingsController.className = 'ticket-settings-controller';

        var leftClass = 'ticket-controller-left';
        var rightClass = 'ticket-controller-right';

        var leftSection = div();
        leftSection.className = 'ticket-settings-left-section';
        var rightSection = div();
        rightSection.className = 'ticket-settings-right-section';

        // Left side
        var title = div();
        title.classList.add(leftClass, 'ticket-controller-title');
        title.innerText = 'Title:';
        var user = div();
        user.classList.add(leftClass, 'ticket-controller-user');
        user.innerText = 'Username:';
        var status = div();
        status.classList.add(leftClass, 'ticket-controller-status');
        status.innerText = 'Status:';
        leftSection.appendChild(title);
        leftSection.appendChild(user);
        leftSection.appendChild(status);

        // Right side
        var titleContent = document.createElement('input');
        var titleContentId = 'ticketTitleContent' + id;
        titleContent.id = titleContentId;
        titleContent.className = rightClass;

        var userContent = div();
        var userContentId = 'ticketUserContent' + id;
        userContent.id = userContentId;
        userContent.className = rightClass;
        userContent.style.display = 'inline-block';

        var statusContent = div();
        var statusContentId = 'ticketStatusContent' + id;
        statusContent.id = statusContentId;
        statusContent.classList = rightClass;
        rightSection.appendChild(titleContent);
        rightSection.appendChild(userContent);
        rightSection.appendChild(statusContent);

        settingsController.appendChild(leftSection);
        settingsController.appendChild(rightSection);
        var boundery = div();
        boundery.className = 'clearing';
        settingsController.appendChild(boundery);

        // Save Button - save settings
        var saveButton = document.createElement('button');
        var saveButtonId = 'ticketSaveButton' + id;
        saveButton.id = saveButtonId;
        saveButton.innerText = 'Save';

        var sectionSave = div();
        sectionSave.className = 'ticket-settings-save-section';
        sectionSave.appendChild(document.createElement('hr'));
        sectionSave.appendChild(saveButton);
        sectionSave.appendChild(document.createElement('hr'));
        settingsController.appendChild(sectionSave);

        // Comments blog
        var commentsContent = div();
        commentsContent.className = 'ticket-comments';
        commentsContent.id = 'ticketComments' + id;

        // Append to main content
        content.appendChild(headerTitle);
        content.appendChild(settingsController);
        content.appendChild(commentsContent);

        wrapper.appendChild(content);

        return wrapper.innerHTML;
    };

    var createComments = function (ticketId)
    {
        var comments = initialData.Comments;
        var commentsContentId = 'ticketComments' + ticketId;
        var infoComments = '<h3>Comments<h3>';
        var numberOfComments = 0;
        var infoCommentsContent = '<div>';
        for (var d = 0; d < comments.length; d += 1)
        {
            var comment = comments[d];
            var commentTicketId = comment.TicketId;
            if (commentTicketId === ticketId)
            {
                numberOfComments += 1;
                infoCommentsContent += ''
                    + '<p>' + '<strong>' + comment.Date + '</strong> added by: ' + comment.By + '</p>'
                    + '<p>' + comment.Description + '</p>'
                    + '<br>'
            }
        }

        if (numberOfComments < 1)
        {
            infoCommentsContent = '<p>There are no comments</p>';
        }

        infoCommentsContent += '</div>';
        infoComments += infoCommentsContent;

        $('#' + commentsContentId).html(infoComments);
    };
    var getIdFromTitle = function (title)
    {
        var firstIndex = title.lastIndexOf(' ') + 1;
        return title.substr(firstIndex);
    };
    var getIndexOfTab = function (tabIndex)
    {
        var length = $('#jqxTabs').jqxTabs('length');
        for (var i = 0; i < length; i += 1)
        {
            var textTitle = $('#jqxTabs').jqxTabs('getTitleAt', i);
            var currentTextTitleId = getIdFromTitle(textTitle) | 0;
            if (currentTextTitleId === tabIndex)
            {
                // If found matched in the elements will return this index.
                return i;
            }
        }

        return false;
    };

    /*
        WINDOW Add group
    */
    $('#addGroupWindow').jqxWindow({
        autoOpen: false,
        isModal: true,
        width: 300,
        height: 120,
        theme: theme,
        initContent: function ()
        {
            /*
                WINDOW Add group - style and functionality
            */
            $('#addGroupNameInput').jqxInput({
                theme: theme,
                placeHolder: 'Enter new group',
                width: 280,
                height: 25
            });

            $('#addGroupButtonOk').jqxButton({
                theme: theme,
                width: 80,
                height: 25,
                disabled: false
            });

            $('#addGroupWindowCancel').jqxButton({
                theme: theme,
                width: 80,
                height: 25,
                disabled: false
            });

            $('#addGroupWindow').on('open', function (event)
            {
                $('#addGroupNameInput').jqxInput('focus');
            });

            $('#addGroupNameInput').jqxTooltip({
                position: 'top',
                theme: themeD,
                content: 'The Group name cannot be empty.',
                width: 240,
                height: 30,
                autoHide: true
            });

            $('#addGroupButtonOk').on('click', function ()
            {
                var newGroupName = $('#addGroupNameInput').jqxInput('val');
                if (VALIDATION.emptyString(newGroupName))
                {
                    var numberOfGroups = initialData.Groups.length;
                    var newGroupId = initialData.Groups[numberOfGroups - 1].GroupId + 1;
                    initialData.Groups.push({ GroupId: newGroupId, GroupName: newGroupName, UsersIdList: [] });

                    $('#listboxGroups').jqxListBox('refresh');
                    $('#groupsGrid').jqxGrid('updatebounddata');
                    $('#addGroupNameInput').jqxTooltip('close');
                    $('#addGroupWindow').jqxWindow('close');
                } else
                {
                    $('#addGroupNameInput').jqxTooltip('open');
                }
            });
        }
    });

    $('#editGroupsButtonNewGroup').on('click', function ()
    {
        $('#addGroupWindow').jqxWindow('open');
        $('#addGroupNameInput').jqxInput('val', null);
    });

    $('#addGroupWindowCancel').on('click', function ()
    {
        $('#addGroupWindow').jqxWindow('close');
    });

    /*
        Initialize Base Widget (Ticketing system)
    */
    function initializeWidget()
    {
        /*
            HEADER group
        */
        var header = $('<div><div class="col-md-8 header-text">Ticketing System</div><div class="col-md-4 header-text" style="text-align:right; padding-right: 28px;"><span id="headerUserName">' + logInUser.Name + '</div></div>');
        header.addClass('header');
        $('.headers-container').append(header);

        $('#headerUserName').on('click', function ()
        {
            $('#loginWindow').jqxWindow('open');
            $('#loginSubmitButton').on('click', function () {
                $('#loginWindow').jqxWindow('close');
                var inputUsername = $('#loginUserNameInput').jqxDropDownList('getSelectedItem');
                logInUser.Name = inputUsername.label;
                logInUser.UserId = inputUsername.value;
                changeHeaderUserName(logInUser.Name);
                $('#loginSubmitButton').off('click');
                $('#dashboardProjectMembersGrid').jqxGrid('updatebounddata');
                $('#editUserGroupsGrid').jqxGrid('updatebounddata');
                $('#dashboardTicketsGrid').jqxGrid('updatebounddata');
  
            });
        });

        /*
            CONTAINER group
        */
        var container = $('<div id="layout">'
                            + '<div data-container="layoutPanelLeft"><div id="projectsGrid"></div></div>'
                            + '<div data-container="layoutPanelRight">'
                                + '<div id="jqxTabs" style="margin-left:auto; margin-right:auto;">'
                                        + '<ul>'
                                            + '<li style="margin-left: 30px;">'
                                               + ' <div style="height: 20px; margin-top: 5px;">'
                                                   + ' <div>US Indexes</div>'
                                               + '</div>'
                                           + ' </li>'
                                        + '</ul>'
                                        + '<div style="overflow: hidden;">'
                                                + '<div id="dashboardColumnChart" style="float: left; width: 48%; height: 47%; margin-top: 1%; margin-bottom: 1%; margin-left: 1%;"></div>'
                                                + '<div id="dashboardTicketsGrid" style="float: left; margin-left: 1%; margin-top: 1%; margin-bottom: 1%;"></div>'
                                                + '<div id="dashboardLineChart" style="float: left; width: 48%; height: 47%; margin-left: 1%;"></div>'
                                                + '<div id="dashboardProjectMembersGrid" style="float: left; margin-left: 1%; "></div>'
                                                + '<div class="clearing"></div>'
                                        + '</div>'
                                + '</div>'
                            + '</div>'
                        + '</div>');
        container.addClass('project-container');
        $('.containers-container').append(container);

        var ticketingSystemLayout = [{
            type: 'layoutGroup',
            orientation: 'horizontal',
            items: [{
                type: 'tabbedGroup',
                alignment: 'left',
                width: '20%',
                items: [{
                    type: 'layoutPanel',
                    title: 'Projects',
                    contentContainer: 'layoutPanelLeft',
                    initContent: function ()
                    {
                        var projectsGridLocalData = [{ project: 'IT' }, { project: 'SDK' }];
                        var projectsGridSource =
                        {
                            datatype: 'array',
                            datafields: [
                                { name: 'project', type: 'string' },
                            ],
                            localdata: projectsGridLocalData
                        };
                        var projectsGridDataAdapter = new $.jqx.dataAdapter(projectsGridSource);
                        var specialTabTitlesCollection = [];

                        $('#projectsGrid').jqxGrid({
                            width: '99%',
                            autoheight: true,
                            showheader: false,
                            theme: theme,
                            source: projectsGridDataAdapter,
                            ready: function ()
                            {
                                $('#projectsGrid').jqxGrid('selectrow', loadedProject);

                                $('#projectsGrid').on('cellclick', function (event)
                                {
                                    var args = event.args;
                                    var rowBoundIndex = args.rowindex;
                                    var dataField = args.datafield;
                                    var projectName = $('#projectsGrid').jqxGrid('getcellvalue', rowBoundIndex, 'project');

                                    var changedChartData = initialData.Projects[rowBoundIndex].sampleData;

                                    for (var s in sourcesOfChartsForUpdates)
                                    {
                                        sourcesOfChartsForUpdates[s].localdata = changedChartData;
                                    }

                                    for (var a in adaptersOfChartsForUpdates)
                                    {
                                        adaptersOfChartsForUpdates[a].dataBind();
                                    }

                                    $('#dashboardColumnChart').jqxChart('update');
                                    $('#dashboardLineChart').jqxChart('update');

                                    if (dataField === 'project')
                                    {
                                        loadedProject = rowBoundIndex;
                                        $('#dashboardTicketsGrid').jqxGrid('updatebounddata');
                                        $('#dashboardProjectMembersGrid').jqxGrid('updatebounddata');

                                        var title = $('#dashboardProjectMembersGrid').jqxGrid('columngroups')[0].text;
                                        var project = initialData.Projects[rowBoundIndex];
                                        var leaderId = project.Lead;
                                        var users = initialData.Users;
                                        for (var user in users)
                                        {
                                            var currentUser = users[user];
                                            if (currentUser.UserId === leaderId)
                                            {
                                                var leaderName = currentUser.Name;
                                                $('#dashboardProjectMembersGrid').jqxGrid({
                                                    columngroups: [{
                                                        text: 'Project-Members - Lead: ' + leaderName,
                                                        name: 'Title',
                                                        align: 'left'
                                                    }]
                                                });

                                                break;
                                            }
                                        }
                                    }

                                    var getIndexOfTabProject = function (title)
                                    {
                                        var length = $('#jqxTabs').jqxTabs('length');
                                        for (var i = 0; i < length; i += 1)
                                        {
                                            var currentTabTitle = $('#jqxTabs').jqxTabs('getTitleAt', i);
                                            if (title === currentTabTitle)
                                            {
                                                return i;
                                            }
                                        }

                                        return false;
                                    };

                                    var createTabContent = function (content, id)
                                    {
                                        var userIndicator = $('<div/>');
                                        userIndicator.css({
                                            'margin': '10px',
                                            'padding-bottom': '25px'
                                        });

                                        var classLabel = 'project-label';
                                        // User
                                        var comboboxId = id + 'Combobox';
                                        var labelUser = $('<label>');
                                        labelUser.prop('id', comboboxId + 'Label');
                                        labelUser.addClass(classLabel);
                                        labelUser.text('User: ');
                                        labelUser.css({
                                            'float': 'left',
                                            'display': 'inline-block',
                                            'padding-top': '5px',
                                            'padding-right': '20px',
                                            'font-weight': 'lighter'
                                        });
                                        var userCombobox = $('<div/>');
                                        userCombobox.prop('id', comboboxId);
                                        userCombobox.css({
                                            'float': 'left',
                                            'margin-right': '50px',
                                        });

                                        // Status
                                        var statusComboboxId = id + 'ComboboxStatus';
                                        var labelStatus = $('<label>');
                                        labelStatus.prop('id', statusComboboxId + 'Label');
                                        labelStatus.addClass(classLabel);
                                        labelStatus.prop('for', statusComboboxId);
                                        labelStatus.text('Status: ');
                                        labelStatus.css({
                                            'float': 'left',
                                            'display': 'inline-block',
                                            'padding-top': '5px',
                                            'padding-right': '20px',
                                            'font-weight': 'lighter'
                                        });
                                        var statusCombobox = $('<div/>');
                                        statusCombobox.prop('id', statusComboboxId);
                                        statusCombobox.css({
                                            'float': 'left'
                                        });

                                        // Refresh Button
                                        var refresh = $('<button/>');
                                        refresh.prop('id', id + 'Button');
                                        refresh.text('Refresh');
                                        refresh.css({
                                            'float': 'left',
                                            'margin-left': '70px'
                                        });

                                        userIndicator
                                            .append(labelUser)
                                            .append(userCombobox)
                                            .append(labelStatus)
                                            .append(statusCombobox)
                                            .append(refresh);

                                        // Grid
                                        var userGrid = $('<div/>');
                                        userGrid.prop('id', id + 'Grid');

                                        content.append(userIndicator);
                                        content.append($('<div style="height: 20px;"></div>'));
                                        content.append(userGrid);
                                    };

                                });
                            },
                            columns: [
                                { text: 'Project', datafield: 'project' }
                            ]
                        });
                    }
                }]
            }, {
                type: 'tabbedGroup',
                allowPin: false,
                width: '80%',
                items: [{
                    type: 'layoutPanel',
                    title: 'Dashboard',
                    contentContainer: 'layoutPanelRight',
                    initContent: function ()
                    {
                        $('#jqxTabs').jqxTabs({ theme: theme, width: '99%', height: '99%', showCloseButtons: true });

                        $('#jqxTabs').jqxTabs('hideCloseButtonAt', 0);
                        var firstLoadChartData = initialData.Projects[loadedProject].sampleData;
                        var ticketStatusChartSource = {
                            datatype: 'json',
                            datafields: [
                                { name: 'a' },
                                { name: 'b' },
                                { name: 'c' }
                            ],
                            localdata: firstLoadChartData,
                        };
                        var ticketStatusChartAdapter = new $.jqx.dataAdapter(ticketStatusChartSource);
                        sourcesOfChartsForUpdates.push(ticketStatusChartSource);
                        adaptersOfChartsForUpdates.push(ticketStatusChartAdapter);

                        var settings = {
                            source: ticketStatusChartAdapter,
                            title: 'Ticket status summary',
                            description: '',
                            enableAnimations: true,
                            colorScheme: 'scheme02',
                            seriesGroups: [{
                                useGradient: false,
                                type: 'column',
                                valueAxis: {
                                    description: 'Value',
                                    logarithmicScale: true,
                                    logarithmicScaleBase: 2,
                                    unitInterval: 1,
                                    tickMarksInterval: 1,
                                    gridLinesInterval: 1,
                                    horizontalTextAlignment: 'right'
                                },
                                xAxis: {
                                    unitInterval: 1,
                                    minValue: 0,
                                    maxValue: today.getMonth(),
                                    labels:
                                    {
                                        formatFunction: function (value)
                                        {
                                            return months[value];
                                        }
                                    },
                                },
                                series: [{
                                    dataField: 'a',
                                    displayText: 'Open'
                                }, {
                                    dataField: 'b',
                                    displayText: 'Pending'
                                }, {
                                    dataField: 'c',
                                    displayText: 'Close'
                                }]
                            }]
                        };

                        $('#dashboardColumnChart').jqxChart(settings);

                        var firstLoadChartOpenCloseSummaryData = initialData.Projects[loadedProject].sampleData;
                        var ticketChartOpenCloseSummarySource = {
                            datatype: 'json',
                            datafields: [
                                { name: 'a' },
                                { name: 'c' }
                            ],
                            localdata: firstLoadChartData,
                        };
                        var ticketChartOpenCloseSummaryAdapter = new $.jqx.dataAdapter(ticketChartOpenCloseSummarySource);
                        sourcesOfChartsForUpdates.push(ticketChartOpenCloseSummarySource);
                        adaptersOfChartsForUpdates.push(ticketChartOpenCloseSummaryAdapter);

                        var settings = {
                            source: ticketChartOpenCloseSummaryAdapter,
                            title: 'Month ticket open summary',
                            description: '',
                            animationDuration: 0,
                            padding: {
                                left: 5,
                                top: 5,
                                right: 10,
                                bottom: 5
                            },
                            titlePadding: {
                                left: 10,
                                top: 5,
                                right: 0,
                                bottom: 10
                            },
                            enableAnimations: true,
                            categoryAxis: {
                                dataField: '',
                                description: '',
                                showGridLines: true,
                                showTickMarks: true
                            },
                            colorScheme: 'scheme08',
                            seriesGroups: [{
                                type: 'line',
                                xAxis:
                                {
                                    minValue: 0,
                                    maxValue: today.getMonth(),
                                    labels:
                                    {
                                        formatFunction: function (value)
                                        {
                                            return months[value];
                                        }
                                    },
                                },
                                valueAxis: {
                                    description: 'Value',
                                    logarithmicScale: true,
                                    logarithmicScaleBase: 2,
                                    unitInterval: 1,
                                    tickMarksInterval: 1,
                                    gridLinesInterval: 1,
                                    horizontalTextAlignment: 'right'
                                },
                                series: [{
                                    dashStyle: '8,5',
                                    lineWidth: 2,
                                    dataField: 'c',
                                    displayText: 'Close'
                                }, {
                                    lineWidth: 5,
                                    dataField: 'a',
                                    displayText: 'Open'
                                }]
                            }]
                        };

                        $('#dashboardLineChart').jqxChart(settings);

                        var dashboardTicketsGridSource =
                        {
                            datatype: 'json',
                            datafields: [
                                { name: 'ticketId', type: 'number', map: 'TicketId' },
                                { name: 'ticketTitle', type: 'string', map: 'Title' },
                                { name: 'userId', type: 'number', map: 'UserId' },
                                { name: 'userName', type: 'string' },
                                { name: 'ticketCreated', type: 'date', map: 'CreatedOn' },
                                { name: 'ticketLastModified', type: 'date', map: 'ModifiedOn' },
                                { name: 'project', type: 'number', map: 'ProjectId' },
                                { name: 'project', type: 'number', map: 'ProjectId' },
                                { name: 'Status' }
                            ],
                            root: 'Tickets',
                            localdata: initialData
                        };

                        var dashboardTicketsGridDataAdapter = new $.jqx.dataAdapter(dashboardTicketsGridSource, {
                            beforeLoadComplete: function (records)
                            {
                                var updatedRecords = new Array();
                                var projectInfo = initialData.Projects[loadedProject];
                                var projectInfoId = projectInfo.ProjectId;
                                for (var rec in records)
                                {
                                    var currentRec = records[rec];
                                    if (currentRec.userId === logInUser.UserId && currentRec.project === projectInfoId)
                                    {
                                        currentRec.userName = logInUser.Name;
                                        updatedRecords.push(currentRec);
                                    }
                                }

                                return updatedRecords;
                            }
                        });

                        var selectedTab = -1;
                        $('#jqxTabs').on('selected', function (event)
                        {
                            selectedTab = event.args.item;
                            var textTitle = $('#jqxTabs').jqxTabs('getTitleAt', selectedTab);
                            var currentTicketId = getIdFromTitle(textTitle);

                            var currentTicketHeaderTitle = $('#ticketHeader-' + currentTicketId);
                            var titleBefore = currentTicketHeaderTitle.text();
                            currentTicketHeaderTitle.text(titleBefore);

                            var currentTicketTitleInputId = 'ticketTitleContent' + currentTicketId;
                            $('#' + currentTicketTitleInputId).val(titleBefore);
                            $('#' + currentTicketTitleInputId).keyup(function ()
                            {
                                var changedHeaderContent = $('#' + currentTicketTitleInputId).val();
                                currentTicketHeaderTitle.text(changedHeaderContent);
                            });
                            event.stopPropagation();
                        });

                        $('#dashboardTicketsGrid').jqxGrid({
                            width: '48%',
                            height: '47%',
                            theme: theme,
                            sortable: true,
                            source: dashboardTicketsGridDataAdapter,
                            ready: function ()
                            {
                                $('#dashboardTicketsGrid').on('cellclick', function (event)
                                {
                                    var args = event.args;
                                    var rowBoundIndex = args.rowindex;
                                    var dataField = args.datafield;

                                    if (dataField === 'edit')
                                    {
                                        var data = $('#dashboardTicketsGrid').jqxGrid('getrowdata', rowBoundIndex);
                                        var ticketId = data.ticketId | 0;
                                        var ticketTitle = data.ticketTitle;

                                        var content = {
                                            title: ticketTitle
                                        };

                                        var indexOfTab = getIndexOfTab(ticketId);
                                        if (!!indexOfTab)
                                        {
                                            // If tab is open -> focus on him
                                            $('#jqxTabs').jqxTabs('select', indexOfTab);
                                        } else
                                        {
                                            // The tab is not created -> create this
                                            addTab('Ticket ID: ' + ticketId,
                                                createTicketContent(ticketId, content) +
                                                '');

                                            var titleContentId = 'ticketTitleContent' + ticketId;
                                            var userContentId = 'ticketUserContent' + ticketId;
                                            var statusContentId = 'ticketStatusContent' + ticketId;
                                            var saveButtonId = 'ticketSaveButton' + ticketId;
                                            var userContentId = 'ticketUserContent' + ticketId;

                                            // - Title Control - input
                                            $('#' + titleContentId).jqxInput({
                                                placeHolder: 'Enter a Title',
                                                height: 25,
                                                width: '79.5%',
                                                theme: theme
                                            });

                                            // - User Control -
                                            var usersListSource =
                                            {
                                                datatype: 'json',
                                                datafields: [
                                                    { name: 'id', type: 'string', map: 'UserId' },
                                                    { name: 'user', type: 'string', map: 'Name' },
                                                ],
                                                root: 'Users',
                                                localdata: initialData,
                                                deleterow: function (rowid, commit)
                                                {
                                                    // synchronize with the server - send delete command
                                                    // call commit with parameter true if the synchronization with the server was successful
                                                    // and with parameter false if the synchronization has failed.
                                                    commit(true);
                                                }
                                            };
                                            var authorizedIdArray = initialData.Projects[loadedProject].UsersIdList;
                                            var selectId = authorizedIdArray.indexOf(logInUser.UserId);
                                            var dataAdapterUsersList = new $.jqx.dataAdapter(usersListSource, {
                                                beforeLoadComplete: function (records)
                                                {
                                                    var updatedRecords = new Array();
                                                    for (var i in records)
                                                    {
                                                        var record = records[i];
                                                        if (compareUser(authorizedIdArray, record.id))
                                                        {
                                                            updatedRecords.push(record);
                                                        }
                                                    }

                                                    return updatedRecords;
                                                }
                                            });

                                            $('#' + userContentId).jqxDropDownList({
                                                width: '80%',
                                                height: 25,
                                                theme: theme,
                                                selectedIndex: selectId,
                                                source: dataAdapterUsersList,
                                                displayMember: 'user',
                                                valueMember: 'id',
                                                autoDropDownHeight: true
                                            });

                                            // - Status Control -
                                            var status = {
                                                1: 'PENDING',
                                                2: 'OPEN',
                                                3: 'CLOSE'
                                            };
                                            var statusIndex = 1;
                                            if (data.Status === 'Pending')
                                                statusIndex = 0;
                                            if (data.Status === 'Close')
                                                statusIndex = 2;

                                            $('#' + statusContentId).jqxDropDownList({
                                                width: '80%',
                                                height: 25,
                                                theme: theme,
                                                selectedIndex: statusIndex,
                                                source: status,
                                                autoDropDownHeight: true
                                            });

                                            // - Save Button -
                                            $('#' + saveButtonId).jqxButton({
                                                width: 100,
                                                height: 30,
                                                theme: theme
                                            });
                                            $("#messageNotification").jqxNotification({
                                                width: 250, position: "top-right", opacity: 0.9,
                                                autoOpen: false, animationOpenDelay: 800, autoClose: true, autoCloseDelay: 3000, template: "success"
                                            });
                                            $('#' + saveButtonId).on('click', function ()
                                            {
                                                var tickets = initialData.Tickets;
                                                for (var i in tickets)
                                                {
                                                    var currentTicket = tickets[i];
                                                    var currentTicketId = currentTicket.TicketId
                                                    if (currentTicketId === ticketId)
                                                    {
                                                        initialData.Tickets[i].Title = $('#' + titleContentId).jqxInput('val');
                                                        var selectedItemID = $('#' + userContentId).jqxDropDownList('getSelectedItem').value;
                                                        initialData.Tickets[i].UserId = selectedItemID;
                                                        initialData.Tickets[i].ModifiedOn = new Date();
                                                        var statusValue = status[$('#' + statusContentId).jqxDropDownList('val')];
                                                        var currentStatus = capitalize(statusValue.toLowerCase());
                                                        initialData.Tickets[i].Status = currentStatus;
                                                        for (var m = 0; m < specialContentSelectorCollection.length; m += 1)
                                                        {
                                                            var currentSpecialSelectorName = specialContentSelectorCollection[m];
                                                            $('#' + currentSpecialSelectorName + 'Grid').jqxGrid('updatebounddata');
                                                        }

                                                        $('#dashboardTicketsGrid').jqxGrid('updatebounddata');
                                                        $("#ticketInfo").html("Ticket" + currentTicketId + " is updated");
                                                        $("#messageNotification").jqxNotification("open");
                                                        break;
                                                    }
                                                }
                                            });

                                            // - Comment Control -
                                            createComments(ticketId);
                                        }
                                    }
                                });
                            },
                            columns: [
                                {
                                    text: 'Id', width: '15%',
                                    sortable: false,
                                    datafield: 'ticketId'
                                },
                                {
                                    text: 'Title', width: '35%',
                                    datafield: 'ticketTitle'
                                },
                                {
                                    text: 'Created',
                                    width: '15%',
                                    datafield: 'ticketCreated',
                                    cellsformat: 'dd-MMM-yyyy HH:mm'
                                },
                                {
                                    text: 'Last modified', width: '25%',
                                    datafield: 'ticketLastModified',
                                    cellsformat: 'dd-MMM-yyyy HH:mm'
                                },
                                {
                                    text: '', width: '10%',
                                    sortable: false,
                                    datafield: 'edit',
                                    cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                    {
                                        return '<div style="text-align: center; margin-top: 5px;"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></div>';
                                    }
                                }
                            ]
                        });

                        $('#dashboardTicketsGrid .jqx-grid-column-header:first-child div').off('click');
                        $('#dashboardTicketsGrid .jqx-grid-column-header:last-child div').off('click');

                        var dashboardProjectMembersGridSource =
                        {
                            datatype: 'json',
                            datafields: [
                                { name: 'id', type: 'number', map: 'UserId' },
                                { name: 'user', type: 'string', map: 'Name' }
                            ],
                            localdata: initialData,
                            root: 'Users'
                        };
                        var compareUser = function (idArray, userId)
                        {
                            for (var t = 0; t < idArray.length; t += 1)
                            {
                                if (idArray[t] === userId)
                                {
                                    return true;
                                }
                            }

                            return false;
                        };
                        var dashboardProjectMembersGridDataAdapter = new $.jqx.dataAdapter(dashboardProjectMembersGridSource, {
                            beforeLoadComplete: function (records)
                            {
                                var updatedRecords = new Array();
                                var project = initialData.Projects[loadedProject];
                                var projectUsers = project.UsersIdList;
                                for (var rec in records)
                                {
                                    var currentRec = records[rec];
                                    var currentUserId = currentRec.id;

                                    if (compareUser(projectUsers, currentUserId))
                                    {
                                        updatedRecords.push(currentRec);
                                    }

                                }

                                return updatedRecords;
                            }
                        });

                        var firstLoadLeadName = '';
                        var leadId = initialData.Projects[0].Lead;
                        var usersList = initialData.Users;
                        for (var ind = 0; ind < usersList.length; ind += 1)
                        {
                            if (usersList[ind].UserId === leadId)
                            {
                                firstLoadLeadName = usersList[ind].Name;
                                break;
                            }
                        }

                        $('#dashboardProjectMembersGrid').jqxGrid({
                            width: '48%',
                            height: '47%',
                            theme: theme,
                            sortable: true,
                            rowsheight: 26,
                            source: dashboardProjectMembersGridDataAdapter,
                            columns: [
                                { text: 'Name', width: '90%', datafield: 'user', columngroup: 'Title' },
                                {
                                    text: '', width: '10%', datafield: 'edit',
                                    columngroup: 'Title',
                                    columntype: 'button',
                                    sortable: false,
                                    cellsrenderer: function (row, columnfield, value, defaulthtml, columnproperties)
                                    {
                                        return 'Edit';
                                    },
                                    buttonclick: function (row)
                                    {
                                        var records = dashboardProjectMembersGridDataAdapter.getrecords();
                                        var data = $('#dashboardProjectMembersGrid').jqxGrid('getrowdata', row);
                                        var currentUserId = data.id;
                                        var currentUserName = data.user;
                                        currentEditUser.UserId = currentUserId;
                                        currentEditUser.Name = currentUserName;
                                        isLogInUser = false;
                                        if (currentUserName === logInUser.Name)
                                        {
                                            isLogInUser = true;
                                        }

                                        arrayGroupsSelectedUser = getGroupsRelatedUserId(currentUserId);
                                        setTimeout(function ()
                                        {
                                            $('#editUserNameInput').jqxInput('val', currentUserName);
                                            changeEditUserNameInput(currentUserName);
                                            getFilteringGroups();
                                        }, 130);

                                        $('#editUserWindow').jqxWindow('open');
                                    }
                                },
                            ],
                            columngroups: [{
                                text: 'Project-Members - Lead: ' + firstLoadLeadName,
                                name: 'Title',
                                align: 'left'
                            }]
                        });

                    }
                }] // End - layoutDashboard ITEMS
            }]
        }];

        $('#layout').jqxLayout({
            width: '100%',
            height: '100%',
            theme: theme,
            layout: ticketingSystemLayout,
            minGroupWidth: '20%'
        });
    }

    var alternativeName = 'unnamed';
    var changeHeaderUserName = function (name)
    {
        // delete unneeded
        name = name || alternativeName;
        $('#headerUserName').text(name);
    }

    var changeEditUserNameInput = function (name)
    {
        // delete unneeded
        name = name || alternativeName;
        $('#editUserUserName').text(name);
    }
});