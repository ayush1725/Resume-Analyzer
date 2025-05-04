import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Popup from "./Popup"; // Import Popup component
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPopup, setShowPopup] = useState(false); // State for showing popup
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/login/", {
        email,
        password,
      });
      // Store the JWT token in localStorage
      localStorage.setItem("access_token", res.data.access_token);
      setShowPopup(true); // Show popup on successful login
      setTimeout(() => {
        setShowPopup(false);
        navigate("/home"); // Redirect to home after login
      }, 2000);
    } catch (err) {
      setError("Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit" className="btn">Login</button>
        </form>
        <p className="signup-link">
          Don't have an account? <a href="/signup">Sign Up</a>
        </p>
      </div>
      {showPopup && <Popup message="Login Successful!" onClose={() => setShowPopup(false)} />}
    </div>
  );
}

export default Login;
