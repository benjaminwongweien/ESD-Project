USE OrderDB;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  CustomerID VARCHAR(100) NOT NULL,
  orderID VARCHAR(200) NOT NULL, -- this is the checkoutID from Stripe
  vendorID VARCHAR(100) NOT NULL,
  delivererID VARCHAR(100) NOT NULL,
  foodID VARCHAR(100) NOT NULL,
  quantity INT NOT NULL,
  price FLOAT NOT NULL,
  -- checkoutID VARCHAR(100) NOT NULL,
  order_status VARCHAR(100),
  delivery_address VARCHAR(1000) NOT NULL,
  PRIMARY KEY(orderID)
);

-- Insert newly created Orders

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1001, "21232323432", 2, 0, 30, 10, 15, "Awaiting Payment", "BLK123 SUMANG AVE #03-159");

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1002, "2123443432", 2, 0, 25, 5, 10, "Awaiting Payment", "SINGAPORE MANAGEMENT UNIVERSITY, SCHOOL OF BUSINESS");

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
(1001, "2hdjfhsfv3432", 2, 0, 20, 15, 8, "Awaiting Payment", "NATIONAL UNIVERSITY OF SINGAPORE, FACULTY OF ARTS AND SOCIAL SCIENCES");


-- INSERT NEWLY ORDERS THAT ARE PAID

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1004, "2039473942", 1, "0", 17, 8, 10, "Order Received", "BLK322 WOODLANDS AVENUE"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1006, "8347238428328", 5, "0", 4, 4, 8, "Order Received", "BLK459 LORANG CHUAN"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  1008, "9382094823", 3, "0", 12, 7, 10, "Order Received", "BLK772 HOUGANG AVE 3"
);


INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "cjj", "9382094847", 4, "0", 15, 6, 9, "Order Received", "Raffles Institution Boarding"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "bellelee51197@gmail.com", "9382094848", 4, "slypoon@gmail.com", 16, 6, 9, "Order Received", "Raffles Institution Boarding"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "cjj", "9382094849", 4, "slypoon@gmail.com", 16, 6, 9, "Order Received", "Raffles Institution Boarding"
);