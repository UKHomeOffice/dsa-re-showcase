#!/usr/bin/env python3
import os
import time
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_test_metrics():
    """Test sending all 5 metrics to Dynatrace"""
    
    dt_api_url = "https://ewo35763.live.dynatrace.com/api/v2/metrics/ingest"
    dt_token = "dt0c01.ST2EY72KQINMH574WMNVI7YN.G3DFPBEJYMODIDAEX454M7YWBUVEFOWKPRVMWFM36SZIRGEIRYMQ"
    namespace = "dsa-re-dev"
    
    timestamp = int(time.time() * 1000)
    
    # Test all 5 metrics
    metrics = [
        f"ho.re.oneagent.pod.uninstrumented-Event,pod_name=test-pod,namespace={namespace},event_type=uninstrumented,uninstrumented_type=not_attempted 1 {timestamp}",
        f"ho.re.oneagent.pods.uninstrumented.gauge,namespace={namespace} 2 {timestamp}",
        f"ho.re.oneagent.monitor.heartbeat,namespace={namespace} 1 {timestamp}",
        f"ho.re.oneagent.monitor.api_failure,namespace={namespace} 1 {timestamp}",
        f"ho.re.oneagent.monitor.stream_stale,namespace={namespace} 1 {timestamp}"
    ]
    
    headers = {
        "Authorization": f"Api-Token {dt_token}",
        "Content-Type": "text/plain; charset=utf-8"
    }
    
    for metric in metrics:
        try:
            response = requests.post(dt_api_url, data=metric, headers=headers, verify=False)
            logger.info(f"Metric sent: {response.status_code} - {metric.split(',')[0]}")
            if response.status_code == 202:
                logger.info(f"SUCCESS: {metric.split(',')[0]}")
            else:
                logger.error(f"FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Failed to send metric: {e}")
        
        time.sleep(1)  # Small delay between metrics

if __name__ == "__main__":
    logger.info("Testing Dynatrace metrics sending...")
    send_test_metrics()
    logger.info("Test completed")