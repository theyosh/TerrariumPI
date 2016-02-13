
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
$query = "SELECT OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM Orders";
$result = $mysqli->prepare($query);
// filter data.
if (isset($_GET['filterscount']))
	{
	$filterscount = $_GET['filterscount'];
	if ($filterscount > 0)
		{
		$where = " WHERE (";
		$tmpdatafield = "";
		$tmpfilteroperator = "";
		$valuesPrep = "";
		$values = [];
		for ($i = 0; $i < $filterscount; $i++)
			{
			// get the filter's value.
			$filtervalue = $_GET["filtervalue" . $i];
			// get the filter's condition.
			$filtercondition = $_GET["filtercondition" . $i];
			// get the filter's column.
			$filterdatafield = $_GET["filterdatafield" . $i];
			// get the filter's operator.
			$filteroperator = $_GET["filteroperator" . $i];
			if ($tmpdatafield == "")
				{
				$tmpdatafield = $filterdatafield;
				}
			  else if ($tmpdatafield <> $filterdatafield)
				{
				$where.= ")AND(";
				}
			  else if ($tmpdatafield == $filterdatafield)
				{
				if ($tmpfilteroperator == 0)
					{
					$where.= " AND ";
					}
				  else $where.= " OR ";
				}
			// build the "WHERE" clause depending on the filter's condition, value and datafield.
			switch ($filtercondition)
				{
			case "CONTAINS":
				$condition = " LIKE ";
				$value = "%{$filtervalue}%";
				break;

			case "DOES_NOT_CONTAIN":
				$condition = " NOT LIKE ";
				$value = "%{$filtervalue}%";
				break;

			case "EQUAL":
				$condition = " = ";
				$value = $filtervalue;
				break;

			case "NOT_EQUAL":
				$condition = " <> ";
				$value = $filtervalue;
				break;

			case "GREATER_THAN":
				$condition = " > ";
				$value = $filtervalue;
				break;

			case "LESS_THAN":
				$condition = " < ";
				$value = $filtervalue;
				break;

			case "GREATER_THAN_OR_EQUAL":
				$condition = " >= ";
				$value = $filtervalue;
				break;

			case "LESS_THAN_OR_EQUAL":
				$condition = " <= ";
				$value = $filtervalue;
				break;

			case "STARTS_WITH":
				$condition = " LIKE ";
				$value = "{$filtervalue}%";
				break;

			case "ENDS_WITH":
				$condition = " LIKE ";
				$value = "%{$filtervalue}";
				break;

			case "NULL":
				$condition = " IS NULL ";
				$value = "%{$filtervalue}%";
				break;

			case "NOT_NULL":
				$condition = " IS NOT NULL ";
				$value = "%{$filtervalue}%";
				break;
				}
			$where.= " " . $filterdatafield . $condition . "? ";
			$valuesPrep = $valuesPrep . "s";
			$values[] = & $value;
			if ($i == $filterscount - 1)
				{
				$where.= ")";
				}
			$tmpfilteroperator = $filteroperator;
			$tmpdatafield = $filterdatafield;
			}
		// build the query.
		$query = "SELECT OrderDate, ShippedDate, ShipName, ShipAddress, ShipCity, ShipCountry FROM Orders" . $where;
		$result = $mysqli->prepare($query);
		call_user_func_array(array(
			$result,
			"bind_param"
		) , array_merge(array(
			$valuesPrep
		) , $values));
		}
	}
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