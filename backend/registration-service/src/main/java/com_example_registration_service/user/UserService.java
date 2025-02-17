package com_example_registration_service.user;

import com_example_registration_service.*;

import java.util.List;
import java.util.Optional;
import java.time.Instant;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import jakarta.transaction.Transactional;

@Service
public class UserService {
  
  private final UserRepository userRepository;

  @Autowired
  public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
  
  // Inject the Kafka producer
  @Autowired // ADDED
  private RegistrationProducer registrationProducer; // ADDED
  
  public List<User> getUsers() {
      return userRepository.findAll();
    }

  public ResponseEntity addNewUser(User user) {
    Optional<User> userOptional = userRepository
      .findUserByEmail(user.getEmail());
    if (userOptional.isPresent())  {
      throw new IllegalStateException("This email is taken");
      }
      user.setPassword(user.getPassword());
      User savedUser = userRepository.save(user);

      String message = String.format("User registered: %s, %s, %s, %s, %s", 
      savedUser.getName(), 
      savedUser.getEmail(), 
      savedUser.getDob(),
      savedUser.getRole(),
      Instant.now().toString());

      // Send Kafka message
      registrationProducer.sendRegistrationMessage(message);
      logger.info("Kafka registration message sent: {}", message);
      return ResponseEntity.status(HttpStatus.CREATED).body(savedUser);
    }

  public void deleteUser(Long userId) {
    boolean exists = userRepository.existsById(userId);
    if (!exists) {
      throw new IllegalStateException(
        "User with ID " + userId + " does not exist!"
      );
    }
    userRepository.deleteById(userId);
  }

@Transactional
public User updateUser(Long userId, User updatedUser) {
  User user = userRepository.findById(userId)
    .orElseThrow(() -> new IllegalStateException(
      "User not found!"
    ));
    user.setName(updatedUser.getName());
    user.setEmail(updatedUser.getEmail());
    user.setDob(updatedUser.getDob());
    
    return userRepository.save(user);
    
  }
  
  private static final Logger logger = LoggerFactory.getLogger(UserService.class);

  public Optional<User> authenticateUser(String email, String password) {
    Optional<User> userOptional = userRepository.findUserByEmail(email);
    if (userOptional.isPresent()) {
      logger.debug("User found: {}", userOptional.get().getEmail());
      logger.debug("Database password: {}", userOptional.get().getPassword());
      logger.debug("Provided password: {}", password);

      if (userOptional.get().getPassword().equals(password)) {
        logger.debug("Passwords match!");

        // Send Kafka message on successful login
        String message = String.format("User logged in: %s, %s, %s", 
                userOptional.get().getName(),
                userOptional.get().getEmail(),
                Instant.now().toString());
        registrationProducer.sendLoginMessage(message);
        logger.info("Kafka message sent: {}", message);

        return userOptional;
      } else {
        logger.debug("Password mismatch!");
      }
    } else {
        logger.debug("User not found for email: {}", email);
    }
    return Optional.empty();
  }
}
