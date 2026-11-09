import json
import logging
import asyncio
from contextlib import nullcontext
from datetime import datetime
from kafka import KafkaConsumer
from ssl import create_default_context
from db import increment_login_count
from custom_metric import login_event_counter
from otel_config import METRIC_ATTRIBUTES
from opensearch_sink import index_login_event
import os

logger = logging.getLogger(__name__)

async def start_consumer(bootstrap_servers, topic, group_id, recent_logins, max_logins, sdk=None):
  """Start consuming login events from kafka"""
  logging.info(f"Starting Kafka consumer: {bootstrap_servers}, topic: {topic}, group: {group_id}")
  
  # Certificate info
  cert_path = os.getenv('KAFKA_CERT_PATH', '/etc/kafka-certs')
  cert_file = os.path.join(cert_path, 'leaf-cert.pem')
  key_file = os.path.join(cert_path, 'leaf-key.pem')
  ca_file = os.path.join(cert_path, 'root-cert.pem')
  
  logger.info(f"Using certificates at: {cert_path}")
  
  while True:
    try:
      # Create SSL context for mTLS
      ssl_context = create_default_context()
      ssl_context.load_cert_chain(cert_file, key_file)
      ssl_context.load_verify_locations(ca_file)
      
      # Create a kafka consumer
      consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers, 
        group_id=group_id,
        security_protocol='SSL',
        ssl_context=ssl_context,
        enable_auto_commit=False,
        session_timeout_ms=60000,
        heartbeat_interval_ms=20000
      )
      
      logger.info("Kafka consumer initialised, waiting for messages...")
      # Increment the total_count in the database
      increment_login_count()
      
      # Process messages
      for message in consumer:
        try:
            raw = message.value.decode('utf-8').strip()
            logging.info(f"Raw login message: {raw}")

            trace_context = (
                sdk.trace_custom_service('Process Kafka Login Message', 'notification-service')
                if sdk else nullcontext()
            )
            if not sdk:
                logging.warning("Dynatrace SDK not initialized. Processing without custom tracing.")

            with trace_context:
                if sdk:
                    sdk.add_custom_request_attribute('kafka.topic', message.topic)
                    sdk.add_custom_request_attribute('kafka.partition', message.partition)
                    sdk.add_custom_request_attribute('kafka.offset', message.offset)
                    sdk.add_custom_request_attribute('kafka.key', str(message.key))

                parts = raw.split(", ")
                if len(parts) == 3 and "User logged in: " in parts[0]:
                    name = parts[0].split("User logged in: ")[1].strip()
                    email = parts[1].strip()
                    timestamp = parts[2].strip()

                    logging.info(f"Login detected: {name} ({email}) at {timestamp}")
                    logging.info(f"Notification sent to {email}")

                    login_event = {
                        "event_type": "login",
                        "name": name,
                        "email": email,
                        "timestamp": timestamp,
                        "kafka": {
                            "topic": message.topic,
                            "partition": message.partition,
                            "offset": message.offset,
                        },
                    }
                    opensearch_document = {
                        "event_type": "login",
                        "timestamp": timestamp,
                        "kafka": login_event["kafka"],
                    }
                    index_login_event(
                        opensearch_document, message.topic, message.partition, message.offset
                    )

                    recent_logins.insert(0, login_event)
                    if len(recent_logins) > max_logins:
                        recent_logins = recent_logins[:max_logins]

                    login_event_counter.add(1, {"event_type": "login", **METRIC_ATTRIBUTES})
                    logging.info("Custom metric 'login_event_counter' incremented by 1.")
                    increment_login_count()
                else:
                    logging.warning("Unexpected message format. Skipping.")

            consumer.commit()

        except Exception as e:
                        logging.error(f"Error processing message; it will be retried: {e}")
                        consumer.close()
                        await asyncio.sleep(5)
                        break
    except Exception as e:
      logger.error(f"Kafka connection error: {e}")
      await asyncio.sleep(5)  