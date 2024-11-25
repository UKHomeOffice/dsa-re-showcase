# Build react app
FROM quay.io/ukhomeofficedigital/dsa-re-node-18-alpine:18-alpine3.19 AS builder

#Set working directory
WORKDIR /app

# Copy over packages
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy code files
COPY . .

# Install dependencies
RUN npm run build

# Serve stage
FROM quay.io/ukhomeofficedigital/dsa-re-nginx:1.25.2-alpine AS serve
WORKDIR /usr/share/nginx/html

# Copy built React files to nginx default location
COPY --from=builder /app/build .

# Expose port 80
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]