<?php	
	$formData = array(
		"firstname" => $_POST["firstname"],
		"middlename" => $_POST["middlename"],
		"lastname" => $_POST["lastname"],
    "email" => $_POST["email"],
		"subject" => $_POST["subject"],
    "message" => $_POST["message"] 
	);
	   
  $response = "<p><h1>Thanks for Contacting Us!</h1></p><p></p>";
  $response .= "Your message has been successfully sent!";
  echo $response;
?>