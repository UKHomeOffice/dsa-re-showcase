package com_example_registration_service.user;

import java.util.List;
import java.util.Optional;

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
      return ResponseEntity.status(HttpStatus.CREATED).body(savedUser); // Return the saved user
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
