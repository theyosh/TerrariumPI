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

    if(!isset($_GET['employeeid'])){
        trigger_error("Missing/Invalid employeeId", E_USER_ERROR);
    }elseif(!isset($_GET['month'])){
        trigger_error("Missing/Invalid month", E_USER_ERROR);
    }elseif(!isset($_GET['usedwidget'])){
        trigger_error("Missing/Invalid widget", E_USER_ERROR);
    }

    switch ($_GET['usedwidget']) {
        case 'employeedropdown':

        $query = "SELECT EmployeeID, FirstName, LastName, Photo from Employees where EmployeeID<9";
        $result = $mysqli->prepare($query);
        $result->execute();
        $result->bind_result($employeeId, $FirstName, $LastName, $Photo);
        while ($result->fetch())
            {
                $response[] = array(
                    'employeeId' => $employeeId,
                    'employeeName' => $FirstName." ".$LastName,
                    'employeePhoto' => strtolower($FirstName).".png",
                );
            }

            break;
        case 'userinfo':

        $query = "SELECT t1.LastName, t1.FirstName, t1.HomePhone, t1.Photo, COUNT(t2.EmployeeID) as employeeOrders from Employees t1 left join Orders t2 on (t1.EmployeeID=t2.EmployeeID) where t2.EmployeeID=".$_GET['employeeid'];
        $result = $mysqli->prepare($query);
        $result->execute();
        $result->bind_result($LastName, $FirstName, $Phone, $Photo, $employeeOrders);
        while ($result->fetch())
            {
                $response[] = array(
                    'employeeName' => $FirstName." ".$LastName,
                    'employeePhone' => $Phone,
                    'employeePhoto' => strtolower($FirstName).".png",
                    'employeeOrders' => $employeeOrders
                );
            }

            break;
        case 'salesgrid':
        $quarterStart = ($_GET['month']- 1)*3+1;
        $quarterEnd = $quarterStart + 2;
        $query = "SELECT distinct date(a.ShippedDate) as ShippedDate, a.CustomerID, b.Subtotal, a.ShipAddress from Orders a inner join ( select distinct OrderID, sum(UnitPrice * Quantity * (1 - Discount)) as Subtotal from `Order Details` group by OrderID ) b on a.OrderID = b.OrderID where a.ShippedDate is not null and a.ShippedDate between date('1997-".$quarterStart."-01') and date('1997-".$quarterEnd."-30') and a.EmployeeID=".$_GET['employeeid']." order by a.ShippedDate";
            
        $result = $mysqli->prepare($query);
        $result->execute();

        $result->bind_result($ShippedDate, $CustomerID, $Subtotal, $ShipAddress);

        while ($result->fetch())
            {
                $response[] = array(
                    'ShippedDate' => $ShippedDate,
                    'ShipAddress' => $ShipAddress,
                    'Customer' => $CustomerID,
                    'Amount' => intval($Subtotal, 10)
                );
            }

            break;
        case 'yearpiechart':
        $query = "SELECT distinct t1.OrderID, t2.employeeId, t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
        $result = $mysqli->prepare($query);
        $result->execute();
        $result->bind_result($OrderID, $employeeId, $OrderDate, $Subtotal);
        while ($result->fetch())
            {
                $response[] = array(
                    'OrderID' => $OrderID,
                    'OrderEmployeeId' => $employeeId,
                    'OrderDate' => $OrderDate,
                    'Subtotal' => intval($Subtotal, 10)
                );
            }

            break;
        case 'monthpiechart':
        $query = "SELECT distinct t1.OrderID, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid']." and t2.ShippedDate between date('1997-".$_GET['month']."-01') and date('1997-".$_GET['month']."-30') GROUP BY t2.OrderID";
        $result = $mysqli->prepare($query);
        $result->execute();
        $result->bind_result($OrderID, $Subtotal);
        while ($result->fetch())
            {
                $response[] = array(
                    'OrderID' => $OrderID,
                    'OrderTotal' => intval($Subtotal, 10)
                );
            }

            break;
        default:
           trigger_error("Missing/Invalid category", E_USER_ERROR);
    }

    echo json_encode($response);

?>