#!/bin/bash

# Deploy Showcase Services to Preprod Environment
# This script deploys all services to dsa-re-preprod namespace with Dynatrace production metrics

set -e

NAMESPACE="dsa-re-preprod"

echo "Deploying Showcase Services to ${NAMESPACE} environment..."

# Create namespace if it doesn't exist
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Deploy Registration Service
echo "Deploying Registration Service..."
cd backend/registration-service/registration-service-chart
helm upgrade --install registration-service . \
  --values=values-preprod.yaml \
  --namespace ${NAMESPACE} \
  --wait

# Deploy Notification Service
echo "Deploying Notification Service..."
cd ../../../backend/notification-service/notification-service-chart
helm upgrade --install notification-service . \
  --values=values-preprod.yaml \
  --namespace ${NAMESPACE} \
  --wait

# Deploy Frontend Service
echo "Deploying Frontend Service..."
cd ../../../frontend/frontend-service/frontend-service-chart
helm upgrade --install frontend-service . \
  --values=values-preprod.yaml \
  --namespace ${NAMESPACE} \
  --wait

# Deploy CronJob
echo "Deploying CronJob..."
cd ../../../
kubectl apply -f k8s/msk-cronjob-preprod.yaml

echo "Preprod deployment completed successfully!"
echo "Services are now pushing metrics to Dynatrace Production environment."
echo ""
echo "Access the application at:"
echo "http://frontend-service.preprod.dsa-re-notprod.homeoffice.gov.uk/"