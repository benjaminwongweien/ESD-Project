package com.deliveryapp.order;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity // Entity Class fpr Order microservice
@Table(name = "orders") // points class to Table in MySQL
public class Order {
    
    private String customerID;
    
    @Id
    @Column(name="orderID")
    private String orderID;

    private String vendorID;
    private String delivererID;
    private String foodID;
    private int quantity;
    private float price;
    private String order_status;

    @Column(name="delivery_address")
    private String delivery_address;

    // Empty Constructor
    public Order() {
        
    }

    // Used for Order Creation
    public Order(String customerID, String orderID, String vendorID, String delivererID, 
        String foodID, int quantity, float price, String order_status, String delivery_address) {
        
        this(customerID, orderID, vendorID, foodID, quantity, price, order_status, delivery_address);
        this.delivererID = delivererID;
        

    }

    // Used to create Pending Order after user confirms order cart and makes payment
    public Order(String customerID, String orderID, String vendorID, String foodID, int quantity, float price , String order_status, String delivery_address) {
        this.customerID = customerID;
        this.vendorID = vendorID;
        this.orderID = orderID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.price = price;
        this.order_status = order_status;
        this.delivery_address = delivery_address;
    }

    // Used for updating Order Status during the acceptance by Vendor and Deliverer
    public Order(String orderID, String deliverID, String order_status) {
        this.orderID = orderID;
        this.order_status = order_status;
        this.delivererID = deliverID;
    }
/*   -----------------------
    |                       |
    |    GETTER METHODS     |
    |                       |
     -----------------------
*/ 

    public String getCustomerID() {
        return customerID;
    }

    public String getOrderID() {
        return orderID;
    }


    public String getVendorID() {
        return vendorID;
    }
 
    public String getDelivererID() {
        return delivererID;
    }

    public String getFoodID() {
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

    public float getPrice() {
        return price;
    }

    /* 
         ---------------------------
        |                           |
        |       SETTER METHOD       |
        |                           |
        ----------------------------
    */

    public void setOrder_status(String order_status) {
        this.order_status = order_status;
    }

    public void setDelivererID(String deliverID) {
        this.delivererID = deliverID;
    }
}
