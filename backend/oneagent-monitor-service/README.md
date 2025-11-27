# OneAgent Monitor Service

A Kubernetes service that monitors pods for OneAgent instrumentation compliance and sends real-time metrics to Dynatrace.

## Overview

This service automatically detects uninstrumented pods in your namespace and sends alerts to Dynatrace when:
- Pods are missing OneAgent init containers
- OneAgent init containers fail to execute
- OneAgent download or installation errors occur

## Features

- **Real-time Detection**: Uses Kubernetes Watch API for instant pod event monitoring
- **Dynatrace Integration**: Sends custom metrics via Dynatrace Metrics API
- **Zero Configuration**: Automatic detection with no pod modifications required
- **Scalable**: Single pod monitors entire namespace efficiently
- **Self-Service**: Deploy in your own namespace with full control

## Quick Start

### Prerequisites
- Kubernetes cluster access
- Helm 3.x installed
- Dynatrace credentials (API URL and token)
- Existing `dsa-pod-patch` ClusterRole access

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/UKHomeOffice/dsa-re-showcase.git
cd dsa-re-showcase/backend/oneagent-monitor-service
```

2. **Deploy to your namespace:**
```bash
helm install oneagent-monitor ./oneagent-monitor-chart \
  --set environment.watchNamespace=YOUR_NAMESPACE \
  --namespace YOUR_NAMESPACE
```

3. **Verify deployment:**
```bash
kubectl get pods -l app.kubernetes.io/name=oneagent-monitor-chart -n YOUR_NAMESPACE
kubectl logs -l app.kubernetes.io/name=oneagent-monitor-chart -n YOUR_NAMESPACE
```

### Configuration

#### Required Settings
```bash
# Replace YOUR_NAMESPACE with your actual namespace
helm install oneagent-monitor ./oneagent-monitor-chart \
  --set environment.watchNamespace=YOUR_NAMESPACE \
  --namespace YOUR_NAMESPACE
```

#### Optional Customization
```bash
# Custom Dynatrace credentials
helm install oneagent-monitor ./oneagent-monitor-chart \
  --set environment.watchNamespace=YOUR_NAMESPACE \
  --set dynatrace.secretName=your-dynatrace-secret \
  --namespace YOUR_NAMESPACE
```

## What Gets Created

The Helm chart automatically creates:
- ✅ **Deployment**: OneAgent monitor service pod
- ✅ **RoleBinding**: Links your service account to `dsa-pod-patch` ClusterRole
- ✅ **NetworkPolicy**: Allows egress to Dynatrace namespace
- ✅ **Service**: Health check endpoints

## Metrics Sent to Dynatrace

### Counter Metric
- **Name**: `ho.re.oneagent.pod.uninstrumented`
- **Type**: Counter (increments for each uninstrumented pod)
- **Dimensions**: `pod_name`, `namespace`, `uninstrumented_type`

### Gauge Metric  
- **Name**: `ho.re.oneagent.pods.uninstrumented.gauge`
- **Type**: Gauge (current count of uninstrumented pods)
- **Dimensions**: `namespace`

## Uninstrumented Pod Types

The service detects these scenarios:
- `no_oneagent_init_container`: Pod has no OneAgent init container
- `oneagent_download_failed`: OneAgent init container failed (exit code != 0)
- `oneagent_init_error`: OneAgent init container in error state

## CI/CD Integration

### Jenkins Pipeline
```groovy
stage('Deploy OneAgent Monitor') {
    steps {
        sh """
            helm upgrade --install oneagent-monitor ./oneagent-monitor-chart \\
              --set environment.watchNamespace=${NAMESPACE} \\
              --namespace ${NAMESPACE} \\
              --wait
        """
    }
}
```

### GitHub Actions
```yaml
- name: Deploy OneAgent Monitor
  run: |
    helm upgrade --install oneagent-monitor ./oneagent-monitor-chart \
      --set environment.watchNamespace=${{ vars.NAMESPACE }} \
      --namespace ${{ vars.NAMESPACE }} \
      --wait
```

### ArgoCD
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: oneagent-monitor
spec:
  source:
    repoURL: https://github.com/UKHomeOffice/dsa-re-showcase.git
    path: backend/oneagent-monitor-service/oneagent-monitor-chart
    helm:
      parameters:
      - name: environment.watchNamespace
        value: "your-namespace"
```

## Troubleshooting

### Check Service Status
```bash
kubectl get pods -l app.kubernetes.io/name=oneagent-monitor-chart -n YOUR_NAMESPACE
kubectl logs -l app.kubernetes.io/name=oneagent-monitor-chart -n YOUR_NAMESPACE --tail=20
```

### Verify RBAC Permissions
```bash
kubectl get rolebinding -n YOUR_NAMESPACE | grep oneagent-monitor
kubectl describe rolebinding oneagent-monitor-oneagent-monitor-chart-rbac -n YOUR_NAMESPACE
```

### Test Dynatrace Connectivity
```bash
kubectl exec -n YOUR_NAMESPACE deployment/oneagent-monitor-oneagent-monitor-chart -- \
  curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Api-Token YOUR_TOKEN" \
  -H "Content-Type: text/plain" \
  -d "test.metric 1 $(date +%s)000" \
  YOUR_DYNATRACE_URL
```

### Common Issues

**Pod CrashLoopBackOff**: Check Dynatrace credentials in secret
**No metrics in Dynatrace**: Verify network policy allows egress to dynatrace namespace
**Permission denied**: Ensure RoleBinding was created successfully

## Health Endpoints

- **Health Check**: `GET /health`
- **Service Info**: `GET /`

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review pod logs for error messages
3. Contact RE Team for Dynatrace credential issues
4. Raise issues in the GitHub repository

## License

This project is licensed under the MIT License.