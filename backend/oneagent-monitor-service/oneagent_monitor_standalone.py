#!/usr/bin/env python3
import os
import time
import logging
import requests
from kubernetes import client, config, watch
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
        self.uninstrumented_pods = set()

    def send_metric(self, pod_name, namespace, uninstrumented_type):
        """Send uninstrumented pod event to Dynatrace"""
        timestamp = int(time.time() * 1000)
        metric_lines = f"ho.re.oneagent.pod.event,pod_name={pod_name},namespace={namespace},event_type=uninstrumented,uninstrumented_type={uninstrumented_type} 1 {timestamp}"
        
        headers = {
            "Authorization": f"Api-Token {self.dt_token}",
            "Content-Type": "text/plain; charset=utf-8"
        }
        
        try:
            response = requests.post(self.dt_api_url, 
                                   data=metric_lines, headers=headers, verify=False)
            logger.info(f"Event sent for {pod_name}: {response.status_code}")
            if response.status_code == 202:
                logger.info(f"SUCCESS: Uninstrumented pod event sent for {pod_name}")
        except Exception as e:
            logger.error(f"Failed to send event: {e}")

    def check_oneagent_status(self, pod):
        """Check OneAgent status using pod annotations"""
        if pod.status.phase != "Running":
            return None
            
        annotations = pod.metadata.annotations or {}
        
        # Check for OneAgent status annotation
        status = annotations.get("dynatrace.oneagent.status", "not-attempted")
        
        if status == "instrumented":
            return None  # Successfully instrumented
        elif status == "failed":
            error = annotations.get("dynatrace.oneagent.error", "unknown")
            return f"failed_{error}"
        elif status == "attempting":
            return "attempting_instrumentation"
        else:  # not-attempted or any other value
            return "not_attempted"

    def watch_pods(self):
        """Watch pod events for OneAgent failures"""
        logger.info(f"Starting OneAgent monitor for namespace: {self.watch_namespace}")
        
        w = watch.Watch()
        for event in w.stream(self.v1.list_namespaced_pod, namespace=self.watch_namespace):
            pod = event['object']
            event_type = event['type']
            
            if event_type in ['ADDED', 'MODIFIED']:
                status_type = self.check_oneagent_status(pod)
                pod_key = f"{pod.metadata.namespace}/{pod.metadata.name}"
                
                if status_type:
                    if pod_key not in self.uninstrumented_pods:
                        logger.warning(f"Non-instrumented pod detected: {pod.metadata.name} - {status_type}")
                        self.send_metric(pod.metadata.name, pod.metadata.namespace, status_type)
                        self.uninstrumented_pods.add(pod_key)
                else:
                    if pod_key in self.uninstrumented_pods:
                        logger.info(f"Pod now instrumented: {pod.metadata.name}")
                        self.uninstrumented_pods.discard(pod_key)
            
            elif event_type == 'DELETED':
                pod_key = f"{pod.metadata.namespace}/{pod.metadata.name}"
                self.uninstrumented_pods.discard(pod_key)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oneagent-monitor"}

@app.get("/")
async def root():
    return {"message": "OneAgent Monitor Service", "namespace": os.getenv("WATCH_NAMESPACE", "dsa-re-dev")}

@app.on_event("startup")
async def startup_event():
    monitor = OneAgentMonitor()
    monitor_thread = threading.Thread(target=monitor.watch_pods, daemon=True)
    monitor_thread.start()
    logger.info("OneAgent Monitor Service started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)