package com_example_registration_service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class RegistrationProducer {

    private final KafkaTemplate<String, String> kafkaTemplate;

    // Inject kafka-topics
    @Value("${spring.kafka.topic.user-login}")
    private String loginTopic;

    @Value("${spring.kafka.topic.user-registration}")
    private String registrationTopic;

    public RegistrationProducer(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendLoginMessage(String message) {
        kafkaTemplate.send(loginTopic, message);
        System.out.println("Login message sent to Kafka: " + message);
    }

    public void sendRegistrationMessage(String message) {
        kafkaTemplate.send(registrationTopic, message);
        System.out.println("Registration message sent to Kafka: " + message);
    }
}
