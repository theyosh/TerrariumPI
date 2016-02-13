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
if (isset($_GET['CustomerID']))
	{
	// get data and store in a json array
	$query = "SELECT CustomerID, ShipCity, OrderID, OrderDate, ShipName, ShipAddress, ShipCountry FROM Orders where CustomerID=?";
	$result = $mysqli->prepare($query);
	$result->bind_param('s', $_GET['CustomerID']);
	$result->execute();
	/* bind result variables */
	$result->bind_result($CustomerID, $ShipCity, $OrderID, $OrderDate, $ShipName, $ShipAddress, $ShipCountry);
	/* fetch values */
	while ($result->fetch())
		{
		$orders[] = array(
			'CustomerID' => $CustomerID,
			'ShipCity' => $ShipCity,
			'OrderID' => $OrderID,
			'OrderDate' => $OrderDate,
			'ShipName' => $ShipName,
			'ShipAddress' => $ShipAddress,
			'ShipCountry' => $ShipCountry
		);
		}
	echo json_encode($orders);
	/* close statement */
	$result->close();
	return;
	}
// get data and store in a json array
$query = "SELECT CustomerID, CompanyName  FROM Customers";
$result = $mysqli->prepare($query);
$result->execute();
/* bind result variables */
$result->bind_result($CustomerID, $CompanyName);
/* fetch values */
while ($result->fetch())
	{
	$customers[] = array(
		'CustomerID' => $CustomerID,
		'CompanyName' => $CompanyName
	);
	}
echo json_encode($customers);
$result->close();
/* close connection */
$mysqli->close();
?>