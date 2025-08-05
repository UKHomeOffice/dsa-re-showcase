import json
import logging
import asyncio
from datetime import datetime
from kafka import KafkaConsumer
from ssl import create_default_context
from db import increment_login_count
from custom_metric import login_event_counter
import os

# Configure logging
log_file_path = os.getenv('LOG_FILE_PATH', '/var/log/notification_service.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = logging.getLogger(__name__)

async def start_consumer(bootstrap_servers, topic, group_id, recent_logins, max_logins, sdk=None):
    """Start consuming login events from Kafka"""
    logger.info(f"Starting Kafka consumer: {bootstrap_servers}, topic: {topic}, group: {group_id}")
    
    # Certificate info
    cert_path = os.getenv('KAFKA_CERT_PATH', '/etc/kafka-certs')
    cert_file = os.path.join(cert_path, 'leaf-cert.pem')
    key_file = os.path.join(cert_path, 'leaf-key.pem')
    ca_file = os.path.join(cert_path, 'root-cert.pem')
    
    logger.info(f"Using certificates at: {cert_path}")
    
    try:
        # Create SSL context for mTLS
        ssl_context = create_default_context()
        ssl_context.load_cert_chain(cert_file, key_file)
        ssl_context.load_verify_locations(ca_file)
        
        # Create a Kafka consumer
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers, 
            group_id=group_id,
            security_protocol='SSL',
            ssl_context=ssl_context,
            session_timeout_ms=60000,
            heartbeat_interval_ms=20000
        )
        
        logger.info("Kafka consumer initialized, waiting for messages...")
        
        # Process messages asynchronously
        while True:
            try:
                for message in consumer:
                    raw = message.value.decode('utf-8').strip()
                    logger.info(f"Raw login message: {raw}")
                    
                    # Increment the total_count in the database
                    increment_login_count()
                    
                    # Increment the custom metric
                    login_event_counter.add(1, {"event_type": "login"})
                    
                    if not sdk:
                        logger.warning("Dynatrace SDK not initialized. Skipping tracing for this message.")
                    
                    if sdk:
                        with sdk.trace_custom_service('Process Kafka Login Message', 'notification-service'):
                            sdk.add_custom_request_attribute('kafka.topic', message.topic)
                            sdk.add_custom_request_attribute('kafka.partition', message.partition)
                            sdk.add_custom_request_attribute('kafka.offset', message.offset)
                            sdk.add_custom_request_attribute('kafka.key', str(message.key))
                    
                    # Process the message (e.g., update recent_logins)
                    parts = raw.split(", ")
                    if len(parts) == 3 and "User logged in: " in parts[0]:
                        name = parts[0].split("User logged in: ")[1].strip()
                        email = parts[1].strip()
                        timestamp = parts[2].strip()
                        
                        logger.info(f"Login detected: {name} ({email}) at {timestamp}")
                        logger.info(f"Notification sent to {email}")
                        
                        # Add the login event to recent_logins
                        login_event = {
                            "name": name,
                            "email": email,
                            "timestamp": timestamp
                        }
                        recent_logins.insert(0, login_event)
                        if len(recent_logins) > max_logins:
                            recent_logins = recent_logins[:max_logins]
            except Exception as e:
                logger.error(f"Error processing Kafka message: {e}")
                await asyncio.sleep(1)  # Prevent tight retry loops
    except Exception as e:
        logger.error(f"Error initializing Kafka consumer: {e}")
        raise