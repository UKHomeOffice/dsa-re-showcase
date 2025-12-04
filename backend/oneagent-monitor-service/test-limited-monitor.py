#!/usr/bin/env python3
import os
import time
from kubernetes import client, config

def test_current_permissions():
    """Test what we can do with current permissions"""
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    
    v1 = client.CoreV1Api()
    namespace = os.getenv('WATCH_NAMESPACE', 'dsa-re-dev')
    
    print(f"Testing permissions in namespace: {namespace}")
    
    # Test list pods (should fail)
    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        print(f"✓ SUCCESS: Can list pods - found {len(pods.items)} pods")
        for pod in pods.items:
            print(f"  - {pod.metadata.name}")
    except Exception as e:
        print(f"✗ FAILED: Cannot list pods - {e}")
    
    # Test get specific pod (should work)
    try:
        pod = v1.read_namespaced_pod(name="test-uninstrumented-pod", namespace=namespace)
        print(f"✓ SUCCESS: Can get specific pod - {pod.metadata.name}")
        
        # Check annotations
        annotations = pod.metadata.annotations or {}
        oneagent_status = annotations.get('dynatrace.com/oneagent-status', 'unknown')
        print(f"  OneAgent status: {oneagent_status}")
        
    except Exception as e:
        print(f"✗ FAILED: Cannot get specific pod - {e}")

if __name__ == "__main__":
    test_current_permissions()