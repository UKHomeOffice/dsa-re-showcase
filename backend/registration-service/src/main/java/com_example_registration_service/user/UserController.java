package com_example_registration_service.user;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path="api/v1/user")
public class UserController {
  
  private final UserService userService;

  @Autowired
  public UserController(UserService userService) {
    this.userService = userService;
  }
  
  @GetMapping
  public List<User> getUsers() {
    return userService.getUsers();
  }
  
  @PostMapping
  public ResponseEntity<User> registerNewUser(@RequestBody User user) {
    throw new RuntimeException("Simulated exception to trigger high error rate.");
  }
  
  @DeleteMapping(path = "{userId}")
  public void deleteUser(@PathVariable("userId") Long userId) {
    userService.deleteUser(userId); 
  }
  
  @PutMapping(path = "{userId}")
  public ResponseEntity<User> updateUser(@PathVariable Long userId, @RequestBody User updatedUser) {
    User updatedUserResponse = userService.updateUser(userId, updatedUser);
    return ResponseEntity.ok(updatedUserResponse);
  }
  
  @PostMapping("/login")
  public ResponseEntity<?> loginUser(@RequestBody UserLoginRequest userLoginRequest) {
    Optional<User> user = userService.authenticateUser(userLoginRequest.getEmail(), userLoginRequest.getPassword());
    if (user.isPresent()) {
        return ResponseEntity.ok(user.get()); // Return the user details - Can be used for the conditional rendering based on role!
    }
    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
  }
}
