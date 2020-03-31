package com.deliveryapp.order.rabbitmq;

import com.deliveryapp.order.Order;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageBuilder;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class OrderSender {
    private final RabbitTemplate rabbitTemplate;

    @Autowired
    public OrderSender(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    @Autowired
    private ObjectMapper objectMapper;

    @Value("${order.rabbitmq.routingkey}")
    String routingkey;

    @Value("${order.rabbitmq.exchange}")
    String exchange;

    public void sendOrder(Order order) {
        try {
            if (order.getOrder_status().equals("Payment Cancelled")) {
                return;
            }
            String orderJson = objectMapper.writeValueAsString(order);
            Message message = MessageBuilder.withBody(orderJson.getBytes()).setContentType(MessageProperties.CONTENT_TYPE_JSON).build();
            this.rabbitTemplate.convertAndSend(exchange, routingkey, message);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }

}