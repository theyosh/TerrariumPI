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

    if(!isset($_GET['usedwidget'])){
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
        case 'salespermonthchart':

        $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
        $result = $mysqli->prepare($query);
        $result->execute();
        $result->bind_result( $OrderDate, $Subtotal);
        while ($result->fetch())
            {
                $response[] = array(
                    'OrderDate' => substr($OrderDate, 0, -11)."01 00:00:00",
                    'Subtotal' => $Subtotal
                );
            }

            break;
        case 'salespermonthgrid':

            for($i=0; $i<13; $i++){
                $month = $i<10 ? "0".$i : $i;
                $response[] = array(
                    'OrderDate' => "1997-".$month."-01 00:00:00",
                    'Subtotal1' => 0,
                    'Subtotal2' => 0);
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid1']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result($OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal1']=$Subtotal;
                    }
                }
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid2']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result( $OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal2']=$Subtotal;
                    }
                }
            }

            array_shift($response);

            break;
        case 'expensespermonthgridchart':

            for($i=0; $i<13; $i++){
                $month = $i<10 ? "0".$i : $i;
                $response[] = array(
                    'OrderDate' => "1997-".$month."-01 00:00:00",
                    'Subtotal1' => 0,
                    'Subtotal2' => 0);
            }

            $query = "SELECT distinct t2.ShippedDate, (sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount))*0.8 - 50) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid1']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result($OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal1']=$Subtotal;
                    }
                }
            }

            $query = "SELECT distinct t2.ShippedDate, (sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount))*0.8 - 50) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid2']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result( $OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal2']=$Subtotal;
                    }
                }
            }

            array_shift($response);

            break;
        case 'salarygridchart':

            for($i=0; $i<13; $i++){
                $month = $i<10 ? "0".$i : $i;
                $response[] = array(
                    'OrderDate' => "1997-".$month."-01 00:00:00",
                    'Subtotal1' => 0,
                    'Subtotal2' => 0);
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount))*0.2 as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid1']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result($OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal1']=$Subtotal;
                    }
                }
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount))*0.2 as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid2']."  and t2.ShippedDate between date('1997-01-01') and date('1997-12-31') GROUP BY YEAR(t2.ShippedDate), MONTH(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result( $OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<13; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -11)."01 00:00:00"){
                        $response[$i]['Subtotal2']=$Subtotal;
                    }
                }
            }

            array_shift($response);

            break;
        case 'yearcomparisonchart':
            for($i=0; $i<3; $i++){
                $month = $i<10 ? "0".$i : $i;
                $response[] = array(
                    'OrderDate' => (1996 + $i)."-01-01 00:00:00",
                    'Subtotal1' => 0,
                    'Subtotal2' => 0);
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid1']." GROUP BY YEAR(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result($OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<3; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -14)."01-01 00:00:00"){
                        $response[$i]['Subtotal1']=$Subtotal;
                    }
                }
            }

            $query = "SELECT distinct t2.ShippedDate, sum(t1.UnitPrice * t1.Quantity * (1 - t1.Discount)) as Subtotal from `Order Details` t1 left join Orders t2 on (t1.OrderID=t2.OrderID) where t2.EmployeeID=".$_GET['employeeid2']." GROUP BY YEAR(t2.ShippedDate) ASC";
            $result = $mysqli->prepare($query);
            $result->execute();
            $result->bind_result( $OrderDate, $Subtotal);
            while ($result->fetch())
            {
                for($i=0; $i<3; $i++){
                    if($response[$i]['OrderDate']==substr($OrderDate, 0, -14)."01-01 00:00:00"){
                        $response[$i]['Subtotal2']=$Subtotal;
                    }
                }
            }

            break;
        default:
           trigger_error("Missing/Invalid category", E_USER_ERROR);
    }

    echo json_encode($response);
?>