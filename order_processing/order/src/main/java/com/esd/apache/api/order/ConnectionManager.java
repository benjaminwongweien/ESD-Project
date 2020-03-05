package com.esd.apache.api.order;

public interface ConnectionManager {
    String host = "localhost";
    int port = 3306;
    String dbName = "Order";
    String dbURL = "jdbc:mysql://" + host + ":" + port + "/" + dbName + "?useSSL=false";

}
