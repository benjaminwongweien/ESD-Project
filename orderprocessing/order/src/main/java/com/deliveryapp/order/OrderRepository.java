package com.deliveryapp.order;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface OrderRepository extends JpaRepository<Order, Integer> {

    List<Order> findByCustomerID(int CustomerID);

    List<Order> findByvendorID(int VendorID);

    List<Order> findBydelivererID(int DelivererID);

}