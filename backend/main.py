from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from analyzer import extract_text_from_pdf_bytes, analyze_resume


app = FastAPI(title="YOUR AI RESUME GUIDE ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Resume Guide API is running"}


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    file_bytes = await resume.read()

    resume_text = extract_text_from_pdf_bytes(file_bytes)

    if not resume_text.strip():
        return {
            "error": "Text not found. Please upload a text-based PDF, not a scanned image PDF."
        }

    result = analyze_resume(resume_text, job_description)
    return result