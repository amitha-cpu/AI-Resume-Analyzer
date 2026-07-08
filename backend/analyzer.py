import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python", "java", "c++", "html", "css", "javascript",
    "sql", "flask", "fastapi", "django", "machine learning",
    "deep learning", "nlp", "tensorflow", "keras", "pytorch",
    "data analysis", "excel", "power bi", "communication",
    "git", "github", "api", "aws", "cloud", "react"
]

ACTION_VERBS = [
    "built", "created", "developed", "designed", "implemented",
    "improved", "analyzed", "trained", "deployed", "automated"
]

WEAK_WORDS = [
    "hardworking", "good", "nice", "responsible",
    "team player", "quick learner"
]


def extract_text_from_pdf_bytes(file_bytes):
    text = ""
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    for page in pdf:
        text += page.get_text("text", sort=True)

    pdf.close()
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def calculate_match_score(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)


def get_resume_strength(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Needs Improvement"


def find_skills(text):
    text = clean_text(text)
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def ats_section_check(text):
    text = clean_text(text)

    sections = {
        "Education": "education" in text,
        "Skills": "skills" in text,
        "Projects": "project" in text or "projects" in text,
        "Experience": "experience" in text or "internship" in text,
        "Contact": "email" in text or "phone" in text or "linkedin" in text
    }

    missing_sections = []

    for section, present in sections.items():
        if not present:
            missing_sections.append(section)

    return sections, missing_sections


def find_action_verbs(text):
    text = clean_text(text)
    found = []

    for verb in ACTION_VERBS:
        if verb in text:
            found.append(verb)

    return found


def find_weak_words(text):
    text = clean_text(text)
    found = []

    for word in WEAK_WORDS:
        if word in text:
            found.append(word)

    return found


def generate_project_suggestions(missing_skills):
    suggestions = []

    if "machine learning" in missing_skills:
        suggestions.append("Build a Fake News Detection project using Machine Learning.")

    if "nlp" in missing_skills:
        suggestions.append("Build a PDF Question Answering project using NLP.")

    if "fastapi" in missing_skills or "api" in missing_skills:
        suggestions.append("Create a FastAPI backend project and deploy it.")

    if "sql" in missing_skills:
        suggestions.append("Create a project using SQL database.")

    if "cloud" in missing_skills:
        suggestions.append("Deploy one project on a cloud platform like AWS or Render.")

    if not suggestions:
        suggestions.append("Add one strong AI project with GitHub link and live demo.")

    return suggestions


def generate_interview_questions(found_skills, missing_skills):
    questions = []

    for skill in found_skills[:5]:
        questions.append(f"Explain your experience with {skill}.")

    for skill in missing_skills[:5]:
        questions.append(f"Why is {skill} important for this job role?")

    if not questions:
        questions.append("Tell me about yourself and your technical skills.")

    return questions


def analyze_resume(resume_text, job_description):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    score = calculate_match_score(resume_clean, jd_clean)
    strength = get_resume_strength(score)

    resume_skills = find_skills(resume_clean)
    job_skills = find_skills(jd_clean)

    missing_skills = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    ats_sections, missing_sections = ats_section_check(resume_clean)
    action_verbs = find_action_verbs(resume_clean)
    weak_words = find_weak_words(resume_clean)

    career_tips = []

    if score < 50:
        career_tips.append("Your resume match score is low. Add more job-related keywords naturally.")

    if missing_skills:
        career_tips.append("Add missing skills only if you really know them.")

    if missing_sections:
        career_tips.append("Add missing ATS sections: " + ", ".join(missing_sections))

    if len(action_verbs) < 3:
        career_tips.append("Use more action verbs like developed, implemented, built, and deployed.")

    if weak_words:
        career_tips.append("Avoid weak words like: " + ", ".join(weak_words))

    if "github" not in resume_clean:
        career_tips.append("Add your GitHub profile link.")

    if "linkedin" not in resume_clean:
        career_tips.append("Add your LinkedIn profile link.")

    return {
        "match_score": score,
        "resume_strength": strength,
        "found_skills": resume_skills,
        "missing_skills": missing_skills,
        "ats_sections": ats_sections,
        "missing_sections": missing_sections,
        "action_verbs": action_verbs,
        "weak_words": weak_words,
        "career_tips": career_tips,
        "project_suggestions": generate_project_suggestions(missing_skills),
        "interview_questions": generate_interview_questions(resume_skills, missing_skills)
    }