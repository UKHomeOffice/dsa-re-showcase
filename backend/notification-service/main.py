from fastapi import FastAPI
import logging
import os
from datetime import datetime
import asyncio
from kafka_consumer import start_consumer
import oneagent
import oneagent.sdk
from db import initialize_db, test_db_connection


# Centralized logger configuration
logging.basicConfig(
    filename="/var/log/notification_service.log",  # Path to the log file
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)

logger = logging.getLogger(__name__)

# Initialize the database
try:
    logger.info("Starting database initialization...")
    initialize_db()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing the database: {e}")
    raise

# Test the database connection
try:
    logger.info("Starting database connection test...")
    test_db_connection()
    logger.info("Database connection test successful.")
except Exception as e:
    logger.error(f"Database connection test failed: {e}")
    raise

oneagent_init = oneagent.initialize()
if not oneagent_init:
  logger.warning('Error initializing OneAgent SDK.')
else:
  logger.info('Dynatrace SDK successfully initialized.')
  
sdk = oneagent.get_sdk()
if not sdk:
  logger.warning('Error: OneAgent SDK failed to instantiate.')
else:
  logger.info('OneAgent SDK successfully instantiated.')

# create FastAPI app
app =FastAPI(title="Notification Service") 

# Basic in memory storage for logins
recent_logins = []
MAX_STORED_LOGINS = 20

# Kafka Config
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS', 'localhost:9092')
KAFKA_TOPIC= os.getenv('KAFKA_TOPIC', 'user-login')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'notification-service')

@app.get("/health")
def health():
  return {"status": "ok", "service": "notification-service"}

@app.get("/recent-logins")
def get_recent_logins():
  return {"logins": recent_logins}

@app.post("/simulate-login")
def simulate_login(email: str = "user@example.com"):
  """Simulate login for testing..."""
  
  global recent_logins
  
  # Create a login event
  login_event = {
    "email": email,
    "timestamp": datetime.now().isoformat(),
    "event_type": "login"
    }
  
  logger.info(f"Simulated login event: {login_event}")
  
  # Simulate sendign a notification
  logger.info(f"Notification sent to {email}")
  
  # store login event and trim the event list if max is exceeded
  recent_logins.insert(0, login_event)
  
  if len(recent_logins) > MAX_STORED_LOGINS:
    recent_logins = recent_logins[:MAX_STORED_LOGINS]
    
  return {"status": "success", "message": f"Login simulated for {email}"}

@app.on_event("startup")
async def startup_event():
    """Start Kafka consumer on startup"""
    logger.info("Starting application startup tasks...")
    # try:
    #     asyncio.create_task(
    #         start_consumer(
    #             bootstrap_servers=KAFKA_SERVERS, 
    #             topic=KAFKA_TOPIC, 
    #             group_id=KAFKA_GROUP_ID, 
    #             recent_logins=recent_logins, 
    #             max_logins=MAX_STORED_LOGINS, 
    #             sdk=sdk,
    #         )
    #     )
    logger.info("Kafka consumer task started successfully.")
    # except Exception as e:
    #     logger.error(f"Error during startup: {e}")

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)