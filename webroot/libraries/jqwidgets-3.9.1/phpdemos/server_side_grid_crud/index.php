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
    <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
            var data = {};
			var theme = 'classic';
            var firstNames = ["Nancy", "Andrew", "Janet", "Margaret", "Steven", "Michael", "Robert", "Laura", "Anne"];
            var lastNames = ["Davolio", "Fuller", "Leverling", "Peacock", "Buchanan", "Suyama", "King", "Callahan", "Dodsworth"];
            var titles = ["Sales Representative", "Vice President, Sales", "Sales Representative", "Sales Representative", "Sales Manager", "Sales Representative", "Sales Representative", "Inside Sales Coordinator", "Sales Representative"];
            var address = ["507 - 20th Ave. E. Apt. 2A", "908 W. Capital Way", "722 Moss Bay Blvd.", "4110 Old Redmond Rd.", "14 Garrett Hill", "Coventry House", "Miner Rd.", "Edgeham Hollow", "Winchester Way", "4726 - 11th Ave. N.E.", "7 Houndstooth Rd."];
            var city = ["Seattle", "Tacoma", "Kirkland", "Redmond", "London", "London", "London", "Seattle", "London"];
            var country = ["USA", "USA", "USA", "USA", "UK", "UK", "UK", "USA", "UK"];
        

            var generaterow = function (id) {
                var row = {};
                var firtnameindex = Math.floor(Math.random() * firstNames.length);
                var lastnameindex = Math.floor(Math.random() * lastNames.length);
                var k = firtnameindex;

                row["EmployeeID"] = id;
                row["FirstName"] = firstNames[firtnameindex];
                row["LastName"] = lastNames[lastnameindex];
                row["Title"] = titles[k];
                row["Address"] = address[k];
                row["City"] = city[k];
                row["Country"] = country[k];
                row["Notes"] = row["FirstName"] + ' received a BA in computer science from the University of Washington';
              
                return row;
            }

            var source =
            {
                 datatype: "json",
				 cache: false,
                 datafields: [
					 { name: 'EmployeeID', type: 'string'},
					 { name: 'FirstName', type: 'string'},
					 { name: 'LastName', type: 'string'},
					 { name: 'Title', type: 'string'},
					 { name: 'Address', type: 'string'},
					 { name: 'City', type: 'string'},
					 { name: 'Country', type: 'string'},
            		 { name: 'Notes', type: 'string'}
                ],
				id: 'EmployeeID',
                url: 'data.php',
				cache: false,
                addrow: function (rowid, rowdata, position, commit) {
                    // synchronize with the server - send insert command
					var data = "insert=true&" + $.param(rowdata);
					   $.ajax({
                            dataType: 'json',
                            url: 'data.php',
                            data: data,
							cache: false,
                            success: function (data, status, xhr) {
							   // insert command is executed.
								commit(true);
							},
							error: function(jqXHR, textStatus, errorThrown)
							{
								commit(false);
							}
						});							
			    },
                deleterow: function (rowid, commit) {
                    // synchronize with the server - send delete command
            		   var data = "delete=true&" + $.param({EmployeeID: rowid});
				       $.ajax({
                            dataType: 'json',
                            url: 'data.php',
							cache: false,
                            data: data,
                            success: function (data, status, xhr) {
							   // delete command is executed.
							   commit(true);
							},
							error: function(jqXHR, textStatus, errorThrown)
							{
								commit(false);
							}
						});							
			   },
                updaterow: function (rowid, rowdata, commit) {
			        // synchronize with the server - send update command
            		   var data = "update=true&" + $.param(rowdata);
					      $.ajax({
                            dataType: 'json',
                            url: 'data.php',
							cache: false,
                            data: data,
                            success: function (data, status, xhr) {
							  // update command is executed.
						 	  commit(true);
							},
							error: function(jqXHR, textStatus, errorThrown)
							{
							  commit(false);
							}							
						});		
                }
            };
			
			 var dataAdapter = new $.jqx.dataAdapter(source);
            // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {
                width: 500,
                height: 350,
                source: dataAdapter,
                theme: theme,
                columns: [
                      { text: 'EmployeeID', datafield: 'EmployeeID', width: 100 },
                      { text: 'First Name', datafield: 'FirstName', width: 100 },
                      { text: 'Last Name', datafield: 'LastName', width: 100 },
                      { text: 'Title', datafield: 'Title', width: 180 },
                      { text: 'Address', datafield: 'Address', width: 180 },
                      { text: 'City', datafield: 'City', width: 100 },
                      { text: 'Country', datafield: 'Country', width: 140 }
                  ]
            });

            $("#addrowbutton").jqxButton({ theme: theme });
            $("#deleterowbutton").jqxButton({ theme: theme });
            $("#updaterowbutton").jqxButton({ theme: theme });

            // update row.
            $("#updaterowbutton").bind('click', function () {
                var selectedrowindex = $("#jqxgrid").jqxGrid('getselectedrowindex');
                var rowscount = $("#jqxgrid").jqxGrid('getdatainformation').rowscount;
                if (selectedrowindex >= 0 && selectedrowindex < rowscount) {
                    var id = $("#jqxgrid").jqxGrid('getrowid', selectedrowindex);
                    var datarow = generaterow(id);
                    $("#jqxgrid").jqxGrid('updaterow', id, datarow);
                }
            });

            // create new row.
            $("#addrowbutton").bind('click', function () {
				
				var datainformation = $('#jqxgrid').jqxGrid('getdatainformation');
				var rowscount = datainformation.rowscount - 1;
				var data = $('#jqxgrid').jqxGrid('getrowdata', rowscount);
				var lastId = data.EmployeeID;
                var datarow = generaterow(lastId + 1);
		         $("#jqxgrid").jqxGrid('addrow', null, datarow);
            });

            // delete row.
            $("#deleterowbutton").bind('click', function () {
                var selectedrowindex = $("#jqxgrid").jqxGrid('getselectedrowindex');
                var rowscount = $("#jqxgrid").jqxGrid('getdatainformation').rowscount;
                if (selectedrowindex >= 0 && selectedrowindex < rowscount) {
                    var id = $("#jqxgrid").jqxGrid('getrowid', selectedrowindex);
                    $("#jqxgrid").jqxGrid('deleterow', id);
                }
            });
        });
    </script>
</head>
<body class='default'>
    <div id='jqxWidget' style="font-size: 13px; font-family: Verdana; float: left;">
        <div style="float: left;" id="jqxgrid">
        </div>
        <div style="margin-left: 30px; float: left;">
            <div>
                <input id="addrowbutton" type="button" value="Add New Row" />
            </div>
            <div style="margin-top: 10px;">
                <input id="deleterowbutton" type="button" value="Delete Selected Row" />
            </div>
            <div style="margin-top: 10px;">
                <input id="updaterowbutton" type="button" value="Update Selected Row" />
            </div>
        </div>
    </div>
</body>
</html>
