<?php
// Include the connect.php file
include ('connect.php');

// Connect to the database
// connection String
$mysqli = new mysqli($hostname, $username, $password, $database);
/* check connection */
if (mysqli_connect_errno())
	{
	printf("Connect failed: %s\n", mysqli_connect_error());
	exit();
	}
// get first visible row.
$firstvisiblerow = $_GET['recordstartindex'];
// get the last visible row.
$lastvisiblerow = $_GET['recordendindex'];
$rowscount = 18;
// build query.
$query = "SELECT SQL_CALC_FOUND_ROWS OrderID, OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM orders  LIMIT ?,?";
$result = $mysqli->prepare($query);
$result->bind_param('ii', $firstvisiblerow, $rowscount);
$result->execute();
// get data and store in a json array
/* bind result variables */
$result->bind_result($OrderID, $OrderDate, $ShippedDate, $ShipName, $ShipAddress, $ShipCity, $ShipCountry);
/* fetch values */
while ($result->fetch())
	{
	$orders[] = array(
		'OrderID' => $OrderID,
		'OrderDate' => $OrderDate,
		'ShippedDate' => $ShippedDate,
		'ShipName' => $ShipName,
		'ShipAddress' => $ShipAddress,
		'ShipCity' => $ShipCity,
		'ShipCountry' => $ShipCountry
	);
	}
$result = $mysqli->prepare("SELECT FOUND_ROWS()");
$result->execute();
$result->bind_result($total_rows);
$result->fetch();
$data[] = array(
	'TotalRows' => $total_rows,
	'Rows' => $orders
);
echo json_encode($data);
/* close statement */
$result->close();
/* close connection */
$mysqli->close();
?>