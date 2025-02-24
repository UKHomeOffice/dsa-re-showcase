# Using base alpine image
FROM alpine:latest

# Install curl
RUN apk add --no-cache curl

# Set the working directory to /app
WORKDIR /app

# Copy script into container
COPY trigger_login.sh /app/trigger_login.sh
RUN chmod +x /app/trigger_login.sh

RUN adduser -D -u 1000 reliabilityenablement

USER 1000

# Set entrypoint
ENTRYPOINT [ "/app/trigger_login.sh" ]
