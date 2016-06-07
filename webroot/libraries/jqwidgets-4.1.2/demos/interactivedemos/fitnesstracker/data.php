<?php
$response;

$progressGaugesValues = array( 
            array ( "now" => 550, "total" => 2700 ),
            array ( "now" => 650, "total" => 1000 ),
            array ( "now" => 4, "total" => 7 ),
            array ( "now" => 1, "total" => 4 )
         );
$foodDropDownValues = array( 
            array ("food" => 'Cheeseburger', "fat" => 19.7, "carb" => 31.5, "protein" => 19.4, "calories" => 380),
            array ("food" => 'Potatoes', "fat" => 19.5, "carb" => 54.8, "protein" => 4.7, "calories" => 413 ),
            array ("food" => 'Cream Soup', "fat" => 9.9, "carb" => 26, "protein" => 5.6, "calories" => 305 ),
            array ("food" => 'Soup fish', "fat" => 2.2, "carb" => 5.6, "protein" => 7.4, "calories" => 72 ),
            array ("food" => 'Cheese', "fat" => 31.9, "carb" => 7.5, "protein" => 27.7, "calories" => 428 ),
            array ("food" => 'Pepperoni Pizza', "fat" => 13.9, "carb" => 35.3, "protein" => 35.7, "calories" => 320 ),
            array ("food" => 'Taco Salad', "fat" => 48.9, "carb" => 80.5, "protein" => 35.7, "calories" => 906 ),
            array ("food" => 'Scrambled Eggs', "fat" => 15, "carb" => 1.9, "protein" => 15.4, "calories" => 196 )
         );
$foodGridValues = array( 
            array ( "time" => '8:00', "food" => 'Egg', "fat" => 2, "carb" => 5, "protein" => 10, "calories" => 38),
            array ( "time" => '9:15', "food" => 'Burger', "fat" => 15, "carb" => 25, "protein" => 12, "calories" => 58 ),
            array ( "time" => '12:30', "food" => 'Cream Soup', "fat" => 32, "carb" => 45, "protein" => 16, "calories" => 32 ),
            array ( "time" => '12:50', "food" => 'Soup Mix', "fat" => 21, "carb" => 54, "protein" => 18, "calories" => 41 ),
            array ( "time" => '16:35', "food" => 'Milk', "fat" => 15, "carb" => 25, "protein" => 12.1, "calories" => 58 ),
            array ( "time" => '17:30', "food" => 'Cocoa', "fat" => 32, "carb" => 45, "protein" => 16.4, "calories" => 32 ),
            array ( "time" => '19:10', "food" => 'Beef', "fat" => 21, "carb" => 54, "protein" => 18.6, "calories" => 41 ),
            array ( "time" => '21:45', "food" => 'Egg', "fat" => 21, "carb" => 54, "protein" => 18, "calories" => 41 )
         );
$dailyCaloriesGridValues = array( 
            array ( "date" => '10/02/2016', "intake" => 2000, "burn" => 1800, "set" => true),
            array ( "date" => '11/02/2016', "intake" => 1950, "burn" => 1600 ),
            array ( "date" => '12/02/2016', "intake" => 2100, "burn" => 2200 ),
            array ( "date" => '13/02/2016', "intake" => 2000, "burn" => 1800 ),
            array ( "date" => '14/02/2016', "intake" => 2100, "burn" => 1600 ),
            array ( "date" => '15/02/2016', "intake" => 1560, "burn" => 2100 ),
            array ( "date" => '16/02/2016', "intake" => 2000, "burn" => 2200 ),
            array ( "date" => '17/02/2016', "intake" => 1560, "burn" => 2100 )
         );
$dailyCaloriesChartValues = array( 
            array ( "date" => '01/02/2016', "intake" => 1950, "burn" => 1600 ),
            array ( "date" => '02/02/2016', "intake" => 2100, "burn" => 2200 ),
            array ( "date" => '03/02/2016', "intake" => 1950, "burn" => 1600 ),
            array ( "date" => '04/02/2016', "intake" => 2100, "burn" => 2200 ),
            array ( "date" => '05/02/2016', "intake" => 2000, "burn" => 1800 ),
            array ( "date" => '06/02/2016', "intake" => 2100, "burn" => 1600 ),
            array ( "date" => '07/02/2016', "intake" => 1560, "burn" => 2100 ),
            array ( "date" => '08/02/2016', "intake" => 2000, "burn" => 2200 ),
            array ( "date" => '09/02/2016', "intake" => 1560, "burn" => 2100 ),
            array ( "date" => '10/02/2016', "intake" => 2000, "burn" => 1800, "set" => true),
            array ( "date" => '11/02/2016', "intake" => 1950, "burn" => 1600 ),
            array ( "date" => '12/02/2016', "intake" => 2100, "burn" => 2200 ),
            array ( "date" => '13/02/2016', "intake" => 2000, "burn" => 1800 ),
            array ( "date" => '14/02/2016', "intake" => 2100, "burn" => 1600 ),
            array ( "date" => '15/02/2016', "intake" => 1560, "burn" => 2100 ),
            array ( "date" => '16/02/2016', "intake" => 2000, "burn" => 2200 ),
            array ( "date" => '17/02/2016', "intake" => 1560, "burn" => 2100 )
         );
$caloriesChartValues = array( 
            array ( "Date" => '01/02/2016', "fat" => 50, "carb" => 100, "protein" => 600 ),
            array ( "Date" => '02/02/2016', "fat" => 100, "carb" => 200, "protein" => 800 ),
            array ( "Date" => '03/02/2016', "fat" => 50, "carb" => 300, "protein" => 500 ),
            array ( "Date" => '04/02/2016', "fat" => 100, "carb" => 100, "protein" => 300 ),
            array ( "Date" => '05/02/2016', "fat" => 100, "carb" => 200, "protein" => 400 ),
            array ( "Date" => '06/02/2016', "fat" => 100, "carb" => 300, "protein" => 800 ),
            array ( "Date" => '07/02/2016', "fat" => 60, "carb" => 100, "protein" => 500 ),
            array ( "Date" => '08/02/2016', "fat" => 30, "carb" => 200, "protein" => 600 ),
            array ( "Date" => '09/02/2016', "fat" => 60, "carb" => 300, "protein" => 900 ),
            array ( "Date" => '10/02/2016', "fat" => 100, "carb" => 100, "protein" => 500 ),
            array ( "Date" => '11/02/2016', "fat" => 50, "carb" => 200, "protein" => 700 ),
            array ( "Date" => '12/02/2016', "fat" => 100, "carb" => 300, "protein" => 300 ),
            array ( "Date" => '13/02/2016', "fat" => 300, "carb" => 100, "protein" => 600 ),
            array ( "Date" => '14/02/2016', "fat" => 100, "carb" => 200, "protein" => 900 ),
            array ( "Date" => '15/02/2016', "fat" => 60, "carb" => 300, "protein" => 300 ),
            array ( "Date" => '16/02/2016', "fat" => 30, "carb" => 100, "protein" => 500 ),
            array ( "Date" => '17/02/2016', "fat" => 60, "carb" => 200, "protein" => 600 )
         );


switch ($_GET['usedwidget']) {
    case 'bargauges':
        $response = $progressGaugesValues;
        break;
    case 'fooddropdown':
        $response = $foodDropDownValues;
        break;
    case 'foodgrid':
        $response = $foodGridValues;
        break;
    case 'dailycaloriesgrid':
        $response = $dailyCaloriesGridValues;
        break;
    case 'dailycalorieschart':
        $response = $dailyCaloriesChartValues;
        break;
    case 'calorieschart':
        $response = $caloriesChartValues;
        break;
    default:
       trigger_error("Missing/Invalid category", E_USER_ERROR);
}

echo json_encode($response);
?>


