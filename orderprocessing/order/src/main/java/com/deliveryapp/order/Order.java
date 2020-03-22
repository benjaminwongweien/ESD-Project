package com.deliveryapp.order;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "Orders")
public class Order {
    
    private int customerID;
    
    @Id
    @Column(name="orderID")
    private String orderID;

    private int vendorID;
    private int delivererID;
    private int foodID;
    private int quantity;
    private int price;
    private String order_status;

    @Column(name="delivery_address")
    private String delivery_address;

    public Order() {
        
    }


    public Order(int customerID, String orderID, int vendorID, int delivererID, 
        int foodID, int quantity, int price, String order_status, String delivery_address) {
        
        this(customerID, orderID, vendorID, foodID, quantity, price, order_status, delivery_address);
        this.delivererID = delivererID;
        

    }

    // Used to create Pending Order after user confirms order cart and makes payment
    public Order(int customerID, String orderID, int vendorID, int foodID, int quantity, int price , String order_status, String delivery_address) {
        this.customerID = customerID;
        this.vendorID = vendorID;
        this.orderID = orderID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.price = price;
        this.order_status = order_status;
        this.delivery_address = delivery_address;
    }

    public int getCustomerID() {
        return customerID;
    }

    public String getOrderID() {
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

    public String getOrder_status() {
        return order_status;
    }

    public String getDelivery_address() {
        return delivery_address;
    }

    public int getPrice() {
        return price;
    }
}
