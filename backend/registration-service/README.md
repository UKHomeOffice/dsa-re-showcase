# Showcase Services - Registration Service

This repository contains the Registration microservice for the Showcase Services application - RE Unicorn Rentals. This is a Java Sprinboot application which handles the backend logic for the registration and management of the application's users.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Setup](#database-setup)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration with email and password.
- Password hashing for security.
- User Login handling verification of credentials existing in DB table
- Role assignment used for user journeys (customer/admin)
- RESTful API to interact with user data incl get/create/update/delete user
- Basic error handling and validation.

## Technologies Used

- **Java**: Version 21
- **Spring Boot**: Version 3.3.4
- **PostgreSQL**: Database for storing user data.
- **Maven**: Dependency management and build tool.

## Installation

1. **Clone the repository with SSH**:

   ```bash
   git clone git@github.com:UKHomeOffice/dsa-re-showcase.git
   ```

2. **Set up PostgreSQL**:

   - Make sure you have PostgreSQL installed and running.
   - Create a new database for the application and create table unicorn_registration_db
   - For any changes you make in your local postgres intance, please update `application.properties` file

3. **Build the project**:
   ```bash
   cd backend/registration-service
   mvn clean install
   ```

## Running the Application Locally

Note to run the application locally there is a prerequisite on having a PostgreSQL accessible to the app

- Make sure to create a database and user in PostgreSQL with the necessary privileges.
- Update the `application.properties` file with your database connection settings, such as:
  ```properties
  spring.datasource.url=jdbc:postgresql://localhost:5432/yourdbname
  spring.datasource.username=yourusername
  spring.datasource.password=yourpassword
  ```

1. **Start the application**:

   ```bash
   mvn spring-boot:run
   ```

2. **Access the API**:
   - The application will be running at `http://localhost:8080`.

## Deploying via Helm

At time of writing there is no pipeline-based Helm deployment. Deployments are done 'by hand' by executing the following command from within the charts directory:

```
helm -n dsa-re-dev upgrade registration-service . --values=values-dev.yaml
```

Remember that by deploying changes from locally branches you are potentially diverging what is deployed from the main branch.


## API Endpoints

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| POST   | /api/v1/user   | Register a new user      |
| GET    | /api/user      | Get all registered users |
| GET    | /api/user/{id} | Get user details by ID   |
| PUT    | /api/user/{id} | Update user details      |
| DELETE | /api/user/{id} | Delete a user            |

### Request and Response Examples

**Register User**:

- **Request**:

  ```json
  POST /api/user
  {
    "name": "Joe Bloggs",
    "email": "example@example.com",
    "dob": "1987-12-11",
    "password": "SecurePassword123",
    "role": "admin"
  }
  ```



## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/UKHomeOffice/dsa-re-showcase/blob/main/LICENSE) file for details.
