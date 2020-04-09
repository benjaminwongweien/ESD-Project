# Elysion EaSy Delivery Microservices 

[![Inline docs](http://inch-ci.org/github/benjaminwongweien/elysion.svg?branch=master)](http://inch-ci.org/github/benjaminwongweien/elysion)
[![codebeat badge](https://codebeat.co/badges/b83dfe49-d566-4f12-b4b2-675979e8e403)](https://codebeat.co/projects/github-com-benjaminwongweien-elysion-master)

<p align="center">
  <img width="400px" height="400px" src="./logo.svg">
</p>


EaSy Delivery is a Microservice Driven Solution for Food Delivery.

# Features!

  - NGINX
  - User Microservice 
  - Menu Microservice
  - RabbiMQ AMQP Messaging Broker
  - Payment Microservise using Stripe API   
  - Notfication Microservice using Telegram API
  - Web UI with Google and Facebook Login Enabled
  - Recommendation Microservice using Google Maps API
  - Order Process Microservice built on Spring Boot Framework, which includes but not limited to:
    - JPA: For Database Interaction with MySQL and Spring using Java
    - Actuator module: Monitoring and managing health of Microservice
    - Gradle: Open-Source build automation system that builds on upon Apache Ant and Apche Maven
    - Tomcat: Open-Source Implementation of the Java Servlet, JavaServer Pages, Java Expression Language and WebSocket technologies

### Tech

EaSy Delivery uses a number of open source projects to work properly:

* [Flask](https://palletsprojects.com/p/flask/) - A lightweight WSGI web application framework.
* [Docker](https://www.docker.com) - Empowering App Development for Developers.
* [Stripe](https://stripe.com/en-sg) - Online payment processing for internet businesses.
* [RabbitMQ](https://www.rabbitmq.com/) - One of the most popular open source message brokers.
* [Bootstrap](https://getbootstrap.com/) - The most popular HTML, CSS, and JS library in the world.
* [Gunicorn](https://gunicorn.org) - Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. 
* [JPA](https://www.javaworld.com/article/3379043/what-is-jpa-introduction-to-the-java-persistence-api.html) - Java Persistence API (JPA) defines the management of relational data in the Java applications.
* [Gradle](https://gradle.org) - Accelerate developer productivity. Gradle helps teams build, automate and deliver better software, faster. 
* [NGINX](https://nginx.com) - NGINX accelerates content and application delivery, improves security, facilitates availability and scalability for the busiest web sites on the Internet.
* [Tomcat](https://tomcat.apache.org/) - The Apache Tomcat® software is an open source implementation of the Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket.
* [Spring Boot](https://spring.io/projects/spring-boot) - Open Source Java Framework that can be used to create Microservice. It helps Java Developers to develop a stand-alone and production grade spring application to just run

### Installation

EaSy Delivery requires [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/install/) to run.

Please install the dependencies to start the server.

To start all the services together (for Windows Machines), run:

```sh
$ G3T4 EaSy Delivery Start Script.cmd
```

To start the services individually:

```sh
$ cd ${microservice_directory}
$ docker-compose up -d
```

### How to Use

Please turn off WAMP/XAMPP or any other Apache Services running on your host computer, if it is running.

This will compose the required EaSy Delivery images and pull in the necessary dependencies. Be sure to swap out `${microservice_directory}` with the actual location of each microservice on your machine.

### Ports

| Microservice                    | Exposed |  :  | Internal | Link                   |
| ------------------------------- | ------: | :-: | -------- | :--------------------: |
| UI - NGINX                      | 443     |  :  | 443      | https://localhost/     |
| UI - PHP-FPM                    | -       |  :  | 9000     | -                      |
| Menu - NGINX                    | 85      |  :  | 80       | http://localhost:85/   |
| Menu - Flask                    | -       |  :  | 8000     | -                      |
| Menu - PostgresDB               | -       |  :  | 5432     | -                      |
| Payment Facilitation - NGINX    | 86      |  :  | 80       | http://localhost:86/   |
| Payment Facilitation - PHP-FPM  | -       |  :  | 9000     | -                      |
| Payment Facilitation - Composer | -       |  :  | -        | -                      |
| User - NGINX                    | 88      |  :  | 80       | http://localhost:88/   |
| User - Flask                    | -       |  :  | 8000     | -                      |
| User - PostgresDB               | -       |  :  | 5432     | -                      |
| Recommendation - NGINX          | 89      |  :  | 80       | http://localhost:89/   |
| Recommendation - Flask          | -       |  :  | 8000     | -                      |
| RabbitMQ Broker                 | 5673    |  :  | 5672     | http://localhost:5673/ |
| RabbitMQ Management             | 15673   |  :  | 15672    | http://localhost:15673/| 
| Order Processing - Spring Boot  | 8080    |  :  | 8080     | http://localhost:8080/ |
| Order Processing - MySQL        | -       |  :  | 3306     | -                      |    
| Notification - Rabbit Listener  | -       |  :  | -        | -                      |      
| Notification - Register         | -       |  :  | -        | -                      |  
| Notification - Updater          | -       |  :  | -        | -                      | 
| Notification - Vendor Broker    | -       |  :  | -        | -                      |  
| Notification - Driver Broker    | -       |  :  | -        | -                      | 
| Notification - MySQL            | -       |  :  | 3306     | -                      |   

### Todos

 - Its Done!

License
----
**Free Software, Hell Yeah!**
