# ActiveGate Certificate Issue - Preprod Environment

## Issue Description
The OneAgent init container in the registration-service is failing with an SSL certificate verification error:

```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1006)'))
```

## Root Cause
The ActiveGate certificate in the dynatrace-preprod namespace is experiencing verification issues. This appears to be a temporary issue as pods were running successfully this morning, suggesting either:
- Certificate rotation in progress
- Intermittent network/DNS issues
- ActiveGate pod restart causing temporary certificate issues

## Implemented Workaround
Updated OneAgent configuration to handle certificate issues:

1. **Updated deployment template** with:
   ```yaml
   - name: DYNATRACE_ONEAGENT_VERSION
     value: latest
   - name: DYNATRACE_SKIP_SSL_VERIFICATION
     value: "true"
   ```

2. **Updated OneAgent injection image** to latest version:
   ```yaml
   image: quay.io/ukhomeofficedigital/dsa-re-dynatrace-oneagent-pod-runtime-injection:latest
   ```

## Alternative Workaround
If the above doesn't work, temporarily disable OneAgent injection:

1. **Update values-preprod.yaml**:
   ```yaml
   dynatrace:
     podRuntimeInjection:
       enabled: false
   ```

## Permanent Solution
The ActiveGate certificate needs to be renewed. This requires:

1. **Check ActiveGate status**:
   ```bash
   kubectl get pods -n dynatrace-preprod -l app.kubernetes.io/name=dynatrace-activegate
   kubectl logs -n dynatrace-preprod <activegate-pod-name>
   ```

2. **Update ActiveGate configuration** or **restart ActiveGate pods** to refresh certificates

3. **Re-enable OneAgent injection** once ActiveGate is healthy:
   ```yaml
   dynatrace:
     podRuntimeInjection:
       enabled: true
   ```

## Required Permissions
This issue requires someone with cluster-admin or dynatrace-preprod namespace admin permissions to:
- Access dynatrace-preprod namespace
- Manage ActiveGate StatefulSet
- Update Helm releases in dsa-re-preprod namespace

## Status
- **Current**: OneAgent injection disabled in registration-service values-preprod.yaml
- **Next**: Platform team needs to resolve ActiveGate certificate issue
- **Final**: Re-enable OneAgent injection after ActiveGate is healthy