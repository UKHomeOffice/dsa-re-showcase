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
        self.uninstrumented_pods = set()
        self.last_event_time = time.time()
        self.start_heartbeat()

    def send_metric(self, pod_name, namespace, uninstrumented_type):
        """Send uninstrumented pod event to Dynatrace"""
        timestamp = int(time.time() * 1000)
        metric_lines = f"ho.re.oneagent.pod.uninstrumented-Event,pod_name={pod_name},namespace={namespace},event_type=uninstrumented,uninstrumented_type={uninstrumented_type} 1 {timestamp}"
        
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

    def send_health_metric(self, metric_name, value=1):
        """Send monitor health metrics to Dynatrace"""
        timestamp = int(time.time() * 1000)
        metric_lines = f"{metric_name},namespace={self.watch_namespace} {value} {timestamp}"
        
        headers = {
            "Authorization": f"Api-Token {self.dt_token}",
            "Content-Type": "text/plain; charset=utf-8"
        }
        
        try:
            response = requests.post(self.dt_api_url, 
                                   data=metric_lines, headers=headers, verify=False)
            logger.info(f"Health metric {metric_name} sent: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send health metric {metric_name}: {e}")

    def send_heartbeat(self):
        """Send heartbeat every 60 seconds"""
        while True:
            try:
                self.send_health_metric("ho.re.oneagent.monitor.heartbeat")
                time.sleep(60)
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
                time.sleep(60)

    def start_heartbeat(self):
        """Start heartbeat thread"""
        heartbeat_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
        heartbeat_thread.start()

    def check_api_health(self):
        """Test Kubernetes API connectivity"""
        try:
            self.v1.list_namespaced_pod(namespace=self.watch_namespace, limit=1)
            logger.info("Kubernetes API accessible")
            return True
        except Exception as e:
            logger.error(f"Kubernetes API failure: {e}")
            self.send_health_metric("ho.re.oneagent.monitor.api_failure")
            return False

    def check_stream_health(self):
        """Check if watch stream is stale"""
        if time.time() - self.last_event_time > 300:  # 5 minutes
            logger.warning("Watch stream appears stale")
            self.send_health_metric("ho.re.oneagent.monitor.stream_stale")
            return False
        return True

    def send_gauge_metric(self):
        """Send gauge metric with current count of uninstrumented pods"""
        timestamp = int(time.time() * 1000)
        count = len(self.uninstrumented_pods)
        metric_lines = f"ho.re.oneagent.pods.uninstrumented.gauge-count,namespace={self.watch_namespace} {count} {timestamp}"
        
        headers = {
            "Authorization": f"Api-Token {self.dt_token}",
            "Content-Type": "text/plain; charset=utf-8"
        }
        
        try:
            response = requests.post(self.dt_api_url, 
                                   data=metric_lines, headers=headers, verify=False)
            logger.info(f"Gauge metric sent: {count} uninstrumented pods - Status: {response.status_code}")
            if response.status_code == 202:
                logger.info(f"SUCCESS: Gauge metric sent with {count} uninstrumented pods")
        except Exception as e:
            logger.error(f"Failed to send gauge metric: {e}")

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
        
        # Initial API health check
        if not self.check_api_health():
            logger.error("Initial API health check failed")
            return
        
        w = watch.Watch()
        try:
            for event in w.stream(self.v1.list_namespaced_pod, namespace=self.watch_namespace):
                self.last_event_time = time.time()  # Update last event time
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
                            self.send_gauge_metric()
                    else:
                        if pod_key in self.uninstrumented_pods:
                            logger.info(f"Pod now instrumented: {pod.metadata.name}")
                            self.uninstrumented_pods.discard(pod_key)
                            self.send_gauge_metric()
                
                elif event_type == 'DELETED':
                    pod_key = f"{pod.metadata.namespace}/{pod.metadata.name}"
                    self.uninstrumented_pods.discard(pod_key)
        except Exception as e:
            logger.error(f"Watch stream error: {e}")
            self.send_health_metric("ho.re.oneagent.monitor.api_failure")


@app.on_event("startup")
async def startup_event():
    monitor = OneAgentMonitor()
    monitor_thread = threading.Thread(target=monitor.watch_pods, daemon=True)
    monitor_thread.start()
    
    # Start stream health checker
    def check_stream_health():
        while True:
            time.sleep(300)  # Check every 5 minutes
            monitor.check_stream_health()
    
    health_thread = threading.Thread(target=check_stream_health, daemon=True)
    health_thread.start()
    
    logger.info("OneAgent Monitor Service started with health monitoring")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oneagent-monitor"}


@app.get("/")
async def root():
    return {"message": "OneAgent Monitor Service", "namespace": os.getenv("WATCH_NAMESPACE", "dsa-re-dev")}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)