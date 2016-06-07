<?php

    $response = []; 

    $instructorsShedulerItems = array( 
            array ( "id" => 'id1', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-22 07:00", "end" => "2015-11-22 08:00"),
            array ( "id" => 'id2', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-22 10:00", "end" => "2015-11-22 11:00"),
            array ( "id" => 'id3', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-22 18:00", "end" => "2015-11-22 19:00"),
            array ( "id" => 'id4', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-22 09:00", "end" => "2015-11-22 10:00"),
            array ( "id" => 'id5', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-22 06:00", "end" => "2015-11-22 07:00"),
            array ( "id" => 'id6', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-22 15:00", "end" => "2015-11-22 16:00"),
            array ( "id" => 'id7', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-22 08:00", "end" => "2015-11-22 09:00"),
            array ( "id" => 'id8', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-23 07:00", "end" => "2015-11-23 08:00"),
            array ( "id" => 'id9', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-23 08:00", "end" => "2015-11-23 09:00"),
            array ( "id" => 'id10', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-23 16:00", "end" => "2015-11-23 17:00"),
            array ( "id" => 'id11', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-23 17:00", "end" => "2015-11-23 18:00"),
            array ( "id" => 'id12', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Janet", "start" => "2015-11-23 06:00", "end" => "2015-11-23 07:00"),
            array ( "id" => 'id13', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-23 10:00", "end" => "2015-11-23 11:00"),
            array ( "id" => 'id14', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Janet", "start" => "2015-11-23 20:00", "end" => "2015-11-23 21:00"),
            array ( "id" => 'id15', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-23 15:00", "end" => "2015-11-23 16:00"),
            array ( "id" => 'id16', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-24 08:00", "end" => "2015-11-24 09:00"),
            array ( "id" => 'id17', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-24 12:00", "end" => "2015-11-24 13:00"),
            array ( "id" => 'id18', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-24 15:00", "end" => "2015-11-24 16:00"),
            array ( "id" => 'id19', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Janet", "start" => "2015-11-24 08:00", "end" => "2015-11-24 09:00"),
            array ( "id" => 'id20', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Janet", "start" => "2015-11-24 10:00", "end" => "2015-11-24 11:00"),
            array ( "id" => 'id21', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Janet", "start" => "2015-11-24 17:00", "end" => "2015-11-24 18:00"),
            array ( "id" => 'id22', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-24 13:00", "end" => "2015-11-24 14:00"),
            array ( "id" => 'id23', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-25 08:00", "end" => "2015-11-25 09:00"),
            array ( "id" => 'id24', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-25 16:00", "end" => "2015-11-25 17:00"),
            array ( "id" => 'id25', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-25 06:00", "end" => "2015-11-25 07:00"),
            array ( "id" => 'id26', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-25 14:00", "end" => "2015-11-25 15:00"),
            array ( "id" => 'id27', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-25 21:00", "end" => "2015-11-25 22:00"),
            array ( "id" => 'id28', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-25 07:00", "end" => "2015-11-25 08:00"),
            array ( "id" => 'id29', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-25 20:00", "end" => "2015-11-25 21:00"),
            array ( "id" => 'id30', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Andrew", "start" => "2015-11-25 17:00", "end" => "2015-11-25 18:00"),
            array ( "id" => 'id31', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Nancy", "start" => "2015-11-26 08:00", "end" => "2015-11-26 09:00"),
            array ( "id" => 'id32', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Michael", "calendar" => "Nancy", "start" => "2015-11-26 15:00", "end" => "2015-11-26 16:00"),
            array ( "id" => 'id33', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-26 17:00", "end" => "2015-11-26 18:00"),
            array ( "id" => 'id34', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-26 11:00", "end" => "2015-11-26 12:00"),
            array ( "id" => 'id35', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-26 21:00", "end" => "2015-11-26 22:00"),
            array ( "id" => 'id36', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-26 19:00", "end" => "2015-11-26 20:00"),
            array ( "id" => 'id37', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Steven", "calendar" => "Nancy", "start" => "2015-11-27 08:00", "end" => "2015-11-27 09:00"),
            array ( "id" => 'id38', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Michael", "calendar" => "Nancy", "start" => "2015-11-27 15:00", "end" => "2015-11-27 16:00"),
            array ( "id" => 'id39', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Nancy", "start" => "2015-11-27 17:00", "end" => "2015-11-27 18:00"),
            array ( "id" => 'id40', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-27 11:00", "end" => "2015-11-27 12:00"),
            array ( "id" => 'id41', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-27 21:00", "end" => "2015-11-27 22:00"),
            array ( "id" => 'id42', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-27 19:00", "end" => "2015-11-27 20:00"),
            array ( "id" => 'id43', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Michael", "calendar" => "Andrew", "start" => "2015-11-27 20:00", "end" => "2015-11-27 21:00"),
            array ( "id" => 'id44', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Robert", "calendar" => "Nancy", "start" => "2015-11-28 08:00", "end" => "2015-11-28 09:00"),
            array ( "id" => 'id45', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Anne", "calendar" => "Janet", "start" => "2015-11-28 06:00", "end" => "2015-11-28 07:00"),
            array ( "id" => 'id46', "description" => 'Cardio training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-28 08:00", "end" => "2015-11-28 09:00"),
            array ( "id" => 'id47', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Janet", "start" => "2015-11-28 20:00", "end" => "2015-11-28 21:00"),
            array ( "id" => 'id48', "description" => 'Strength training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-28 06:00", "end" => "2015-11-28 07:00"),
            array ( "id" => 'id49', "description" => 'Flexibility training', "location" => 'Athletic Fitness', "subject" => "Personal training with Laura", "calendar" => "Margaret", "start" => "2015-11-28 18:00", "end" => "2015-11-28 19:00"),
    );

    $roomsShedulerItems = array( 
            array ( "id" => 'id1', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-22 06:00", "end" => "2015-11-22 22:00"),
            array ( "id" => 'id2', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-23 06:00", "end" => "2015-11-23 22:00"),
            array ( "id" => 'id3', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-24 06:00", "end" => "2015-11-24 22:00"),
            array ( "id" => 'id4', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-25 06:00", "end" => "2015-11-25 22:00"),
            array ( "id" => 'id5', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-26 06:00", "end" => "2015-11-26 22:00"),
            array ( "id" => 'id6', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-27 06:00", "end" => "2015-11-27 22:00"),
            array ( "id" => 'id7', "description" => '', "location" => 'Athletic Fitness', "subject" => "Fitness - Open", "calendar" => "Fitness", "start" => "2015-11-28 06:00", "end" => "2015-11-28 22:00"),
            array ( "id" => 'id8', "description" => '', "location" => 'Athletic Fitness', "subject" => "Group - Tae-Bo", "calendar" => "Groups", "start" => "2015-11-22 10:00", "end" => "2015-11-22 11:00"),
            array ( "id" => 'id9', "description" => '', "location" => 'Athletic Fitness', "subject" => "Group - Yoga", "calendar" => "Groups", "start" => "2015-11-23 12:00", "end" => "2015-11-23 13:00"),
            array ( "id" => 'id10', "description" => '', "location" => 'Athletic Fitness', "subject" => "Group - Pilates", "calendar" => "Groups", "start" => "2015-11-25 20:00", "end" => "2015-11-25 21:00"),
            array ( "id" => 'id11', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-22 16:00", "end" => "2015-11-22 20:00"),
            array ( "id" => 'id12', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-23 10:00", "end" => "2015-11-23 14:00"),
            array ( "id" => 'id13', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-24 14:00", "end" => "2015-11-24 18:00"),
            array ( "id" => 'id14', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-25 08:00", "end" => "2015-11-25 12:00"),
            array ( "id" => 'id15', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-26 06:00", "end" => "2015-11-26 10:00"),
            array ( "id" => 'id16', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-27 10:00", "end" => "2015-11-27 14:00"),
            array ( "id" => 'id17', "description" => '', "location" => 'Athletic Fitness', "subject" => "Sauna", "calendar" => "Sauna", "start" => "2015-11-28 06:00", "end" => "2015-11-28 10:00"),
    );

    $instructorsGrid = array( 
            array ( "id" => 'id1', "lastname" => 'Leverling', "firstname" => 'Andrew', "phone" => "Mobile: (206) 555-9857", "image" => "images/person1.png"),
            array ( "id" => 'id2', "lastname" => 'Suyama', "firstname" => 'Nancy', "phone" => "Mobile: (206) 555-9482", "image" => "images/person2.png"),
            array ( "id" => 'id3', "lastname" => 'Callahan', "firstname" => 'Janet', "phone" => "Mobile: (206) 555-3412", "image" => "images/person3.png"),
            array ( "id" => 'id4', "lastname" => 'Davolio', "firstname" => 'Margaret', "phone" => "Mobile: (206) 555-8122", "image" => "images/person4.png"),
    );

    $tasks = array( 
            array ( "id" => '1161', "state" => 'new', "label" => 'To be ordered a new fitness equipment', "tags" => "new fitness equipment", "hex" => "#36c7d0", "resourceId" => 3 ),
            array ( "id" => '1645', "state" => 'work', "label" => 'Repair of broken gym equipment', "tags" => "Repair, gym, equipment", "hex" => "#ff7878", "resourceId" => 1 ),
            array ( "id" => '9213', "state" => 'new', "label" => 'Staff recruitment', "tags" => "Staff, recruitment", "hex" => "#96c443", "resourceId" => 3 ),
            array ( "id" => '6546', "state" => 'done', "label" => 'Instructors course', "tags" => "Instructors, course", "hex" => "#ff7878", "resourceId" => 4 ),
            array ( "id" => '9034', "state" => 'new', "label" => 'Buy a new bench press', "tags" => "expenses, bench press", "hex" => "#96c443" ),
    );

    $users = array( 
            array ( "id" => 0, "name" => 'No name', "image" => '../../jqwidgets/styles/images/common.png', "common" => true ),
            array ( "id" => 1, "name" => 'Andrew Fuller', "image" => 'images/person1.png'),
            array ( "id" => 2, "name" => 'Nancy Davolio', "image" => 'images/person2.png'),
            array ( "id" => 3, "name" => 'Janet Leverling', "image" => 'images/person3.png'),
            array ( "id" => 4, "name" => 'Margaret Buchanan', "image" => 'images/person4.png')
    );

    $workloadTagCloudItems = array( 
            array ( "fitnessInstructorName" => 'Andrew Fuller', "clientsPerWeek" => 3 ),
            array ( "fitnessInstructorName" => 'Nancy Davolio', "clientsPerWeek" => 52 ),
            array ( "fitnessInstructorName" => 'Janet Leverling', "clientsPerWeek" => 30 ),
            array ( "fitnessInstructorName" => 'Margaret Buchanan', "clientsPerWeek" => 15 ),
    );

    $workloadTreeItems = array( 
            array ( "id" => 'instructor1', "icon" => "images/person1.png", "parentid" => "-1", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Andrew<br/><span style='font-size:10px;'>Fitness instructor<span></div>", "value" => "$15" ),
            array ( "id" => 'instructor2', "icon" => "images/person2.png", "parentid" => "-1", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Nancy<br/><span style='font-size:10px;'>Fitness instructor<span></div>", "value" => "$10"  ),
            array ( "id" => 'instructor3', "icon" => "images/person3.png", "parentid" => "-1", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Janet<br/><span style='font-size:10px;'>Fitness instructor<span></div>", "value" => "$12"  ),
            array ( "id" => 'instructor4', "icon" => "images/person4.png", "parentid" => "-1", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Margaret<br/><span style='font-size:10px;'>Fitness instructor<span></div>", "value" => "$5"  ),
            array ( "id" => 'client1', "icon" => "images/client1m.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Steven Davolio<br/><span style='font-size:10px; padding-left:5px;'>Andrew's client<span></div>", "parentid" => "instructor1" ),
            array ( "id" => 'client2', "icon" => "images/client2m.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Michael Buchanan<br/><span style='font-size:10px; padding-left:5px;'>Andrew's client<span></div>", "parentid" => "instructor1" ),
            array ( "id" => 'client3', "icon" => "images/client3m.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Robert Dodsworth<br/><span style='font-size:10px; padding-left:5px;'>Nancy's client<span></div>", "parentid" => "instructor2" ),
            array ( "id" => 'client4', "icon" => "images/client2f.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Laura Callahan<br/><span style='font-size:10px; padding-left:5px;'>Nancy's client<span></div>", "parentid" => "instructor2" ),
            array ( "id" => 'client5', "icon" => "images/client3f.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Anne Fuller<br/><span style='font-size:10px; padding-left:5px;'>Janet's client<span></div>", "parentid" => "instructor3" ),
            array ( "id" => 'client6', "icon" => "images/client2f.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Laura Fuller<br/><span style='font-size:10px; padding-left:5px;'>Janet's client<span></div>", "parentid" => "instructor3" ),
            array ( "id" => 'client7', "icon" => "images/client2f.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Laura Callahan<br/><span style='font-size:10px; padding-left:5px;'>Margaret's client<span></div>", "parentid" => "instructor4" ),
            array ( "id" => 'client8', "icon" => "images/client1f.png", "text" => "", "html" => "<div style='padding:10px 40px 10px 10px;'>Laura Fuller<br/><span style='font-size:10px; padding-left:5px;'>Andrew's client<span></div></div>", "parentid" => "instructor1" ),
    );

    $workloadChartData = array( 
            array ( "Day" => 'Sunday', "Andrew" => 1, "Nancy" => 3, "Janet" => 2, "Margaret" => 2 ),
            array ( "Day" => 'Monday', "Andrew" => 0, "Nancy" => 4, "Janet" => 3, "Margaret" => 1 ),
            array ( "Day" => 'Tuesday', "Andrew" => 0, "Nancy" => 3, "Janet" => 3, "Margaret" => 1 ),
            array ( "Day" => 'Wednesday', "Andrew" => 1, "Nancy" => 2, "Janet" => 3, "Margaret" => 2 ),
            array ( "Day" => 'Thursday', "Andrew" => 0, "Nancy" => 2, "Janet" => 2, "Margaret" => 3 ),
            array ( "Day" => 'Friday', "Andrew" => 1, "Nancy" => 3, "Janet" => 2, "Margaret" => 1 ),
            array ( "Day" => 'Saturday', "Andrew" => 0, "Nancy" => 1, "Janet" => 3, "Margaret" => 2 ),
    );

    $workloadTagCloudData = array( 
            array ( "fitnessInstructorName" => 'Andrew', "clientsPerWeek" => 3 ),
            array ( "fitnessInstructorName" => 'Nancy', "clientsPerWeek" => 18  ),
            array ( "fitnessInstructorName" => 'Janet', "clientsPerWeek" => 18  ),
            array ( "fitnessInstructorName" => 'Margaret', "clientsPerWeek" => 12  ),
    );

    $quickNotesData = array( 
            array ( "id" => 1213, "image" => 'images/person1.png', "firstname" => 'Andrew', "lastname" => 'Fuller', "job" => 'Fitness Instructor', "title" => 'Note 1', "notes" => "Repair of broken gym equipment"),
            array ( "id" => 1313, "image" => 'images/person2.png', "firstname" => 'Nancy', "lastname" => 'Davolio', "job" => 'Fitness Instructor', "title" => 'Note 2', "notes" => "Staff recruitment"),
            array ( "id" => 2213, "image" => 'images/person3.png', "firstname" => 'Janet', "lastname" => 'Leverling', "job" => 'Fitness Instructor', "title" => 'Note 3', "notes" => "Instructors course"),
            array ( "id" => 1243, "image" => 'images/person4.png', "firstname" => 'Margaret', "lastname" => 'Buchanan', "job" => 'Fitness Instructor', "title" => 'Note 4', "notes" => "Buy a new bench press"),
    );


    if(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "instructorsscheduler")){
        $response = $instructorsShedulerItems;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "roomsscheduler")){
        $response = $roomsShedulerItems;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "instructorsgrid")){
        $response = $instructorsGrid;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "taskskanban")){
        $response = $tasks;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "taskskanbanusers")){
        $response = $users;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "workloadtree")){
        $response = $workloadTreeItems;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "workloadtaglloud")){
        $response = $workloadTagCloudData;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "workloadchart")){
        $response = $workloadChartData;
    }elseif(isset($_GET['usedwidget'])&&($_GET['usedwidget'] == "quicknotesdata")){
        $response = $quickNotesData;
    }

    echo json_encode($response);
?>