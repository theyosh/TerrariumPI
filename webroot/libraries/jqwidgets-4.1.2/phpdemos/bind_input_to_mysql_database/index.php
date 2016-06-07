<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.classic.css" type="text/css" />
    <script type="text/javascript" src="../../scripts/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
	<script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxinput.js"></script>
    <script type="text/javascript">
        $(document).ready(function () {
			$("#jqxinput").jqxInput(
            {
                theme: 'classic',
				width: 200,
				height: 25,
				source: function (query, response) {
					var dataAdapter = new $.jqx.dataAdapter
					(
						{
							datatype: "json",
					   	    datafields: [
								{ name: 'CompanyName', type: 'string'}
							],
							url: 'data.php'
						},
						{
							autoBind: true,
							formatData: function (data) {
								data.query = query;
								return data;
							},
							loadComplete: function (data) {
								if (data.length > 0) {
									response($.map(data, function (item) {
										return item.CompanyName;
									}));
								}
							}
						}
					);
				}
            });        
        });
    </script>
</head>
<body class='default'>
   <input id="jqxinput"/>
</body>
</html>
