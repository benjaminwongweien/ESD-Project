package com.deliveryapp.order;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

import com.deliveryapp.order.rabbitmq.OrderReceiver;
import com.deliveryapp.order.rabbitmq.OrderSender;

@RestController
@RequestMapping(value="/order")
public class OrderController {

    @Autowired
    OrderSender orderSender;

    @Autowired
    OrderReceiver orderReceiver;

    @Autowired
    OrderRepository OrderRepo;

    @GetMapping("/all")
    public List<Order> index() {
        return OrderRepo.findAll();
    }

    @PostMapping("/history/customer")
    public List<Order> findOrdersbyUserID(@RequestBody Map<String, String> body) {
        String custID = body.get("customerID");
        return OrderRepo.findByCustomerID(custID);
    }

    @PostMapping("/history/vendor")
    public List<Order> findOrdersbyVendorID(@RequestBody Map<String, String> body) {
        String vendorID = body.get("vendorID");
        return OrderRepo.findByvendorID(vendorID);
    }

    @PostMapping("/history/deliverer")
    public List<Order> findOrdersbyDelivererID(@RequestBody Map<String, String> body) {
        String delID = body.get("delivererID");
        return OrderRepo.findBydelivererID(delID);
    }

    public Order create(Order order) {
        return OrderRepo.save(order);
    }

    public Order update(Order order) {
        orderSender.sendOrder(order);
        return OrderRepo.save(order);
    }

    public Order findOrderByorderID(String orderID) {
        return OrderRepo.findOrderByorderID(orderID);
    }

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



}