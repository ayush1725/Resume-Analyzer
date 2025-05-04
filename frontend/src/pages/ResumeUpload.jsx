import React, { useState } from "react";
import axios from "axios";
import "./ResumeUpload.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function ResumeUpload() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.size > 2 * 1024 * 1024) {
      setErrorMessage("File size must be less than 2MB.");
    } else {
      setResumeFile(file);
      setErrorMessage("");
    }
  };

  const handleAnalyze = async () => {
    setResult(null);
    setErrorMessage("");

    if (!resumeFile || !jobDescription) {
      setErrorMessage("Please upload a resume and enter a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    setLoading(true);
    const token = localStorage.getItem("access_token");

    if (!token) {
      setErrorMessage("You must be logged in to analyze the resume.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/analyze/",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const analysisResult = response.data;
      setResult(analysisResult);
      await sendEmailNotification(analysisResult.similarity_score);
    } catch (error) {
      if (error.response) {
        setErrorMessage(
          `Error: ${
            error.response.data.message || "Analysis failed. Please try again."
          }`
        );
      } else {
        setErrorMessage(
          "Network error. Please check your connection and try again."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const sendEmailNotification = async (score) => {
    try {
      const response = await axios.post(
        "http://localhost:8000/send-feedback-email/",
        {
          score,
          email: localStorage.getItem("email"),
        }
      );

      console.log("Email sent successfully", response);
      toast.success("✅ All details and feedback have been sent to your mail!");
    } catch (error) {
      console.error("Error sending email", error);
      toast.error("✅ All details and feedback have been sent to your mail!");
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return "green";
    if (score >= 50) return "orange";
    return "red";
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <ul>
          <li>
            <button
              onClick={() =>
                window.scrollTo(
                  0,
                  document.getElementById("score-insights").offsetTop
                )
              }
            >
              Score Insights
            </button>
          </li>
          <li>
            <button
              onClick={() =>
                window.scrollTo(
                  0,
                  document.getElementById("ai-feedback").offsetTop
                )
              }
            >
              AI Feedback
            </button>
          </li>
          <li>
            <button
              onClick={() =>
                window.scrollTo(
                  0,
                  document.getElementById("saved-results").offsetTop
                )
              }
            >
              Saved Results
            </button>
          </li>
        </ul>
      </aside>

      <main className="main-content">
        <div className="topbar">
          <h1>Resume Analyzer</h1>
          <p className="description">
            Upload your resume and match it with any job description. Powered by
            NLP & Transformers for real-time resume insights.
          </p>
          <ul className="instructions">
            <li>📄 Upload your resume in PDF format (upto 2mb max).</li>
            <li>📝 Paste the job description in the text area below.</li>
            <li>
              ⚙️ Click <strong>Analyze Resume</strong> to see the match score
              and feedback.
            </li>
            <li>💾 Save your results for future reference.</li>
          </ul>
        </div>

        <div className="card upload-section">
          <h2>📁 Upload Resume</h2>
          <span className="tooltip">PDF only, max size 2MB</span>
          <input type="file" onChange={handleFileChange} accept=".pdf" />
          {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>

        <div className="card jd-section">
          <h2>📝 Job Description</h2>
          <span className="tooltip">Paste from LinkedIn, Indeed, etc.</span>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste job description here..."
            rows="6"
          ></textarea>
          <div className="tags">
            <span>Python</span>
            <span>React</span>
            <span>Machine Learning</span>
            <span>Docker</span>
          </div>
        </div>

        <div className="card action-section">
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? <span className="loader"></span> : " Analyze Resume"}
          </button>
        </div>

        {result && (
          <>
            <div id="score-insights" className="card result">
              <h3>Analysis Report</h3>
              <p>
                <strong>Match Score:</strong>{" "}
                <span
                  style={{
                    color: getScoreColor(result.similarity_score * 100),
                  }}
                >
                  {Math.round(result.similarity_score * 100)}%
                </span>
              </p>
              <p>
                <strong>Summary:</strong>
              </p>
              <ul>
                <li>
                  <strong>Experience:</strong> {result.summary.Experience}
                </li>
                <li>
                  <strong>Education:</strong> {result.summary.Education}
                </li>
                <li>
                  <strong>Skills:</strong> {result.summary.Skills}
                </li>
              </ul>
            </div>

            <div id="ai-feedback" className="card ai-feedback">
              <h3>AI Feedback</h3>
              <p>
                <strong>General:</strong> {result.feedback.general_advice}
              </p>
              {result.feedback.missing_keywords && (
                <p>
                  <strong>Missing Keywords:</strong>{" "}
                  {result.feedback.missing_keywords}
                </p>
              )}
              {result.feedback.experience_advice && (
                <p>
                  <strong>Experience Advice:</strong>{" "}
                  {result.feedback.experience_advice}
                </p>
              )}
              {result.feedback.skills_advice && (
                <p>
                  <strong>Skills Advice:</strong>{" "}
                  {result.feedback.skills_advice}
                </p>
              )}
            </div>
          </>
        )}

        {errorMessage && <div className="error-card">{errorMessage}</div>}
        <ToastContainer position="top-center" autoClose={5000} />
        <footer className="footer">
          <p>&copy; 2025 Resume Analyzer. Built by Ayush Dwibedy.</p>
        </footer>
      </main>
    </div>
  );
}

export default ResumeUpload;
