# OneAgent Monitor Service

A dedicated monitoring service that watches for Dynatrace OneAgent failures in Kubernetes pods and sends custom metrics to Dynatrace for alerting.

## Features

- **Real-time Pod Monitoring** - Watches pod events for OneAgent init container failures
- **Dynatrace Integration** - Sends custom metrics to Dynatrace for alerting
- **Namespace Scoped** - Monitors specific namespace (default: dsa-re-dev)
- **FastAPI Health Endpoints** - Provides health checks and status endpoints

## Deployment

### Prerequisites
- Kubernetes cluster with RBAC permissions for pod watching
- Existing Dynatrace secrets for metrics ingestion
- Service account with pod list/watch permissions

### Deploy to dsa-re-dev
```bash
cd oneagent-monitor-chart
helm upgrade --install oneagent-monitor . \
  --values=values-dev.yaml \
  --namespace dsa-re-dev
```

## Configuration

### Environment Variables
- `WATCH_NAMESPACE` - Kubernetes namespace to monitor (default: dsa-re-dev)
- `DYNATRACE_METRICS_TOKEN` - Dynatrace API token for metrics ingestion
- `DYNATRACE_METRICS_API_URL` - Dynatrace metrics API endpoint

### Service Account
Uses the `default` service account with existing `default-sa-role` RoleBinding that provides:
- Pod list/watch permissions via `dsa-pod-patch` ClusterRole

## Metrics

### Custom Metric: `dsa.re.oneagent.pod.uninstrumented`
- **Type**: Counter (sent when uninstrumented pod detected)

### Gauge Metric: `dsa.re.oneagent.pods.uninstrumented.gauge`
- **Type**: Gauge (current count of uninstrumented pods)
- **Frequency**: Every 60 seconds
- **Dimensions**: `namespace`
- **Type**: Counter
- **Dimensions**: 
  - `pod_name` - Name of the uninstrumented pod
  - `namespace` - Kubernetes namespace
  - `uninstrumented_type` - Type of instrumentation issue detected

### Uninstrumented Types Detected
- `no_oneagent_init_container` - Pod has no OneAgent init container configured
- `oneagent_download_failed` - OneAgent init container failed (non-zero exit code)
- `oneagent_init_error` - OneAgent init container in error/waiting state

## Endpoints

- `GET /` - Service information
- `GET /health` - Health check endpoint

## Architecture

```
Kubernetes Pod Events → OneAgent Monitor → Dynatrace Metrics → Alerts
```

The service runs as a single pod deployment that continuously watches for pod events in the specified namespace and sends failure metrics to Dynatrace when OneAgent issues are detected.