<?php
/**
 * Main Payment Page | payment.php - Payment Facilitation Microservice
 * 
 * @author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
 * @team   - G3T4
 * 
 * - DEPENDENCIES -
 * (1) stripe/stripe-php       - Payment
 * (2) php-amqplib/php-amqplib - RabbitMQ Compatibility
*/

/* --- Error Handling Functions --- */

  function redirect_to_error($e,$location=FALSE) {
    if (!$location) {
      $url = "https://localhost/c_homepage.php";
    }
    else {
      $url = "https://localhost/food.php?vendor_id={$_POST['vendor_id']}";
    }
    echo "<!DOCTYPE html>
          <html>
          <head>
              <meta charset='utf-8'>
              <title>Redirecting...</title>
              <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>
              <meta http-equiv='refresh' content='10;URL=https://localhost/c_homepage.php'>
          </head>
          <body>
              You are being automatically redirected due to an error.<br />
              If your browser does not redirect you in 10 seconds, or you do
              not wish to wait, <a href='https://localhost/c_homepage.php'>click here</a>. 
          </body>
          </html>";
    exit();
  }

/* --- Error Handling Functions --- */

  if (!$_POST) {
    redirect_to_error("Request Missing POST");
  }
  else {
    if (
        empty($_POST['vendor_id'])        ||
        empty($_POST['food_id'])          ||
        empty($_POST['customer_id'])      ||
        empty($_POST['food_name'])        || 
        empty($_POST['food_description']) || 
        empty($_POST['quantity'])         || 
        empty($_POST['amount'])           || 
        empty($_POST['delivery_address'])
      ) {
        redirect_to_error(("Request Missing POST Var"));
    }
  }
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=yes">
  <title>Payment Processing...</title>
</head>

<body>
  <?php

  /* --- Require the Dependencies --- */
  // uses composer autoload
  require_once(__DIR__ . "/vendor/autoload.php");

  try {
    // initialize Stripe with private key
    Stripe\Stripe::setApiKey('sk_test_IGEllSO26K2ZNmsjykkK0yom00Wh5CGkdw');

    $customer = \Stripe\Checkout\Session::create([
      'success_url'          => "http://localhost:86/success.php?customer_id={$_POST['customer_id']}&session_id={CHECKOUT_SESSION_ID}",
      'cancel_url'           => "http://localhost:86/cancel.php?customer_id={$_POST['customer_id']}&session_id={CHECKOUT_SESSION_ID}",
      'payment_method_types' => ['card'],
      'line_items'           => [
        [
          'name'        => $_POST['food_name'],
          'description' => $_POST['food_description'],
          'images'      => ['https://media.giphy.com/media/QUSUYLUUAIZ7EQpepf/giphy.gif'],
          'amount'      => $_POST['amount'] * 100,
          'currency'    => 'sgd',
          'quantity'    => $_POST['quantity'],
        ],
      ],
    ]);
  }
  // throw an error if stripe session fails to create
  catch (Exception $e) {
    redirect_to_error($e,TRUE);
  }

  // obtain the checkout session id from the customer object using the getter method
  $id = $customer->getLastResponse()->json['id'];

  // initialize AMQP Classes
  use PhpAmqpLib\Connection\AMQPStreamConnection;
  use PhpAmqpLib\Message\AMQPMessage;

  define('RABBITMQ_HOST', 'host.docker.internal');
  define('RABBITMQ_PORT', '5673');
  define('RABBITMQ_USERNAME', 'rabbit');
  define('RABBITMQ_PASSWORD', 'tibbar');
  define('EXCHANGE_NAME', 'receive_order_exchange');

  $connection = new AMQPStreamConnection(
    RABBITMQ_HOST, 
    RABBITMQ_PORT, 
    RABBITMQ_USERNAME, 
    RABBITMQ_PASSWORD
  );

  $channel = $connection->channel();

  $channel->exchange_declare(
      EXCHANGE_NAME, 
      'direct', # type
      FALSE,    # passive
      TRUE,     # durable
      FALSE     # auto_delete
  );

  list($queue_name, ,) = $channel->queue_declare(
    "receive_order_queue", # queue
    FALSE,                 # passive
    TRUE,                  # durable
    FALSE,                 # exclusive
    FALSE                  # auto delete
  );

  $channel->queue_bind(
    $queue_name,        # queue_name
    EXCHANGE_NAME,      # exchange name
    'receive_order_key' # routing key
  );

  $message = new AMQPMessage(
    json_encode(
      [
        'order_id'         => $id,
        'customer_id'      => $_POST['customer_id'],
        'vendor_id'        => $_POST['vendor_id'],
        'food_id'          => $_POST['food_id'],
        'quantity'         => $_POST['quantity'],
        'price'            => $_POST['amount'],
        'order_status'     => 'Awaiting Payment',
        'delivery_address' => $_POST['delivery_address']
      ]
    )
  );

  $channel->basic_publish(
    $message,
    EXCHANGE_NAME,
    'receive_order_key',
    ['delivery_mode' => 2]
  );

  $channel->close();
  $connection->close();

  // perform the Javascript redirect to checkout
  echo '';
  echo "<script src='https://js.stripe.com/v3/'></script>
        <script>
          var stripe = Stripe('pk_test_56Qu5vUEGwiUGLHrQ1IZXORf00M3K2og5l');

          stripe.redirectToCheckout({
            sessionId: '$id'
          }).then(function (result) {
            window.location.replace('http://localhost:86/cancel.php?customer_id={$_POST['customer_id']}&session_id={CHECKOUT_SESSION_ID}')
          }); 
        </script>";
  ?>
  </body>
</html>