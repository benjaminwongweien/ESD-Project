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

/* 
====================================    Autowire Portions   ========================================
    
    This is where we autowired the other files that we create to support the API Controller. It
    automatically instantiate the component when we need it in the API endpoints when needed

    OrderSender - Configure OrderSender class to link it with RabbitTemplate
    ObjectMapper - used to map Order Object to JSON Format as String type

====================================================================================================
*/

    @Autowired
    public OrderSender(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    @Autowired
    private ObjectMapper objectMapper;

// ==================================================================================================

    // OrderSender Key Name -- From application.properties
    @Value("${order.rabbitmq.routingkey}")
    String routingkey;

    // OrderSender Exchange Name -- From application.properties
    @Value("${order.rabbitmq.exchange}")
    String exchange;

    // send Order details after querying from OrderDatabase
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