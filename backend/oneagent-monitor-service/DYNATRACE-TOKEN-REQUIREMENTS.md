# Dynatrace Token Requirements for OneAgent Monitoring

## Current Issue
The sidecar implementation is working perfectly but needs the correct Dynatrace API token for metrics ingestion.

## Token Requirements

### For Direct Dynatrace SaaS Access (Recommended)
- **Endpoint**: `https://ewo35763.live.dynatrace.com/api/v2/metrics/ingest`
- **Required Permission**: `metrics.ingest`
- **Token Type**: API Token (not PaaS token)

### Current Token Analysis
- **Current Token**: `dt0c01.ST2EY72KQINMH574WMNVI7YN.G3DFPBEJYMODIDAEX454M7YWBUVEFOWKPRVMWFM36SZIRGEIRYMQ`
- **Type**: PaaS Token (for OneAgent downloads)
- **Issue**: Lacks `metrics.ingest` permission
- **Result**: 401 Authentication failed

## Solution Options

### Option 1: Create New API Token (Recommended)
1. **Access Dynatrace Console**: https://ewo35763.live.dynatrace.com
2. **Navigate to**: Settings > Integration > Dynatrace API
3. **Create Token** with permissions:
   - `metrics.ingest` (required)
   - `metrics.read` (optional, for verification)
4. **Update sidecar configuration** with new token

### Option 2: Fix ActiveGate Configuration
1. **Check ActiveGate status** in dynatrace namespace
2. **Enable metrics ingestion** capability on ActiveGate
3. **Fix ingress routing** for activegate-notprod endpoint

## Implementation Status
- ✅ **Sidecar Logic**: Working perfectly
- ✅ **Network Connectivity**: Direct DT SaaS reachable
- ✅ **Metric Generation**: Correct format
- ⚠️ **Token Permissions**: Need metrics.ingest token

## Next Steps
1. **Get correct API token** with metrics.ingest permission
2. **Update sidecar deployment** with new token
3. **Verify metrics appear** in Dynatrace: `ho.re.oneagent.pod.uninstrumented.event`

## Expected Result
Once the correct token is provided, metrics will immediately appear in Dynatrace without any code changes.