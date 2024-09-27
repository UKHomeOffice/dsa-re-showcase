import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import logo from "../../assets/images/unicorn-logo.png";

const Home = () => {
  return (
    <div className="home-container">
      <img className="logo" src={logo} alt="RE Unicorn Rentals Logo" />
      <div className="home-content">
        <h1>Welcome to Unicorn Rentals</h1>
        <p>Discover your dream unicorn and make magical memories!</p>

        <div className="button-container">
          <Link to="/login" className="login-button">
            Sign In
          </Link>
          <p>
            Are you new to Unicorn Rentals?{" "}
            <Link to="/registration" className="signup-link">
              Sign up!
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
