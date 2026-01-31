from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os, shutil

from websocket import interview_socket
from ai.resume_parser import parse_resume, extract_skills
from ai.question_generator import generate_questions
from ai.interviewer import load_questions

app = FastAPI(title="InterviewIQ Backend")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_resume")
async def upload_resume(resume: UploadFile = File(...)):
    upload_dir = os.path.join(BASE_DIR, "uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)

    path = os.path.join(upload_dir, resume.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    text = parse_resume(path)
    skills = extract_skills(text)
    questions = generate_questions(skills)
    load_questions(questions)

    return {"status": "ok", "skills": skills}

@app.websocket("/ws/interview")
async def interview_ws(ws: WebSocket):
    await interview_socket(ws)

@app.get("/report")
def download_report():
    report_path = os.path.join(PROJECT_ROOT, "reports", "Interview_Report.pdf")

    if not os.path.exists(report_path):
        return {"error": "Report not generated yet"}

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename="Interview_Report.pdf"
    )
