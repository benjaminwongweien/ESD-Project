package com.deliveryapp.order.receiver;


import com.deliveryapp.order.Order;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class OrderReceiver {

    @RabbitListener(queues = "${order.rabbitmq.queue}")
    public void receiveMessage(String message) {
        System.out.println("Received from RabbitMQ: " + message);
    }

}