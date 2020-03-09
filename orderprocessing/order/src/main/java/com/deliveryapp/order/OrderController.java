package com.deliveryapp.order;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


import java.util.*;

@RestController
public class OrderController {

    @Autowired
    OrderRepository OrderRepo;

    @GetMapping("/")
    public List<Order> index() {
        return OrderRepo.findAll();
    }

    @PostMapping("/retrieve")
        public List<Order> findOrdersbyUserID(@RequestBody Map<String, String> body) {
            String custID = body.get("userid");
            int CustID = Integer.parseInt(custID);
            return OrderRepo.findByCustomerID(CustID);
    }


}