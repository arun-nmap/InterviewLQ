import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "Interview_Report.pdf")

def generate_pdf(history, timeline):
    os.makedirs(REPORT_DIR, exist_ok=True)

    if not history:
        return

    c = canvas.Canvas(REPORT_PATH, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "InterviewIQ – AI Interview Report")
    y -= 40

    c.setFont("Helvetica", 11)

    for i, h in enumerate(history, 1):
        if y < 100:
            c.showPage()
            y = height - 50

        c.drawString(50, y, f"Q{i}: {h['question']}")
        y -= 18
        c.drawString(60, y, f"Answer: {h['answer']}")
        y -= 18
        c.drawString(60, y, f"Confidence: {h['confidence']}%")
        y -= 18
        c.drawString(60, y, f"Emotion: {h['emotion']}")
        y -= 18
        c.drawString(60, y, f"Difficulty: {h['difficulty']}")
        y -= 30

    c.save()
