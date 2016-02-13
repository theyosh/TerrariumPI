<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.classic.css" type="text/css" />
    <script type="text/javascript" src="../../scripts/jquery-1.10.2.min.js"></script>  
	<script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxscrollbar.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxmenu.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxcheckbox.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxlistbox.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdropdownlist.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.edit.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.pager.js"></script>	
    <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
            var data = {};
			var theme = 'classic';

            var source =
            {
                 datatype: "json",
                 datafields: [
					 { name: 'EmployeeID', type: 'string'},
					 { name: 'FirstName', type: 'string'},
					 { name: 'LastName', type: 'string'},
					 { name: 'Title', type: 'string'},
					 { name: 'Address', type: 'string'},
					 { name: 'City', type: 'string'},
					 { name: 'Country', type: 'string'}
                ],
				id: 'EmployeeID',
                url: 'data.php',    
				root: 'Rows',
				cache: false,
				beforeprocessing: function(data)
				{		
					source.totalrecords = data[0].TotalRows;
				},				
                updaterow: function (rowid, rowdata, commit) {
			        // synchronize with the server - send update command
                    var data = "update=true&FirstName=" + rowdata.FirstName + "&LastName=" + rowdata.LastName + "&Title=" + rowdata.Title;
					data = data + "&Address=" + rowdata.Address + "&City=" + rowdata.City  + "&Country=" + rowdata.Country + "&Notes=''";
					data = data + "&EmployeeID=" + rowdata.EmployeeID;
					
					$.ajax({
						dataType: 'json',
						url: 'data.php',
						data: data,
						success: function (data, status, xhr) {
							// update command is executed.
							commit(true);
						}
					});		
                }
            };
 		    var dataadapter = new $.jqx.dataAdapter(source);
           // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {
                width: 700,
				selectionmode: 'singlecell',
                source: dataadapter,
                theme: theme,
				editable: true,
				autoheight: true,
				pageable: true,
				virtualmode: true,
				rendergridrows: function(obj)
				{
					  return obj.data;     
				},
                columns: [
                      { text: 'EmployeeID', editable: false, datafield: 'EmployeeID', width: 100 },
                      { text: 'First Name', datafield: 'FirstName', width: 100 },
                      { text: 'Last Name', datafield: 'LastName', width: 100 },
                      { text: 'Title', datafield: 'Title', width: 180 },
                      { text: 'Address', datafield: 'Address', width: 180 },
                      { text: 'City', datafield: 'City', width: 100 },
                      { text: 'Country', datafield: 'Country', width: 140 }
                  ]
            });
        });
    </script>
</head>
<body class='default'>
	<div id="jqxgrid">
	</div>
</body>
</html>
