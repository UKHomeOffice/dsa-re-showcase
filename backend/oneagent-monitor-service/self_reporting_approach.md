# Self-Reporting OneAgent Monitoring Approach

## Architecture
```
Pod Init Container → Sets annotation → Pod reports own status → Dynatrace
```

## Implementation

### 1. OneAgent Init Container (Already Working)
- Sets `dynatrace.oneagent.status` annotation
- Values: `attempting`, `instrumented`, `failed`

### 2. Application Sidecar (New)
- Each pod includes a lightweight sidecar container
- Sidecar reads its own pod annotation
- Sends metrics directly to Dynatrace

### 3. Benefits
- **Reliable**: No external API dependencies
- **Scalable**: Works with any number of pods
- **Real-time**: Immediate reporting when status changes
- **Self-contained**: Each pod manages its own reporting

## Sidecar Container Code
```python
import os
import time
import requests
from kubernetes import client, config

def report_own_status():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    
    pod_name = os.getenv("POD_NAME")
    namespace = os.getenv("POD_NAMESPACE")
    
    while True:
        try:
            # Read own pod annotation
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            status = pod.metadata.annotations.get("dynatrace.oneagent.status", "not-attempted")
            
            if status != "instrumented":
                # Send metric to Dynatrace
                send_metric(pod_name, namespace, status)
            
            time.sleep(60)  # Check every minute
        except Exception as e:
            time.sleep(60)
```

## Deployment
- Add sidecar to existing deployments
- Minimal resource usage (10m CPU, 32Mi memory)
- Uses same RBAC as main container