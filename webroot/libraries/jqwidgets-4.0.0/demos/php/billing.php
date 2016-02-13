<?php	
	$formData = array(
		"firstname" => $_POST["firstName"],
		"middlename" => $_POST["middleInitial"],
		"lastname" => $_POST["lastName"],
    "billingAddress" => $_POST["billingAddress"],
    "billingAddressLine2" => $_POST["billingAddressLine2"],
    "billingCity" => $_POST["billingCity"],
    "billingState" => $_POST["billingState"],
    "billingZipCode" => $_POST["billingZipCode"],
    "billingCountry" => $_POST["billingCountries"],
    "shippingAddressCheckBox" => $_POST["shippingAddressCheckBox"],
    "shippingAddress" => $_POST["shippingAddress"],
    "shippingAddressLine2" => $_POST["shippingAddressLine2"],
    "shippingCity" => $_POST["shippingCity"],
    "shippingState" => $_POST["shippingState"],
    "shippingZipCode" => $_POST["shippingZipCode"],
    "shippingCountry" => $_POST["shippingCountries"],
    "cardNumber" => $_POST["cardNumber"],
    "expirationDate" => $_POST["expirationDate"],
    "expirationYear" => $_POST["expirationYear"],
    "securityCode" => $_POST["securityCode"],
    "cardType" => $_POST["cardType"]
 );
	
  $response = "<table>";
  $response .= "<tr><th>Customer Details</th></tr>";
  $response .= "<tr><td>" . $formData['firstname'] . "</td><td>" .  $formData['middlename'] . "</td><td>" . $formData['lastname'] . "</td></tr>";
  $response .= "<tr><td>Billing Address</td></tr>";
  $response .= "<tr><td>" . $formData['billingAddress'] . "</td></tr>";
  $response .= "<tr><td>" . $formData['billingAddressLine2'] . "</td></tr>";
  $response .= "<tr><td>" . $formData['billingCity'] . "</td><td>" . $formData['billingState'] . "</td></tr>";
  $response .= "<tr><td>" . $formData['billingZipCode'] . "</td><td>" . $formData['billingCountry'] . "</td></tr>";
  
  if (isset($_POST["shippingAddressCheckBox"]) && $_POST["shippingAddressCheckBox"] == 'true')
  {
    $response .= "<tr><td>Shipping Address</td></tr>";
    $response .= "<tr><td>" . $formData['shippingAddress'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['shippingAddressLine2'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['shippingCity'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['shippingState'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['shippingCity'] . "</td><td>" . $formData['shippingState'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['shippingZipCode'] . "</td><td>" . $formData['shippingCountry'] . "</td></tr>"; 
   }
    $response .= "<tr><td>Billing Information</td></tr>";
    $response .= "<tr><td>" . $formData['cardType'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['cardNumber'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['expirationDate'] . "</td><td>" . $formData['expirationYear'] . "</td></tr>";
    $response .= "<tr><td>" . $formData['securityCode'] . "</td></tr>";


  echo $response;
?>