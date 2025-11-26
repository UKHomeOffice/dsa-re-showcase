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
        self.uninstrumented_pods = set()  # Track uninstrumented pods
        
    def send_metric(self, pod_name, namespace, uninstrumented_type):
        """Send uninstrumented pod metric to Dynatrace"""
        metric_data = {
            "displayName": "Uninstrumented Pods",
            "unit": "Count",
            "dimensions": ["pod_name", "namespace", "uninstrumented_type"],
            "series": [{
                "metricKey": "dsa.re.oneagent.pod.uninstrumented",
                "dataPoints": [{
                    "timestamp": int(time.time() * 1000),
                    "value": 1,
                    "dimensions": {
                        "pod_name": pod_name,
                        "namespace": namespace,
                        "uninstrumented_type": uninstrumented_type
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
    
    def send_gauge_metric(self):
        """Send gauge metric with current count of uninstrumented pods"""
        metric_data = {
            "displayName": "Uninstrumented Pods Gauge",
            "unit": "Count",
            "dimensions": ["namespace"],
            "series": [{
                "metricKey": "dsa.re.oneagent.pods.uninstrumented.gauge",
                "dataPoints": [{
                    "timestamp": int(time.time() * 1000),
                    "value": len(self.uninstrumented_pods),
                    "dimensions": {
                        "namespace": self.watch_namespace
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
            logger.info(f"Gauge metric sent: {len(self.uninstrumented_pods)} uninstrumented pods")
        except Exception as e:
            logger.error(f"Failed to send gauge metric: {e}")

    def check_oneagent_uninstrumented(self, pod):
        """Check if pod is running but OneAgent is not properly installed"""
        # Skip if pod is not running
        if pod.status.phase != "Running":
            return None
            
        # Check if pod has OneAgent init container configured
        has_oneagent_init = False
        if pod.spec.init_containers:
            for init_container in pod.spec.init_containers:
                if "oneagent" in init_container.name.lower():
                    has_oneagent_init = True
                    break
        
        # If no OneAgent init container, pod is uninstrumented
        if not has_oneagent_init:
            return "no_oneagent_init_container"
            
        # Check if OneAgent init container failed
        if pod.status.init_container_statuses:
            for status in pod.status.init_container_statuses:
                if "oneagent" in status.name.lower():
                    if status.state.terminated and status.state.terminated.exit_code != 0:
                        return "oneagent_download_failed"
                    if status.state.waiting and "Error" in str(status.state.waiting.reason):
                        return "oneagent_init_error"
        
        # Check if OneAgent files exist in running container
        # This would require exec into container - for now we assume if init succeeded, OneAgent is present
        # Could be enhanced to check for LD_PRELOAD env var or OneAgent files
        
        return None

    def watch_pods(self):
        """Watch pod events for OneAgent failures"""
        logger.info(f"Starting OneAgent monitor for namespace: {self.watch_namespace}")
        
        w = watch.Watch()
        for event in w.stream(self.v1.list_namespaced_pod, namespace=self.watch_namespace):
            pod = event['object']
            event_type = event['type']
            
            if event_type in ['ADDED', 'MODIFIED']:
                uninstrumented_type = self.check_oneagent_uninstrumented(pod)
                pod_key = f"{pod.metadata.namespace}/{pod.metadata.name}"
                
                if uninstrumented_type:
                    if pod_key not in self.uninstrumented_pods:
                        logger.warning(f"Uninstrumented pod detected: {pod.metadata.name} - {uninstrumented_type}")
                        self.send_metric(pod.metadata.name, pod.metadata.namespace, uninstrumented_type)
                        self.uninstrumented_pods.add(pod_key)
                else:
                    # Pod is properly instrumented, remove from tracking
                    self.uninstrumented_pods.discard(pod_key)
            
            elif event_type == 'DELETED':
                pod_key = f"{pod.metadata.namespace}/{pod.metadata.name}"
                self.uninstrumented_pods.discard(pod_key)

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