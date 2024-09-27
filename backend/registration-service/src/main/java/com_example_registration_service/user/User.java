package com_example_registration_service.user;

import java.time.LocalDate;
import java.time.Period;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;


@Entity
@Table(name = "registered_users")

public class User {
  @Id
  @SequenceGenerator(
    name = "user_sequence",
    sequenceName = "user_sequence",
    allocationSize = 1
  )
  @GeneratedValue(
    strategy = GenerationType.SEQUENCE,
    generator = "user_sequence"
  )
  private Long id;
  private String name;
  private String email;
  private LocalDate dob;
  private String password;
  private String role;
  @Transient
  private Integer age;
  
  public User() {
  }

  public User(Long id,
                String name,
                String email,
                LocalDate dob,
                String password,
                String role) {
  this.id = id;
    this.name = name;
    this.email = email;
    this.dob = dob;
    this.password = password;
    this.role = role;
  }

  public User(String name,
                String email,
                LocalDate dob,
                String password,
                String role) {
    this.name = name;
    this.email = email;
    this.dob = dob;
    this.password = password;
    this.role = role;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public LocalDate getDob() {
    return dob;
  }

  public void setDob(LocalDate dob) {
    this.dob = dob;
  }

  public String getPassword() {
    return password;
  }

  public void setPassword(String password) {
    this.password = password;
  }
  
  public String getRole() {
    return role;
  }

  public void setRole(String role) {
    this.role = role;
  }
  
  public Integer getAge() {
    return Period.between(this.dob, LocalDate.now()).getYears();
  }

  public void setAge(Integer age) {
    this.age = age;
  }

  @Override
  public String toString() {
    return "User [id=" + id + ", name=" + name + ", email=" + email + ", dob=" + dob + ", password=" + password + ", role=" + role + ", age=" + age + "]";
  }
}
