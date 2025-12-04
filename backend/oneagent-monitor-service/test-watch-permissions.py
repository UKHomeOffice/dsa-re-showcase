#!/usr/bin/env python3
import os
import time
from kubernetes import client, config, watch

def test_watch_permissions():
    """Test if we can watch pods"""
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    
    v1 = client.CoreV1Api()
    namespace = os.getenv('WATCH_NAMESPACE', 'dsa-re-dev')
    
    print(f"Testing watch permissions in namespace: {namespace}")
    
    try:
        w = watch.Watch()
        print("Starting watch for 10 seconds...")
        
        count = 0
        for event in w.stream(v1.list_namespaced_pod, namespace=namespace, timeout_seconds=10):
            count += 1
            event_type = event['type']
            pod_name = event['object'].metadata.name
            print(f"  {event_type}: {pod_name}")
            
            if count >= 5:  # Limit output
                break
                
        print(f"✓ SUCCESS: Watch worked - received {count} events")
        
    except Exception as e:
        print(f"✗ FAILED: Cannot watch pods - {e}")

if __name__ == "__main__":
    test_watch_permissions()