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

# Set working directory
WORKDIR /usr/share/nginx/html

# Copy built React files to nginx default location
COPY --from=builder /app/build .

# Copy over custom nginx.conf file
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

# Set permissions globally in dockerfile
RUN chown -R 1000:1000 /usr/share/nginx/html /var/cache/nginx /var/run /etc/nginx \
    chmod -R 755 /usr/share/nginx/html /var/cache/nginx /var/run /etc/nginx

# Switch to non-root user
USER 1000

# Expose port 80
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]