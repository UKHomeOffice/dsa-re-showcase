#!/bin/bash

# Deploy all services to preprod namespace
set -e

echo "Deploying all services to dsa-re-preprod namespace..."

# Deploy Frontend Service
echo "Deploying frontend-service..."
cd /home/d-johnsok4/dsa-re-showcase/frontend/frontend-service/frontend-service-chart
helm upgrade --install frontend-service . --values=values-preprod.yaml --namespace dsa-re-preprod

# Deploy Notification Service  
echo "Deploying notification-service..."
cd /home/d-johnsok4/dsa-re-showcase/backend/notification-service/notification-service-chart
helm upgrade --install notification-service . --values=values-preprod.yaml --namespace dsa-re-preprod

# Deploy Registration Service (already deployed but ensure it's up to date)
echo "Updating registration-service..."
cd /home/d-johnsok4/dsa-re-showcase/backend/registration-service/registration-service-chart
helm upgrade --install registration-service . --values=values-preprod.yaml --namespace dsa-re-preprod

echo "All services deployed successfully!"
echo "Check status with: kubectl get pods -n dsa-re-preprod"