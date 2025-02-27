#!/bin/bash
set -e

REGISTRATION_SERVICE_URL="http://frontend-service.dev.dsa-re-notprod.homeoffice.gov.uk/api/v1/user"

# Existing users
USER1_EMAIL="Chris.Hunter@gmail.com"
USER1_PASSWORD="chrispassword"

USER2_EMAIL="Michael.McCarthy@gmail.com"
USER2_PASSWORD="michaelpassword"

# Select user
if [ $(($RANDOM % 2)) -eq 0 ]; then
	EMAIL=$USER1_EMAIL
	PASSWORD=$USER1_PASSWORD
else
	EMAIL=$USER2_EMAIL
	PASSWORD=$USER2_PASSWORD
fi

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
