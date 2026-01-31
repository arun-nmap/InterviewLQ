import pdfplumber, docx

SKILLS = ["python", "fastapi", "flask", "sql", "machine learning", "docker"]

def parse_resume(path):
    text = ""
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                text += p.extract_text() or ""
    else:
        doc = docx.Document(path)
        for p in doc.paragraphs:
            text += p.text
    return text.lower()

def extract_skills(text):
    return [s for s in SKILLS if s in text]
