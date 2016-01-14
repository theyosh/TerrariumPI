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
$pagenum = $_GET['pagenum'];
$pagesize = $_GET['pagesize'];
$start = $pagenum * $pagesize;
$query = "SELECT SQL_CALC_FOUND_ROWS CompanyName, ContactName, ContactTitle, Address, City, Country FROM customers LIMIT ?,?";
$result = $mysqli->prepare($query);
$result->bind_param('ii', $start, $pagesize);
$result->execute();
/* bind result variables */
$result->bind_result($CompanyName, $ContactName, $ContactTitle, $Address, $City, $Country);
/* fetch values */
while ($result->fetch())
	{
	$customers[] = array(
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
/* close statement */
$result->close();
/* close connection */
$mysqli->close();
?>