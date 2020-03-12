package com.deliveryapp.order;

import com.deliveryapp.order.sender.*;
import com.deliveryapp.order.receiver.*;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

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

    

    @PostMapping("/create")
    public Order create(@RequestBody Map<String, String> body) {

        String customerID = body.get("customer_id");
        String food = body.get("food_id");
        String qty = body.get("quantity");

        int custID = Integer.parseInt(customerID);
        int foodID = Integer.parseInt(food);
        int quantity = Integer.parseInt(qty);

        String checkoutID = body.get("checkout_id");
        String status = body.get("status");

        orderReceiver.receiveMessage(customerID);
        return OrderRepo.save(new Order(custID, foodID, quantity, checkoutID, status));
    }



}