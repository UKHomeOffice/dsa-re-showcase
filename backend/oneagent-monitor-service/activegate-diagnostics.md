# ActiveGate Diagnostics Report

## Issue Summary
The ActiveGate endpoint `https://activegate-notprod.dsa-notprod.homeoffice.gov.uk/e/ewo35763/api/v2/metrics/ingest` is returning "default backend - 404" for all requests.

## Test Results
- **Base URL**: 404 - default backend
- **Environment URL**: 404 - default backend  
- **All API endpoints**: 404 - default backend

## Root Cause Analysis
The "default backend - 404" response indicates the ingress controller cannot route requests to the ActiveGate backend service.

## Possible Causes
1. **ActiveGate Pod Not Running**: Backend service is down
2. **Ingress Misconfiguration**: Routing rules not properly configured
3. **Service Discovery Issue**: Ingress can't find the ActiveGate service
4. **Metrics Ingestion Disabled**: ActiveGate doesn't have metrics capability enabled

## Recommended Actions
1. **Check ActiveGate Pod Status**: Verify pods are running in dynatrace namespace
2. **Verify Ingress Configuration**: Check ingress rules for activegate-notprod
3. **Confirm Service Endpoints**: Ensure ActiveGate service is properly exposed
4. **Enable Metrics Ingestion**: Configure ActiveGate with metrics ingestion capability

## Impact Assessment
- **Existing Services**: No impact - diagnostic tests only
- **OneAgent Monitoring**: Sidecar implementation is working, waiting for ActiveGate fix
- **Metrics**: Will appear in Dynatrace once ActiveGate is properly configured

## Next Steps
Contact platform team to:
1. Verify ActiveGate deployment status
2. Check ingress configuration
3. Enable metrics ingestion capability if needed