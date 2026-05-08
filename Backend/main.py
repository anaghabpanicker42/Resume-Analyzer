# -------------------------------
# IMPORT LIBRARIES
# -------------------------------
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

import pdfplumber
import re

from sentence_transformers import SentenceTransformer, util
import spacy

# -------------------------------
# LOAD NLP + MODEL
# -------------------------------
nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# FASTAPI APP
# -------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# SKILLS DATABASE
# -------------------------------
SKILLS_DB = [
    "python",
    "java",
    "react",
    "machine learning",
    "deep learning",
    "sql",
    "mongodb",
    "django",
    "flask",
    "nlp",
    "data analysis",
    "javascript",
    "html",
    "css",
    "communication",
    "teamwork",
    "leadership",
    "problem solving",
    "critical thinking",
    "customer handling",
    "customer service",
    "time management",
    "adaptability",
    "patience",
    "interpersonal skills",
]

# -------------------------------
# EXTRACT TEXT FROM PDF
# -------------------------------
def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    # CLEAN TEXT
    text = text.lower()
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)

    return text


# -------------------------------
# EXTRACT SKILLS
# -------------------------------
def extract_skills(text):

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------------
# EXPERIENCE EXTRACTION
# -------------------------------
def extract_experience(text):

    experience = re.findall(r"(\d+)\+?\s+years", text)

    if experience:
        return max([int(x) for x in experience])

    return 0


# -------------------------------
# STRUCTURE SCORE
# -------------------------------
def calculate_structure_score(text):

    score = 0

    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
    ]

    found_sections = 0

    for section in sections:
        if section in text:
            found_sections += 1

    score += found_sections * 15

    # EMAIL CHECK
    if re.search(r"\S+@\S+\.\S+", text):
        score += 10

    # PHONE CHECK
    if re.search(r"\d{10}", text):
        score += 10

    # LENGTH CHECK
    if len(text.split()) > 150:
        score += 10

    if score > 100:
        score = 100

    return score


# -------------------------------
# JD RANKING
# -------------------------------
def get_jd_ranking(score):

    if score >= 85:
        return "Highly Recommended"

    elif score >= 70:
        return "Recommended"

    elif score >= 50:
        return "Moderate Recommendation"

    else:
        return "Low Recommendation"


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.get("/")
def home():
    return {"message": "ATS Resume Analyzer Backend Running"}


# -------------------------------
# ANALYZE API
# -------------------------------
@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # -------------------------------
    # EXTRACT RESUME TEXT
    # -------------------------------
    resume_text = extract_text_from_pdf(file)

    job_description = job_description.lower()

    # -------------------------------
    # SKILL EXTRACTION
    # -------------------------------
    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # -------------------------------
    # KEYWORD SCORE
    # -------------------------------
    total_skills = len(jd_skills)

    if total_skills == 0:
        keyword_score = 0

    else:
        keyword_score = int(
            (len(matched_skills) / total_skills) * 100
        )

    # -------------------------------
    # SEMANTIC SCORE
    # -------------------------------
    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    jd_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        jd_embedding
    ).item()

    semantic_score = int(similarity * 100)

    if semantic_score > 100:
        semantic_score = 100

    # -------------------------------
    # STRUCTURE SCORE
    # -------------------------------
    structure_score = calculate_structure_score(
        resume_text
    )

    # -------------------------------
    # EXPERIENCE
    # -------------------------------
    experience = extract_experience(resume_text)

    # -------------------------------
    # FINAL ATS SCORE
    # -------------------------------
    ats_score = int(
        (semantic_score * 0.40)
        + (keyword_score * 0.40)
        + (structure_score * 0.20)
    )

    if ats_score > 100:
        ats_score = 100

    # -------------------------------
    # JD RANKING
    # -------------------------------
    jd_ranking = get_jd_ranking(ats_score)

    # -------------------------------
    # SUGGESTIONS
    # -------------------------------
    suggestions = []

    if missing_skills:
        suggestions.append(
            "Add missing skills: "
            + ", ".join(missing_skills)
        )

    if semantic_score < 50:
        suggestions.append(
            "Resume content does not strongly match job role"
        )

    if structure_score < 60:
        suggestions.append(
            "Improve resume structure and formatting"
        )

    if ats_score < 50:
        suggestions.append(
            "Improve technical and soft skills"
        )

    elif ats_score < 75:
        suggestions.append(
            "Moderate ATS score. Improve resume quality."
        )

    else:
        suggestions.append(
            "Excellent resume match for this role"
        )

    # -------------------------------
    # RETURN RESPONSE
    # -------------------------------
    return {

        "ATS_score": ats_score,

        "semantic_score": semantic_score,

        "keyword_score": keyword_score,

        "structure_score": structure_score,

        "experience": experience,

        "jd_ranking": jd_ranking,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "suggestions": suggestions,
    }