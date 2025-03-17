package com_example_registration_service;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Service;

@Service
public class CustomMetricService {

  private final Counter customApiCounter;

  public CustomMetricService(MeterRegistry registry) {
    this.customApiCounter = Counter.builder("custom_test.oneagent.api.calls")
      .description("Test counter for OneAgent API integration")
      .tag("test", "oneagent")
      .register(registry);
  }

  public void incrementCustomCounter() {
    customApiCounter.increment();
  }
}