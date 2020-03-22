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
        String custID = body.get("userid");
        int CustID = Integer.parseInt(custID);
        return OrderRepo.findByCustomerID(CustID);
    }

    @PostMapping("/history/vendor")
    public List<Order> findOrdersbyVendorID(@RequestBody Map<String, String> body) {
        String vendorID = body.get("vendorid");
        int venID = Integer.parseInt(vendorID);
        return OrderRepo.findByvendorID(venID);
    }

    @PostMapping("/history/deliverer")
    public List<Order> findOrdersbyDelivererID(@RequestBody Map<String, String> body) {
        String delID = body.get("delivererid");
        int delivererID = Integer.parseInt(delID);
        return OrderRepo.findBydelivererID(delivererID);
    }

    public Order create(Order order) {
        return OrderRepo.save(order);
    }



}