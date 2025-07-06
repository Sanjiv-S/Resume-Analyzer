import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactSpeedometer from 'react-d3-speedometer';
import { Viewer } from '@react-pdf-viewer/core';
import { Worker } from '@react-pdf-viewer/core';
import { Chart as ChartJS } from 'chart.js'; // still required for compatibility

import '@react-pdf-viewer/default-layout/lib/styles/index.css';

import './App.css';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [fileURL, setFileURL] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile) {
      alert("Please upload your resume first!");
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDesc);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/upload_resume', formData);
      setResult(res.data);
    } catch (err) {
      console.error("API error:", err);
      alert("Error analyzing resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    <div class="wave-background"></div>

      {/* Navigation */}
      <nav className="navbar">
        <div className="logo">SResumeChecker</div>
        <ul>
          <li><a href="#">Resume</a></li>
          <li><a href="#">Services</a></li>
          <li><a href="#">Resources</a></li>
          <li><a href="#">Blog</a></li>
        </ul>
        <div className="auth">
          <button onClick={() => setDarkMode(!darkMode)}>{darkMode ? '🌞' : '🌙'}</button>
          <button className="login">Login</button>
          <button className="signup">Sign up</button>
        </div>
      </nav>

      {/* Upload Page */}
      {!result && (
        <div className="upload-page">
          <div className="info-box">
            <h2>📄 Resume Analyzer</h2>
            <p>
              Upload your resume to evaluate how well it is structured,
              highlights your skills, matches the job you're applying for,
              and more!
            </p>
          </div>

          <form onSubmit={handleSubmit} className="upload-section">
            <label htmlFor="upload" className="upload-box">
              <input
                type="file"
                id="upload"
                accept=".pdf"
                onChange={(e) => {
                  setResumeFile(e.target.files[0]);
                  setFileURL(URL.createObjectURL(e.target.files[0]));
                }}
              />
              <span>📎 Drag or click to upload your resume</span>
            </label>

            <select onChange={(e) => setJobDesc(e.target.value)} defaultValue="">
              <option value="" disabled>Choose a job role</option>
              <option>Machine Learning Engineer</option>
              <option>Frontend Developer</option>
              <option>Backend Developer</option>
              <option>Full Stack Developer</option>
              <option>Cloud Engineer</option>
              <option>Data Analyst</option>
            </select>

            <button type="submit" disabled={loading}>
                {loading ? "🔍 Analyzing..." : "Analyze Resume"}
            </button>
            {fileURL && (
              <div className="pdf-preview">
                  <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
                  <Viewer fileUrl={fileURL} />
                </Worker>
              </div>
            )}
          </form>
        <div className="checklist-section">
  <h2>🧩 Resume Perfection Checklist</h2>
  <p>Use this vibrant interactive guide to ensure your resume covers all the essentials.</p>

  

  {/* 🌈 Floating Background Icons */}
<span className="floating-icon" style={{ top: '8%', left: '5%' }}>📄</span>
<span className="floating-icon" style={{ top: '25%', left: '90%' }}>✏️</span>
<span className="floating-icon" style={{ top: '60%', left: '30%' }}>📁</span>
<span className="floating-icon" style={{ top: '78%', left: '80%' }}>✅</span>
<span className="floating-icon" style={{ top: '42%', left: '50%' }}>💡</span>
<span className="floating-icon" style={{ top: '18%', left: '40%' }}>🧠</span>
<span className="floating-icon" style={{ top: '77%', left: '33%' }}>🖋️</span>
<span className="floating-icon" style={{ top: '23%', left: '77%' }}>👀</span>
<span className="floating-icon" style={{ top: '33%', left: '10%' }}>📁</span>
<span className="floating-icon" style={{ top: '67%', left: '60%' }}>🔍</span>
<span className="floating-icon" style={{ top: '85%', left: '15%' }}>👀</span>
<span className="floating-icon" style={{ top: '10%', left: '75%' }}>💬</span>
<span className="floating-icon" style={{ top: '55%', left: '90%' }}>🎯</span>


  <div className="checklist-grid">
    {[
      {
        icon: '📄',
        title: 'Format',
        size: '1.2',
        items: ['File format and size', 'Resume length', 'Bullet point length tips']
      },
      {
        icon: '📑',
        title: 'Resume sections',
        size: '1',
        items: ['Contact information', 'Essential sections', 'Personality showcase tips']
      },
      {
        icon: '✏️',
        title: 'Content',
        size: '1.4',
        items: ['ATS parse rate', 'Word repetition', 'Grammar & spelling', 'Impact quantification']
      },
      {
        icon: '💡',
        title: 'Skills suggestion',
        size: '1',
        items: ['Hard skills', 'Soft skills']
      },
      {
        icon: '🅰️',
        title: 'Style',
        size: '1.1',
        items: ['Resume design', 'Email address presence', 'Active voice usage', 'Buzzword avoidance']
      }
    ].map((card, i) => (
      <div
        className="checklist-card"
        style={{ '--i': i, '--size': card.size }}
        key={i}
      >
        <div className="icon">{card.icon}</div>
        <h3>{card.title}</h3>
        <ul>
          {card.items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>
    ))}
  </div>
</div>


        </div>
      )}
      {loading && (
  <div className="analyzing-loader">
    <div className="spinner"></div>
    <p>Analyzing resume, please wait...</p>
  </div>
)}

{result && (
  <div className="result-page">
    {/* 🎯 Strict Score Speedometer */}
<div className="speedometer strict">
  <h2>🎯 Strict ATS Simulation Score</h2>
  <ReactSpeedometer
    maxValue={100}
    value={result.strict_score}
    needleColor="#000"
    startColor="red"
    endColor="green"
    segments={10}
    ringWidth={30}
    textColor={darkMode ? "#fff" : "#000"}
  />
  <p><strong>Strict Score:</strong> {result.strict_score}%</p>
</div>

    <div className="result-grid">
      {/* 🔍 Section Breakdown (Strict) */}
<div className="result-card">
  <h3>🔍 Section-wise ATS Evaluation</h3>
  <ul>
    {Object.entries(result.strict_breakdown).map(([section, score]) => (
      <li key={section}>
        <strong>{section}:</strong> {score}%{" "}
        {result.strict_feedback[section] && (
          <span>– ⚠️ {result.strict_feedback[section]}</span>
        )}
      </li>
    ))}
  </ul>
</div>

      {/* 📝 ATS Breakdown Table */}
      <div className="result-card">
        <h3>📄 ATS Breakdown</h3>
        <table className="ats-table">
          <thead>
            <tr><th>Criteria</th><th>Evaluation</th><th>Deductions</th></tr>
          </thead>
          <tbody>
            {result.ats_breakdown.map((row, i) => (
              <tr key={i}>
                <td>{row.criteria}</td>
                <td>{row.evaluation}</td>
                <td>-{row.deduction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

{/* 🧠 Grouped Skill Highlights */}
          <div className="result-card">
  <h3>🧠 Skill Highlights Detected (ATS Match)</h3>
  <ul>
    {Object.entries(result.ats_grouped_skills).map(([category, skills]) => (
      <li key={category}>
        ✅ <strong>{category}:</strong> {skills.length ? skills.join(', ') : 'None'}
      </li>
    ))}
  </ul>
</div>

      {/* ❌ Missing Keywords */}
      <div className="result-card">
        <h3>❌ Missing Keywords from JD</h3>
        <ul>
          {result.ats_missing_keywords.map((kw, i) => (
            <li key={i}>{kw}</li>
          ))}
        </ul>
      </div>
    </div>

    {/* 💡 Feedback Summary */}
    <div className="card feedback">
      <h3>💡 Feedback Summary</h3>
      <ul>
        {result.ats_feedback_summary.map((tip, i) => (
          <li key={i}>📝 {tip}</li>
        ))}
        {result.feedback.map((msg, i) => (
          <li key={`gen-${i}`}>- {msg}</li>
        ))}
      </ul>
    </div>

    {/* 🔁 Retry Button */}
    <button className="back-btn" onClick={() => setResult(null)}>← Analyze Another</button>
  </div>
)}

    </>
  );
}

export default App;
