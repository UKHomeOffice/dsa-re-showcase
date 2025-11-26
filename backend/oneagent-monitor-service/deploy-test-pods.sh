#!/bin/bash

# Deploy test pods to trigger OneAgent monitoring alerts
# Run this after deploying the OneAgent monitor service

set -e

NAMESPACE="dsa-re-dev"

echo "Deploying test pods to trigger OneAgent monitoring..."

# Deploy uninstrumented pod (no OneAgent at all)
echo "1. Deploying uninstrumented pod..."
kubectl apply -f test-uninstrumented-pod.yaml

# Deploy failed OneAgent pod (OneAgent init fails)
echo "2. Deploying failed OneAgent pod..."
kubectl apply -f test-failed-oneagent-pod.yaml

echo ""
echo "Test pods deployed successfully!"
echo ""
echo "Expected metrics to be sent:"
echo "- dsa.re.oneagent.pod.uninstrumented (counter) - for both pods"
echo "- dsa.re.oneagent.pods.uninstrumented.gauge (gauge) - count = 2"
echo ""
echo "Check pod status:"
echo "kubectl get pods -n ${NAMESPACE} -l app=uninstrumented-pod"
echo "kubectl get pods -n ${NAMESPACE} -l app=failed-oneagent-pod"
echo ""
echo "Check OneAgent monitor logs:"
echo "kubectl logs -n ${NAMESPACE} -l app.kubernetes.io/name=oneagent-monitor-chart -f"