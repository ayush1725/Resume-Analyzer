import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Popup from "./Popup"; 
import "./Signup.css";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [showPopup, setShowPopup] = useState(false); // State for showing popup
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
    } else {
      try {
        const res = await axios.post("http://127.0.0.1:8000/signup/", {
          email,
          password,
        });
        setShowPopup(true); // Show popup on successful signup
        setTimeout(() => {
          setShowPopup(false);
          navigate("/login"); // Navigate after a brief delay
        }, 2000);
      } catch (err) {
        setError("Error signing up. Please try again.");
      }
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-card">
        <h2 className="signup-title">Sign Up</h2>
        <form onSubmit={handleSubmit} className="signup-form">
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
          <div className="input-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit" className="btn">Sign Up</button>
        </form>
        <p className="login-link">
          Already have an account? <a href="/login">Login</a>
        </p>
      </div>
      {showPopup && <Popup message="Signup Successful!" onClose={() => setShowPopup(false)} />}
    </div>
  );
}

export default Signup;
