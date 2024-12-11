# Stage 1 - Build Application

# Base image with JDK
FROM quay.io/ukhomeofficedigital/dsa-re-amazoncorretto:21.0.5-alpine3.20 AS builder

#Set working directory
WORKDIR /app

# Install curl
RUN apk add --no-cache curl

# Copy over maven wrapper files
COPY mvnw .
COPY mvnw.cmd .
COPY .mvn ./.mvn

# Ensure mvnw is executable
RUN chmod +x mvnw

# Copy over pom and application source code
COPY pom.xml .
COPY src ./src

# Compile code into jar
RUN ./mvnw clean install -Dskiptests

# Stage 2 - Run application
FROM quay.io/ukhomeofficedigital/dsa-re-amazoncorretto:21.0.5-alpine3.20

#Set working directory
WORKDIR /app

# Copy over jar from stage 1
COPY --from=builder app/target/registration-service-0.0.1-SNAPSHOT.jar app.jar

# Expose port
EXPOSE 8080

# Run Springboot app
ENTRYPOINT [ "java", "-jar", "app.jar" ]
