import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_contact_info(text):
    doc = nlp(text)

    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    email = re.findall(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
    phone = re.findall(r'(\+?\d[\d\-\(\) ]{8,}\d)', text)
    linkedin = re.findall(r"linkedin\.com/in/[A-Za-z0-9_-]+", text)
    github = re.findall(r"github\.com/[A-Za-z0-9_-]+", text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
    }
