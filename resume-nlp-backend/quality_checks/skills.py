def analyze_skills(skill_categories):
    score = 100
    feedback = []

    total_categories = len(skill_categories)
    matched_categories = sum(1 for skills in skill_categories.values() if skills)

    if matched_categories < total_categories:
        score -= 10
        feedback.append("Add more diverse skills across multiple domains.")

    if matched_categories == 0:
        score -= 30
        feedback.append("No recognizable hard/soft skills detected.")

    # Feedback per missing category
    for category, skills in skill_categories.items():
        if not skills:
            feedback.append(f"Consider adding skills in: {category}")

    return max(score, 40), feedback
