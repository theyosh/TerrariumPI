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
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script>	
    <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
			var source =
			{
				url: 'data.php',
				dataType: 'json',
				datatype: "json",
				cache: false,
				datafields: [
					 { name: 'OrderID', type: 'string' },
					 { name: 'ShippedDate', type: 'date' },
					 { name: 'ShipName', type: 'string' },
					 { name: 'ShipAddress', type: 'string' },
					 { name: 'ShipCity', type: 'string' },
					 { name: 'ShipCountry', type: 'string' }
				],
				root: 'Rows',
				cache: false,
				beforeprocessing: function (data) {
					source.totalrecords = data[0].TotalRows;
				}     
			};

            var dataAdapter = new $.jqx.dataAdapter(source);
			
			$("#jqxgrid").jqxGrid(
            {
                source: dataAdapter,
                theme: 'classic',
				virtualmode: true,
				rendergridrows: function(obj)
				{
					return obj.data;
				},
				columns: [
					  { text: 'ID', datafield: 'OrderID', width: 200 },
					  { text: 'Shipped Date', datafield: 'ShippedDate', cellsformat: 'd', width: 200 },
					  { text: 'Ship Name', datafield: 'ShipName', width: 200 },
					  { text: 'Address', datafield: 'ShipAddress', width: 180 },
					  { text: 'City', datafield: 'ShipCity', width: 100 },
					  { text: 'Country', datafield: 'ShipCountry', width: 140 }
				  ]
            });        
        });
    </script>
</head>
<body class='default'>
   <div id="jqxgrid"></div>
</body>
</html>
