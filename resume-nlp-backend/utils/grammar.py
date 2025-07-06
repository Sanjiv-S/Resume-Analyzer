import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text):
    matches = tool.check(text)
    serious = [m for m in matches if m.ruleIssueType == 'grammar']
    score = max(100 - len(serious) * 3, 40)
    return {
        "error_count": len(serious),
        "messages": [m.message for m in serious[:5]],
        "score": score
    }
