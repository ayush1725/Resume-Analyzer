from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from transformers import pipeline
from pydantic import BaseModel
from datetime import datetime, timedelta
import shutil, os, re, jwt
from jwt import PyJWTError
from dotenv import load_dotenv

from resume_parser import extract_text_from_pdf
from matcher import calculate_similarity
from models.user_model import create_user, get_user_by_email, verify_password
from services.email_service import send_feedback_email


# Load .env vars
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# App setup
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths & Models
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Token management
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except PyJWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

# Summarization
def summarize_with_model(text: str) -> str:
    max_input_length = 1024
    chunks = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]

    chunk_summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        chunk_summaries.append(summary[0]['summary_text'])

    final_summary = " ".join(chunk_summaries)
    return summarizer(final_summary, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

# Feedback generation
def generate_feedback(score, resume_text, job_description):
    feedback = {}
    if score < 0.4:
        feedback['general_advice'] = "Your resume's similarity score to the job description is low. Consider including more relevant keywords."
        job_keywords = set(re.findall(r'\b[A-Za-z0-9\+\#]+(?:\s[A-Za-z0-9\+]+)?\b', job_description.lower()))
        resume_keywords = set(re.findall(r'\b[A-Za-z0-9\+\#]+(?:\s[A-Za-z0-9\+]+)?\b', resume_text.lower()))
        missing = job_keywords - resume_keywords
        if missing:
            feedback['missing_keywords'] = f"Consider adding: {', '.join(sorted(missing))}."
        if "experience" in resume_text.lower():
            feedback['experience_advice'] = "Highlight tools, technologies, and roles aligned with the job description."
        if "skills" in resume_text.lower():
            feedback['skills_advice'] = "Ensure your skills section reflects specific job-required technologies."
    else:
        feedback['general_advice'] = "Great match! Your resume aligns well with the job description."
    return feedback

# Signup
@app.post("/signup/")
async def signup(user: User):
    try:
        return create_user(user.email, user.password)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup error: {str(e)}")

# Login
@app.post("/login/", response_model=Token)
async def login(user: User):
    stored = get_user_by_email(user.email)
    if not stored or not verify_password(stored['password'], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Resume Analysis
@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, resume.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        resume_text = extract_text_from_pdf(file_path)

        section_keywords = {
            "Experience": ["experience", "work", "internship", "projects"],
            "Education": ["education", "qualification"],
            "Skills": ["skills", "technical skills", "technologies"],
            "Summary": ["summary", "about", "profile", "overview"]
        }

        section_texts = {key: "" for key in section_keywords}
        current_section = None

        for line in resume_text.splitlines():
            line_lower = line.lower().strip()
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    current_section = section
                    break
            if current_section:
                section_texts[current_section] += line.strip() + '\n'

        summarized_sections = {}
        for section, text in section_texts.items():
            if section == "Skills":
                summarized_sections[section] = text.strip()
            elif section != "Summary":
                summarized_sections[section] = summarize_with_model(text.strip()) if text.strip() else ""

        experience_text = section_texts.get("Experience", "")
        similarity_score = calculate_similarity(experience_text, job_description)
        feedback = generate_feedback(similarity_score, resume_text, job_description)

        

        send_feedback_email(current_user, similarity_score, feedback, summarized_sections)

        return {
            "summary": summarized_sections,
            "similarity_score": round(similarity_score, 2),
            "feedback": feedback
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
