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
$query = "SELECT EmployeeID, FirstName, LastName, Title FROM employees";
if (isset($_POST['update']))
	{
	// UPDATE COMMAND

	$query = "UPDATE employees SET FirstName=?, LastName=?, Title=? WHERE EmployeeID=?";
	$result = $mysqli->prepare($query);
	$result->bind_param('sssi', $_POST['FirstName'], $_POST['LastName'], $_POST['Title'], $_POST['EmployeeID']);
	$res = $result->execute() or trigger_error($result->error, E_USER_ERROR);

	echo $res;
	
	//echo $result;
	}
  else
	{
	// SELECT COMMAND
	$result = $mysqli->prepare($query);
	$result->execute();
	/* bind result variables */
	$result->bind_result($EmployeeID, $FirstName, $LastName, $Title);
	/* fetch values */
	while ($result->fetch())
		{
		$employees[] = array(
			'EmployeeID' => $EmployeeID,
			'FirstName' => $FirstName,
			'LastName' => $LastName,
			'Title' => $Title
		);
		}
	echo json_encode($employees);

	}
	
$result->close();
$mysqli->close();
/* close connection */
?>