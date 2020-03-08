package com.deliveryapp.order;

import com.deliveryapp.order.repository.*;
import com.deliveryapp.order.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The type User controller.
 *
 * @author Givantha Kalansuriya
 */

@RestController
@RequestMapping("/order")
public class OrderController {

  /**
   * Get all Orders list.
   *
   * @return the list
   */

  @GetMapping("/retrieveAll")
  public List<Order> getAllOrders() {

}