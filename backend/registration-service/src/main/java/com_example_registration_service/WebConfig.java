// package com_example_registration_service;

// import org.springframework.context.annotation.Configuration;
// import org.springframework.web.servlet.config.annotation.CorsRegistry;
// import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

// @Configuration
// public class WebConfig implements WebMvcConfigurer {

//   @Override
//   public void addCorsMappings(CorsRegistry registry) {
//       registry.addMapping("/**")
//               .allowedOrigins("http://frontend-service.dev.dsa-re-notprod.homeoffice.gov.uk, http://registration-service.dev.dsa-re-dev.homeoffice.gov.uk") // Replace with your React app URL
//               .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
//               .allowedHeaders("*")
//               .allowCredentials(true);
//   }
// }