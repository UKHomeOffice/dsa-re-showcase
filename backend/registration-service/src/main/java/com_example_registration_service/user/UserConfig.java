package com_example_registration_service.user;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class UserConfig {
  
  private final UserService userService;  // Injecting the UserService

  @Autowired
  public UserConfig(UserService userService) {
    this.userService = userService;
  }
  
  @Bean
  CommandLineRunner commandLineRunner(
    UserRepository repository) {
    return args -> {
      // Hash the passwords using the hashPassword method from UserService
      String hashedChrisPassword = userService.hashPassword("chrispassword");
      String hashedMichaelPassword = userService.hashPassword("michaelpassword");
      
      User chris = new User(
        "Chris",
        "Chris.Hunter@gmail.com",
        LocalDate.of(1989,07,27),
        hashedChrisPassword, 
        "customer"
      );
      
      User michael = new User(
        "Michael",
        "Michael.McCarthy@gmail.com",
        LocalDate.of(1984,11,12),
        hashedMichaelPassword,
        "admin"
      ); 
      
      repository.saveAll(
        List.of(chris, michael)
      );
    };
  }
}
