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
("user@user.com", "21232323432", 2, 0, 30, 10, 15, "completed", "BLK123 SUMANG AVE #03-159");

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
("user@user.com", "2123443432", 2, 0, 25, 5, 10, "completed", "SINGAPORE MANAGEMENT UNIVERSITY, SCHOOL OF BUSINESS");

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES 
("user@user.com", "2hdjfhsfv3432", 2, 0, 20, 15, 8, "completed", "NATIONAL UNIVERSITY OF SINGAPORE, FACULTY OF ARTS AND SOCIAL SCIENCES");


-- INSERT NEWLY ORDERS THAT ARE PAID

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "2039473942", 1, "0", 17, 8, 10, "completed", "BLK322 WOODLANDS AVENUE"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "8347238428328", 5, "0", 4, 4, 8, "completed", "BLK459 LORANG CHUAN"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "9382094823", 3, "0", 12, 7, 10, "completed", "BLK772 HOUGANG AVE 3"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "9382094847", 4, "0", 16, 6, 8.85, "completed", "Raffles Institution Boarding"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "9382094848", 4, "slypoon@gmail.com", 16, 6, 8.85, "completed", "Raffles Institution Boarding"
);

INSERT INTO orders (CustomerID, orderID, vendorID, delivererID, foodID, quantity, price, order_status, delivery_address) VALUES (
  "yourEmailHere@yourEmailHere.com", "9382094849", 4, "slypoon@gmail.com", 16, 6, 8.85, "completed", "Raffles Institution Boarding"
);