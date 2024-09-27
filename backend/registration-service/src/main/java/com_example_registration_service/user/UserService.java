package com_example_registration_service.user;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

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
      user.setPassword(hashPassword(user.getPassword()));
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
  
  public Optional<User> authenticateUser(String email, String password) {
    Optional<User> userOptional = userRepository.findUserByEmail(email);
    if (userOptional.isPresent() && userOptional.get().getPassword().equals(hashPassword(password))) {
        return userOptional;
    }
    return Optional.empty(); // No valid user found or password mismatch
  }
  
  public String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(password.getBytes());
            StringBuilder hexString = new StringBuilder();

            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            } 
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}
