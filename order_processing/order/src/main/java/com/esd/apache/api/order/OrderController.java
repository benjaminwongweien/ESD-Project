package com.esd.apache.api.order;

import java.util.ArrayList;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class OrderController {

    private static final String Template = "Hello %s!";

    @GetMapping("/retrieveAll")
    @ResponseBody
    public Order retrieveAll() {
        OrderDAO orderDAO = new OrderDAO();
        return orderDAO.retrieveOrderbyUserID(123).get(0);
//        for (int i = 0; i<OrderList.size(); i++) {
//            Order order = OrderList.get(i);
//
//        }
    }

}
