# Preprod Deployment Commands

This document contains the Helm commands to deploy all services to the `dsa-re-preprod` namespace.

## Prerequisites
- Access to ACP preprod cluster
- Helm 3.x installed
- kubectl configured for dsa-re-preprod namespace

## Service Deployments

### 1. Registration Service
```bash
cd backend/registration-service/registration-service-chart
helm upgrade --install registration-service . --values=values-preprod.yaml --namespace dsa-re-preprod
```

### 2. Frontend Service
```bash
cd frontend/frontend-service/frontend-service-chart
helm upgrade --install frontend-service . --values=values-preprod.yaml --namespace dsa-re-preprod
```

### 3. Notification Service
```bash
cd backend/notification-service/notification-service-chart
helm upgrade --install notification-service . --values=values-preprod.yaml --namespace dsa-re-preprod
```

## Monitoring Deployments

### 4. OneAgent Example
```bash
cd monitoring/oneagent-example-chart
helm upgrade --install oneagent-example . --values=values-preprod.yaml --namespace dsa-re-preprod
```

### 5. OneAgent Failure Watcher
```bash
cd monitoring/oneagent-failure-watcher-chart
helm upgrade --install oneagent-failure-watcher . --values=values-preprod.yaml --namespace dsa-re-preprod
```

## Verification Commands

### Check all pods are running
```bash
kubectl get pods -n dsa-re-preprod
```

### Check services
```bash
kubectl get svc -n dsa-re-preprod
```

### Check Helm releases
```bash
helm list -n dsa-re-preprod
```

## Pipeline Integration

These commands can be integrated into CI/CD pipelines for automated deployments to preprod and production environments.

### Example Pipeline Stage
```yaml
deploy-preprod:
  stage: deploy
  script:
    - helm upgrade --install registration-service backend/registration-service/registration-service-chart --values=backend/registration-service/registration-service-chart/values-preprod.yaml --namespace dsa-re-preprod
    - helm upgrade --install frontend-service frontend/frontend-service/frontend-service-chart --values=frontend/frontend-service/frontend-service-chart/values-preprod.yaml --namespace dsa-re-preprod
    - helm upgrade --install notification-service backend/notification-service/notification-service-chart --values=backend/notification-service/notification-service-chart/values-preprod.yaml --namespace dsa-re-preprod
    - helm upgrade --install oneagent-example monitoring/oneagent-example-chart --values=monitoring/oneagent-example-chart/values-preprod.yaml --namespace dsa-re-preprod
    - helm upgrade --install oneagent-failure-watcher monitoring/oneagent-failure-watcher-chart --values=monitoring/oneagent-failure-watcher-chart/values-preprod.yaml --namespace dsa-re-preprod
```