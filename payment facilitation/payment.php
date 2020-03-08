<?php
// if ($_POST) {
//   // subject to change in the future
//   if (empty($_POST['vendorid']) || empty($_POST['foodname'])) {
//     header("location:TEST.html");
//     exit();
//   }
// }
// else {
//   header("location:TEST.html");
//   exit();
// }

// we need to cURL Menu Microservice for more information but doesn't matter now
require_once("./stripe-php-7.27.1/init.php");
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
  Stripe\Stripe::setApiKey('sk_test_IGEllSO26K2ZNmsjykkK0yom00Wh5CGkdw');

  $customer = \Stripe\Checkout\Session::create([
    'success_url' => "http://localhost/run/success.php?customerid={$_POST['customerid']}&session_id={CHECKOUT_SESSION_ID}",
    'cancel_url' => "http://localhost/run/cancel?customerid={$_POST['customerid']}&session_id={CHECKOUT_SESSION_ID}",
    'payment_method_types' => ['card'],
    'line_items' => [
      [
        'name' => $_POST['foodname'],
        'description' => 'A very unique description',
        'amount' => 1000,
        'currency' => 'sgd',
        'quantity' => $_POST['quantity'],
      ],
    ],
  ]);

  $id = $customer->getLastResponse()->json['id'];

  echo '<script src="https://js.stripe.com/v3/"></script>';
  echo "<script>
          var stripe = Stripe('pk_test_56Qu5vUEGwiUGLHrQ1IZXORf00M3K2og5l');
          stripe.redirectToCheckout({
            sessionId: '$id'
          }).then(function (result) {
            $('.container-fluid').hide();
          }); 
        </script>";
  ?>
  </body>
</html>