<?php
// Include the connect.php file
include ('connect.php');

// Connect to the database
$mysqli = new mysqli($hostname, $username, $password, $database);
/* check connection */
if (mysqli_connect_errno())
	{
	printf("Connect failed: %s\n", mysqli_connect_error());
	exit();
	}
// get data and store in a json array
$query = "SELECT OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM orders";
if (isset($_GET['sortdatafield']))
	{
	$sortfields = array(
		"OrderDate",
		"ShippedDate",
		"ShipName",
		"ShipAddress",
		"ShipCity",
		"ShipCountry"
	);
	$sortfield = $_GET['sortdatafield'];
	$sortorder = $_GET['sortorder'];
	if (($sortfield != NULL) && (in_array($sortfield, $sortfields)))
		{
		if ($sortorder == "desc")
			{
			$query = "SELECT OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM orders ORDER BY " . $sortfield . " DESC";
			}
		  else if ($sortorder == "asc")
			{
			$query = "SELECT OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM orders ORDER BY " . $sortfield . " ASC";
			}
		}
	}
$result = $mysqli->prepare($query);
$result->execute();
/* bind result variables */
$result->bind_result($OrderDate, $ShippedDate, $ShipName, $ShipAddress, $ShipCity, $ShipCountry);
/* fetch values */
while ($result->fetch())
	{
	$orders[] = array(
		'OrderDate' => $OrderDate,
		'ShippedDate' => $ShippedDate,
		'ShipName' => $ShipName,
		'ShipAddress' => $ShipAddress,
		'ShipCity' => $ShipCity,
		'ShipCountry' => $ShipCountry
	);
	}
echo json_encode($orders);
/* close statement */
$result->close();
/* close connection */
$mysqli->close();
?>