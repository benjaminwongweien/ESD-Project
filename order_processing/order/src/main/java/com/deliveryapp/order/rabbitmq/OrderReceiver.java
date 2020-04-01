package com.deliveryapp.order.rabbitmq;

import com.deliveryapp.order.*;

import org.springframework.amqp.rabbit.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

@Service
public class OrderReceiver {

    @Autowired
    OrderController orderController;

    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "receive_order_queue", durable = "true"),
        exchange = @Exchange(value = "receive_order_exchange", ignoreDeclarationExceptions = "false"),
        key = "receive_order_key.key")
    )
    public void receiveMessage(@Payload Order order) {
        orderController.create(order);
    }


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