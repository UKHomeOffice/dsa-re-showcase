# DSA SRE Showcase Services Monorepo

This monorepo contains the Showcase Services application, designed to mimic a business service to act as a playground for testing and demonstrating various dynatrace configurations for various application stacks and builds. It consists of several microservices that work together to simulate a real-world business workflow - "Rent a Unicorn."

## Table of Contents

- [Overview](#overview)
- [Microservices](#microservices)
- [Technologies](#technologies)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Showcase Services monorepo contains multiple microservices that simulate different functionalities, such as user registration, catalog browsing, booking, and notifications. These services are built to help developers test distributed tracing, performance monitoring, and metric collection with Dynatrace across different technologies.

## Microservices

This project currently includes the following microservices:

- **Registration Service (Spring Boot)**: Handles user registration and authentication.
- **Frontend Service (React)**: A user interface that interacts with the backend services.
- **Other Services**: Additional microservices like catalog, booking, and notification to be added in the near future

Each microservice resides in its own directory within this monorepo.

## Technologies

The project makes use of multiple technologies across different microservices:

- **Java (Spring Boot)**: For backend services like registration.
- **React**: For the frontend web interface.
- **PostgreSQL**: As the database for backend services.
- **Other Technologies**: More technologies to be added as the project evolves.

## Setup

### Clone the Monorepo with SSH:

```bash
git clone git@github.com:UKHomeOffice/dsa-re-showcase.git
```

### Install Dependencies for Each Microservice

Each microservice has its own set of dependencies and setup instructions. Follow the individual README files within each microservice directory to set them up:

- **Registration Service**: Located in `backend/registration-service/`
- **Frontend Service**: Located in `frontend/frontend-service/`

## Running the Application

1. **Start the Backend Services**: Navigate to each microservice directory (e.g., `registration-service/`) and follow the instructions in their respective README files to start the services.

2. **Start the Frontend Service**: Similarly, navigate to `frontend-service/` and follow its README instructions to start the frontend.

3. **Access the Application**: Once all services are up and running, you can access the frontend via `http://localhost:3000` (or another port depending on your configuration).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/UKHomeOffice/dsa-re-showcase/blob/main/LICENSE) file for details.
