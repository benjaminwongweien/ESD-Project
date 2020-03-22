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
    
    @Column(name="orderID")
    private String orderID;

    private int vendorID;
    private int delivererID;
    private int foodID;
    private int quantity;
    private int price;
    private String order_status;
    private String delivery_address;

    public Order() {
        
    }


    public Order(int customerID, String orderID, int vendorID, int delivererID, 
        int foodID, int quantity, int price, String order_status, String delivery_address) {
        
        this(customerID, orderID, foodID, quantity, price, order_status, delivery_address);
        this.delivererID = delivererID;
        

    }

    // Used to create Pending Order after user confirms order cart and makes payment
    public Order(int customerID, String orderID, int foodID, int quantity, int price , String order_status, String delivery_address) {
        this.customerID = customerID;
        this.orderID = orderID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.price = price;
        this.order_status = order_status;
        this.delivery_address = delivery_address;
    }

    public int getCustomerId() {
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

    public String getStatus() {
        return order_status;
    }

    public String getDeliveryAddress() {
        return delivery_address;
    }
}
