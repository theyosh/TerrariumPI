<?php	
	$formData = array(
		"username" => $_POST["username"],
		"password" => $_POST["password"],
		"rememberme" => $_POST["rememberme"]
	);
	
    if($formData['username'] == 'admin' && $formData['password'] == 'admin123') {
	    // get the checked state of the checkbox with name - "rememberme". The value could be true - 
	    if($formData['rememberme'] == 'true') {
		    $response = "<p><h1>Login Successful</h1></p><p>We'll keep you logged in on this computer.</p>";
        }
        else
		{
            $response = "<p><h1>Login Successful</h1></p><p>We won't keep you logged in on this computer.</p>";
        }
    }
    else {
        $response = "<p><h1>Login Not Successful</h1></p><p>Invalid username or password.</p>";
    }

	echo $response;
?>