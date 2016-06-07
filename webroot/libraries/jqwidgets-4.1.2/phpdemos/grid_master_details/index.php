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
				cache: false,
				root: 'Rows',
                beforeprocessing: function (data) {
                    source.totalrecords = data[0].TotalRows;
                }     
            };

            var dataAdapter = new $.jqx.dataAdapter(source);
			
			$("#jqxgrid").jqxGrid(
            {
                source: dataAdapter,
                theme: 'classic',
				pageable: true,
				autoheight: true,
                virtualmode: true,
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
			
			// init Orders Grid
			$("#ordersGrid").jqxGrid(
			{
				virtualmode: true,
				pageable: true,
				autoheight: true,
				theme: 'classic',
				rendergridrows: function (obj) {
					return [];
				},
				columns: [
					  { text: 'Shipped Date', datafield: 'ShippedDate', cellsformat: 'd', width: 200 },
					  { text: 'Ship Name', datafield: 'ShipName', width: 200 },
					  { text: 'Address', datafield: 'ShipAddress', width: 180 },
					  { text: 'City', datafield: 'ShipCity', width: 100 },
					  { text: 'Country', datafield: 'ShipCountry', width: 140 }
				  ]
			});
			
			 $("#jqxgrid").bind('rowselect', function (event) {
				var row = event.args.rowindex;
				var id = $("#jqxgrid").jqxGrid('getrowdata', row)['CustomerID'];
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
					}     
 				};
				var adapter = new $.jqx.dataAdapter(source);
					// initialize jqxGrid
					$("#ordersGrid").jqxGrid(
					{
						source: adapter,
						rendergridrows: function (obj) {
							return obj.data;
						}
					});
			  });
        });
    </script>
</head>
<body class='default'>
   <h3>Customers</h3>
   <div id="jqxgrid"></div>
   <h3>Orders by Customer</h3> 
   <div id="ordersGrid"></div>
</body>
</html>