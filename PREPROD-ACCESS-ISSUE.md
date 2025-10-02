# Preprod Access Issue Resolution

## Problem
Registration service in preprod has multiple pods running simultaneously, causing volume mounting conflicts with the `kafka-tls-storage` PVC (ReadWriteOnce).

## Current Status
- Multiple registration service pods detected:
  - `registration-service-7b68b87798-96ksp` (48m old, running successfully)  
  - `registration-service-6ff546fd58-xzzgs` (21s old, failing to start)

## Root Cause
The RWO (ReadWriteOnce) volume `kafka-tls-storage` can only be mounted by one pod at a time. The old pod is holding the volume, preventing the new pod from starting.

## Access Issue
Current user `kingsford.johnson1@digital.homeoffice.gov.uk` has permissions for `dsa-re-dev` namespace but not `dsa-re-preprod`.

## Resolution Steps

### Option 1: Request Preprod Access
Contact platform team to grant RBAC permissions for `dsa-re-preprod` namespace.

### Option 2: Use Service Account with Permissions
If available, use a service account that has preprod access:
```bash
kubectl --as=system:serviceaccount:dsa-re-preprod:<service-account-name> scale deployment registration-service -n dsa-re-preprod --replicas=0
```

### Option 3: Clean Deployment via Helm (if permissions allow)
```bash
# Scale down via helm upgrade
helm upgrade registration-service . --values=values-preprod.yaml --namespace dsa-re-preprod --set replicaCount=0

# Wait for pods to terminate, then scale back up
helm upgrade registration-service . --values=values-preprod.yaml --namespace dsa-re-preprod --set replicaCount=1
```

### Option 4: Manual Pod Cleanup (requires preprod access)
```bash
# Delete all registration service pods
kubectl delete pods -n dsa-re-preprod -l app.kubernetes.io/name=registration-service

# Or scale deployment to 0 then back to 1
kubectl scale deployment registration-service -n dsa-re-preprod --replicas=0
kubectl scale deployment registration-service -n dsa-re-preprod --replicas=1
```

## Prevention
To prevent this issue in future:
1. Always scale deployment to 0 before major updates
2. Use `--force` flag with helm upgrades when changing volume configurations
3. Monitor for multiple pods during deployments

## Next Steps
1. Obtain preprod namespace access
2. Clean up duplicate pods
3. Verify single pod deployment
4. Test database connectivity