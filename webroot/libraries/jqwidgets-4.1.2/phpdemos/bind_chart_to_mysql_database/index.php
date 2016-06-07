<!DOCTYPE html>
<html lang="en">
<head>
	<link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
	<script type="text/javascript" src="../../scripts/jquery-1.10.2.min.js"></script>
	<script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
	<script type="text/javascript" src="../../jqwidgets/jqxchart.js"></script>	
	<script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script>	
	<script type="text/javascript">
		$(document).ready(function () {
			var source =
			{
				datatype: "json",
				datafields: [
				{ name: 'OrderDate', type: 'date'},
				{ name: 'Quantity'},
				{ name: 'ProductName'}
				],
				url: 'data.php'
			};		
			
			var dataAdapter = new $.jqx.dataAdapter(source,
			{
				autoBind: true,
				async: false,
				downloadComplete: function () { },
				loadComplete: function () { },
				loadError: function () { }
			});
			
		    // prepare jqxChart settings
			var settings = {
			    title: "Orders by Date",
			    showLegend: true,
			    padding: { left: 5, top: 5, right: 50, bottom: 5 },
			    titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
			    source: dataAdapter,
			    xAxis:
				{
				    text: 'Category Axis',
				    textRotationAngle: 0,
                    valuesOnTicks: false,
                    dataField: 'OrderDate',
				    type: 'date',
				    baseUnit: 'month',
				    formatFunction: function (value) {
				        return $.jqx.dataFormat.formatdate(value, 'dd/MM/yyyy');
				    },
				    showTickMarks: true
				},
			    colorScheme: 'scheme05',
			    seriesGroups:
				[
					{
					    type: 'line',
					    columnsGapPercent: 25,
					    seriesGapPercent: 10,
					    columnsMaxWidth: 50,
					    valueAxis:
						{
						    displayValueAxis: true,
						    description: 'Quantity',
						    axisSize: 'auto',
						    tickMarksColor: '#888888',
						    unitInterval: 20,
						    minValue: 0,
						    maxValue: 100
						},
					    series: [
                            { dataField: 'Quantity', displayText: 'Quantity' }
					    ]
					}
				]
			};
			// setup the chart
			$('#jqxChart').jqxChart(settings);
		});
	</script>
</head>
<body class='default'>
      <div style="width:670px; height:400px" id="jqxChart"></div>
</body>
</html>
