# Build react app
FROM quay.io/ukhomeofficedigital/dsa-re-node-18-alpine:18-alpine3.19 AS builder
WORKDIR /app

#Set working directory
WORKDIR /app

# Copy over maven wrapper files
COPY package.json .

# Install dependencies
RUN npm install

# Copy code files
COPY . .

# Expose Port
EXPOSE 3000

# Run Applicatoion
RUN npm run start