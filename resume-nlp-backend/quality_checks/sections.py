def analyze_sections(text):
    score = 100
    feedback = []

    text_lower = text.lower()

    # Required sections
    required_sections = ["experience", "education", "skills"]
    for section in required_sections:
        if section not in text_lower:
            score -= 10
            feedback.append(f"Missing required section: {section.capitalize()}.")

    # Optional personality-related
    if "project" not in text_lower:
        feedback.append("Consider adding a Projects section.")

    if "interest" not in text_lower and "hobby" not in text_lower:
        feedback.append("Add Interests or Hobbies to showcase personality.")

    return max(score, 40), feedback
