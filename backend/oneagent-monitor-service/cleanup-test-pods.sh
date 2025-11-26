#!/bin/bash

# Cleanup test pods after testing OneAgent monitoring

set -e

NAMESPACE="dsa-re-dev"

echo "Cleaning up test pods..."

# Remove test deployments
kubectl delete deployment uninstrumented-pod -n ${NAMESPACE} --ignore-not-found=true
kubectl delete deployment failed-oneagent-pod -n ${NAMESPACE} --ignore-not-found=true

echo "Test pods cleaned up successfully!"
echo ""
echo "Expected result:"
echo "- dsa.re.oneagent.pods.uninstrumented.gauge should drop to 0"
echo "- No more uninstrumented pod alerts should be generated"