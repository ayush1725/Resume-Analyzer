import { useState } from "react";
import axios from "axios";
import "./ResumeUpload.css";

function ResumeUpload() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [summary, setSummary] = useState("");
  const [score, setScore] = useState(null);
  const [feedback, setFeedback] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resume || !jobDesc) return alert("Upload resume & enter job description");

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_desc", jobDesc);

    try {
      const token = localStorage.getItem("access_token");
      const res = await axios.post("http://localhost:8000/upload-resume/", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setSummary(res.data.summary);
      setScore(res.data.score);
      setFeedback(res.data.feedback);
    } catch (err) {
      alert("Error uploading resume. Try again.");
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <h2 style={{ color: "var(--primary)" }}>Upload Resume</h2>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setResume(e.target.files[0])}
          required
        />
        <textarea
          placeholder="Paste job description here..."
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          rows={5}
          required
        />
        <button type="submit">Analyze</button>
      </form>

      {summary && (
        <div className="result">
          <h3>Summary</h3>
          <p>{summary}</p>
          <h3>Match Score: <span className="score">{score}%</span></h3>
          <h3>Feedback</h3>
          <p>{feedback}</p>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
