#!/bin/bash

# Configuration
REGISTRATION_SERVICE_URL="http://frontend-service.dev.dsa-re-notprod.homeoffice.gov.uk/api/v1/user"
EMAIL="Chris.Hunter@gmail.com"
PASSWORD="chrispassword"

# Simulate login
echo "Simulating login for user: $EMAIL"
response=$(curl -v -s -o /dev/null -w "%{http_code}" \
	-X POST "$REGISTRATION_SERVICE_URL/login" \
	-H "Content-Type: application/json" \
	-d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

# Check response
if [ "$response" -eq 200 ]; then
	echo "Simulated login successfully"
else 
	echo "Sumilated login failed with HTTP status: $response"
fi
