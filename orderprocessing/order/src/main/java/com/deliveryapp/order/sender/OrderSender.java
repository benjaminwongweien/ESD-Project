package com.deliveryapp.order.sender;

import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PostMapping;

@Service
public class OrderSender {
    @Autowired
    private AmqpTemplate rabbitTemplate;
 
    @Value("${order.rabbitmq.exchange}")
    private String exchange;
 
    @Value("${send.rabbitmq.routingkey}")
    private String routingkey;
    
    public void send(String message) {
        String CustomMessage = "This is a message from sender"+ message;
    
        rabbitTemplate.convertAndSend(exchange, routingkey, CustomMessage);
        System.out.println("Send msg to consumer= " + CustomMessage+" ");
    }

}