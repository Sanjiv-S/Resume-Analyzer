import re
def calculate_contact_score(contact):
    score = 0
    if contact.get("email"):
        score += 25
    if contact.get("phone"):
        score += 25
    if contact.get("linkedin"):
        score += 25
    if contact.get("github"):
        score += 25
    return score


def has_section(text, section_name):
    """Accurately detects section headers like 'Experience', 'Certifications', etc."""
    pattern = rf'^\s*{section_name}\s*:?\s*$'
    lines = text.lower().splitlines()
    return any(re.match(pattern, line.strip()) for line in lines)

def calculate_section_scores(text, contact_info):
    text_lower = text.lower()
    scores = {}
    feedback = {}

    # --- Experience ---
    if has_section(text, "experience") or has_section(text, "professional experience"):
        exp_years = re.findall(r'\b(19|20)\d{2}\b', text_lower)
        scores["Experience"] = 100 if exp_years else 60
        feedback["Experience"] = "Years of experience missing in section." if not exp_years else ""
    else:
        scores["Experience"] = 0
        feedback["Experience"] = "Experience section not found."

    # --- Education ---
    education_keywords = ["b.tech", "m.tech", "bachelor", "master", "phd", "mba", "degree"]
    scores["Education"] = 100 if any(kw in text_lower for kw in education_keywords) else 0
    feedback["Education"] = "" if scores["Education"] else "Education section not found."

    # --- Projects ---
    scores["Projects"] = 100 if has_section(text, "projects") else 0
    feedback["Projects"] = "" if scores["Projects"] else "Projects section not found."

    # --- Certifications ---
    CERT_KEYWORDS = ["certification", "certified", "certificate", "completed", "achievement"]
    scores["Certifications"] = 100 if any(kw in text_lower for kw in CERT_KEYWORDS) else 0
    feedback["Certifications"] = "" if scores["Certifications"] else "Certifications section not found."


    # --- Skills ---
    scores["Skills"] = 100 if has_section(text, "skills") else 0
    feedback["Skills"] = "" if scores["Skills"] else "Skills section not found."

    # --- Contact Info ---
    has_email = bool(contact_info.get("email"))
    has_phone = bool(contact_info.get("phone"))
    scores["Contact Info"] = 100 if has_email and has_phone else 50 if has_email or has_phone else 0
    feedback["Contact Info"] = "Missing email or phone." if scores["Contact Info"] < 100 else ""

    return scores, feedback

import re

def calculate_strict_score(text, grammar_errors, contact_info, detected_skills):
    text_lower = text.lower()
    score = 0
    breakdown = {}
    feedback = {}

    # --- Experience (25%) ---
    lines = text_lower.splitlines()
    breakdown["Experience"] = 0
    feedback["Experience"] = "❌ Experience section not found"

    for i, line in enumerate(lines):
        if re.search(r'\b(work|professional)?\s*experience\b', line):
            experience_block = "\n".join(lines[i:i+8])  # Only look at lines under experience heading
            years = re.findall(r'\b(?:19|20)\d{2}\b', experience_block)

            if len(years) >= 2:
                breakdown["Experience"] = 25
                feedback["Experience"] = "✓ Experience section found with valid years"
            elif len(years) == 1:
                breakdown["Experience"] = 12
                feedback["Experience"] = "⚠️ Experience section found, only one year present"
            else:
                breakdown["Experience"] = 6
                feedback["Experience"] = "⚠️ Experience section found, but no valid years"
            break  # Stop after finding first valid experience block

    # --- Education (15%) ---
    edu_keywords = ["b.tech", "bachelor", "master", "phd", "m.tech", "mba"]
    has_edu = any(kw in text_lower for kw in edu_keywords)
    edu_year = re.search(r'\b(19|20)\d{2}\b', text_lower)
    if has_edu and edu_year:
        breakdown["Education"] = 15
        feedback["Education"] = "✓ Education with degree and year found"
    elif has_edu:
        breakdown["Education"] = 10
        feedback["Education"] = "✓ Degree found, but no year"
    else:
        breakdown["Education"] = 0
        feedback["Education"] = "Education section not found"

    # --- Projects (10%) ---
    if re.search(r'^\s*projects?\s*:?$', text_lower, re.MULTILINE):
        breakdown["Projects"] = 10
        feedback["Projects"] = "✓ Projects section found"
    else:
        breakdown["Projects"] = 0
        feedback["Projects"] = "Projects section not found"

    # --- Certifications (10%) ---
    cert_keywords = ["certification", "certified", "certificate", "coursera", "udemy", "ibm", "microsoft", "aws"]
    cert_present = any(kw in text_lower for kw in cert_keywords)
    if cert_present:
        breakdown["Certifications"] = 10
        feedback["Certifications"] = "✓ Certifications mentioned"
    else:
        breakdown["Certifications"] = 0
        feedback["Certifications"] = "No certifications detected"

    # --- Skills (20%) ---
    skill_count = sum(len(v) for v in detected_skills.values())
    if skill_count >= 6:
        breakdown["Skills"] = 20
        feedback["Skills"] = f"✓ {skill_count} skills detected"
    elif skill_count >= 3:
        breakdown["Skills"] = 12
        feedback["Skills"] = f"✓ Only {skill_count} skills found — add more"
    else:
        breakdown["Skills"] = 5 if skill_count > 0 else 0
        feedback["Skills"] = "Too few skills detected"

    # --- Contact Info (10%) ---
    email = contact_info.get("email")
    phone = contact_info.get("phone")
    if email and phone:
        breakdown["Contact Info"] = 10
        feedback["Contact Info"] = "✓ Email and phone present"
    elif email or phone:
        breakdown["Contact Info"] = 5
        feedback["Contact Info"] = "✓ Only one contact info found"
    else:
        breakdown["Contact Info"] = 0
        feedback["Contact Info"] = "Missing both email and phone"

    # --- Grammar & Spelling (10%) ---
    grammar_score = max(10 - grammar_errors * 2, 2)
    breakdown["Grammar"] = grammar_score
    feedback["Grammar"] = f"{grammar_errors} grammar issues detected"

    # --- Final Score ---
    total_score = sum(breakdown.values())

    return total_score, breakdown, feedback


def calculate_final_score(category_scores):
    """
    Calculate overall quality score from 5 quality check categories.
    Example input:
    {
        "format": 90,
        "sections": 80,
        "content": 85,
        "style": 75,
        "skills": 88
    }
    """
    overall = round(sum(category_scores.values()) / len(category_scores), 2)
    category_scores["overall"] = overall
    return category_scores
