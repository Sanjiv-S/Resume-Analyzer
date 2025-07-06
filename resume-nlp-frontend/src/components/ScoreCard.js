import React from 'react';
// Optional: style separately if you want

function ScoreCard({ scores }) {
  return (
    <div className="scorecard">
      <h3>Section-wise Scores</h3>
      {Object.entries(scores).map(([label, value]) => (
        <div key={label} className="score-item">
          <label>{label}</label>
          <div className="progress">
            <div className="progress-fill" style={{ width: `${value}%` }}></div>
          </div>
          <span>{value}</span>
        </div>
      ))}
    </div>
  );
}

export default ScoreCard;
