package com.esd.apache.api.order;

public class Order {
    private int OrderID;
    private int CustomerID;
    private int vendorID;
    private int delivererID;
    private int foodID;
    private int quantity;
    private String checkoutID;

    public Order(int OrderID, int CustomerID, int vendorID, int delivererID, int foodID, int quantity, String checkoutID) {
        this.OrderID = OrderID;
        this.CustomerID = CustomerID;
        this.vendorID = vendorID;
        this.delivererID = delivererID;
        this.foodID = foodID;
        this.quantity = quantity;
        this.checkoutID = checkoutID;
    }

    public int getOrderID() {
        return this.OrderID;
    }

    public int getCustomerID() {
        return CustomerID;
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

    public int getVendorID() {
        return vendorID;
    }

    public String getCheckoutID() {
        return checkoutID;
    }
}
