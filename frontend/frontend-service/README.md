# Showcase Services - Frontend Service

This repository contains the frontend microservice for the Showcase Services application - RE Unicorn Rentals. This is a javascript react application which provides the user interface for the Showcase Services. It allows users to interact with various services like registration, catalog, and bookings through communication with the backend microservices to demonstrate a real-world business service flow.

This application remains a work in progress and will evolve as more microservices are developed to integrate with the front end user interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Login handling verification of credentials existing in DB table
- User registration with email and password
- Conditional page rendering based on user role
- Forms for creating/updating/deleting user information
- Catalogue page for shocasing products
- Basic error handling and validation

## Technologies Used

- **React**: JavaScript library for building user interfaces.
- **Axios**: For making HTTP requests to the backend services.
- **CSS**: For styling the components.
- **JavaScript (ES6+)**: Core language for the application logic.
- **React Dom Router**: For routing between pages.

## Installation

1. **Clone the repository with SSH**:

   ```bash
   git clone git@github.com:UKHomeOffice/dsa-re-showcase.git
   ```

2. **Install dependencies**:
   Make sure you have Node.js installed on your machine, then run:
   ```bash
   cd frontend/frontend-services
   npm install
   ```

## Running the Application

To start the React development server, run:

```bash
npm start
```

This will start the application on `http://localhost:3000`.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/UKHomeOffice/dsa-re-showcase/blob/main/LICENSE) file for details.
