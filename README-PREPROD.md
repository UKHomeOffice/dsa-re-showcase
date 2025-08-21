# Preprod Environment Setup

This document explains how to deploy to the preprod environment following the manual dev pattern.

## Manual Deployment (Current Approach)

### 1. Create Secrets
```bash
# Run the secrets script to see required commands
./preprod-secrets.sh

# Copy and run the displayed kubectl commands with actual values
```

### 2. Deploy Services
```bash
# Deploy all services to preprod
./deploy-preprod.sh
```

## Automated Deployment (Future Option)

If you want to enable full automation later:

### 1. Use Automation Files
```bash
# Copy automation configuration
cp .drone-automated.yml .drone.yml

# Add required secrets to Drone (11 secrets total)
# See .drone-automated.yml for the complete list
```

### 2. Automation Features
- Triggers on pushes to main branch
- Automatically creates secrets from Drone vault
- Deploys all services via Helm
- No manual intervention required

## Files Overview

- `preprod-secrets.sh` - Manual secret creation (displays commands)
- `deploy-preprod.sh` - Manual deployment script
- `.drone-automated.yml` - Full automation pipeline (saved for future)
- `.drone-preprod-automated.yml` - Alternative automation config

## Environment Differences

| Environment | Secrets | Deployment | Dynatrace |
|-------------|---------|------------|-----------|
| Dev | Manual | Manual | Dev metrics |
| Preprod | Manual | Manual | **Production metrics** |
| Preprod (Auto) | Automated | Automated | Production metrics |