import re

def calculate_ats_score(text, contact, matched_skills, job_desc):
    score = 100
    deductions = 0
    breakdown = []
    feedback_summary = []
    missing_keywords = []

    # ---------- 1. Parsing Success ----------
    if len(text.strip()) < 200:
        deductions += 25
        breakdown.append({
            "criteria": "Parsing Success",
            "evaluation": "Resume content is too short. Parsing may have failed.",
            "deduction": 25
        })
        feedback_summary.append("Resume content is too short. Parsing may have failed.")
    else:
        breakdown.append({
            "criteria": "Parsing Success",
            "evaluation": "Resume parsed successfully.",
            "deduction": 0
        })

    # ---------- 2. Essential Section Presence ----------
    sections = ["experience", "education", "skills", "projects"]
    missing_sections = [s for s in sections if s not in text.lower()]
    if missing_sections:
        sec_deduction = len(missing_sections) * 5
        deductions += sec_deduction
        breakdown.append({
            "criteria": "Section Coverage",
            "evaluation": f"Missing sections: {', '.join(missing_sections)}",
            "deduction": sec_deduction
        })
        feedback_summary.append(f"Missing sections: {', '.join(missing_sections)}.")
    else:
        breakdown.append({
            "criteria": "Section Coverage",
            "evaluation": "All essential sections present.",
            "deduction": 0
        })

    # ---------- 3. Contact Info ----------
    if not contact.get("email") or not contact.get("phone"):
        deductions += 10
        breakdown.append({
            "criteria": "Contact Info",
            "evaluation": "Missing email or phone number.",
            "deduction": 10
        })
        feedback_summary.append("Missing email or phone number.")
    else:
        breakdown.append({
            "criteria": "Contact Info",
            "evaluation": "Email and phone number present.",
            "deduction": 0
        })

    # ---------- 4. Formatting Cleanliness ----------
    messy_indicators = ["##", "==", "__", "{{", "}}", "[ ]", "[x]", "<>", "\\t"]
    if any(sym in text for sym in messy_indicators):
        deductions += 5
        breakdown.append({
            "criteria": "Formatting Cleanliness",
            "evaluation": "Resume contains formatting artifacts (e.g., Markdown or LaTeX).",
            "deduction": 5
        })
        feedback_summary.append("Resume has formatting issues or extra symbols.")
    else:
        breakdown.append({
            "criteria": "Formatting Cleanliness",
            "evaluation": "Clean formatting detected.",
            "deduction": 0
        })

    # ---------- 5. Keyword Matching with Job Description ----------
    if job_desc:
        stopwords = {
            "with", "from", "this", "have", "that", "your", "will", "must",
            "good", "able", "and", "the", "you", "are", "for", "our", "they",
            "their", "who", "should", "can", "all", "any", "more", "than"
        }
        job_keywords = set(
            word for word in re.findall(r'\b\w{4,}\b', job_desc.lower())
            if word not in stopwords
        )
        resume_words = set(re.findall(r'\b\w{4,}\b', text.lower()))
        overlap = job_keywords & resume_words
        match_percent = (len(overlap) / len(job_keywords)) * 100 if job_keywords else 0

        if match_percent < 20:
            deductions += 15
            breakdown.append({
                "criteria": "Keyword Match to JD",
                "evaluation": f"Low keyword match ({round(match_percent)}%) with job description.",
                "deduction": 15
            })
            feedback_summary.append("Low keyword match with job description.")
        elif match_percent < 40:
            deductions += 10
            breakdown.append({
                "criteria": "Keyword Match to JD",
                "evaluation": f"Partial keyword match ({round(match_percent)}%) with job description.",
                "deduction": 10
            })
            feedback_summary.append("Improve keyword match with job description.")
        else:
            breakdown.append({
                "criteria": "Keyword Match to JD",
                "evaluation": f"Good keyword match ({round(match_percent)}%) with job description.",
                "deduction": 0
            })

        missing_keywords = sorted(list(job_keywords - resume_words))[:15]

    # ---------- 6. Skill Coverage ----------
    num_categories = len(matched_skills)
    num_matched = sum(1 for k in matched_skills if matched_skills[k])
    if num_matched < num_categories:
        deductions += 10
        breakdown.append({
            "criteria": "Skill Coverage",
            "evaluation": "Limited skill match across multiple categories.",
            "deduction": 10
        })
        feedback_summary.append("Some skill categories are underrepresented.")
    else:
        breakdown.append({
            "criteria": "Skill Coverage",
            "evaluation": "Matched skills across categories.",
            "deduction": 0
        })

    # ---------- 7. Manual Missing Developer Keywords ----------
    manual_missing = []
    keyword_phrases = {
        "Object-Oriented Programming": ["oop", "object-oriented programming"],
        "REST APIs": ["rest api", "api integration"],
        "CI/CD Pipelines": ["ci/cd", "continuous integration", "pipeline"],
        "Version Control": ["git", "version control"],
        "Unit Testing / Debugging / Agile": ["unit test", "debugging", "agile"]
    }
    resume_text = text.lower()
    for label, phrases in keyword_phrases.items():
        if not any(p in resume_text for p in phrases):
            manual_missing.append(f"❌ {label}")

    ats_score = max(100 - deductions, 30)

    # ---------- Flatten and Group Skills ----------
    detected_skills = [skill for skills in matched_skills.values() for skill in skills]

    grouped_skills = {
        "Languages": [],
        "Tools": [],
        "ML Projects": [],
        "Certifications": []
    }
    for skill in detected_skills:
        s = skill.lower()
        if s in {"python", "java", "c", "sql", "html", "css", "html/css", "javascript"}:
            grouped_skills["Languages"].append(skill)
        elif s in {"github", "vs code", "gcp", "google cloud", "power bi", "docker", "vscode"}:
            grouped_skills["Tools"].append(skill)
        elif "project" in s or s in {"yolo", "voice assistant", "spotify", "object detection"}:
            grouped_skills["ML Projects"].append(skill)
        elif "cert" in s or s in {"ibm", "microsoft", "internship", "power bi"}:
            grouped_skills["Certifications"].append(skill)

    return {
        "ats_score": ats_score,
        "breakdown": breakdown,
        "detected_skills": detected_skills,
        "grouped_skills": grouped_skills,
        "missing_keywords": missing_keywords + manual_missing,
        "feedback_summary": feedback_summary
    }
