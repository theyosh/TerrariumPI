<!DOCTYPE html>
<html lang="en">
<head>
    <title id='Description'>In order to enter in edit mode, click any of the 'Edit' buttons. To save the changes, click the 'Save' button in the popup dialog. To cancel the changes
    click the 'Cancel' button in the popup dialog.</title>
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
    <script type="text/javascript" src="../../scripts/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script> 
    <script type="text/javascript" src="../../jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxscrollbar.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxmenu.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.pager.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script> 
    <script type="text/javascript" src="../../jqwidgets/jqxwindow.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxlistbox.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdropdownlist.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxinput.js"></script>
    <script type="text/javascript" src="../../scripts/gettheme.js"></script>
    <script type="text/javascript">
        $(document).ready(function () {
            var source =
            {
                datatype: "json",
			    datafields: [
					 { name: 'EmployeeID', type: 'string'},
					 { name: 'FirstName', type: 'string'},
					 { name: 'LastName', type: 'string'},
					 { name: 'Title', type: 'string'}
                ],
				cache: false,
				id: 'EmployeeID',
                url: 'data.php',           
                updaterow: function (rowid, rowdata, commit) {
			        // synchronize with the server - send update command
                    var data = "update=true&FirstName=" + rowdata.FirstName + "&LastName=" + rowdata.LastName + "&Title=" + rowdata.Title;
					data = data + "&EmployeeID=" + rowid;
					
					$.ajax({
						dataType: 'json',
						url: 'data.php',
						type: 'POST',
						data: data,
						success: function (data, status, xhr) {
							// update command is executed.
							commit(true);
						}
					});		
                }
            };
			
			var dataAdapter = new $.jqx.dataAdapter(source);

            // initialize the input fields.
            $("#firstName").jqxInput({width: 150, height: 23});
            $("#lastName").jqxInput({width: 150, height: 23});
            $("#title").jqxInput({width: 150, height: 23});
        
            var dataAdapter = new $.jqx.dataAdapter(source);
            var editrow = -1;

            // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {
                width: 600,
                source: dataAdapter,	
                autoheight: true,
                columns: [
				  { text: 'EmployeeID', editable: false, datafield: 'EmployeeID', width: 100 },
				  { text: 'First Name', columntype: 'dropdownlist', datafield: 'FirstName', width: 100 },
				  { text: 'Last Name', columntype: 'dropdownlist', datafield: 'LastName', width: 100 },
				  { text: 'Title', datafield: 'Title', width: 180 },
                  { text: 'Edit', datafield: 'Edit', columntype: 'button', cellsrenderer: function () {
                     return "Edit";
					 }, buttonclick: function (row) {
                     // open the popup window when the user clicks a button.
                     editrow = row;
                     var offset = $("#jqxgrid").offset();
                     $("#popupWindow").jqxWindow({ position: { x: parseInt(offset.left) + 60, y: parseInt(offset.top) + 60 } });

                     // get the clicked row's data and initialize the input fields.
                     var dataRecord = $("#jqxgrid").jqxGrid('getrowdata', editrow);
                     $("#firstName").val(dataRecord.FirstName);
                     $("#lastName").val(dataRecord.LastName);
                     $("#title").val(dataRecord.Title);
                  
                     // show the popup window.
                     $("#popupWindow").jqxWindow('open');
                 }
                 }
                ]
            });

            // initialize the popup window and buttons.
            $("#popupWindow").jqxWindow({
                width: 280, resizable: false, isModal: true, autoOpen: false, cancelButton: $("#Cancel"), modalOpacity: 0.01           
            });

            $("#popupWindow").on('open', function () {
                $("#firstName").jqxInput('selectAll');
            });
         
            $("#Cancel").jqxButton();
            $("#Save").jqxButton();

            // update the edited row when the user clicks the 'Save' button.
            $("#Save").click(function () {
                if (editrow >= 0) {
                    var row = { FirstName: $("#firstName").val(), LastName: $("#lastName").val(), Title: $("#title").val()};
                	
                    var rowID = $('#jqxgrid').jqxGrid('getrowid', editrow);
                    $('#jqxgrid').jqxGrid('updaterow', rowID, row);
                    $("#popupWindow").jqxWindow('close');
                }
            });
        });
    </script>
</head>
<body class='default'>
    <div id='jqxWidget'>
        <div id="jqxgrid"></div>
        <div style="margin-top: 30px;">
            <div id="cellbegineditevent"></div>
            <div style="margin-top: 10px;" id="cellendeditevent"></div>
       </div>
       <div id="popupWindow">
            <div>Edit</div>
            <div style="overflow: hidden;">
                <table>
                    <tr>
                        <td align="right">First Name:</td>
                        <td align="left"><input id="firstName" /></td>
                    </tr>
                    <tr>
                        <td align="right">Last Name:</td>
                        <td align="left"><input id="lastName" /></td>
                    </tr>
                    <tr>
                        <td align="right">Title:</td>
                        <td align="left"><input id="title"/></td>
                    </tr>
					<tr>
                        <td align="right"></td>
                        <td style="padding-top: 10px;" align="right"><input style="margin-right: 5px;" type="button" id="Save" value="Save" /><input id="Cancel" type="button" value="Cancel" /></td>
                    </tr>          	
                </table>
            </div>
       </div>
    </div>
</body>
</html>
