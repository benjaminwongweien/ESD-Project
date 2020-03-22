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
        value = @Queue(value = "receive_order_queue.queue", durable = "true"),
        exchange = @Exchange(value = "receive_order_exchange.exchange", ignoreDeclarationExceptions = "false"),
        key = "receive_order_key.key")
    )
    public void receiveMessage(@Payload Order order) {
        orderController.create(order);
    }

}