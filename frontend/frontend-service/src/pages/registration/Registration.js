import React from "react";
import "./Registration.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../../config";

const Registration = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    dob: "",
    password: "",
    role: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${config.API_URL}/api/v1/user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        console.log("Registration successful");
        const user = await response.json();
        if (user.role === "customer") {
          navigate("/catalogue");
        } else {
          navigate("/admin");
        }
      } else {
        const message = await response.text();
        setError(message);
      }
    } catch (error) {
      console.error("Error during registration:", error);
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <div className="registration-container">
      <div className="registration-content">
        <h1 className="title">Sign Up</h1>
        <form className="registration-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="date"
            name="dob"
            placeholder="Date of Birth"
            value={formData.dob}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="" disabled>
              Select
            </option>{" "}
            <option value="Customer">Customer</option>
            <option value="Admin">Admin</option>
          </select>
          <button type="submit" className="submit-btn">
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default Registration;
