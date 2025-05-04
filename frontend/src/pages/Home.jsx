import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">
      {/* Header Section */}
      <header className="home-header">
        <h1 className="home-title">Welcome to Resume Analyzer</h1>
        <p className="home-description">
          An AI-powered tool that helps you optimize your resume by analyzing it against job descriptions.
        </p>
      </header>

      {/* Feature Highlights Section */}
      <section className="home-features">
        <div className="feature-item">
          <i className="feature-icon fas fa-upload"></i>
          <h3>Upload Your Resume</h3>
          <p>
            Simply upload your resume and let our AI analyze it against relevant job descriptions.
          </p>
        </div>
        <div className="feature-item">
          <i className="feature-icon fas fa-comments"></i>
          <h3>Get Personalized Feedback</h3>
          <p>
            Receive tailored feedback on your resume, including skills match, missing keywords, and overall compatibility with the job description.
          </p>
        </div>
        <div className="feature-item">
          <i className="feature-icon fas fa-chart-line"></i>
          <h3>Track Progress</h3>
          <p>
            Keep track of your past uploads, view scores, and improve your resume over time.
          </p>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="cta-section">
        <h2>Ready to optimize your resume?</h2>
        <Link to="/upload" className="cta-button">
          Upload Your Resume
        </Link>
      </section>

      {/* Footer Section */}
      <footer className="home-footer">
        <p>© 2025 Resume Analyzer. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
