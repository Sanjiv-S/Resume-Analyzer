import PyPDF2
import io

def analyze_format(file_bytes, filename, text):
    score = 100
    feedback = []

    # Check file type
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        score -= 20
        feedback.append("Use .pdf or .docx format only.")

    # Estimate length by number of pages or lines
    page_count = 1
    if filename.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
        except Exception:
            feedback.append("Could not determine PDF page count.")
            score -= 10
    elif filename.endswith(".docx"):
        line_count = text.count("\n")
        page_count = line_count // 40  # rough estimate

    if page_count > 1:
        score -= 10
        feedback.append("Keep resume under 2 pages for most roles.")

    # Bullet point length
    long_bullets = [
        line for line in text.splitlines()
        if line.strip().startswith(('-', '*', '•')) and len(line.split()) > 25
    ]
    if long_bullets:
        score -= 10
        feedback.append("Use concise bullet points (under ~25 words).")

    return max(score, 40), feedback
