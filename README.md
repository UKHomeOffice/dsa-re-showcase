# DSA SRE Showcase Services Monorepo

This monorepo contains the **Showcase Services** application, a playground environment built to simulate a real-world business service and demonstrate various **Dynatrace monitoring**, **distributed tracing**, and **application observability** implementations across different tech stacks.

The system is designed around a fictional scenario, "**Rent a Unicorn**," where users can register, log in, and trigger events — creating consistent, traceable workflows across multiple services built with different technology stacks. This architecture enables testing, validation, and demonstration of required Dynatrace configurations for a variety of product types, reflecting real-world environments where diverse applications and technologies should be monitored seamlessly.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Microservices](#microservices)
- [Technologies](#technologies)
- [Kafka Topics and Messaging](#kafka-topics-and-messaging)
- [CronJob - Simulated User Login](#cronjob---simulated-user-login)
- [Setup](#setup)
- [Deploying](#deploying-to-kubernetes)
- [Accessing the Services](#accessing-the-deployed-application)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Showcase Services project includes multiple microservices communicating via **REST APIs** and **Kafka messaging**.  
It aims to provide a lightweight but realistic system to:

- Test **distributed tracing** with Dynatrace.
- Explore **metrics** and **logs** collection across services.
- Validate **secure service-to-service communication** (mTLS with Kafka).
- Showcase **best practices** for observability in Kubernetes environments.

All services are containerized, deployed into **Kubernetes** clusters using **Helm charts**, and monitored via **Dynatrace ActiveGate** and **OneAgent**.

---

## Architecture

```
User
 ↓
Frontend (Javascript/React)
 ↓ (REST API)
Registration Service (Java/Spring Boot)
 ↓ (Kafka - mTLS secured)
userLogin Topic (AWS MSK)
 ↓
Notification Service (Python FastAPI)
```

- A **Kubernetes CronJob** named ***trigger-login*** regularly triggers simulated user login (every approx 10 mins) activity to maintain traffic through the system for monitoring and tracing purposes, ensuring consistency in data being sent to Dynatrace SAAS.
- **RDS PostgreSQL** database instance is used by the Registration Service to manage user data in the *users* table.
- **Amazon MSK (Kafka)** is used for inter-service messaging.

---

## Microservices

| Service | Stack | Description |
| :--- | :--- | :--- |
| **Frontend Service** | React | User-facing web application. Handles user login and registration via APIs to backend services. | Conditional routing based on user roles of *admin* or *customer*. |
| **Registration Service** | Spring Boot (Java) | Backend service for user registration, login and authentication. Publishes Kafka messages on user login using kafka-consumer viar the [RegistrationProducer](/backend/registration-service/src/main/java/com_example_registration_service/RegistrationProducer.java) class |
| **Notification Service** | FastAPI (Python) | Kafka consumer service that processes login events published by the Registration Service. |

Each microservice resides in its own subdirectory within the monorepo.

---

## Technologies

- **Java (Spring Boot)**: Backend service for registration and authentication.
- **React**: Frontend UI for users.
- **Python (FastAPI)**: Lightweight Kafka consumer for notification processing.
- **PostgreSQL**: Persistent user database (AWS RDS).
- **Kafka (Amazon MSK)**: Event-driven messaging platform.
- **Kubernetes**: Deployment and orchestration.
- **Helm**: Kubernetes package management.
- **Dynatrace**: Monitoring, metrics, distributed tracing (ActiveGate + OneAgent).
- **mTLS**: Secure Kafka communication between services.

---

## Kafka Topics and Messaging

- **Topics**:
  - `userLogin`: Published by the Registration Service when users successfully log in. Consumed by the Notification Service.

- **mTLS Authentication**:
  - Kafka client certificates are generated, stored in a Kubernetes **PersistentVolumeClaim (PVC)**, and mounted into the service pods that interact with Kafka.

- **Kafka Tools Pod**:
  - A special tools pod is available to run Kafka client commands using mTLS certificates for validation and testing. Documentation on using the pod [here](https://confluence.dsa.homeoffice.gov.uk/display/SPS/How+to+diagnose+network+connectivity+within+the+Kubernetes+cluster).

---

## CronJob - Simulated User Login

- A **Kubernetes CronJob** is deployed to regularly simulate a user login by calling the Registration Service API.
- This ensures that consistent Kafka traffic is generated for distributed tracing and metrics collection, even without manual user interaction.

---

## Setup

### Clone the Monorepo

```bash
git clone git@github.com:UKHomeOffice/dsa-re-showcase.git
cd dsa-re-showcase
```

## Deploying to Kubernetes

Each microservice (Frontend Service, Registration Service, Notification Service) has its own dedicated Helm chart.  
These charts are structured with:

- **Global configuration** (common settings, secrets, networking templates)
- **Environment-specific values files** (e.g., `values-dev.yaml`)

For development deployments, we typically deploy into the `dsa-re-dev` namespace using Helm.  
Example command to deploy registration-service:

```bash
cd registration-service/registration-service-chart
helm deploy registration-service . --values=values-dev.yaml --namespace dsa-re-dev
```

Make sure you have authenticated access to the Kubernetes cluster and have the necessary secrets (e.g., Kafka certificates, Postgres credentials) already set up before deploying. Refer to [Technical Onboarding Guide](https://confluence.dsa.homeoffice.gov.uk/display/SPS/Dynatrace+-+Technical+Onboarding+Guide) for access requirements.

---

## Accessing the Deployed Application

- The **Frontend Service** provides the only public-facing UI.
- Once deployed, it can be accessed at:

```text
http://frontend-service.dev.dsa-re-notprod.homeoffice.gov.uk/
```

- The **Registration Service** and **Notification Service** are backend services and are not publicly exposed. They communicate internally within the Kubernetes cluster via REST and Kafka.

To **view the logs** of any deployed service:

1. List the pods in the namespace:

```bash
kubectl get pods -n dsa-re-dev
```

2. Stream the logs of a specific pod:

```bash
kubectl logs <pod-name> -n dsa-re-dev -f
```

For example, to view live logs of the Registration Service pod:

```bash
kubectl logs registration-service-<pod-suffix> -n dsa-re-dev -f
```

Replace `<pod-suffix>` with the actual pod identifier.

This is useful for troubleshooting and observing service activity, including Kafka message production and consumption.

---

## Contributing
  
The showcase-services are currently in active development and for contricuting, pleease follow these steps:

1. Fork the repository.

2. Create a new branch:

    ```bash
    git checkout -b feature/YourFeature
    ```

3. Make your changes and commit them:

    ```bash
    git commit -m "Add new feature"
    ```

4. Push your branch:

    ```bash
    git push origin feature/YourFeature
    ```

5. Open a Pull Request against the `main` branch.

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/UKHomeOffice/dsa-re-showcase/blob/main/LICENSE) file for details.
