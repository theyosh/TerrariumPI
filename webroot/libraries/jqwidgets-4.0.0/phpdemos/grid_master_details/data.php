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
if (isset($_GET['customerid']))
	{
	// get data and store in a json array
	$pagenum = $_GET['pagenum'];
	$pagesize = $_GET['pagesize'];
	$customerid = $_GET['customerid'];
	$start = $pagenum * $pagesize;
	$query = "SELECT SQL_CALC_FOUND_ROWS OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM orders WHERE CustomerID=? LIMIT ?,?";
	$result = $mysqli->prepare($query);
	$result->bind_param('sii', $customerid, $start, $pagesize);
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
	$result = $mysqli->prepare("SELECT FOUND_ROWS()");
	$result->execute();
	$result->bind_result($total_rows);
	$result->fetch();
	$data[] = array(
		'TotalRows' => $total_rows,
		'Rows' => $orders
	);
	echo json_encode($data);
	}
  else
	{
	// get data and store in a json array
	$pagenum = $_GET['pagenum'];
	$pagesize = $_GET['pagesize'];
	$start = $pagenum * $pagesize;
	$query = "SELECT SQL_CALC_FOUND_ROWS CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Country FROM customers LIMIT ?,?";
	$result = $mysqli->prepare($query);
	$result->bind_param('ii', $start, $pagesize);
	$result->execute();
	/* bind result variables */
	$result->bind_result($CustomerID, $CompanyName, $ContactName, $ContactTitle, $Address, $City, $Country);
	/* fetch values */
	while ($result->fetch())
		{
		$customers[] = array(
			'CustomerID' => $CustomerID,
			'CompanyName' => $CompanyName,
			'ContactName' => $ContactName,
			'ContactTitle' => $ContactTitle,
			'Address' => $Address,
			'City' => $City,
			'Country' => $Country
		);
		}
	$result = $mysqli->prepare("SELECT FOUND_ROWS()");
	$result->execute();
	$result->bind_result($total_rows);
	$result->fetch();
	$data[] = array(
		'TotalRows' => $total_rows,
		'Rows' => $customers
	);
	echo json_encode($data);
	}
$result->close();
/* close connection */
$mysqli->close();
?>