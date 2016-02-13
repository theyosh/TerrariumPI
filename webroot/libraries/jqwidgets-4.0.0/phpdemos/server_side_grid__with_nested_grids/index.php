<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.classic.css" type="text/css" />
    <script type="text/javascript" src="../../scripts/jquery-1.10.2.min.js"></script>  
	<script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxscrollbar.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxlistbox.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdropdownlist.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxmenu.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.js"></script>
	<script type="text/javascript" src="../../jqwidgets/jqxgrid.sort.js"></script>	
	<script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script>
  	<script type="text/javascript" src="../../jqwidgets/jqxgrid.pager.js"></script>
   <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
            var source =
            {
                datatype: "json",
                datafields: [
                    { name: 'CustomerID', type: 'string'},
                    { name: 'CompanyName', type: 'string'},
                    { name: 'ContactName', type: 'string'},
                    { name: 'ContactTitle', type: 'string'},
                    { name: 'Address', type: 'string'},
                    { name: 'City', type: 'string'}
                ],
				id: 'CustomerID',
                url: 'data.php',
				root: 'Rows',
				cache: false,
                beforeprocessing: function (data) {
                    source.totalrecords = data[0].TotalRows;
                },
				sort: function()
				{
					$("#jqxgrid").jqxGrid('updatebounddata', 'sort');
				}				
            };

            var dataAdapter = new $.jqx.dataAdapter(source);
			
			var initrowdetails = function (index, parentElement, gridElement) {      
				var row = index;
				var id = $("#jqxgrid").jqxGrid('getrowdata', row)['CustomerID'];
			    var grid = $($(parentElement).children()[0]);
            
				var source =
				{
					url: 'data.php',
					dataType: 'json',
					data: {customerid: id},
					datatype: "json",
					cache: false,
					datafields: [
						 { name: 'ShippedDate' },
						 { name: 'ShipName' },
						 { name: 'ShipAddress' },
						 { name: 'ShipCity' },
						 { name: 'ShipCountry' }
					],
					root: 'Rows',
					beforeprocessing: function (data) {
						source.totalrecords = data[0].TotalRows;
					},     
					sort: function()
					{
						grid.jqxGrid('updatebounddata', 'sort');
					}
 				};
				var adapter = new $.jqx.dataAdapter(source);

				// init Orders Grid
				grid.jqxGrid(
				{
					virtualmode: true,
					height: 190,
					width: 530,
					sortable: true,
					pageable: true,
					pagesize: 5,
					source: adapter,
					theme: 'classic',
					rendergridrows: function (obj) {
						return obj.data;
					},
					columns: [
						  { text: 'Shipped Date', datafield: 'ShippedDate', cellsformat: 'd', width: 200 },
						  { text: 'Ship Name', datafield: 'ShipName', width: 200 },
						  { text: 'Address', datafield: 'ShipAddress', width: 180 },
						  { text: 'City', datafield: 'ShipCity', width: 100 },
						  { text: 'Country', datafield: 'ShipCountry', width: 140 }
					  ]
				});					
			};
			  
			// set rows details.
            $("#jqxgrid").bind('bindingcomplete', function (event) {
                if (event.target.id == "jqxgrid") {
                    $("#jqxgrid").jqxGrid('beginupdate');
                    var datainformation = $("#jqxgrid").jqxGrid('getdatainformation');
                    for (i = 0; i < datainformation.rowscount; i++) {
                        $("#jqxgrid").jqxGrid('setrowdetails', i, "<div id='grid" + i + "' style='margin: 10px;'></div>", 220, true);
                    }
                    $("#jqxgrid").jqxGrid('resumeupdate');
                }
            });
			
			$("#jqxgrid").jqxGrid(
            {
                source: dataAdapter,
                theme: 'classic',
				pageable: true,
				sortable: true,
				autoheight: true,
                virtualmode: true,
                rowdetails: true,
                initrowdetails: initrowdetails,
                rendergridrows: function () {
                    return dataAdapter.records;
                },				
                columns: [
                  { text: 'Company Name', datafield: 'CompanyName', width: 250},
                  { text: 'ContactName', datafield: 'ContactName', width: 150 },
                  { text: 'Contact Title', datafield: 'ContactTitle', width: 180 },
                  { text: 'Address', datafield: 'Address', width: 200 },
                  { text: 'City', datafield: 'City', width: 120 }
              ]
            });        	
        });
    </script>
</head>
<body class='default'>
   <div id="jqxgrid"></div>
</body>
</html>