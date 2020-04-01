package com.deliveryapp.order;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

import com.deliveryapp.order.rabbitmq.OrderReceiver;
import com.deliveryapp.order.rabbitmq.OrderSender;

/* 
===========================    Rest API Controller for Order Processing  =============================
    
    This is where the API endpoints are created. The RequestMapping annotation lets Spring Boot knows
    that the root access to this api starts with /order

*/

@RestController
@RequestMapping(value="/order")
public class OrderController {

/* 

====================================    Autowire Portions   ========================================
    
    This is where we autowired the other files that we create to support the API Controller. It
    automatically instantiate the component when we need it in the API endpoints when needed

    OrderSender --> In charge of utilising RabbitMQ to send out JSON Messages
    OrderReceiver --> In charge of utilising RabbitMQ to receive JSON Messages
    OrderRepository --> In charge of communication with the Database for CRUD Purposes

*/

    @Autowired
    OrderSender orderSender;

    @Autowired
    OrderReceiver orderReceiver;

    @Autowired
    OrderRepository OrderRepo;

/* 
    
=======================================    GET ENDPOINT   =============================================
    
*/

    /*
    ==================================    DUMP ALL ENDPOINT  ==========================================
    */
    @GetMapping("/all")
    public List<Order> index() {
        return OrderRepo.findAll();
    }

/*

======================================    POST ENDPOINT  ==============================================

*/

    /* --------------------------------
       |  Query for History of Users  |
       --------------------------------    
    */
    
    // Query for Customer's Order History
    @PostMapping("/history/customer")
    public List<Order> findOrdersbyUserID(@RequestBody Map<String, String> body) {
        String custID = body.get("customerID");
        return OrderRepo.findByCustomerID(custID);
    }

    // Query for Vendor's Order History
    @PostMapping("/history/vendor")
    public List<Order> findOrdersbyVendorID(@RequestBody Map<String, String> body) {
        String vendorID = body.get("vendorID");
        return OrderRepo.findByvendorID(vendorID);
    }

    // Query for Deliverer's Order History
    @PostMapping("/history/deliverer")
    public List<Order> findOrdersbyDelivererID(@RequestBody Map<String, String> body) {
        String delID = body.get("delivererID");
        return OrderRepo.findBydelivererID(delID);
    }

    /* -------------------------------- 
       |       RabbitMQ Endpoints     |
       --------------------------------
    */

    /* ---------------------------------------------------------------------------
        Use by OrderReceiver
        --> Receives an Order object and insert or update the rows in the database
        (Matched by primary key - orderID)
       ----------------------------------------------------------------------------
    */

     public Order create(Order order) {
        return OrderRepo.save(order);
    }

    /* ---------------------------------------------------------------------------
        Use by OrderReceiver
        --> Receives an Order object
        --> uses orderSender to send Order Object as JSON through RabbitMQ
        --> then updates the database on the Order Status
       ----------------------------------------------------------------------------
    */

    public Order update(Order order) {
        System.out.println("Inside the Database: \r\n\tOrderID : " + order.getOrderID() + ", DelivererID :" + order.getDelivererID());
        orderSender.sendOrder(order);
        return OrderRepo.save(order);
    }

    /* ---------------------------------------------------------------------------
        Use by OrderReceiver
        --> Receives an Order object and get the orderID from Order object
        --> find the Order in database that has orderID matches the orderID
        --> then returns the actual Order Object that we are interested in
       ----------------------------------------------------------------------------
    */

    public Order findOrderByorderID(String orderID) {
        return OrderRepo.findOrderByorderID(orderID);
    }

    /*
        ----------------------    Commented Out Testpoint for OrderSender   ---------------------------

    @PostMapping("/testpoint")
    public Order findOrderByorderID(@RequestBody Map<String, String> body) {
        String orderID = body.get("orderID");
        String customerID = body.get("CustomerID");
        String vendorID = body.get("vendorID");
        String foodID = body.get("foodID");
        String delivererID = body.get("delivererID");
        int quantity = Integer.parseInt(body.get("quantity"));
        float price = Float.parseFloat(body.get("price"));
        String order_status = body.get("order_status");
        String delivery_address = body.get("delivery_address");

        // Order order = OrderRepo.findOrderByorderID(orderID);
        Order order = new Order(customerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address);
        orderSender.sendOrder(order);
        return order;
    }
    */



}