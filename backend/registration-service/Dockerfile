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

# Install Kafka client dependencies (Kafka tools)
RUN apk add --no-cache bash wget && \
    wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz && \
    tar -xzvf kafka_2.13-3.0.0.tgz && \
    rm kafka_2.13-3.0.0.tgz

# Copy over jar from stage 1
COPY --from=builder app/target/registration-service-0.0.1-SNAPSHOT.jar app.jar

# Expose port
EXPOSE 8080

# Run Springboot app
ENTRYPOINT [ "java", "$JAVA_OPTS", "-jar", "app.jar" ]
