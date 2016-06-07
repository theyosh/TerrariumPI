<?php

    $moviesByGeanre = []; 

    $moviesList = array( 
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y"), "startsat" => "15:20", "rating" => 5),
            array ( "movie" => 'End Game', "geanre" => 'Action', "cinema" => 'Cine Grand', "price" => 12, "promo" => false, "projectiondate" => date("m/d/Y"), "startsat" => "10:30", "rating" => 3),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Arena', "price" => 8, "promo" => true, "projectiondate" => date("m/d/Y"), "startsat" => "18:10", "rating" => 4),
            array ( "movie" => 'Unknown', "geanre" => 'Action', "cinema" => 'Arena', "price" => 7, "promo" => true, "projectiondate" => date("m/d/Y"), "startsat" => "22:30", "rating" => 2),
            array ( "movie" => 'Unstoppable', "geanre" => 'Action', "cinema" => 'Cineplex', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y"), "startsat" => "12:20", "rating" => 6),
            array ( "movie" => 'Twilight', "geanre" => 'Drama', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y"), "startsat" => "13:20", "rating" => 1),
            array ( "movie" => 'Kung Fu Panda', "geanre" => 'Animation', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y"), "startsat" => "15:45", "rating" => 6),
            array ( "movie" => 'Knockout', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y"), "startsat" => "10:20", "rating" => 3),
            array ( "movie" => 'Kung Fu Panda', "geanre" => 'Animation', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y"), "startsat" => "18:20", "rating" => 4),
            array ( "movie" => 'Big Daddy', "geanre" => 'Comedy', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y"), "startsat" => "05:20", "rating" => 5),
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "15:20", "rating" => 5),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Cine Grand', "price" => 12, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "10:30", "rating" => 3),
            array ( "movie" => 'Big Daddy', "geanre" => 'Comedy', "cinema" => 'Arena', "price" => 8, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "18:10", "rating" => 4),
            array ( "movie" => 'Unknown', "geanre" => 'Action', "cinema" => 'Arena', "price" => 7, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "22:30", "rating" => 2),
            array ( "movie" => 'Unstoppable', "geanre" => 'Action', "cinema" => 'Cineplex', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "12:20", "rating" => 6),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "13:20", "rating" => 1),
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "15:45", "rating" => 6),
            array ( "movie" => 'Twilight', "geanre" => 'Drama', "cinema" => 'Arena', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "10:20", "rating" => 3),
            array ( "movie" => 'End Game', "geanre" => 'Action', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "18:20", "rating" => 4),
            array ( "movie" => 'Kung Fu Panda', "geanre" => 'Animation', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+1, date("Y"))), "startsat" => "05:20", "rating" => 5),
            array ( "movie" => 'Unstoppable', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "15:20", "rating" => 5),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Cine Grand', "price" => 12, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "10:30", "rating" => 3),
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Arena', "price" => 8, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "18:10", "rating" => 4),
            array ( "movie" => 'Big Daddy', "geanre" => 'Comedy', "cinema" => 'Arena', "price" => 7, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "22:30", "rating" => 2),
            array ( "movie" => 'Knockout', "geanre" => 'Action', "cinema" => 'Cineplex', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "12:20", "rating" => 6),
            array ( "movie" => 'Unknown', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "13:20", "rating" => 1),
            array ( "movie" => 'Kung Fu Panda', "geanre" => 'Animation', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "15:45", "rating" => 6),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Arena', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "10:20", "rating" => 3),
            array ( "movie" => 'Kung Fu Panda', "geanre" => 'Animation', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "18:20", "rating" => 4),
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+2, date("Y"))), "startsat" => "05:20", "rating" => 5),
            array ( "movie" => 'Unknown', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "15:20", "rating" => 5),
            array ( "movie" => 'Twilight', "geanre" => 'Drama', "cinema" => 'Cine Grand', "price" => 12, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "10:30", "rating" => 3),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Arena', "price" => 8, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "18:10", "rating" => 4),
            array ( "movie" => 'Avatar', "geanre" => 'Fantasy', "cinema" => 'Arena', "price" => 7, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "22:30", "rating" => 2),
            array ( "movie" => 'Knockout', "geanre" => 'Action', "cinema" => 'Cineplex', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "12:20", "rating" => 6),
            array ( "movie" => 'Unstoppable', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "13:20", "rating" => 1),
            array ( "movie" => 'End Game', "geanre" => 'Action', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "15:45", "rating" => 6),
            array ( "movie" => 'Priest', "geanre" => 'Horror', "cinema" => 'Arena', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "10:20", "rating" => 3),
            array ( "movie" => 'End Game', "geanre" => 'Action', "cinema" => 'Cine Grand', "price" => 10, "promo" => false, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "18:20", "rating" => 4),
            array ( "movie" => 'Unknown', "geanre" => 'Action', "cinema" => 'Arena', "price" => 10, "promo" => true, "projectiondate" => date("m/d/Y", mktime(0, 0, 0, date("m")  , date("d")+3, date("Y"))), "startsat" => "05:20", "rating" => 5)
         );

    $reservedSeats=array(
        array("row"=>1, "seat"=>1),
        array("row"=>1, "seat"=>6),
        array("row"=>1, "seat"=>7),
        array("row"=>1, "seat"=>8),
        array("row"=>1, "seat"=>21),
        array("row"=>2, "seat"=>11),
        array("row"=>2, "seat"=>12),
        array("row"=>2, "seat"=>2),
        array("row"=>2, "seat"=>3),
        array("row"=>2, "seat"=>18),
        array("row"=>3, "seat"=>3),
        array("row"=>3, "seat"=>12),
        array("row"=>3, "seat"=>13),
        array("row"=>3, "seat"=>14),
        array("row"=>3, "seat"=>15),
        array("row"=>4, "seat"=>1),
        array("row"=>4, "seat"=>2),
        array("row"=>4, "seat"=>8),
        array("row"=>4, "seat"=>9),
        array("row"=>4, "seat"=>10),
        array("row"=>5, "seat"=>15),
        array("row"=>5, "seat"=>16),
        array("row"=>5, "seat"=>17),
        array("row"=>5, "seat"=>18),
        array("row"=>5, "seat"=>19),
        array("row"=>5, "seat"=>20),
        array("row"=>5, "seat"=>2),
        array("row"=>5, "seat"=>3),
        array("row"=>5, "seat"=>4),
        array("row"=>5, "seat"=>5),
    );

if(isset($_GET['reservation'])&&($_GET['reservation'] == "seats")){
    $response = $reservedSeats;
}elseif(isset($_GET['reservation'])&&($_GET['reservation'] == "movieslist")){
    $response = $moviesList;
}elseif(isset($_GET['moviebygeanre'])){

    $moviesCount = count($moviesList);

    for($i=0; $i<$moviesCount; $i++){
        if(($moviesList[$i]["geanre"] == $_GET['moviebygeanre'])||($_GET['moviebygeanre'] == "")){
            $item = array("geanre"=>$_GET['moviebygeanre'], "movie"=>$moviesList[$i]["movie"]);
            array_push($moviesByGeanre, $item);
        }
    }

    $response = $moviesByGeanre;
}

    echo json_encode($response);
?>