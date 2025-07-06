# quality_checks/style.py
import re

PASSIVE_VOICE_PHRASES = ["was", "were", "is being", "are being", "have been", "has been", "had been"]
BUZZWORDS = ["synergy", "go-getter", "hardworking", "dynamic", "team player", "innovative"]

def analyze_style(text):
    score = 100
    feedback = []
    text_lower = text.lower()

    # Passive voice count (simplified)
    passive_count = sum(1 for phrase in PASSIVE_VOICE_PHRASES if phrase in text_lower)
    if passive_count > 5:
        score -= 20
        feedback.append("Try to use more active voice instead of passive.")

    # Buzzword check
    used_buzzwords = [word for word in BUZZWORDS if word in text_lower]
    if used_buzzwords:
        score -= 20
        feedback.append("Avoid generic buzzwords like: " + ", ".join(used_buzzwords))

    return max(score, 40), feedback
