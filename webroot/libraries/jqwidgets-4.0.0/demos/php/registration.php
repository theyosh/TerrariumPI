<?php
// check whether the entered year is in the range of 1900 - 2012
if (isset($_POST["birthInputYear"]))
	{
	$year = $_POST["birthInputYear"];
	// validate year.
	if ($year > "2012" || $year < "1900")
		{
		echo "false";
		}
	  else
		{
		echo "true";
		}
	return;
	}
$formData = array(
	"username" => $_POST["username"],
	"password" => $_POST["password"],
	"realname" => $_POST["realname"],
	"birthdate" => $_POST["birthdate"],
	"email" => $_POST["email"],
	"ssn" => $_POST["ssn"],
	"phone" => $_POST["phone"],
	"zip" => $_POST["zip"],
	"acceptterms" => $_POST["acceptterms"]
);
// check whether the terms are accepted.
if ($formData['acceptterms'] != 'true')
	{
	$response = "<p><h1>Registration Not Successful</h1></p><p>You need to accept the terms.</p>";
	echo $response;
	return;
	}
// the registration is successful only if the username is 'admin' and the password is 'admin123'.
if ($formData['username'] == 'admin' && $formData['password'] == 'admin123')
	{
	$response = "<p><h1>Registration Successful</h1></p><p></p>";
	$response.= "Username:" . $formData['username'].= "<br/>";
	$response.= "Password:" . $formData['password'].= "<br/>";
	$response.= "Real name:" . $formData['realname'].= "<br/>";
	$response.= "Birth date:" . $formData['birthdate'].= "<br/>";
	$response.= "E-mail:" . $formData['email'].= "<br/>";
	$response.= "SSN:" . $formData['ssn'].= "<br/>";
	$response.= "Phone:" . $formData['phone'].= "<br/>";
	$response.= "Zip code:" . $formData['zip'].= "<br/>";
	}
  else
	{
	$response = "<p><h1>Registration Not Successful</h1></p><p>Invalid username or password.</p>";
	}
echo $response;
?>