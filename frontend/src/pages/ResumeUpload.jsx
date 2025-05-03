import React, { useState } from "react";
import axios from "axios";
import "./ResumeUpload.css";

function ResumeUpload() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Please upload a resume and enter job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/analyze/", formData);
      setResult(response.data);
    } catch (error) {
      alert("Analysis failed. Please try again.");
    }
    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 75) return "green";
    if (score >= 50) return "orange";
    return "red";
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>ResumeIQ</h2>
        <ul>
          <li>🏠 Dashboard</li>
          <li>📄 Upload Resume</li>
          <li>📊 Score Insights</li>
          <li>🧠 AI Feedback</li>
          <li>🗃️ Saved Results</li>
        </ul>
      </aside>

      <main className="main-content">
        <div className="topbar">
          <h1>🔍 Resume Analyzer</h1>
          <p className="description">
            Upload your resume and match it with any job description. Powered by NLP & Transformers for real-time resume insights.
          </p>
        </div>

        <div className="card upload-section">
          <h2>📁 Upload Resume</h2>
          <span className="tooltip">PDF only, max size 2MB</span>
          <input type="file" onChange={handleFileChange} accept=".pdf" />
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
            {loading ? <span className="loader"></span> : "🚀 Analyze Resume"}
          </button>
        </div>

        {result && (
          <div className="card result">
            <h3>📈 Analysis Report</h3>
            <p>
              <strong>Match Score:</strong>{" "}
              <span style={{ color: getScoreColor(result.score) }}>
                {result.score}%
              </span>
            </p>
            <p><strong>Summary:</strong> {result.summary}</p>
            <p><strong>AI Feedback:</strong> {result.feedback}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default ResumeUpload;
