package com.deliveryapp.order;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface OrderRepository extends JpaRepository<Order, Integer> {

    /* 
        
        Creates Abstract Methods for JpaRepository to recognise and match the respective 
        SQL Commands to query and work with the Order Database
    
    */

    Order findOrderByorderID(String orderID);

    List<Order> findByCustomerID(String CustomerID);

    List<Order> findByvendorID(String VendorID);

    List<Order> findBydelivererID(String DelivererID);

}