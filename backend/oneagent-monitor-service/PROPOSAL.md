# Pod-Level Alerting via Dynatrace OneAgent Monitoring Service

## Background

As part of ongoing efforts to improve observability across ACP-managed Kubernetes clusters, several product teams require real-time monitoring of pod instrumentation compliance. This addresses scenarios where workloads are dynamically deployed and may lack proper Dynatrace OneAgent instrumentation.

The challenge lies in enabling automated detection of uninstrumented workloads and generating immediate compliance alerts, capable of discovering instrumentation failures based on runtime analysis.

## Proposed Solution

The DSA SRE team has developed a OneAgent monitoring service that continuously watches for pod creation and modification events, automatically detecting uninstrumented workloads and sending real-time metrics to Dynatrace for alerting. The solution leverages Kubernetes Watch API for instant detection, eliminating polling overhead whilst providing immediate visibility into instrumentation compliance.

The DSA SRE team will provide the complete code package to product teams for deployment.

## Product Team Implementation Options

### Option 1: Deploy via Helm Chart (Recommended)

**Product Team Prerequisites:**
1. Raise ACP request to grant your Service Account permission to bind the `dsa-pod-patch` ClusterRole
2. Obtain Dynatrace metrics API token from DSA SRE team

**Product Team Deployment Steps:**
```bash
helm install oneagent-monitor ./oneagent-monitor-chart \
  --set environment.watchNamespace=YOUR_NAMESPACE \
  --namespace YOUR_NAMESPACE
```

**Benefits:**
- Ready-to-use solution with automated RBAC setup
- Network policies included
- Self-service deployment
- Minimal configuration required

### Option 2: Integrate Code into Your Pipeline

**Product Team Prerequisites:**
1. Raise ACP request to grant your Service Account permission to bind the `dsa-pod-patch` ClusterRole
2. Copy monitoring code from DSA SRE repository
3. Add Kubernetes client dependencies to your project

**Product Team Implementation Steps:**
- Copy the provided monitoring code from DSA SRE team
- Add the code to your existing application or create new service
- Configure environment variables for your namespace and Dynatrace API
- Deploy using your current CI/CD pipeline

**Benefits:**
- Full control over deployment and customisation
- Integration with existing infrastructure
- Ability to modify monitoring logic for specific requirements

## Required Permissions

Both implementation options require ACP approval for your Service Account to bind the existing `dsa-pod-patch` ClusterRole. This ClusterRole provides necessary permissions to:
- List and watch pods in your namespace
- Read pod status and container information
- Access init container execution status

**Important:** Product teams must raise this request with ACP before deployment. The DSA SRE team cannot grant these permissions directly.

## Responsibilities

### Product Team Responsibilities
- Raise ACP request for ClusterRole binding permissions
- Choose and implement preferred deployment option
- Respond to Dynatrace alerts for uninstrumented pods
- Maintain their deployed monitoring service instance
- Provide namespace consent for monitoring

### DSA SRE Team Responsibilities
- Provide complete code package and Helm chart
- Supply Dynatrace API credentials and configuration
- Maintain monitoring service code and updates
- Provide deployment documentation and support
- Configure Dynatrace dashboards and alerting rules

## Metrics Generated

The service sends two metric types to Dynatrace:
- `ho.re.oneagent.pod.uninstrumented`: Alerts for each pod that lacks OneAgent, including the specific reason (missing init container, download failed, or initialization error)
- `ho.re.oneagent.pods.uninstrumented.gauge`: Total count of uninstrumented pods per namespace

## Next Steps for Product Teams

1. Choose implementation option (Helm chart recommended for most teams)
2. Raise ACP request for ClusterRole binding permissions
3. Contact DSA SRE team for Dynatrace API credentials
4. Deploy the service using chosen method
5. Verify monitoring functionality and alert configuration

## Support

For technical questions, deployment assistance, or Dynatrace credentials, contact the DSA SRE team.