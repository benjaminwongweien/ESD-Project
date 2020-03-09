package com.deliveryapp.order;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "Orders")
public class Order {
    
    @Id
    @Column(name="CustomerID")
    private int customerID;
    
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="orderID")
    private int orderID;

    private int vendorID;
    private int delivererID;
    private int foodID;
    private int quantity;
    private String checkoutID;
    private String order_status;

    public Order() {
        
    }

    public Order(int customerID, int orderID, int vendorID, int delivererID, 
        int foodID, int quantity, String checkoutID, String order_status) {
        
        this.customerID = customerID;
        this.vendorID = vendorID;
        this.orderID = orderID;
        this.delivererID = delivererID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.checkoutID = checkoutID;
        this.order_status = order_status;

    }

    public Order(int customerID, int vendorID, int delivererID, 
        int foodID, int quantity, String checkoutID, String order_status) {
        
        this.customerID = customerID;
        this.vendorID = vendorID;
        this.delivererID = delivererID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.checkoutID = checkoutID;
        this.order_status = order_status;

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

    public String getStatus() {
        return order_status;
    }
}
