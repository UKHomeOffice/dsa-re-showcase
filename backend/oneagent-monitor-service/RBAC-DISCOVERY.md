# RBAC Permission Discovery for OneAgent Monitor Service

## Problem Identified

The OneAgent monitor service requires `list` and `watch` permissions on pods to detect uninstrumented workloads, but the existing `dsa-pod-patch` ClusterRole only provides insufficient permissions.

## Current RBAC Status

### Existing RoleBindings in dsa-re-dev namespace:
```
NAME                                         ROLE                                      AGE
acp:notprod:ns-admin:dsa-re-dev              ClusterRole/acp:robot:default             450d
default-sa-role                              ClusterRole/dsa-pod-patch                 14d
dsa-default-sa-role                          ClusterRole/dsa-pod-patch                 145d
dynatrace-oneagent-metadata-viewer-binding   Role/dynatrace-oneagent-metadata-viewer   412d
```

### Actual Permissions of dsa-pod-patch ClusterRole:
```
kubectl auth can-i --list --as=system:serviceaccount:dsa-re-dev:default -n dsa-re-dev | grep pods
pods    []    []    [get patch]
```

### Required Permissions for Monitor Service:
```
pods    []    []    [get list watch]
```

## Root Cause

The `dsa-pod-patch` ClusterRole was designed for patching pods (likely for OneAgent injection), not for monitoring services that need to list and watch all pods in a namespace.

## Solution Required

### Option 1: Request ACP to Create Proper Role
Product teams need to request ACP to create a Role with proper permissions:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: oneagent-monitor-pod-reader
  namespace: dsa-re-dev
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### Option 2: Use Existing dynatrace-oneagent-metadata-viewer Role
The existing `dynatrace-oneagent-metadata-viewer` role only has `get` permissions, so it's also insufficient.

## Current Limitations

- Cannot create Roles or RoleBindings (403 Forbidden)
- Cannot use existing ClusterRole `dsa-pod-patch` (insufficient permissions)
- Cannot use existing Role `dynatrace-oneagent-metadata-viewer` (insufficient permissions)

## Next Steps

1. Update Helm chart to reference the correct Role name once created by ACP
2. Request ACP to create the required Role with `list` and `watch` permissions
3. Test the monitor service once proper RBAC is in place

## Updated Helm Chart

The Helm chart has been updated to create the proper Role and RoleBinding, but deployment requires ACP approval to create RBAC resources.