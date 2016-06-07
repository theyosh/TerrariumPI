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

$earningsPieChartValues = array( 
            array ( "year" => 2014, "earnings" => 220000 ),
            array ( "year" => 2015, "earnings" => 250000 ),
            array ( "year" => 2016, "earnings" => 100000 )
         );

$targetBarGaugeValues = array( 
            array ( "value" => 20, "description" => "Target for the year"),
            array ( "value" => 50, "description" => "Target for the month"),
            array ( "value" => 90, "description" => "Target for the week" )
         );

$revenuesChartValues = array( 
            array ( "Month" => 'January', "2014" => 2000, "2015" => 1800, "2016" => 1500 ),
            array ( "Month" => 'February', "2014" => 1950, "2015" => 1600, "2016" => 1800 ),
            array ( "Month" => 'March', "2014" => 2100, "2015" => 2200, "2016" => 1700 ),
            array ( "Month" => 'April', "2014" => 2000, "2015" => 1800, "2016" => 2100 ),
            array ( "Month" => 'May', "2014" => 2100, "2015" => 1600, "2016" => 2200 ),
            array ( "Month" => 'June', "2014" => 1560, "2015" => 2100, "2016" => 0 ),
            array ( "Month" => 'July', "2014" => 2000, "2015" => 2200, "2016" => 0 ),
            array ( "Month" => 'August', "2014" => 1560, "2015" => 2100, "2016" => 0 ),
            array ( "Month" => 'September', "2014" => 1560, "2015" => 2100, "2016" => 0 ),
            array ( "Month" => 'October', "2014" => 2000, "2015" => 2200, "2016" => 0 ),
            array ( "Month" => 'November', "2014" => 1560, "2015" => 2100, "2016" => 0 ),
            array ( "Month" => 'December', "2014" => 1560, "2015" => 2100, "2016" => 0 )
         );
$popularProductsChartValues = array( 
            array ( "Product" => 'Chocolade', "Sales" => 1600, "av" => 1800),
            array ( "Product" => 'Tarte au sucre', "Sales" => 1600, "av" => 1800 ),
            array ( "Product" => 'Longlife Tofu', "Sales" => 2200, "av" => 1800 ),
            array ( "Product" => 'Mozzarella di Giovanni', "Sales" => 1800, "av" => 1800),
            array ( "Product" => 'Vegie-spread', "Sales" => 1600, "av" => 1800 ),
            array ( "Product" => 'Manjimup Dried Apples', "Sales" => 2100, "av" => 1800 ),
            array ( "Product" => 'Maxilaku', "Sales" => 2200, "av" => 1800 ),
            array ( "Product" => 'Chai', "Sales" => 2100, "av" => 1800 )
         );
$tasksKanbanValues = array( 
            array ( "id" => "1161", "state" => "new", "label" => "Combine Orders", "tags" => "orders, combine", "hex" => "#5dc3f0", "resourceId" => 3),
            array ( "id" => "1645", "state" => "work", "label" => "Change Billing Address", "tags" => "change, adress", "hex" => "#f19b60", "resourceId" => 1),
            array ( "id" => "9213", "state" => "new", "label" => "One item added to the cart", "tags" => "items, cart", "hex" => "#5dc3f0", "resourceId" => 3),
            array ( "id" => "6546", "state" => "done", "label" => "Edit Item Price", "tags" => "price, edit", "hex" => "#5dc3f0", "resourceId" => 4),
            array ( "id" => "9034", "state" => "new", "label" => "Combine Orders", "tags" => "orders, combine", "hex" => "#6bbd49", "resourceId" => 3),
         );

switch ($_GET['usedwidget']) {
    case 'piechart':
        $response = $earningsPieChartValues;
        break;
    case 'targetbargauge':
        $response = $targetBarGaugeValues;
        break;
    case 'revenueschart':
        $response = $revenuesChartValues;
        break;
    case 'popularproductschart':
        $response = $popularProductsChartValues;
        break;
    case 'ordersgrid':
        $query = "SELECT OrderID, CustomerID, OrderDate, ShipAddress, ShipCity, ShipCountry FROM Orders";
        // SELECT COMMAND
        $result = $mysqli->prepare($query);
        $result->execute();
        /* bind result variables */
        $result->bind_result($OrderID, $CustomerID, $OrderDate, $ShipAddress, $ShipCity, $ShipCountry);
        /* fetch values */
        while ($result->fetch())
            {
                $response[] = array(
                    'orderID' => $OrderID,
                    'orderDate' => $OrderDate,
                    'customer' => $CustomerID,
                    'address' => $ShipAddress,
                    'city' => $ShipCity,
                    'country' => $ShipCountry
                );
            }
        break;
    case 'productsgrid':
        $query = "SELECT ProductID, ProductName, UnitPrice, UnitsInStock FROM Products";
        // SELECT COMMAND
        $result = $mysqli->prepare($query);
        $result->execute();
        /* bind result variables */
        $result->bind_result($productID, $ProductName, $UnitPrice, $UnitsInStock );
        /* fetch values */
        while ($result->fetch())
            {
                $response[] = array(
                    'productID' => $productID,
                    'name' => $ProductName,
                    'price' => $UnitPrice,
                    'unitsInStock' => $UnitsInStock
                );
            }
        break;
    case 'customersgrid':
        $query = "SELECT CustomerID, ContactName, ContactTitle, Address, Phone FROM Customers";
        // SELECT COMMAND
        $result = $mysqli->prepare($query);
        $result->execute();
        /* bind result variables */
        $result->bind_result($customerID, $ContactName, $ContactTitle, $Address, $Phone);
        /* fetch values */
        while ($result->fetch())
            {
                $response[] = array(
                    'customerID' => $customerID,
                    'name' => $ContactName,
                    'title' => $ContactTitle,
                    'address' => $Address,
                    'phone' => $Phone
                );
            }
        break;
        case 'staffgrid':
        $query = "SELECT EmployeeID, LastName, FirstName, Title, HomePhone, Photo FROM Employees";
        // SELECT COMMAND
        $result = $mysqli->prepare($query);
        $result->execute();
        /* bind result variables */
        $result->bind_result($employeeID, $LastName, $FirstName, $Title, $HomePhone, $Photo);
        /* fetch values */
        while ($result->fetch())
            {
                $response[] = array(
                    'employeeID' => $employeeID,
                    'name' => $FirstName." ".$LastName,
                    'title' => $Title,
                    'photo' => "http://www.jqwidgets.com/jquery-widgets-demo/images/".strtolower($FirstName).".png",
                    'phone' => $HomePhone
                );
            }
        break;
    case 'taskskanban':
        $response = $tasksKanbanValues;
        break;
    default:
       trigger_error("Missing/Invalid category", E_USER_ERROR);
}

echo json_encode($response);
?>