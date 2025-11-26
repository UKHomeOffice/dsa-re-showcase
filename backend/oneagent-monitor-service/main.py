import os
import time
import logging
import requests
from kubernetes import client, config, watch
from datetime import datetime
import threading
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OneAgent Monitor Service")

class OneAgentMonitor:
    def __init__(self):
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        
        self.v1 = client.CoreV1Api()
        self.watch_namespace = os.getenv("WATCH_NAMESPACE", "dsa-re-dev")
        self.dt_api_url = os.getenv("DYNATRACE_METRICS_API_URL")
        self.dt_token = os.getenv("DYNATRACE_METRICS_TOKEN")
        
    def send_metric(self, pod_name, namespace, failure_type):
        """Send failure metric to Dynatrace"""
        metric_data = {
            "displayName": "OneAgent Pod Failures",
            "unit": "Count",
            "dimensions": ["pod_name", "namespace", "failure_type"],
            "series": [{
                "metricKey": "dsa.re.oneagent.pod.failure",
                "dataPoints": [{
                    "timestamp": int(time.time() * 1000),
                    "value": 1,
                    "dimensions": {
                        "pod_name": pod_name,
                        "namespace": namespace,
                        "failure_type": failure_type
                    }
                }]
            }]
        }
        
        headers = {
            "Authorization": f"Api-Token {self.dt_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(f"{self.dt_api_url}/v2/metrics/ingest", 
                                   json=metric_data, headers=headers)
            logger.info(f"Metric sent for {pod_name}: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send metric: {e}")

    def check_oneagent_failure(self, pod):
        """Check if pod has OneAgent failure"""
        if not pod.spec.init_containers:
            return None
            
        for init_container in pod.spec.init_containers:
            if "oneagent" in init_container.name.lower():
                if pod.status.init_container_statuses:
                    for status in pod.status.init_container_statuses:
                        if status.name == init_container.name:
                            if status.state.terminated and status.state.terminated.exit_code != 0:
                                return "init_container_failed"
                            if status.state.waiting and "Error" in str(status.state.waiting.reason):
                                return "init_container_error"
        return None

    def watch_pods(self):
        """Watch pod events for OneAgent failures"""
        logger.info(f"Starting OneAgent monitor for namespace: {self.watch_namespace}")
        
        w = watch.Watch()
        for event in w.stream(self.v1.list_namespaced_pod, namespace=self.watch_namespace):
            pod = event['object']
            event_type = event['type']
            
            if event_type in ['ADDED', 'MODIFIED']:
                failure_type = self.check_oneagent_failure(pod)
                if failure_type:
                    logger.warning(f"OneAgent failure detected: {pod.metadata.name} - {failure_type}")
                    self.send_metric(pod.metadata.name, pod.metadata.namespace, failure_type)

@app.on_event("startup")
async def startup_event():
    monitor = OneAgentMonitor()
    monitor_thread = threading.Thread(target=monitor.watch_pods, daemon=True)
    monitor_thread.start()
    logger.info("OneAgent Monitor Service started")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oneagent-monitor"}

@app.get("/")
async def root():
    return {"message": "OneAgent Monitor Service", "namespace": os.getenv("WATCH_NAMESPACE", "dsa-re-dev")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)