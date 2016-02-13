<?php
  #Include the connect.php file
  include('connect.php');
  #Connect to the database
  //connection String

$mysqli = new mysqli($hostname, $username, $password, $database);
	/* check connection */
	if (mysqli_connect_errno()) {
		printf("Connect failed: %s\n", mysqli_connect_error());
		exit();
	}

  // get data and store in a json array
    $query = "SELECT EmployeeID, FirstName, LastName FROM Employees";
	$result = $mysqli->prepare($query);
	$result->execute();
	
	/* bind result variables */
	$result->bind_result($EmployeeID, $FirstName, $LastName);
	/* fetch values */
	while ($result -> fetch()) {
	  $employees[] = array(
          'EmployeeID' => $EmployeeID,
          'FirstName' => $FirstName,
	      'LastName' => $LastName,
	      'Name' => $FirstName . " " . $LastName
      );
}	

echo json_encode($employees);

	/* close statement */
$result->close();
	/* close connection */
$mysqli->close();
?>