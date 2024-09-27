package com_example_registration_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class RegistrationServiceApplication {

    public static void main(String[] args) {
      SpringApplication.run(RegistrationServiceApplication.class, args);
	}
}
