import React from 'react';
import './FeedbackSection.css';

const FeedbackSection = ({ feedback, similarityScore, onSave }) => {
  if (!feedback || similarityScore === undefined || similarityScore === null) {
    return (
      <div className="feedback-card">
        <h2>AI Feedback</h2>
        <p>No feedback available.</p>
      </div>
    );
  }

  const getMatchLevel = () => {
    if (similarityScore >= 0.75) return 'Excellent Match';
    if (similarityScore >= 0.5) return 'Good Match';
    if (similarityScore >= 0.3) return 'Fair Match';
    return 'Needs Improvement';
  };

  return (
    <div className="feedback-card">
      <h2>🧠 AI Feedback</h2>

      <div className="score">
        <p><strong>📊 Similarity Score:</strong> {(similarityScore * 100).toFixed(2)}%</p>
        <span className={`score-indicator ${similarityScore < 0.4 ? 'low' : 'high'}`}>
          {getMatchLevel()}
        </span>
      </div>

      <div className="feedback">
        <h3>💬 General Feedback</h3>
        <p>{feedback.general_advice}</p>

        {feedback.missing_keywords && (
          <div className="feedback-block">
            <h4>❌ Missing Keywords</h4>
            <p>{feedback.missing_keywords}</p>
          </div>
        )}

        {feedback.experience_advice && (
          <div className="feedback-block">
            <h4>💼 Experience Advice</h4>
            <p>{feedback.experience_advice}</p>
          </div>
        )}

        {feedback.skills_advice && (
          <div className="feedback-block">
            <h4>🛠 Skills Advice</h4>
            <p>{feedback.skills_advice}</p>
          </div>
        )}
      </div>

      <button className="save-btn" onClick={onSave}>💾 Save Feedback</button>
    </div>
  );
};

export default FeedbackSection;
