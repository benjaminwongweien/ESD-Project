package com.deliveryapp.order.rabbitmq.config;

// Import of AMQP Component under Spring Framework
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.annotation.RabbitListenerConfigurer;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.listener.RabbitListenerEndpointRegistrar;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;

// Import of Annotations used in Spring Boot Framework
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// Import of Message handler used in the RabbitMQConfiguration for Listeners
import org.springframework.messaging.converter.MappingJackson2MessageConverter;
import org.springframework.messaging.handler.annotation.support.DefaultMessageHandlerMethodFactory;
import org.springframework.messaging.handler.annotation.support.MessageHandlerMethodFactory;

@Configuration // Configuration Class
public class RabbitMQConfiguration implements RabbitListenerConfigurer {

    // OrderSender Queue Name -- From application.properties
    @Value("${order.rabbitmq.queue}")
    String queueName;

    // OrderSender Exchange Name -- From application.properties
    @Value("${order.rabbitmq.exchange}")
    String exchange;

    // OrderSender Key Name -- From application.properties
    @Value("${order.rabbitmq.routingkey}")
    private String routingkey;

/* 
-----------    Creating Queue, DirectExchange and Binds the Queue to Exchange with Key      -----------
*/

    @Bean
    Queue queue() {
        return new Queue(queueName, true, false, false);
    }

    @Bean
    DirectExchange exchange() {
        return new DirectExchange(exchange);
    }

    @Bean
    Binding binding(Queue queue, DirectExchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with(routingkey);
    }


/*
-------------------  Configure RabbitListeners for OrderReceiver to receive JSON ----------------------
*/

    @Override
    public void configureRabbitListeners(RabbitListenerEndpointRegistrar registar) {
        registar.setMessageHandlerMethodFactory(messageHandlerMethodFactory());
    }

    @Bean
    MessageHandlerMethodFactory messageHandlerMethodFactory() {
        DefaultMessageHandlerMethodFactory messageHandlerMethodFactory = new DefaultMessageHandlerMethodFactory();
        messageHandlerMethodFactory.setMessageConverter(consumerJackson2MessageConverter());
        return messageHandlerMethodFactory;
    }

    @Bean
    public MappingJackson2MessageConverter consumerJackson2MessageConverter() {
        return new MappingJackson2MessageConverter();
    }

/* 
------------------      Configure RabbitTemplate for OrderSender to send JSON    ----------------------
*/

    @Bean
    public RabbitTemplate rabbitTemplate(final ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(producerJackson2MessageConverter());
        return rabbitTemplate;
    }
  
    @Bean
    public Jackson2JsonMessageConverter producerJackson2MessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

}