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
$from = 0;
$to = 100;
$query = "SELECT OrderDate, ProductName, Quantity FROM  Invoices ORDER BY OrderDate LIMIT ?,?";
$result = $mysqli->prepare($query);
$result->bind_param('ii', $from, $to);
$result->execute();
/* bind result variables */
$result->bind_result($OrderDate, $ProductName, $Quantity);
/* fetch values */
while ($result->fetch())
	{
	$orders[] = array(
		'OrderDate' => $OrderDate,
		'ProductName' => $ProductName,
		'Quantity' => $Quantity
	);
	}
echo json_encode($orders);
/* close statement */
$result->close();
/* close connection */
$mysqli->close();
?>