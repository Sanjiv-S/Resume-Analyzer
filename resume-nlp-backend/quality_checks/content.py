# quality_checks/content.py
from collections import Counter
import re
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def analyze_content(text):
    score = 100
    feedback = []
    text_lower = text.lower()

    # Repetition Check
    words = [word for word in re.findall(r'\b\w+\b', text_lower) if len(word) > 3]
    common_words = Counter(words).most_common(5)
    if any(count > 10 for word, count in common_words):
        score -= 10
        feedback.append("Avoid repeating the same words too frequently.")

    # Grammar Check
    matches = tool.check(text)
    grammar_issues = [m for m in matches if m.ruleIssueType in ('grammar', 'typographical')]
    if len(grammar_issues) > 5:
        score -= 10
        feedback.append(f"Found {len(grammar_issues)} grammar/spelling issues.")

    # Quantified impact statements
    if not re.search(r'\b(\d+%|increased|reduced|boosted|achieved|saved)\b', text_lower):
        score -= 10
        feedback.append("Use quantified impact like 'increased revenue by 20%' to stand out.")

    return max(score, 40), feedback
