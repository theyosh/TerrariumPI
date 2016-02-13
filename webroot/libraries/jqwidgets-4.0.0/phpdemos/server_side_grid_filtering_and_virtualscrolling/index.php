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
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.sort.js"></script>	
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script>	
	<script type="text/javascript" src="../../jqwidgets/jqxgrid.filter.js"></script>		
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>	
	<script type="text/javascript" src="../../jqwidgets/jqxlistbox.js"></script>	
	<script type="text/javascript" src="../../jqwidgets/jqxgrid.pager.js"></script>		
	<script type="text/javascript" src="../../jqwidgets/jqxdropdownlist.js"></script>	
    <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
            var theme = 'classic';
      
            var source =
            {
                 datatype: "json",
                 datafields: [
					 { name: 'ShippedDate', type: 'date'},
					 { name: 'ShipName', type: 'string'},
					 { name: 'ShipAddress', type: 'string'},
					 { name: 'ShipCity', type: 'string'},
					 { name: 'ShipCountry', type: 'string'}
                ],
			    url: 'data.php',
				cache: false,
				filter: function()
				{
					// update the grid and send a request to the server.
					$("#jqxgrid").jqxGrid('updatebounddata', 'filter');
				},
				sort: function()
				{
					// update the grid and send a request to the server.
					$("#jqxgrid").jqxGrid('updatebounddata', 'sort');
				},
				root: 'Rows',
				beforeprocessing: function(data)
				{		
					source.totalrecords = data[0].TotalRows;					
				}
            };		
		    var dataadapter = new $.jqx.dataAdapter(source, {
					loadError: function(xhr, status, error)
					{
						alert(error);
					}
				}
			);
	
            // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {		
                source: dataadapter,
                theme: theme,
				filterable: true,
				sortable: true,
				virtualmode: true,
				showfilterrow: true,
				rendergridrows: function(obj)
				{
					  return obj.data;     
				},
			    columns: [
                      { text: 'Shipped Date', datafield: 'ShippedDate', cellsformat: 'yyyy-MM-dd', width: 200 },
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
    <div id='jqxWidget'">
        <div id="jqxgrid"></div>
    </div>
</body>
</html>
