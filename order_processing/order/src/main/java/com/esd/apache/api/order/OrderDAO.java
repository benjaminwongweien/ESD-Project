package com.esd.apache.api.order;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.lang.reflect.InvocationTargetException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class OrderDAO implements ConnectionManager {

    public ArrayList<Order> retrieveOrderbyUserID(int customerID) {
        String dbUsername = "root";
        String dbPassword = "";

        String sql = "select * from order where CustomerID=?";

        ArrayList<Order> OrderList = new ArrayList<>();

        try {

            // step 2: Gets a connection to the database
            Connection conn = DriverManager.getConnection(dbURL, dbUsername, dbPassword);

            // step 3: Prepare the SQL to be sent to the database
            PreparedStatement stmt = conn.prepareStatement(sql);

            // bind the parameters
            stmt.setInt(1, customerID);

            // step 4: executes the query
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                int orderID = rs.getInt("orderID");
                int vendorID = rs.getInt("vendorID");
                int delivererID = rs.getInt("delivererID");
                int foodID = rs.getInt("foodID");
                int quantity = rs.getInt("quantity");
                String checkoutID = rs.getString("checkoutID");

                OrderList.add(new Order(orderID, customerID, vendorID, delivererID, foodID, quantity, checkoutID));
            }

            return OrderList;
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {

        }
        return OrderList;

    }
}
