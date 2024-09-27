package com_example_registration_service.user;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long>{

    // @Query("SELECT s FROM registered_users WHERE s.email = ?1") 
  Optional<User> findUserByEmail(String email);
}
