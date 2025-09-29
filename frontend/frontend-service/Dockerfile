# Build react app
FROM quay.io/ukhomeofficedigital/dsa-re-node:18-alpine3.20 AS builder

#Set working directory
WORKDIR /app

# Install curl
RUN apk add --no-cache curl

# Copy over packages
COPY package.json package-lock.json ./

# Install dendencies
RUN npm install

# Copy code files
COPY . .

# Build react app
RUN npm run build

# Install static file server
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start static file server and expose react app on 3000
CMD ["serve", "-s", "build", "-l", "3000"]
