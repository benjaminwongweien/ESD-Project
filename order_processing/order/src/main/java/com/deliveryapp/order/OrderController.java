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
        int CustID = Integer.parseInt(custID);
        return OrderRepo.findByCustomerID(CustID);
    }

    @PostMapping("/history/vendor")
    public List<Order> findOrdersbyVendorID(@RequestBody Map<String, String> body) {
        String vendorID = body.get("vendorID");
        int venID = Integer.parseInt(vendorID);
        return OrderRepo.findByvendorID(venID);
    }

    @PostMapping("/history/deliverer")
    public List<Order> findOrdersbyDelivererID(@RequestBody Map<String, String> body) {
        String delID = body.get("delivererID");
        int delivererID = Integer.parseInt(delID);
        return OrderRepo.findBydelivererID(delivererID);
    }

    public Order create(Order order) {
        return OrderRepo.save(order);
    }

    @PostMapping("/testpoint")
    public Order findOrderByorderID(@RequestBody Map<String, String> body) {
        String orderID = body.get("orderID");
        int customerID = Integer.parseInt(body.get("CustomerID"));
        int vendorID = Integer.parseInt(body.get("vendorID"));
        int foodID = Integer.parseInt(body.get("foodID"));
        int delivererID = Integer.parseInt(body.get("delivererID"));
        int quantity = Integer.parseInt(body.get("quantity"));
        int price = Integer.parseInt(body.get("price"));
        String order_status = body.get("order_status");
        String delivery_address = body.get("delivery_address");

        // Order order = OrderRepo.findOrderByorderID(orderID);
        Order order = new Order(customerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address);
        orderSender.sendOrder(order);
        return order;
    }



}