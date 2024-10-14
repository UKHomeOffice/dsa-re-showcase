# Stage 1 - Build Application

# Base image with JDK
FROM maven:3.8.7-openjdk-18-slim as builder

#Set working directory
WORKDIR /app

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
FROM maven:3.8.7-openjdk-18-slim

#Set working directory
WORKDIR /app

# Copy over jar from stage 1
COPY --from=builder app/target/registration-service-0.0.1-SNAPSHOT.jar app.jar

# Expose port
EXPOSE 8080

# Run Springboot app
ENTRYPOINT [ "java", "-jar", "app.jar" ]