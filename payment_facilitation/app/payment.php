<?php
/* Validation Section of the Code*/

// Validate the POST Request
  // Code Here

// Validate the contents of the POST Request
  // we need to cURL Menu Microservice for all the details as only some information is sent over
  // Code Here

/* The STRIPE Library Dependencies: curl, json, mbstring */
require_once(__DIR__ . "/vendor/autoload.php");
?>

<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=yes">
  <title>Payment Processing...</title>
</head>

<body>
  <?php
  // This is the Private Key
  // If deployed, these should be stored as an evironment variable
  Stripe\Stripe::setApiKey('sk_test_IGEllSO26K2ZNmsjykkK0yom00Wh5CGkdw');

  $customer = \Stripe\Checkout\Session::create([
    'success_url'          => "http://localhost/run/success.php?customerid={$_POST['customerid']}&session_id={CHECKOUT_SESSION_ID}",
    'cancel_url'           => "http://localhost/run/cancel?customerid={$_POST['customerid']}&session_id={CHECKOUT_SESSION_ID}",
    'payment_method_types' => ['card'],
    'line_items'           => [
      [
        'name'        => $_POST['foodname'],
        'description' => $_POST['food_description'],
        'images' => ['https://media.giphy.com/media/QUSUYLUUAIZ7EQpepf/giphy.gif'],
        'amount'      => $_POST['amount'] * 100,
        'currency'    => 'sgd',
        'quantity'    => $_POST['quantity'],
      ],
    ],
  ]);

  // Obtain the Checkout/Session ID from the customer object using the getter method
  $id = $customer->getLastResponse()->json['id'];

  // Perform the Javascript Redirect to Checkout
  echo '<script src="https://js.stripe.com/v3/"></script>';
  echo "<script>
          var stripe = Stripe('pk_test_56Qu5vUEGwiUGLHrQ1IZXORf00M3K2og5l');

          stripe.redirectToCheckout({
            sessionId: '$id'
          }).then(function (result) {
            window.location.replace('http://localhost/run/cancel?customerid={$_POST['customerid']}&session_id={CHECKOUT_SESSION_ID}')
          }); 

        </script>";
  ?>
  </body>
</html>