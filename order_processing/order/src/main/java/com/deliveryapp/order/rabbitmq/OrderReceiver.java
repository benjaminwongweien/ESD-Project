package com.deliveryapp.order.rabbitmq;

import com.deliveryapp.order.*;

import org.springframework.amqp.rabbit.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

@Service
public class OrderReceiver {

/* 
====================================    Autowire Portions   ========================================
    
    This is where we autowired the other files that we create to support the API Controller. It
    automatically instantiate the component when we need it in the API endpoints when needed

    OrderController - Intialise orderController to utilise its own API Endpoint to query database

====================================================================================================
*/
    @Autowired
    OrderController orderController;


/* 
====================================    Receiver Setup   ========================================
    
    Sets up the RabbitListner with customised Queue, Exchange and Key. This will allow us to 
    create the channels that we are listening with and carry out the respective function 
    when a JSON message is received

====================================================================================================
*/    

    // To receive JSON message and convert to Order object and used to create pending order when
    // user submits Order and is redirected to Stripe for Payment
    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "receive_order_queue", durable = "true"),
        exchange = @Exchange(value = "receive_order_exchange", ignoreDeclarationExceptions = "false"),
        key = "receive_order_key.key")
    )
    public void receiveMessage(@Payload Order order) {
        orderController.create(order);
    }

    // To receive JSON Message and convert Order Object and used to update Order Status whenver needed
    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "update_order_queue", durable = "true"),
        exchange = @Exchange(value = "receive_order_exchange", ignoreDeclarationExceptions = "false"),
        key = "update_order_key")
    )
    public void receiveUpdate(@Payload Order order) {
        String orderID = order.getOrderID();
        Order data = orderController.findOrderByorderID(orderID);
        data.setOrder_status(order.getOrder_status());
        System.out.println("Before Updating: " + data.getDelivererID());
        data.setDelivererID(order.getDelivererID());
        System.out.println("After Updating:" + data.getDelivererID());
        orderController.update(data);
    }

}