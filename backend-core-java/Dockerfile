# Stage 1: Build JAR using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

COPY pom.xml .
# Pre-download dependencies to cache Docker layer
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Hardened Runtime
FROM eclipse-temurin:17-jre

# Hardening: Run as non-root user
RUN groupadd -r c2group && useradd -r -g c2group -d /app -s /sbin/nologin c2user

WORKDIR /app

COPY --from=builder /build/target/*.jar app.jar

USER c2user

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]