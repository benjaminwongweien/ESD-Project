DROP DATABASE IF EXISTS OrderDB;
CREATE DATABASE OrderDB;

USE OrderDB;

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
  CustomerID INT(50) NOT NULL,
  orderID INT(50) NOT NULL,
  vendorID INT(50) NOT NULL,
  delivererID INT(50),
  foodID INT(50) NOT NULL,
  quantity INT(10) NOT NULL,
  checkoutID VARCHAR(100) NOT NULL,
  order_status VARCHAR(100),
  PRIMARY KEY(CustomerID, OrderID)
);

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, checkoutID, order_status) VALUES 
(1001, 1, 2, NULL, 30, 10, "21232323432", NULL);

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, checkoutID, order_status) VALUES 
(1002, 1, 2, NULL, 25, 5, "2123443432", NULL);

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, checkoutID, order_status) VALUES 
(1001, 2, 2, NULL, 20, 15, "2hdjfhsfv3432", NULL);


