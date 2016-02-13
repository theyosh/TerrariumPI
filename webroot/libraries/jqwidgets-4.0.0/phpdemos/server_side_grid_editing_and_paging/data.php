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
// $query = "SELECT EmployeeID, FirstName, LastName, Title, Address, City, Country, Notes FROM employees";
if (isset($_GET['update']))
	{
	// UPDATE COMMAND
	$query = "UPDATE `employees` SET `FirstName`=?, `LastName`=?, `Title`=?, `Address`=?, `City`=?, `Country`=?, `Notes`=? WHERE `EmployeeID`=?";
	$result = $mysqli->prepare($query);
	$result->bind_param('sssssssi', $_GET['FirstName'], $_GET['LastName'], $_GET['Title'], $_GET['Address'], $_GET['City'], $_GET['Country'], $_GET['Notes'], $_GET['EmployeeID']);
	$res = $result->execute() or trigger_error($result->error, E_USER_ERROR);
	// printf ("Updated Record has id %d.\n", $_GET['EmployeeID']);
	echo $res;
	}
  else
	{
	// get data and store in a json array
	$pagenum = $_GET['pagenum'];
	$pagesize = $_GET['pagesize'];
	$start = $pagenum * $pagesize;
	$query = "SELECT SQL_CALC_FOUND_ROWS EmployeeID, FirstName, LastName, Title, Address, City, Country, Notes FROM employees LIMIT ?,?";
	$result = $mysqli->prepare($query);
	$result->bind_param('ii', $start, $pagesize);
	$result->execute();
	/* bind result variables */
	$result->bind_result($EmployeeID, $FirstName, $LastName, $Title, $Address, $City, $Country, $Notes);
	/* fetch values */
	while ($result->fetch())
		{
		$employees[] = array(
			'EmployeeID' => $EmployeeID,
			'FirstName' => $FirstName,
			'LastName' => $LastName,
			'Title' => $Title,
			'Address' => $Address,
			'City' => $City,
			'Country' => $Country,
			'Notes' => $Notes
		);
		}
	$result = $mysqli->prepare("SELECT FOUND_ROWS()");
	$result->execute();
	$result->bind_result($total_rows);
	$result->fetch();
	$data[] = array(
		'TotalRows' => $total_rows,
		'Rows' => $employees
	);
	echo json_encode($data);
	$result->close();
	}
/* close statement */
$mysqli->close();
/* close connection */
?>