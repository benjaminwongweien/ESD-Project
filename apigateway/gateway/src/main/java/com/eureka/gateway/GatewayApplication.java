package com.eureka.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

	@Bean
	public RouteLocator myRoutes(RouteLocatorBuilder builder) {
		return builder.routes()
		.route(p -> p
			.path("/get")
			.filters(f -> f.addRequestHeader("Hello", "World"))
			.uri("http://httpbin.org:80"))
		.build();
	}



}
