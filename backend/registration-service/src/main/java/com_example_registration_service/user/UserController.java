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

import com_example_registration_service.CustomMetricService;

@RestController
@RequestMapping(path="api/v1/user")
public class UserController {
  
  private final UserService userService;
  private final CustomMetricService metricService;

  @Autowired
  public UserController(UserService userService, CustomMetricService metricService) {
    this.userService = userService;
    this.metricService = metricService;
  }
  
  @GetMapping
  public List<User> getUsers() {
    metricService.incrementCustomCounter();
    return userService.getUsers();
  }
  
  @PostMapping
  public ResponseEntity<User> registerNewUser(@RequestBody User user) {
    metricService.incrementCustomCounter();
    return userService.addNewUser(user);
  }
  
  @DeleteMapping(path = "{userId}")
  public void deleteUser(@PathVariable("userId") Long userId) {
    metricService.incrementCustomCounter();
    userService.deleteUser(userId); 
  }
  
  @PutMapping(path = "{userId}")
  public ResponseEntity<User> updateUser(@PathVariable Long userId, @RequestBody User updatedUser) {
    metricService.incrementCustomCounter();
    User updatedUserResponse = userService.updateUser(userId, updatedUser);
    return ResponseEntity.ok(updatedUserResponse);
  }
  
  @PostMapping("/login")
  public ResponseEntity<?> loginUser(@RequestBody UserLoginRequest userLoginRequest) {
    metricService.incrementCustomCounter();
    Optional<User> user = userService.authenticateUser(userLoginRequest.getEmail(), userLoginRequest.getPassword());
    if (user.isPresent()) {
        return ResponseEntity.ok(user.get()); // Return the user details - Can be used for the conditional rendering based on role!
    }
    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
  }
}
