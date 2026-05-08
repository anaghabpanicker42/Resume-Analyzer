import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [file, setFile] = useState(null);

  const [jobDescription, setJobDescription] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  // -------------------------------
  // HANDLE SUBMIT
  // -------------------------------
  const handleSubmit = async () => {

    if (!file || !jobDescription) {

      alert("Please upload resume and enter job description");

      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    formData.append("job_description", jobDescription);

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        formData
      );

      setResult(response.data);

    } catch (error) {

      console.log(error);

      alert("Backend Error");

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="app">

      <div className="overlay">

        <div className="container">

          <h1>ATS Resume Analyzer</h1>

          <p className="subtitle">
            AI Powered Resume Screening System
          </p>

          <div className="card">

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <textarea
              placeholder="Paste Job Description Here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            ></textarea>

            <button
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze Resume"}
            </button>

          </div>

          {/* RESULTS */}

          {result && (

            <div className="result-card">

              <h2>
                ATS Score: {result.ATS_score}%
              </h2>

              <div className="score-bar">

                <div
                  className="score-fill"
                  style={{
                    width: `${result.ATS_score}%`
                  }}
                ></div>

              </div>

              <div className="score-grid">

                <div className="score-box">
                  <h3>Semantic Score</h3>
                  <p>{result.semantic_score}%</p>
                </div>

                <div className="score-box">
                  <h3>Keyword Score</h3>
                  <p>{result.keyword_score}%</p>
                </div>

                <div className="score-box">
                  <h3>Structure Score</h3>
                  <p>{result.structure_score}%</p>
                </div>

                <div className="score-box">
                  <h3>Experience</h3>
                  <p>{result.experience_years} Years</p>
                </div>

              </div>

              <div className="ranking">

                <h3>JD Ranking</h3>

                <p>{result.JD_ranking}</p>

              </div>

              <div className="skills-section">

                <h3>Matched Skills</h3>

                <div className="skills-list">

                  {result.matched_skills.length > 0 ? (

                    result.matched_skills.map((skill, index) => (

                      <span
                        key={index}
                        className="skill matched"
                      >
                        {skill}
                      </span>

                    ))

                  ) : (
                    <p>None</p>
                  )}

                </div>

              </div>

              <div className="skills-section">

                <h3>Missing Skills</h3>

                <div className="skills-list">

                  {result.missing_skills.length > 0 ? (

                    result.missing_skills.map((skill, index) => (

                      <span
                        key={index}
                        className="skill missing"
                      >
                        {skill}
                      </span>

                    ))

                  ) : (
                    <p>None</p>
                  )}

                </div>

              </div>

              <div className="suggestions">

                <h3>Suggestions</h3>

                <ul>

                  {result.suggestions.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

export default App;