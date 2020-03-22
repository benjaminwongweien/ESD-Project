package com.deliveryapp.order.rabbitmq;


import com.deliveryapp.order.*;

import org.springframework.amqp.rabbit.annotation.*;
import org.springframework.stereotype.Component;

@Component
public class OrderReceiver {

    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "receive_order_queue.queue", durable = "true"),
        exchange = @Exchange(value = "receive_order_exchange.exchange", ignoreDeclarationExceptions = "true"),
        key = "receive_order_key.key")
    )
    public void receiveMessage(Order order) {
        OrderController orderController = new OrderController();
        orderController.create(order);
    }

}