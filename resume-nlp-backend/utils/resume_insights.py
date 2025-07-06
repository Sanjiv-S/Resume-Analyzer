import re

def extract_resume_insights(text):
    insights = {
        "has_education": False,
        "has_projects": False,
        "years_of_experience": "Not found",
        "soft_skills": [],
        "languages": []
    }

    text_lower = text.lower()

    # 🎓 Education detection - robust with multiple patterns
    education_keywords = [
        r"b[.\s]?tech", r"m[.\s]?tech", "bsc", "msc", "mba", "phd",
        "bachelor[s]?", "master[s]?", "degree in", "education"
    ]
    insights["has_education"] = any(re.search(kw, text_lower) for kw in education_keywords)

    # 📝 Projects section
    insights["has_projects"] = bool(re.search(r"\b(projects?)\b", text_lower))

    # 🧑‍💼 Experience (match different experience phrases)
    exp_match = re.search(r"(\d{1,2})\s*(\+)?\s*(years|yrs).*?(experience)?", text_lower)
    if not exp_match:
        exp_match = re.search(r"experience\s*[:\-]?\s*(\d{1,2})\s*(years|yrs)?", text_lower)
    if exp_match:
        insights["years_of_experience"] = f"{exp_match.group(1)} years"

    # 💬 Soft skills
    SOFT_SKILLS = [
        "leadership", "teamwork", "communication", "time management",
        "critical thinking", "problem solving", "adaptability", "creativity"
    ]
    insights["soft_skills"] = [skill for skill in SOFT_SKILLS if skill in text_lower]

    # 🌐 Language detection (spoken languages)
    KNOWN_LANGUAGES = ["english", "hindi", "tamil", "telugu", "kannada", "french", "german", "spanish"]
    found_langs = []
    for lang in KNOWN_LANGUAGES:
        if re.search(rf"\b{lang}\b", text_lower):
            found_langs.append(lang.capitalize())
    insights["languages"] = found_langs

    return insights
