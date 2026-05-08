## ATS Resume Analyzer
-------------------------------------
AI-powered ATS Resume Analyzer built using React, FastAPI, NLP, spaCy, and DistilBERT semantic matching. The system analyzes resumes against job descriptions using AI-based semantic similarity, keyword extraction, ATS scoring, resume parsing, skill detection, experience extraction, JD ranking, and smart improvement suggestions.
# Features
* ATS Score Calculation
* Semantic Similarity Matching using DistilBERT
* Resume Parsing from PDF
* Skill Extraction using NLP
* Missing Skill Detection
* Resume Structure Analysis
* Experience Extraction
* Real-time Resume Evaluation
* Modern Responsive UI
## Tech Stack
# Frontend
* React
* CSS
* Axios
# Backend
* FastAPI
* Python
* spaCy
* Sentence Transformers
* pdfplumber
  
## Installation
# Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend Setup
cd frontend
npm install
npm run dev
## Project Workflow
* Upload Resume PDF
* Enter Job Description
* System extracts resume text
* NLP extracts skills and experience
* DistilBERT performs semantic matching
* ATS score is generated
* Suggestions and ranking are displayed
## Future Improvements
* Multi-resume ranking
* Resume recommendation system
* Authentication system
* Database integration
* Deployment on cloud
