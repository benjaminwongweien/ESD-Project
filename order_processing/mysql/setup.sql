USE OrderDB;

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
  CustomerID INT NOT NULL,
  orderID VARCHAR(200) NOT NULL, -- this is the checkoutID from Stripe
  vendorID INT NOT NULL,
  delivererID INT,
  foodID INT NOT NULL,
  quantity INT NOT NULL,
  price FLOAT NOT NULL,
  -- checkoutID VARCHAR(100) NOT NULL,
  order_status VARCHAR(100),
  delivery_address VARCHAR(1000) NOT NULL,
  PRIMARY KEY(OrderID)
);

-- Insert newly created Orders

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1001, "21232323432", 2, NULL, 30, 10, 15, "Awaiting Payment", "BLK123 SUMANG AVE #03-159");

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1002, "2123443432", 2, NULL, 25, 5, 10, "Awaiting Payment", "SINGAPORE MANAGEMENT UNIVERSITY, SCHOOL OF BUSINESS");

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1001, "2hdjfhsfv3432", 2, NULL, 20, 15, 8, "Awaiting Payment", "NATIONAL UNIVERSITY OF SINGAPORE, FACULTY OF ARTS AND SOCIAL SCIENCES");


-- INSERT NEWLY ORDERS THAT ARE PAID

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1004, "2039473942", 1, NULL, 17, 8, 10, "Order Received", "BLK322 WOODLANDS AVENUE"
);

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1006, "8347238428328", 5, NULL, 4, 4, 8, "Order Received", "BLK459 LORANG CHUAN"
);

INSERT INTO Orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1008, "9382094823", 3, NULL, 12, 7, 10, "Order Received", "BLK772 HOUGANG AVE 3"
);

