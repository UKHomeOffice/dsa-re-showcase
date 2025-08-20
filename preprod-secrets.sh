#!/bin/bash

# Setup Preprod Secrets for Showcase Services
# Run this script before deploying to preprod environment

set -e

NAMESPACE="dsa-re-preprod"

echo "Setting up secrets for ${NAMESPACE} environment..."

# Create namespace if it doesn't exist
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

echo "Please create the following secrets manually in ${NAMESPACE} namespace:"
echo ""
echo "1. RDS Database Secret:"
echo "kubectl create secret generic dsarepreprodshowcase-rds \\"
echo "  --from-literal=endpoint=<PREPROD_RDS_ENDPOINT> \\"
echo "  --from-literal=port=5432 \\"
echo "  --from-literal=default_db=<DB_NAME> \\"
echo "  --from-literal=username=<DB_USERNAME> \\"
echo "  --from-literal=password=<DB_PASSWORD> \\"
echo "  --namespace ${NAMESPACE}"
echo ""
echo "2. Dynatrace Production Metrics Secret:"
echo "kubectl create secret generic registration-service-dynatrace-prod-metrics-ingest \\"
echo "  --from-literal=token=<DT_PROD_METRICS_TOKEN> \\"
echo "  --from-literal=api_url=<DT_PROD_METRICS_API_URL> \\"
echo "  --namespace ${NAMESPACE}"
echo ""
echo "3. Dynatrace OneAgent Secret:"
echo "kubectl create secret generic registration-service-dynatrace-oneagent \\"
echo "  --from-literal=api-url=<DT_PROD_API_URL> \\"
echo "  --from-literal=paas-installer-download-token=<DT_PROD_PAAS_TOKEN> \\"
echo "  --namespace ${NAMESPACE}"
echo ""
echo "Replace <PLACEHOLDER> values with actual preprod credentials."