import re
from fuzzywuzzy import fuzz

# Define your skill database
SKILL_DB = {
    "Languages": [
        "python", "java", "c", "c++", "sql", "javascript", "typescript", "html", "css", "bash", "shell"
    ],
    "Tools": [
        "git", "github", "docker", "kubernetes", "vscode", "aws", "gcp", "azure", "jupyter", "postman", "heroku"
    ],
    "ML Projects": [
        "yolo", "object detection", "voice assistant", "chatbot", "recommendation system",
        "classification", "regression", "nlp", "neural network", "cnn", "rnn", "transformer"
    ],
    "Certifications": [
        "ibm", "coursera", "udemy", "microsoft", "aws certified", "internship", "certified", "google"
    ],
    "Soft Skills": [
        "problem-solving", "communication", "leadership", "teamwork", "adaptability",
        "time management", "creativity", "collaboration"
    ]
}

def match_skills(text, job_desc=None):
    text = text.lower()
    matched_skills = {category: [] for category in SKILL_DB}

    for category, skill_list in SKILL_DB.items():
        for skill in skill_list:
            # 1. Exact match
            if skill in text:
                matched_skills[category].append(skill)
                continue

            # 2. Fuzzy match (strict: ≥95)
            for word in re.findall(r'\b\w+\b', text):
                if fuzz.partial_ratio(skill, word) >= 95:
                    matched_skills[category].append(skill)
                    break

            # 3. Semantic match removed for accuracy

    # Remove duplicates
    for category in matched_skills:
        matched_skills[category] = list(set(matched_skills[category]))

    # Optional JD match score
    jd_score = 0
    if job_desc:
        job_keywords = set(re.findall(r'\b\w{4,}\b', job_desc.lower()))
        resume_words = set(re.findall(r'\b\w{4,}\b', text))
        common = job_keywords & resume_words
        jd_score = (len(common) / len(job_keywords)) * 100 if job_keywords else 0

    return matched_skills, jd_score
