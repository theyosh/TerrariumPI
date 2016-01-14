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
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.pager.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.selection.js"></script>	
    <script type="text/javascript" src="../../jqwidgets/jqxgrid.sort.js"></script>		
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>	
    <script type="text/javascript">
        $(document).ready(function () {
            // prepare the data
            var theme = 'classic';
        
            var source =
            {
                 datatype: "json",
                 datafields: [
					 { name: 'CompanyName', type: 'string'},
					 { name: 'ContactName', type: 'string'},
					 { name: 'ContactTitle', type: 'string'},
					 { name: 'Address', type: 'string'},
					 { name: 'City', type: 'string'},
					 { name: 'Country', type: 'string'}
                ],
				cache: false,
			    url: 'data.php',
				root: 'Rows',
				beforeprocessing: function(data)
				{		
					source.totalrecords = data[0].TotalRows;
				},
				sort: function()
				{
					// update the grid and send a request to the server.
					$("#jqxgrid").jqxGrid('updatebounddata', 'sort');
				}
            };		
			
		    var dataadapter = new $.jqx.dataAdapter(source);

            // initialize jqxGrid
            $("#jqxgrid").jqxGrid(
            {
                width: 600,
			    source: dataadapter,
                theme: theme,
			    autoheight: true,
				pageable: true,
				virtualmode: true,
				sortable: true,
				rendergridrows: function()
				{
					  return dataadapter.records;     
				},
                columns: [
                      { text: 'Company Name', datafield: 'CompanyName', width: 250 },
                      { text: 'Contact Name', datafield: 'ContactName', width: 200 },
                      { text: 'Contact Title', datafield: 'ContactTitle', width: 200 },
                      { text: 'Address', datafield: 'Address', width: 180 },
                      { text: 'City', datafield: 'City', width: 100 },
                      { text: 'Country', datafield: 'Country', width: 140 }
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
