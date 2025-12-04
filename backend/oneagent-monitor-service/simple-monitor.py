#!/usr/bin/env python3
import os
import time
import logging
import requests
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_health_metric(metric_name, dt_api_url, dt_token, namespace, value=1):
    """Send monitor health metrics to Dynatrace"""
    timestamp = int(time.time() * 1000)
    metric_lines = f"{metric_name},namespace={namespace} {value} {timestamp}"
    
    headers = {
        "Authorization": f"Api-Token {dt_token}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    try:
        response = requests.post(dt_api_url, data=metric_lines, headers=headers, verify=False)
        logger.info(f"Health metric {metric_name} sent: {response.status_code}")
        if response.status_code == 202:
            logger.info(f"SUCCESS: {metric_name}")
        else:
            logger.error(f"FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Failed to send health metric {metric_name}: {e}")

def send_heartbeat(dt_api_url, dt_token, namespace):
    """Send heartbeat every 60 seconds"""
    while True:
        try:
            send_health_metric("ho.re.oneagent.monitor.heartbeat", dt_api_url, dt_token, namespace)
            time.sleep(60)
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")
            time.sleep(60)

def main():
    """Main monitoring function"""
    namespace = os.getenv("WATCH_NAMESPACE", "dsa-re-dev")
    dt_api_url = os.getenv("DYNATRACE_METRICS_API_URL")
    dt_token = os.getenv("DYNATRACE_METRICS_TOKEN")
    
    logger.info(f"Starting OneAgent Monitor for namespace: {namespace}")
    logger.info(f"Dynatrace URL: {dt_api_url}")
    
    # Start heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(dt_api_url, dt_token, namespace), daemon=True)
    heartbeat_thread.start()
    
    # Send initial test metrics
    logger.info("Sending initial test metrics...")
    send_health_metric("ho.re.oneagent.monitor.heartbeat", dt_api_url, dt_token, namespace)
    send_health_metric("ho.re.oneagent.monitor.api_failure", dt_api_url, dt_token, namespace)
    send_health_metric("ho.re.oneagent.monitor.stream_stale", dt_api_url, dt_token, namespace)
    
    # Send test uninstrumented pod event
    timestamp = int(time.time() * 1000)
    metric_lines = f"ho.re.oneagent.pod.uninstrumented-Event,pod_name=test-pod,namespace={namespace},event_type=uninstrumented,uninstrumented_type=not_attempted 1 {timestamp}"
    
    headers = {
        "Authorization": f"Api-Token {dt_token}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    try:
        response = requests.post(dt_api_url, data=metric_lines, headers=headers, verify=False)
        logger.info(f"Test uninstrumented event sent: {response.status_code}")
        if response.status_code == 202:
            logger.info("SUCCESS: Test uninstrumented event")
    except Exception as e:
        logger.error(f"Failed to send test event: {e}")
    
    # Keep running
    logger.info("Monitor started successfully - sending heartbeats every 60 seconds")
    while True:
        time.sleep(300)  # Sleep 5 minutes
        logger.info("Monitor still running...")

if __name__ == "__main__":
    main()