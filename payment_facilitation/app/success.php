<?php
/**
 * Payment Success Page | cancel.php - Payment Facilitation Microservice
 * 
 * @author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
 * @team   - G3T4
 * 
 * - DEPENDENCIES -
 * (1) php-amqplib/php-amqplib - RabbitMQ Compatibility
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

  if (!$_GET) {
    redirect_to_error("Request Missing GET");
  }
  else {
    if (empty($_GET['customer_id']) || empty($_GET['session_id'])) {
        redirect_to_error(("Request Missing GET Var"));
    }
  }

/* --- Require the Dependencies --- */
  // uses composer autoload
  require_once(__DIR__ . "/vendor/autoload.php");

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
    "update_order_queue", # queue
    FALSE,                 # passive
    TRUE,                  # durable
    FALSE,                 # exclusive
    FALSE                  # auto delete
  );

  $channel->queue_bind(
    $queue_name,        # queue_name
    EXCHANGE_NAME,      # exchange name
    'update_order_key' # routing key
  );

  $message = new AMQPMessage(
    json_encode(
      [
        'orderID'      => $_GET['session_id'],
        'delivererID'  => "0",
        'order_status' => 'Payment Success',
      ]
    )
  );

  $channel->basic_publish(
    $message,
    EXCHANGE_NAME,
    'update_order_key',
    ['delivery_mode' => 2,
    'content-type' => 'application/json']
  );

  $channel->close();
  $connection->close();

  // perform the Javascript redirect to checkout
  echo "<!DOCTYPE html>
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Payment Successful</title>
            <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>
            <meta http-equiv='refresh' content='10;URL=https://localhost/c_homepage.php'>
        </head>
        <body>
            Your payment was successful!  
            Redirecting you back to home. <br />
            If your browser does not redirect you in 10 seconds, or you do
            not wish to wait, <a href='https://localhost/c_homepage.php'>click here</a>. 
        </body>
        </html>";