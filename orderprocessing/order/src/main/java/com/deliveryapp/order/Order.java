package com.deliveryapp.order;

import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;

@Entity
@Table(name = "order")
@EntityListeners(AuditingEntityListener.class)
public class Order {
    @Id
    @Column (name = "CustomerID", nullable = false)
    private int customerID;
    @Id
    @Column(name = "orderID", nullable = false)
    private int orderID;
    @Column(name = "vendorID", nullable = false)
    private int vendorID;
    @Column(name = "delivererID", nullable = false)
    private int delivererID;
    @Column(name = "foodID", nullable = false)
    private int foodID;
    @Column(name = "quantity", nullable = false)
    private int quantity;
    @Column(name = "checkoutID", nullable = false)
    private String checkoutID;

    public Order(int customerID, int orderID, int vendorID, int delivererID, 
        int foodID, int quantity, String checkoutID) {
        
        this.customerID = customerID;
        this.orderID = orderID;
        this.vendorID = vendorID;
        this.delivererID = delivererID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.checkoutID = checkoutID;

    }

    public int getCustomerId() {
        return customerID;
    }

    public int getOrderID() {
        return orderID;
    }


    public int getVendorID() {
        return vendorID;
    }
 
 
    public int getDelivererID() {
        return delivererID;
    }

    public int getFoodID() {
        return foodID;
    }

    public int getQuantity() {
        return quantity;
    }

    public String getCheckoutID() {
        return checkoutID;
    }
}