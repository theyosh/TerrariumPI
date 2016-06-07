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
// get data and store in a json array
$query = "SELECT EmployeeID, OrderDate, ShipCity, ShipAddress, ShipCountry  FROM Orders where EmployeeID=?";
$result = $mysqli->prepare($query);
$result->bind_param('i', $_POST["EmployeeID"]);
$result->execute();
/* bind result variables */
$result->bind_result($EmployeeID, $OrderDate, $ShipCity, $ShipAddress, $ShipCountry);
/* fetch values */
while ($result->fetch())
	{
	$orders[] = array(
		'EmployeeID' => $EmployeeID,
		'OrderDate' => $OrderDate,
		'ShipCity' => $ShipCity,
		'ShipAddress' => $ShipAddress,
		'ShipCountry' => $ShipCountry
	);
	}
echo json_encode($orders);
/* close statement */
$result->close();
/* close connection */
$mysqli->close();
?>