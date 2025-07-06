from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.ats import calculate_ats_score
from utils.parser import extract_text
from utils.contact_info import extract_contact_info
from utils.grammar import check_grammar
from utils.skills import match_skills
from utils.resume_insights import extract_resume_insights
from utils.scorer import calculate_final_score
from utils.scorer import calculate_section_scores  # NEW
from utils.scorer import calculate_strict_score  #NEW

from quality_checks.format import analyze_format
from quality_checks.sections import analyze_sections
from quality_checks.content import analyze_content
from quality_checks.style import analyze_style
from quality_checks.skills import analyze_skills

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_resume")
async def upload_resume(resume: UploadFile = File(...), job_description: str = Form(None)):
    print("✅ Received file:", resume.filename)
    contents = await resume.read()

    # Step 1: Extract text from resume
    text = extract_text(contents, resume.filename)
    print("🧠 Extracted text (first 200 chars):", text[:200])

    # Step 2: Resume insights
    contact = extract_contact_info(text)
    grammar = check_grammar(text)
    resume_insights = extract_resume_insights(text)
    matched_skills, jd_match_score = match_skills(text, job_description)
    skill_categories = matched_skills  # alias for compatibility


    # Step 3: Quality checks (5 categories)
    format_score, format_feedback = analyze_format(contents, resume.filename, text)
    section_score, section_feedback = analyze_sections(text)
    content_score, content_feedback = analyze_content(text)
    style_score, style_feedback = analyze_style(text)
    skill_score, skill_feedback = analyze_skills(skill_categories)

    # Step 4: Feedback aggregation
    all_feedback = (
        format_feedback +
        section_feedback +
        content_feedback +
        style_feedback +
        skill_feedback +
        grammar["messages"]
    )

    # Step 5: Scoring logic
    category_scores = calculate_final_score({
        "format": format_score,
        "sections": section_score,
        "content": content_score,
        "style": style_score,
        "skills": skill_score
    })

    section_scores, section_feedback = calculate_section_scores(text, contact)

    strict_total, strict_breakdown, strict_feedback = calculate_strict_score(
    text=text,
    grammar_errors=grammar["error_count"],
    contact_info=contact,
    detected_skills=skill_categories
)

    # Step 6: Enhanced ATS scoring
    ats_result = calculate_ats_score(text, contact, skill_categories, job_description)

    # Step 7: Final response
    return {
        "overall_score": category_scores["overall"],
        "category_scores": category_scores,
        "section_scores": section_scores,
        "section_feedback": section_feedback,
        "strict_score": strict_total,
        "strict_breakdown": strict_breakdown,
        "strict_feedback": strict_feedback,

        "feedback": all_feedback,
        "contact_info": contact,
        "skills": skill_categories,
        "resume_insights": resume_insights,

        # ✅ ATS Fields
        "ats_score": ats_result["ats_score"],
        "ats_breakdown": ats_result["breakdown"],
        "ats_skills": ats_result["detected_skills"],
        "ats_grouped_skills": ats_result["grouped_skills"],
        "ats_missing_keywords": ats_result["missing_keywords"],
        "ats_feedback_summary": ats_result["feedback_summary"]
    }
