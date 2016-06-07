<?php

    $response = []; 

    $chartDataClicks = array( 
            array ( "day" => 'Monday', "spline1" => '10', "spline2" => '30'),
            array ( "day" => 'Tuesday', "spline1" => '15', "spline2" => '25'),
            array ( "day" => 'Wednesday', "spline1" => '10', "spline2" => '30'),
            array ( "day" => 'Thursday', "spline1" => '20', "spline2" => '40'),
            array ( "day" => 'Friday', "spline1" => '20', "spline2" => '45'),
            array ( "day" => 'Saturday', "spline1" => '20', "spline2" => '30'),
            array ( "day" => 'Sunday', "spline1" => '30', "spline2" => '30'),

    );

    $chartDataWon = array( 
            array ( "day" => 'Monday', "spline1" => '15', "spline2" => '34'),
            array ( "day" => 'Tuesday', "spline1" => '10', "spline2" => '15'),
            array ( "day" => 'Wednesday', "spline1" => '10', "spline2" => '20'),
            array ( "day" => 'Thursday', "spline1" => '20', "spline2" => '30'),
            array ( "day" => 'Friday', "spline1" => '10', "spline2" => '15'),
            array ( "day" => 'Saturday', "spline1" => '20', "spline2" => '30'),
            array ( "day" => 'Sunday', "spline1" => '10', "spline2" => '20'),
    );

    $chartDataSales = array( 
            array ( "day" => 'Monday', "spline1" => '15', "spline2" => '30'),
            array ( "day" => 'Tuesday', "spline1" => '25', "spline2" => '25'),
            array ( "day" => 'Wednesday', "spline1" => '20', "spline2" => '30'),
            array ( "day" => 'Thursday', "spline1" => '30', "spline2" => '40'),
            array ( "day" => 'Friday', "spline1" => '40', "spline2" => '45'),
            array ( "day" => 'Saturday', "spline1" => '25', "spline2" => '30'),
            array ( "day" => 'Sunday', "spline1" => '10', "spline2" => '20'),
    );

    $chartDataGoals = array( 
            array ( "day" => 'Monday', "spline1" => '5', "spline2" => '10'),
            array ( "day" => 'Tuesday', "spline1" => '15', "spline2" => '20'),
            array ( "day" => 'Wednesday', "spline1" => '15', "spline2" => '20'),
            array ( "day" => 'Thursday', "spline1" => '10', "spline2" => '20'),
            array ( "day" => 'Friday', "spline1" => '20', "spline2" => '30'),
            array ( "day" => 'Saturday', "spline1" => '20', "spline2" => '20'),
            array ( "day" => 'Sunday', "spline1" => '15', "spline2" => '20'),
    );

    $chartPerformanceAAPL = array( 
      array ( "day" => 'Monday', "SPOpen" => '108', "SPHigh" => '109', "SPLow" => '107', "SPClose" => '107'),
            array ( "day" => 'Tuesday', "SPOpen" => '112', "SPHigh" => '113', "SPLow" => '111', "SPClose" => '109'),
            array ( "day" => 'Wednesday', "SPOpen" => '111', "SPHigh" => '114', "SPLow" => '109', "SPClose" => '112'),
            array ( "day" => 'Thursday', "SPOpen" => '110', "SPHigh" => '111', "SPLow" => '109', "SPClose" => '112'),
            array ( "day" => 'Friday', "SPOpen" => '109', "SPHigh" => '112', "SPLow" => '108', "SPClose" => '110'),
            array ( "day" => 'Saturday', "SPOpen" => '110', "SPHigh" => '111', "SPLow" => '109', "SPClose" => '109'),
            array ( "day" => 'Sunday', "SPOpen" => '111', "SPHigh" => '113', "SPLow" => '110', "SPClose" => '110')
    );

    $chartPerformanceGOOGL = array( 
            array ( "day" => 'Monday', "SPOpen" => '760', "SPHigh" => '768', "SPLow" => '757', "SPClose" => '766'),
            array ( "day" => 'Tuesday', "SPOpen" => '753', "SPHigh" => '761', "SPLow" => '752', "SPClose" => '759'),
            array ( "day" => 'Wednesday', "SPOpen" => '754', "SPHigh" => '757', "SPLow" => '752', "SPClose" => '753'),
            array ( "day" => 'Thursday', "SPOpen" => '749', "SPHigh" => '754', "SPLow" => '744', "SPClose" => '751'),
            array ( "day" => 'Friday', "SPOpen" => '738', "SPHigh" => '742', "SPLow" => '731', "SPClose" => '743'),
            array ( "day" => 'Saturday', "SPOpen" => '740', "SPHigh" => '750', "SPLow" => '730', "SPClose" => '737'),
            array ( "day" => 'Sunday', "SPOpen" => '742', "SPHigh" => '748', "SPLow" => '740', "SPClose" => '741')
    );

    $profitLoss = array(  	    
            array ( "region" => 'Asia', "account" => 'Total Revenue', "q1" => '8714.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'Asia', "account" => 'Cost Of Revenue', "q1" => '8314.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'Asia', "account" => 'Gross Profit', "q1" => '8754.96', "q2" => '4932.96', "q3" => '4238.96', "q4" => '4248.96'),
            array ( "region" => 'Asia', "account" => 'Research Development', "q1" => '8414.96', "q2" => '4942.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'Asia', "account" => 'Administrative', "q1" => '8716.96', "q2" => '4942.96', "q3" => '4243.96', "q4" => '4258.96'),        
            array ( "region" => 'Europe', "account" => 'Total Revenue', "q1" => '8414.96', "q2" => '4212.96', "q3" => '4233.96', "q4" => '4348.96'),
            array ( "region" => 'Europe', "account" => 'Cost Of Revenue', "q1" => '8614.96', "q2" => '4916.96', "q3" => '4248.96', "q4" => '4258.96'),
            array ( "region" => 'Europe', "account" => 'Gross Profit', "q1" => '8717.96', "q2" => '4412.96', "q3" => '4258.95', "q4" => '4245.96'),
            array ( "region" => 'Europe', "account" => 'Research Development', "q1" => '8814.96', "q2" => '4612.96', "q3" => '4247.96', "q4" => '4246.96'),
            array ( "region" => 'Europe', "account" => 'Administrative', "q1" => '8718.96', "q2" => '4712.96', "q3" => '4278.96', "q4" => '4548.96'),
            array ( "region" => 'Australia', "account" => 'Total Revenue', "q1" => '8714.96', "q2" => '4952.96', "q3" => '4248.96', "q4" => '4548.96'),
            array ( "region" => 'Australia', "account" => 'Cost Of Revenue', "q1" => '8714.96', "q2" => '4952.96', "q3" => '5248.96', "q4" => '4245.96'),
            array ( "region" => 'Australia', "account" => 'Gross Profit', "q1" => '8764.96', "q2" => '4922.96', "q3" => '4258.96', "q4" => '4238.96'),
            array ( "region" => 'Australia', "account" => 'Research Development', "q1" => '8734.96', "q2" => '4932.96', "q3" => '4248.96', "q4" => '4228.96'),
            array ( "region" => 'Australia', "account" => 'Administrative', "q1" => '8715.96', "q2" => '4913.96', "q3" => '4238.96', "q4" => '4228.96'),
            array ( "region" => 'North America', "account" => 'Total Revenue', "q1" => '8714.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'North America', "account" => 'Cost Of Revenue', "q1" => '8314.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'North America', "account" => 'Gross Profit', "q1" => '8754.96', "q2" => '4932.96', "q3" => '4238.96', "q4" => '4248.96'),
            array ( "region" => 'North America', "account" => 'Research Development', "q1" => '8414.96', "q2" => '4942.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'North America', "account" => 'Administrative', "q1" => '8716.96', "q2" => '4942.96', "q3" => '4243.96', "q4" => '4258.96'),
	    array ( "region" => 'South America', "account" => 'Total Revenue', "q1" => '8714.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'South America', "account" => 'Cost Of Revenue', "q1" => '8314.96', "q2" => '4912.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'South America', "account" => 'Gross Profit', "q1" => '8754.96', "q2" => '4932.96', "q3" => '4238.96', "q4" => '4248.96'),
            array ( "region" => 'South America', "account" => 'Research Development', "q1" => '8414.96', "q2" => '4942.96', "q3" => '4248.96', "q4" => '4248.96'),
            array ( "region" => 'South America', "account" => 'Administrative', "q1" => '8716.96', "q2" => '4942.96', "q3" => '4243.96', "q4" => '4258.96'),
    );

    $posts = array( 
            array ( "post" => 'forum', "by" => 'Michael Douglas', "image" => 'images/person1.png',"when" => '02:00 PM', "title" => 'Duis aliquam elit id semper maximus.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),
            array ( "post" => 'news', "by" => 'Berta Simpson', "image" => 'images/person2.png',"when" => '03:00 PM', "title" => 'Pellentesque tristique dui in fermentum.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),
            array ( "post" => 'forum', "by" => 'Tina Rodriges', "image" => 'images/person3.png',"when" => '05:00 PM', "title" => 'Vestibulum rutrum semper sapien.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),
            array ( "post" => 'news', "by" => 'Michael Douglas', "image" => 'images/person1.png',"when" => '07:00 PM', "title" => 'Proin purus sapien, consequat eget diam sed.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),
            array ( "post" => 'forum', "by" => 'Berta Simpson', "image" => 'images/person2.png',"when" => '09:00 PM', "title" => 'Vivamus et urna non metus sodales consectetur.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),
            array ( "post" => 'news', "by" => 'Tina Rodriges', "image" => 'images/person3.png',"when" => '10:00 PM', "title" => 'Curabitur lectus sapien, ornare sed leo eget.', "text" => "Just the good ol' boys, never meanin' no harm. Beats all you've ever saw, been in trouble with the law since the day they was born. Straight'nin' the curve, flat'nin' the hills. Someday the mountain might get 'em, but the law never will. Makin' their way, the only way they know how, that's just a little bit more than the law will allow. Just good ol' boys, wouldn't change if they could, fightin' the system like a true modern day Robin Hood."),

    );


    if(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartdataclicks")){
        $response = $chartDataClicks;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartdatawon")){
        $response = $chartDataWon;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartdatasales")){
        $response = $chartDataSales;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartdatagoals")){
        $response = $chartDataGoals;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartperformance1")){
        $response = $chartPerformanceAAPL;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "chartperformance2")){
        $response = $chartPerformanceGOOGL;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "profitloss")){
        $response = $profitLoss;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "posts")){
        $response = $posts;
    }

    echo json_encode($response);
?>
